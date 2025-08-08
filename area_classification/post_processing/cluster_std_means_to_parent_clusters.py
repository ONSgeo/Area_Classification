
# This script creates means standardized to the parent cluster
# group means standardised to the supergroup mean
# subgroup means standardised to the group mean

import pandas as pd
import os

from utilities.load_config import load_config
config = load_config('area_classification/config.yaml')

def cluster_std_means_to_parent_clusters(config):
    """
    This function reads the clustering output CSV file, calculates the means for each cluster,
    and standardizes these means to their parent clusters. It then saves the standardized means
    to a new CSV file.

    Parameters:
        config (dict): Configuration dictionary containing paths and parameters.
        processed_subclustering_output_df: DataFrame containing the clustering output data.
        pre_clustering_data_df: DataFrame containing the input data used for clustering, in percentages.

    Returns:
        pd.DataFrame: DataFrame containing standardized means for each cluster.
    """

    # Load in the pre-clustering percentages data
    pre_clustering_data = config["pre_clustering_data_df"]
    pre_clustering_data_df = pd.read_csv(pre_clustering_data)

    # Load the clustering output data
    processed_subclustering_output = config["processed_subclustering_output_df"]
    processed_subclustering_output_df = pd.read_csv(processed_subclustering_output)

        # Isolate LAD_names for each supergroup
    lad_names_by_supergroup = (
        processed_subclustering_output_df.groupby("supergroup")["LAD_name"]
        .apply(list)
        .to_dict()
    )

    # Print the LAD_names grouped by supergroup
    for supergroup, lad_names in lad_names_by_supergroup.items():
        print(f"Supergroup {supergroup}: {lad_names}")

    # Return the dictionary for further use if needed
    return lad_names_by_supergroup

if __name__ == "__main__":
    cluster_std_means_to_parent_clusters(config)









