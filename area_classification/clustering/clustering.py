# Note: Supergroup = cluster, group = subcluster, subgroup = subsubcluster.

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from clustergram import Clustergram
import matplotlib.pyplot as plt
from typing import Union
import os
import logging

logger = logging.getLogger(__name__)

from area_classification.utilities.load_config import load_config
from area_classification.utilities.loading_data import load_data

def clustering_wrapper(config: dict,
                       input_dataframe: Union[pd.DataFrame, str],
                       number_of_clusters: int,
                       n_init: int, 
                       output_directory: str, 
                       clustergram_directory: str,
                       random_seed: int = None) -> pd.DataFrame:
    """
    Wrapper function to perform clustering on input data, create supergroups and subgroups.

    Parameters
    ----------
    config : dict
        A dictionary containing user configuration settings.
    input_dataframe : str or pd.DataFrame
        Path to the input data CSV file or a pandas DataFrame.
    number_of_clusters : int
        Number of superclusters to create.
    n_init : int
        Number of times KMeans will be initialized.
    output_directory : str
        Directory to save the final cluster assignments.
    clustergram_directory : str
        Directory to save generated plots.
    random_seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with cluster assignments after supergroup and subgroup clustering.
    """
    #Create folders to save the outputs into
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(clustergram_directory, exist_ok=True)
    
    if isinstance(input_dataframe, str):
        #If a file path is provided, load the data from the CSV file
        logger.info(f"Loading data from {input_dataframe}")
        variable_df = load_data(input_dataframe)
    elif isinstance(input_dataframe, pd.DataFrame):
        # If a DataFrame is provided, use it directly
        logger.info("Using provided DataFrame for clustering.")
        variable_df = input_dataframe.copy()
        variable_df.set_index(variable_df.columns[0], inplace=True)
        missing_values = variable_df.isnull().sum().sum()
        if missing_values > 0:
            logger.warning(f"Warning: {missing_values} missing values found in input data. Missing values will be replaced with 0.")
            variable_df.fillna(0, inplace=True)        
    else:
        raise ValueError("Input must be a file path (str) or a pandas DataFrame.")

    ###SUPERGROUP SECTION ###
    # Validate number_of_clusters compared to input data, will fail if 10 data points attempted to group in 11 clusters
    if len(variable_df) < number_of_clusters:
       logger.warning(f"Warning: Reducing number_of_clusters from {number_of_clusters} to {len(variable_df)}.")
       number_of_clusters = len(variable_df)

    # Create a clustergram from all the data to establish number of supergroups (clusters) for K means  
    create_clustergram(variable_df,
                       number_of_clusters, 
                       n_init, 
                       save_location=clustergram_directory+"/supergroup_clustergram.png",
                       random_seed=random_seed)
    
    logger.info("create supergroup clustergrams completed.")

    # Add a break
    input("Press Enter to continue with supergroups creation...")
    
    #Assign the file path to save the supergroup cluster output
    supergroup_output_filepath = output_directory+"/cluster_assignments/supergroups_clustering_output.csv"
    
    #Run the K means clustering to create supergroups
    supergroup_variable_df = run_kmeans(variable_df, 
                                          number_of_clusters, 
                                          n_init, 
                                          supergroup_output_filepath, 
                                          random_seed)
    logger.info("Kmeans run completed.")

    # Add a break
    logger.info(f"Unique clusters at this stage: {supergroup_variable_df['cluster'].unique()}")
    logger.info("Check that dictionary in config for subsubclustering mapping is correct")
    input("Press Enter to continue to move onto groups...")
    
    ###GROUP SECTION ###
    # Create a clustergram for each supergroup to establish number of groups (subclusters) for K means  
    create_subcluster_clustergrams(cluster_variable_df=supergroup_variable_df,
                                   clustergram_directory=clustergram_directory, 
                                   number_of_clusters=number_of_clusters, 
                                   drop_columns=['cluster'],
                                   cluster_col_name='cluster',
                                   n_init=n_init,
                                   random_seed=random_seed)
    logger.info("group clustergrams completed.")

    # Add a break
    input("Press Enter to continue with the subcluster numbers below for groups creation...")
    
    # Run the K means clustering to create groups, mapping in config for this
    grouped_variable_df = run_subclustering(input_df=supergroup_variable_df, 
                                            output_location=f"{output_directory}cluster_assignments/group", 
                                            drop_columns="cluster", 
                                            column_name="subcluster",
                                            cluster_col_name="cluster",
                                            cluster_to_numbers = config["subclustering_mapping"],
                                            n_init=n_init,
                                            random_seed=random_seed)
    logger.info("groups cluster run completed.")

    # Add a break
    input("Press Enter to continue to move onto subgroup...")

    ###SUBGROUP SECTION ###    
    # Create a clustergram for each group to establish number of subgroups (subsubclusters) for K means 
    create_subcluster_clustergrams(cluster_variable_df=grouped_variable_df,
                                   clustergram_directory=clustergram_directory, 
                                   number_of_clusters= number_of_clusters, 
                                   drop_columns=['cluster', 'subcluster'],
                                   cluster_col_name='subcluster',
                                   n_init=n_init,
                                   random_seed=random_seed)
    logger.info("subgroup clustergrams completed.")
    
    # Add a break
    logger.info(f"Unique subclusters at this stage: {grouped_variable_df['subcluster'].unique()}")
    logger.info("Check that dictionary in config for subsubclustering mapping is correct")
    input("Press Enter to continue with the cluster numbers below for subgroups creation...")

    # Run the K means clustering to create subgroups, mapping in config for this
    subgrouped_variable_df = run_subclustering(input_df=grouped_variable_df, 
                                               output_location=f"{output_directory}cluster_assignments/subgroup", 
                                               drop_columns=['cluster', 'subcluster'],
                                               column_name="subsubcluster",
                                               cluster_col_name="subcluster",
                                               cluster_to_numbers = config["subsubclustering_mapping"],
                                               n_init=n_init,
                                               random_seed=random_seed)
    
    logger.info("subgroup cluster run completed.")
    
    logger.info("Final output for supergroup, group and subgroup saved to outputs_data folder")
    return subgrouped_variable_df

## Clustergrams
# We produce a clustergram plot to assess an appropriate number of clusters for the supergroups.
# Some guidance on interpreting clustergrams and choosing the number of clusters can be found here: 
# [Clustergram](https://clustergram.readthedocs.io/en/stable/notebooks/introduction.html)

def create_clustergram(df, number_of_clusters, n_init, save_location, random_seed=None):
    """
    Create and save a clustergram for evaluating k-means clustering solutions.

    The clustergram visualizes clustering stability and helps identify the optimal 
    number of clusters by performed the k-means algorithm for a range of cluster
    numbers.
    Since k-means is sensitive to initialization, `n_init` determines the number of 
    times the algorithm runs with different centroid seeds. The final result is the 
    best outcome based on inertia/WCSS (within-cluster sum of squares).

    Parameters
    ----------
    df : pd.DataFrame or np.ndarray
        The input data for clustering.
    number_of_clusters : int
        The number of clusters.
    n_init : int
        Number of k-means runs with different initial centroid seeds. 
                  Higher values (e.g., ~1000) improve solution stability but increase runtime.
    save_location : str
        File path to save the clustergram plot.
    random_seed : int, optional
        Random seed for reproducibility.
    """
    # Validate the number of clusters
    if len(df) < number_of_clusters:
        logger.warning(f"Warning: Reducing number_of_clusters from {number_of_clusters} to {len(df)} (number of samples).")
        number_of_clusters = len(df)

    # Create the clustergram
    # Define the range of clusters to evaluate
    k_range = range(1, number_of_clusters + 1)  # Start from 2 clusters up to number_of_clusters

    # Create the clustergram
    cgram = Clustergram(k_range=k_range, method='kmeans', random_state=random_seed, n_init=n_init)
    
    cgram.fit(df)  # Fit model to data
    cgram.plot()  # Generate plot
    plt.savefig(save_location)  # Save figure
    # plt.show()  # Display plot

## Clusters = supergroup
# Run kmeans to cluster the geographies in K clusters (supergroups)

def run_kmeans(input_df, number_of_clusters, n_init, output_filepath, random_seed=None):
    """
    Run K-means clustering on the input dataset and save the cluster assignments.

    This function applies K-means clustering to the provided dataset, assigns cluster 
    labels to each row, and saves the cluster assignments as a lookup table.

    Parameters
    ----------
    input_df : pd.DataFrame
        The input dataset to be clustered.
    number_of_clusters : int
        The number of clusters (K) to create.
    n_init : int
        Number of times the K-means algorithm runs with different initial centroid seeds. 
        The best result based on inertia/WCSS is chosen. A higher value (e.g., ~1000) is 
        recommended for final results, but a lower value can be used for testing.
    output_filepath : str
        Path to save the resulting cluster assignments.
    random_seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        The input DataFrame with an added 'cluster' column containing 
        the assigned cluster for each row.
    """
    df = input_df.copy()
    if number_of_clusters > len(df):
        logger.warning(f"Warning: Reducing number_of_clusters from {number_of_clusters} to {len(df)} (number of samples).")
        number_of_clusters = len(df)
    # Initialize the K-means model
    kmeans_model = KMeans(n_clusters=number_of_clusters, max_iter=1000, random_state=random_seed, n_init=n_init)
    
    # Fit the model and assign clusters
    df['cluster'] = kmeans_model.fit_predict(df)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    # Save the cluster assignments to a CSV file
    df[['cluster']].to_csv(output_filepath)

    # Show the first few rows of the assigned clusters
    logger.info(f"K-means clusters:\n{df[['cluster']].head()}")

    return df


## Subclusters = groups and subgroups
# For LAD area classification the supergroup clusters created above are split further into groups and subgroups by applying the above process iteratively. 

def create_subcluster_clustergrams(cluster_variable_df, clustergram_directory, number_of_clusters, drop_columns, cluster_col_name, n_init, random_seed=None):
    """
    Generate and save clustergrams for each supercluster.
    This function loops through the existing clusters and creates a clustergram 
    for each
    
    Parameters
    ----------
    cluster_variable_df : pd.DataFrame
        DataFrame containing cluster assignments.
    number_of_clusters : int
        The total number of clusters to iterate over.
    clustergram_directory : str
        The clustergram directory path to save the resulting clustergram plots.
    n_init : int, optional
        The number of times KMeans will be initialized. Defaults to 10. Increase for more stable results.
    """
    # Get all unique values in the 'subcluster' column
    unique_subclusters = cluster_variable_df[cluster_col_name].unique()

    # Iterate through the unique values
    for subcluster in unique_subclusters:
        # Select rows corresponding to the current cluster
        filtered_df = cluster_variable_df[cluster_variable_df[cluster_col_name] == subcluster]
        # Drop the cluster related columns after filtering as they are strings.
        subcluster_df = filtered_df.drop(columns=drop_columns)
        logger.info(f"Cluster: {subcluster}, {len(subcluster_df)} geographies in cluster")
 
        # Define save location
        save_location = os.path.join(clustergram_directory, f"subcluster_clustergram_cluster{subcluster}.png")
        logger.info(f"Saving clustergram to {save_location}")

        if len(subcluster_df) <= 2:
            # Skip this subcluster if it has insufficient data points (2 or fewer).
            # For example when running on number_of_times_k_means_initialised = 1000 the Oxford and Cambridge
            # subgroup have an errors when creating the clustergram so skip this subcluster instead.
            logger.info(f"Skipping cluster {subcluster} due to insufficient data points ({len(subcluster_df)}).")
            continue
        else:
            # Generate clustergram
            create_clustergram(subcluster_df, number_of_clusters, n_init=n_init, save_location=save_location, random_seed=random_seed)

def run_subclustering(input_df, output_location,drop_columns,column_name, cluster_col_name, cluster_to_numbers, n_init, random_seed = None) -> pd.DataFrame:
    """
    Runs subclustering for each supergroup using KMeans and returns a modified DataFrame with subcluster labels.
    
    Parameters
    ----------
    input_df : pd.DataFrame
        The original DataFrame containing data and cluster assignments.
    output_location : str
        The filepath for where the output tables will be saved.
    drop_columns
    column_name
    cluster_col_name
    cluster_to_numbers
    n_init : int, optional
        The number of times KMeans will be initialized. Defaults to 100. Increase for more stable results.
    random_seed = None

    Returns
    -------
    pd.DataFrame
        A new the output dataFrame with an added 'subcluster' column.
    """

    # create a directory to save the subcluster outputs
    os.makedirs(output_location, exist_ok=True)

    # Work on a copy of the DataFrame to prevent unintended modifications
    df = input_df.copy()

    # Changed cluster from an integer to a string
    for cluster, num_subclusters in cluster_to_numbers.items():

        logger.info(f"Clustering supergroup {cluster} into {cluster_to_numbers[cluster]} subclusters.")

        # Select rows corresponding to the current cluster, drop the cluster column before clustering
        logger.debug(f"input_df shape: {input_df.shape}")
        cluster_df = input_df.query(f"{cluster_col_name} == @cluster").drop(columns=drop_columns).copy()
        logger.debug(f"cluster_df shape: {cluster_df.shape}")

        # Run KMeans clustering for the selected supergroup
        subcluster_output_df = run_kmeans(
            cluster_df, 
            num_subclusters, 
            n_init=n_init, 
            output_filepath=output_location+f"/supergroup{cluster}_subclusteroutput.csv",
            random_seed=random_seed  # Use a different random seed for each subclustering to ensure diversity
        )

        # Improve interpretability of the clustering results by convert subcluster numbers (0, 1, 2)
        # into a more readable format ('0a', '0b', '0c'). Tthe numeric part represents the main cluster 
        # The letter represents the subcluster.
        subcluster_output_df[column_name] = [str(cluster) + chr(97 + i) for i in subcluster_output_df["cluster"]]

        # Update the modified DataFrame with subclustering results
        df.loc[cluster_df.index, column_name] = subcluster_output_df[column_name]

    # Save the cluster outputs one directory up from the output_location - the cluster assignment folder
    if column_name == "subcluster":
        file_name = "group_clustering_output.csv"
    elif column_name == "subsubcluster":
        file_name = "subgroup_clustering_output.csv"
    else:
        file_name = f"{column_name}_output_.csv"

    cluster_assignment_location = os.path.dirname(output_location)
    df[[column_name]].to_csv(f"{cluster_assignment_location}/{file_name}")

    logger.info(f"Subcluster Output DataFrame shape: {subcluster_output_df.shape}")

    return df  # Return the modified DataFrame with clusters and subclusters


if __name__ == "__main__":
    config = load_config()

    function_output = clustering_wrapper(config,
        input_dataframe= config["pre_clustering_data_std_mean"],
        number_of_clusters=config["number_of_clusters"],
        n_init=config["number_of_times_k_means_initialised"],
        output_directory=config["output_directory"],
        clustergram_directory=config["clustergram_directory"],
        random_seed=config["random_seed"])
    print(function_output.head())
    function_output.to_csv('function_output.csv', index=False)
