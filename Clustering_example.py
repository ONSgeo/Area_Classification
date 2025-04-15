# Install dependencies if running in a new environment and not using requirements.txt
%pip install pandas clustergram scikit-learn matplotlib

## Geodemographic python example
# This notebook contains the workflow for producing a geodemographic classification in python using k-means clustering. 
#It follows a simplified process, similar to that described in the [2021 OAC Paper](https://rgs-ibg.onlinelibrary.wiley.com/doi/full/10.1111/geoj.12550).

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from clustergram import Clustergram
import matplotlib.pyplot as plt
import os
# set a  random seed for reproducibility
random_seed = 507


# create outputs and plots directories if they do not exist
OUTPUT_DIR = "outputs"
PLOT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

# load the input data from a csv file 
# The names of the columns are not important, BUT;
# the first column should be the geography code (e.g., Output Area or Local Authority District),
# which will be used as the DataFrame index.
# The remaining columns should be variables for clustering, provided as fractions or percentages of the table total.
def load_data(filepath):
    input_df = pd.read_csv(filepath, index_col=0)
    
    # Check for missing values
    missing_values = input_df.isnull().sum().sum()
    if missing_values > 0:
        print(f"Warning: {missing_values} missing values found in input data. Missing values will be replaced with 0.")
        input_df.fillna(0, inplace=True)
    
    return input_df

# File path to the dataset
inputdata_filepath = "example_oacdata.csv"

# Load the dataset
variable_df = load_data(inputdata_filepath)
# show first 5 rows of the dataset
variable_df.head()


## Data transformation
# Transform the input data to make it more suitable for clustering

def transform_and_standardize_data(df):
    """
    Apply data transformations to handle non-normality and scale the data:
    1. Apply the inverse hyperbolic sine (arcsinh) transformation to reduce skewness.
    2. Perform min-max scaling to normalize the data to a range of [0, 1].
    
    Args:
        df (pd.DataFrame): Input dataframe with numerical data to transform.
    
    Returns:
        pd.DataFrame: Transformed and standardized dataframe.
    """
    df = np.arcsinh(df) # Apply inverse hyperbolic sine transformation
    df = (df - df.min()) / (df.max() - df.min()) # Apply min-max scaling
    return df

# Apply the transformation and standardization to the input data
transformed_variable_df = transform_and_standardize_data(variable_df)
transformed_variable_df.head()


## Clustergrams
# We produce a clustergram plot to assess an appropriate number of clusters for the supergroups.
# For OAC, eight supergroups were created.
# Some guidance on interpreting clustergrams and choosing the number of clusters can be found here: [Clustergram](https://clustergram.readthedocs.io/en/stable/notebooks/introduction.html)

def create_clustergram(df, n_init, save_loc, random_seed=random_seed):
    """
    Create and save a clustergram for evaluating k-means clustering solutions.

    The clustergram visualizes clustering stability and helps identify the optimal 
    number of clusters by performed the k-means algorithm for a range of cluster
    numbers.
    Since k-means is sensitive to initialization, `n_init` determines the number of 
    times the algorithm runs with different centroid seeds. The final result is the 
    best outcome based on inertia/WCSS (within-cluster sum of squares).

    Parameters:
    df (pd.DataFrame or np.ndarray): The input data for clustering.
    n_init (int): Number of k-means runs with different initial centroid seeds. 
                  Higher values (e.g., ~1000) improve solution stability but increase runtime.
    save_loc (str): File path to save the clustergram plot.
    random_seed (int, optional): Random seed for reproducibility.
    """
    cgram = Clustergram(range(1, 15), n_init=n_init, random_state=random_seed)  # Initialize clustergram model
    cgram.fit(df)  # Fit model to data
    cgram.plot()  # Generate plot
    plt.savefig(save_loc)  # Save figure
    plt.show()  # Display plot

# Example usage
n_init = 10  # Use a low value for quick testing, increase for final results
create_clustergram(transformed_variable_df, n_init, save_loc=PLOT_DIR+"/supergroup_clustergram.png")


## Supergroup Clustering
# Run kmeans to cluster the geographies in K clusters (supergroups)

def run_kmeans(input_df, num_clusters, n_init = 1000, output_filepath = "output.csv", random_seed=None):
    """
    Run K-means clustering on the input dataset and save the cluster assignments.

    This function applies K-means clustering to the provided dataset, assigns cluster 
    labels to each row, and saves the cluster assignments as a lookup table.

    Parameters:
    input_df (pd.DataFrame): The input dataset to be clustered.
    num_clusters (int): The number of clusters (K) to create.
    n_init (int): Number of times the K-means algorithm runs with different initial 
                  centroid seeds. The best result based on inertia/WCSS is chosen. 
                  A higher value (e.g., ~1000) is recommended for final results, 
                  but a lower value can be used for testing.
    output_filepath (str): Path to save the resulting cluster assignments.
    random_seed (int, optional): Random seed for reproducibility.

    Returns:
    pd.DataFrame: The input DataFrame with an added 'cluster' column containing 
                  the assigned cluster for each row.
    """
    df = input_df.copy()
    # Initialize the K-means model
    kmeans_model = KMeans(n_clusters=num_clusters, max_iter=1000, random_state=random_seed, n_init=n_init)
    
    # Fit the model and assign clusters
    df['cluster'] = kmeans_model.fit_predict(df)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    # Save the cluster assignments to a CSV file
    df[['cluster']].to_csv(output_filepath)

    # Show the first few rows of the assigned clusters
    print(f"K-means clusters:\n{df[['cluster']].head()}")

    return df

# Define the number of clusters (K). Choose K based on the clustergram plot.
num_clusters = 8 
n_init = 100  #1000 is recommended for final results, but a lower value can be used for testing as it is faster
output_filepath = OUTPUT_DIR+"/supergroups_clusteroutput.csv"

# Run K-means clustering
supergrouped_variable_df = run_kmeans(transformed_variable_df, num_clusters, n_init, output_filepath = output_filepath, random_seed=random_seed)

#supregrouped_variable_df contains the cluster assignments for each row in the input data, and the input data itself.
supergrouped_variable_df.head()


## Subgroups
# For OAC the supergroup clusters created above are split further into groups and subgroups by applying the above process iteratively. 
# Example code for creating the first layer of subclusters (groups) is below

def create_subcluster_clustergrams(output_df, num_clusters, n_init=10):
    """
    Generate and save clustergrams for each supercluster.
    This function loops through the existing clusters and creates a clustergram 
    for each
    Parameters:
    output_df (pd.DataFrame): DataFrame containing cluster assignments.
    num_clusters (int): The total number of clusters to iterate over.
    n_init (int, optional): The number of times KMeans will be initialized. Defaults to 10. Increase for more stable results.
                            

    """

    for cluster in range(num_clusters):
        # Select rows corresponding to the current cluster, dropping the 'cluster' column
        cluster_df = output_df.query(f"cluster == {cluster}").drop(columns='cluster')

        print(f"Cluster: {cluster}, {len(cluster_df)} geographies in cluster")

        # Define save location
        save_loc = os.path.join(PLOT_DIR, f"subcluster_clustergram_cluster{cluster}.png")
        print(f"Saving clustergram to {save_loc}")

        # Generate clustergram
        create_clustergram(cluster_df, n_init=n_init, save_loc=save_loc)

# Create clustergrams for splitting each of the superclusters
create_subcluster_clustergrams(supergrouped_variable_df, num_clusters, n_init=10)



def run_subclustering(input_df, subcluster_nums, num_clusters, n_init= 1000) -> pd.DataFrame:
    """
    Runs subclustering for each supergroup using KMeans and returns a modified DataFrame with subcluster labels.
    
    Parameters:
    - output_df (pd.DataFrame): The original DataFrame containing data and cluster assignments.
    - subcluster_nums (list): A list specifying the number of subclusters to split each supergroup into.
    - num_clusters (int): The total number of supergroups.
    - n_init (int, optional): The number of times KMeans will be initialized. Defaults to 100. Increase for more stable results.

    Returns:
    - pd.DataFrame: A new the output dataFrame with an added 'subcluster' column.
    """

    # create a directory to save the subcluster outputs
    os.makedirs(OUTPUT_DIR+"/subclusters", exist_ok=True)

    if len(subcluster_nums) != num_clusters:
        raise ValueError(f"Length of subcluster_nums ({len(subcluster_nums)}) does not match num_clusters ({num_clusters}).")

    # Work on a copy of the DataFrame to prevent unintended modifications
    df = input_df.copy()


    for cluster, num_subclusters in zip(range(num_clusters), subcluster_nums): # Iterate over each supergroup
        print(f"Clustering supergroup {cluster} into {num_subclusters} subclusters.")

        # Select rows corresponding to the current cluster, drop the cluster column before clustering
        cluster_df = input_df.query(f"cluster == {cluster}").drop(columns='cluster').copy()
        # Run KMeans clustering for the selected supergroup
        subcluster_output_df = run_kmeans(
            cluster_df, 
            num_subclusters, 
            n_init=n_init, 
            output_filepath=OUTPUT_DIR+f"/subclusters/supergroup{cluster}_subclusteroutput.csv"
        )

        # Convert subcluster numbers (0, 1, 2, ...) into a more readable format (e.g., '0a', '0b', '0c', ...),
        # where the numeric part represents the main cluster and the letter represents the subcluster.
        # This improves interpretability of the clustering results.
        subcluster_output_df['subcluster'] = [str(cluster) + chr(97 + i) for i in subcluster_output_df['cluster']]

        # Update the modified DataFrame with subclustering results
        df.loc[cluster_df.index, 'subcluster'] = subcluster_output_df['subcluster']

    # Save the final output
    df[["subcluster"]].to_csv(OUTPUT_DIR+"/subgroups_clusteroutput.csv")
    print("Final output saved to outputs/subgroups_clusteroutput.csv")

    return df  # Return the modified DataFrame with clusters and subclusters


# We can now select the number of subclusters to split each of the supergroups into using the clustergrams above.
# For this example, we choose three subclusters for each supergroup.
# The length of the list must match num_clusters (the number of supergroups).

subcluster_nums = [3, 3, 3, 3, 3, 3, 3, 3]
# Example with different number of subclusters for each supergroup
# subcluster_nums = [2, 4, 2, 2, 5, 2, 3, 3]

# num clusters is the number of supergroups (set earlier)
# n_init is the number of times the KMeans algorithm will be initialized (as before)
n_init = 1000
subgrouped_variable_df = run_subclustering(supergrouped_variable_df, subcluster_nums, num_clusters, n_init)
