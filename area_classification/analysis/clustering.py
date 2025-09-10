## Clustering
# Note: Supergroup = cluster, group = subcluster, subgroup = subsubcluster.

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from clustergram import Clustergram
import matplotlib.pyplot as plt
import os
import logging

#logging.basicConfig(level=logger.info, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

from utilities.load_config import load_config

#REQUIRED TO MAKE RADIAL PLOTS EARLY - need updating as radial plot function changed
from post_processing.create_radial_plots import create_radial_plots
from post_processing.cluster_variables_mean import cluster_variable_means
from post_processing.cluster_table_restructure import cluster_table_restructure
# from post_processing.cluster_std_means_to_parent_clusters import cluster_std_means_to_parent_clusters   


def clustering_wrapper(config: dict,
                       #input_dataframe_or_filepath: str | pd.DataFrame, 
                       input_dataframe_or_filepath: pd.DataFrame,
                       num_clusters: int,
                       n_init: int, 
                       output_directory: str, 
                       plot_directory: str,
                       random_seed: int = None) -> pd.DataFrame:
    """
    Wrapper function to perform clustering on input data, create supergroups and subgroups.

    Parameters
    ----------
    config : dict
        A dictionary containing user configuration settings.
    input_dataframe_or_filepath : str or pd.DataFrame
        Path to the input data CSV file or a pandas DataFrame.
    num_clusters : int
        Number of superclusters to create.
    n_init : int
        Number of times KMeans will be initialized.
    output_directory : str
        Directory to save the final cluster assignments.
    plot_directory : str
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
    os.makedirs(plot_directory, exist_ok=True)
    
    if isinstance(input_dataframe_or_filepath, str):
        #If a file path is provided, load the data from the CSV file
        logger.info(f"Loading data from {input_dataframe_or_filepath}")
        variable_df = load_data(input_dataframe_or_filepath)
    elif isinstance(input_dataframe_or_filepath, pd.DataFrame):
        # If a DataFrame is provided, use it directly
        logger.info("Using provided DataFrame for clustering.")
        variable_df = input_dataframe_or_filepath.copy()
        variable_df.set_index(variable_df.columns[0], inplace=True)
        missing_values = variable_df.isnull().sum().sum()
        if missing_values > 0:
            logger.warning(f"Warning: {missing_values} missing values found in input data. Missing values will be replaced with 0.")
            variable_df.fillna(0, inplace=True)
            
    else:
        raise ValueError("Input must be a file path (str) or a pandas DataFrame.")


    # Validate num_clusters compared to input data
    if len(variable_df) < num_clusters:
        logging.warning(f"Warning: Reducing num_clusters from {num_clusters} to {len(variable_df)}.")
        num_clusters = len(variable_df)


    create_clustergram(variable_df,
                       num_clusters, 
                       n_init, 
                       save_loc=plot_directory+"/supergroup_clustergram.png",
                       random_seed=random_seed)
    output_filepath = output_directory+"/supergroups_clusteroutput.csv"
    logger.info("create supergroup clustergrams completed.")

    # Add a break
    input("Press Enter to continue with supergroups creation...")
    
    ###SUPERGROUP SECTION ###

    supergroup_variable_df = run_kmeans(variable_df, 
                                          num_clusters, 
                                          n_init, 
                                          output_filepath, 
                                          random_seed)
    logger.info("Kmeans run completed.")

    # Validate num_clusters
    if len(supergroup_variable_df) < num_clusters:
        logger.warning(f"Warning: Reducing num_clusters from {num_clusters} to {len(supergroup_variable_df)}.")
        num_clusters = len(supergroup_variable_df)

    # Add a break
    input("Press Enter to create radial plots for supergroups...")
    
    # # WHILST TESTING WITH JEN - CREATING RADIAL PLOTS EARLY
    # # Create radial plots of supergroup against UK
    # clustering_output = pd.read_csv('data/output_data/supergroups_clusteroutput.csv')
    # chosen_clustering_variables_std =pd.read_csv(config["pre_clustering_data_std_mean"])
    # restructured_cluster_table_df = cluster_table_restructure(config, clustering_output, 'cluster', chosen_clustering_variables_std)
    # print(type(restructured_cluster_table_df))  # Should be DataFrame
    # print(type(chosen_clustering_variables_std))  # Should be DataFrame
    # uk_std_cluster_means = cluster_variable_means(config, restructured_cluster_table_df, chosen_clustering_variables_std)

    # Create radial plots for supergroups, groups and subgroups against UK
    #create_radial_plots(config, uk_std_cluster_means, level="UK")

    # Add a break
    input(f"Unique clusters at this stage: {supergroup_variable_df['cluster'].unique()}")
    input("Check that dictionary in config for subsubclustering mapping is correct")
    input("Press Enter to continue to move onto groups...")

    ###GROUP SECTION ###

    # Call the function with the adjusted number of clusters - if we try and group 10 data points in 11 clusters it will fail
    # function should take inpupt of highest amount of clusters to look at
    create_subcluster_clustergrams(output_df=supergroup_variable_df,
                                   plot_dir=plot_directory, 
                                   num_clusters=num_clusters, 
                                   drop_columns=['cluster'],
                                   cluster_col_name='cluster',
                                   n_init=n_init,
                                   random_seed=random_seed)
    logger.info("group clustergrams completed.")
    
    # Add a break
    input("Press Enter to continue with the subcluster numbers below for groups creation...")


    grouped_variable_df = run_subclustering(input_df=supergroup_variable_df, 
                                            output_dir=f"{output_directory}group", 
                                            drop_columns=["cluster"], 
                                            column_name="subcluster",
                                            cluster_col_name="cluster",
                                            cluster_to_numbers = config["subclustering_mapping"],
                                            n_init=n_init,
                                            random_seed=random_seed)
    logger.info("groups cluster run completed.")

    # Add a break
    input("Press Enter to create radial plots for groups...")
    # WHILST TESTING WITH JEN - CREATING RADIAL PLOTS EARLY
    # Create radial plots of group against parents (supergroup)
    # clustering_output = pd.read_csv('data/output_data/group/subclustering_output.csv')
    # restructured_cluster_table = cluster_table_restructure(config, clustering_output, 'subcluster')
    # chosen_clustering_variables =pd.read_csv(config["pre_clustering_data_filtered"])
    # combined_group_means, combined_subgroup_means = cluster_std_means_to_parent_clusters(
    #     config, restructured_cluster_table, chosen_clustering_variables
    # )
    # # Create radial plots for groups against their parent (groups)
    # create_radial_plots(config, combined_group_means, level="group")

    # Add a break
    input("Press Enter to continue to move onto subgroup...")
    print(grouped_variable_df)
    ###SUBGROUP SECTION ###    
    create_subcluster_clustergrams(output_df=grouped_variable_df,
                                   plot_dir=plot_directory, 
                                   num_clusters=num_clusters, 
                                   drop_columns=['cluster', 'subcluster'],
                                   cluster_col_name='subcluster',
                                   n_init=n_init,
                                   random_seed=random_seed)
    logger.info("subgroup clustergrams completed.")
    # Add a break
    input(f"Unique subclusters at this stage: {grouped_variable_df['subcluster'].unique()}")
    input("Check that dictionary in config for subsubclustering mapping is correct")
    input("Press Enter to continue with the cluster numbers below for subgroups creation...")

    subgrouped_variable_df = run_subclustering(input_df=grouped_variable_df, 
                                               output_dir=f"{output_directory}subgroup", 
                                               drop_columns=['cluster', 'subcluster'],
                                               column_name="subsubcluster",
                                               cluster_col_name="subcluster",
                                               cluster_to_numbers = config["subsubclustering_mapping"],
                                               n_init=n_init,
                                               random_seed=random_seed)
    
    # Add a break
    input("Press Enter to create radial plots for subgroups...")
    # WHILST TESTING WITH JEN - CREATING RADIAL PLOTS EARLY
    # Create radial plots of supergroup against UK

    #clustering_output = pd.read_csv('data/output_data/subgroup/subclustering_output.csv')
    #restructured_cluster_table_df = cluster_table_restructure(config, clustering_output, 'subsubcluster')
    #chosen_clustering_variables_std =pd.read_csv(config["pre_clustering_data_std_mean"])
    #uk_std_cluster_means = cluster_variable_means(config, restructured_cluster_table_df, chosen_clustering_variables_std)
    #create_radial_plots_uk(config, uk_std_cluster_means)

    logger.info("subgroup cluster run completed.")
    
    logger.info("Final output for supergroup, group and subgroup saved to outputs_data folder")
    return subgrouped_variable_df

def load_data(filepath):
    # load the input data from a csv file 
    # The names of the columns are not important, first column should be geography code used as DataFrame index
    # Remaining columns should be variables for clustering, provided as fractions or percentages of the table total.
    input_df = pd.read_csv(filepath, index_col=0)

    # Check for missing values
    missing_values = input_df.isnull().sum().sum()
    if missing_values > 0:
        logger.warning(f"Warning: {missing_values} missing values found in input data. Missing values will be replaced with 0.")
        input_df.fillna(0, inplace=True)

    return input_df


def transform_and_standardize_data(df):
    """
    Apply data transformations to handle non-normality and scale the data:
    1. Apply the inverse hyperbolic sine (arcsinh) transformation to reduce skewness.
    2. Perform min-max scaling to normalize the data to a range of [0, 1].
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with numerical data to transform.
    
    Returns
    -------
    pd.DataFrame
        Transformed and standardized dataframe.
    """

    df = np.arcsinh(df) # Apply inverse hyperbolic sine transformation
    df = (df - df.min()) / (df.max() - df.min()) # Apply min-max scaling
    return df



## Clustergrams
# We produce a clustergram plot to assess an appropriate number of clusters for the supergroups.
# Some guidance on interpreting clustergrams and choosing the number of clusters can be found here: [Clustergram](https://clustergram.readthedocs.io/en/stable/notebooks/introduction.html)

def create_clustergram(df, num_clusters, n_init, save_loc, random_seed=None):
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
    num_clusters : int
        The number of clusters.
    n_init : int
        Number of k-means runs with different initial centroid seeds. 
                  Higher values (e.g., ~1000) improve solution stability but increase runtime.
    save_loc : str
        File path to save the clustergram plot.
    random_seed : int, optional
        Random seed for reproducibility.
    """
    # Validate the number of clusters
    if len(df) < num_clusters:
        logger.warning(f"Warning: Reducing num_clusters from {num_clusters} to {len(df)} (number of samples).")
        num_clusters = len(df)
    
    # Create the clustergram
    # Define the range of clusters to evaluate
    k_range = range(1, num_clusters + 1)  # Start from 2 clusters up to num_clusters

    # Create the clustergram
    cgram = Clustergram(k_range=k_range, method='kmeans', random_state=random_seed, n_init=n_init)
    
    cgram.fit(df)  # Fit model to data
    cgram.plot()  # Generate plot
    plt.savefig(save_loc)  # Save figure
    # plt.show()  # Display plot

## Clusters = supergroup
# Run kmeans to cluster the geographies in K clusters (supergroups)

def run_kmeans(input_df, num_clusters, n_init = 1000, output_filepath = "output.csv", random_seed=None):
    """
    Run K-means clustering on the input dataset and save the cluster assignments.

    This function applies K-means clustering to the provided dataset, assigns cluster 
    labels to each row, and saves the cluster assignments as a lookup table.

    Parameters
    ----------
    input_df : pd.DataFrame
        The input dataset to be clustered.
    num_clusters : int
        The number of clusters (K) to create.
    n_init : int
        Number of times the K-means algorithm runs with different initial centroid seeds. 
        The best result based on inertia/WCSS is chosen. A higher value (e.g., ~1000) is 
        recommended for final results, but a lower value can be used for testing.
    output_filepath : str
        Path to save the resulting cluster assignments.
    random_seed : int, optional
        Random seed for reproducibility.

    Returns:
    pd.DataFrame
        The input DataFrame with an added 'cluster' column containing 
        the assigned cluster for each row.
    """
    df = input_df.copy()
    if num_clusters > len(df):
        logger.warning(f"Warning: Reducing num_clusters from {num_clusters} to {len(df)} (number of samples).")
        num_clusters = len(df)
    # Initialize the K-means model
    kmeans_model = KMeans(n_clusters=num_clusters, max_iter=1000, random_state=random_seed, n_init=n_init)
    
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

def create_subcluster_clustergrams(output_df, plot_dir, num_clusters, drop_columns,cluster_col_name, n_init=10, random_seed=None):
    """
    Generate and save clustergrams for each supercluster.
    This function loops through the existing clusters and creates a clustergram 
    for each
    
    Parameters
    ----------
    output_df : pd.DataFrame
        DataFrame containing cluster assignments.
    num_clusters : int
        The total number of clusters to iterate over.
    plot_dir : str
        Path to save the resulting clustergram plots.
    n_init : int, optional
        The number of times KMeans will be initialized. Defaults to 10. Increase for more stable results.
    """

    for cluster in range(num_clusters):
        # Select rows corresponding to the current cluster, dropping the 'cluster' column
        cluster_df = output_df.query(f"cluster == {cluster}").drop(columns=drop_columns)

        logger.info(f"Cluster: {cluster}, {len(cluster_df)} geographies in cluster")
 
        # Define save location
        save_loc = os.path.join(plot_dir, f"subcluster_clustergram_cluster{cluster}.png")
        logger.info(f"Saving clustergram to {save_loc}")

        # Generate clustergram
        create_clustergram(cluster_df, num_clusters, n_init=n_init, save_loc=save_loc, random_seed=random_seed)


def run_subclustering(input_df, output_dir,drop_columns,column_name, cluster_col_name, cluster_to_numbers, n_init= 1000, random_seed = None) -> pd.DataFrame:
    """
    Runs subclustering for each supergroup using KMeans and returns a modified DataFrame with subcluster labels.
    
    Parameters
    ----------
    output_df : pd.DataFrame
        The original DataFrame containing data and cluster assignments.
    n_init : int, optional
        The number of times KMeans will be initialized. Defaults to 100. Increase for more stable results.

    Returns
    -------
    pd.DataFrame
        A new the output dataFrame with an added 'subcluster' column.
    """

    # create a directory to save the subcluster outputs
    os.makedirs(output_dir+"/subclusters", exist_ok=True)

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
            output_filepath=output_dir+f"/subclusters/supergroup{cluster}_subclusteroutput.csv",
            random_seed=random_seed  # Use a different random seed for each subclustering to ensure diversity
        )

        # Improve interpretability of the clustering results by convert subcluster numbers (0, 1, 2)
        # into a more readable format ('0a', '0b', '0c'). Tthe numeric part represents the main cluster 
        # The letter represents the subcluster.
        subcluster_output_df[column_name] = [str(cluster) + chr(97 + i) for i in subcluster_output_df["cluster"]]

        # Update the modified DataFrame with subclustering results
        df.loc[cluster_df.index, column_name] = subcluster_output_df[column_name]

    # Save the final output
    df[[column_name]].to_csv(output_dir+"/subclustering_output.csv")

    logger.info(f"Subcluster Output DataFrame shape: {subcluster_output_df.shape}")
    subcluster_output_df.to_csv('subcluster_output_df.csv', index=False)

    return df  # Return the modified DataFrame with clusters and subclusters


if __name__ == "__main__":
    config = load_config()

    function_output = clustering_wrapper(config,
        input_dataframe_or_filepath= config["pre_clustering_data_std_mean"],
        num_clusters=config["number_of_clusters"],
        n_init=config["number_of_times_k_means_initialised"],
        output_directory=config["output_directory"],
        plot_directory=config["plot_directory"],
        random_seed=config["random_seed"])
    print(function_output.head())
    function_output.to_csv('function_output.csv', index=False)
