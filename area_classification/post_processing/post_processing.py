# Post clustering wrapper
import os
import pandas as pd
from utilities.load_config import load_config
from area_classification.cluster_table_restructure import cluster_table_restructure  
from post_processing.cluster_variables_mean import cluster_variable_means
from post_processing.cluster_std_means_to_parent_clusters import cluster_std_means_to_parent_clusters  
from post_processing.create_radial_plots import create_radial_plots_wrapper

def post_processing(config, clustering_output, chosen_clustering_variables_std, chosen_clustering_variables):
    """
    Wrapper function to run restrcuture the table created when clustering, 
    
    Parameters
    ----------
    config : dict
        main pipeline config dictionary containing output directory.
    chosen_clustering_variables

    clustering_output : pd.DataFrame
        the output from running the clustering algroithm

    Returns
    ----------
        The result of get_cluster_means.
    """

    # Step 1: Restructure the cluster table to have separate columns for supergroup, group and subgroup
    restructured_cluster_table_df = cluster_table_restructure(config, clustering_output, config["split_column"],chosen_clustering_variables_std)

    # Step 2: Calculate means for each cluster and each variable
    uk_std_cluster_means = cluster_variable_means(config, restructured_cluster_table_df, chosen_clustering_variables_std)

    # Step 3: Run cluster_std_means_to_parent_clusters and capture the returned means
    combined_group_means, combined_subgroup_means = cluster_std_means_to_parent_clusters(
        config, restructured_cluster_table_df, chosen_clustering_variables
    )

    # Step 4: Create radial plots for the clusters using the combined means
    create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means)

    # Return the combined means for further use if needed
    return combined_group_means, combined_subgroup_means
    

# Run the function if the script is executed directly
if __name__ == "__main__":
    config = load_config('area_classification/config.yaml')
    clustering_output_filepath = os.path.join(config["output_directory"], "subgroup", "subclustering_output.csv")
    clustering_output = pd.read_csv(clustering_output_filepath)
    chosen_clustering_variables = config["pre_clustering_data_filtered_std_mean"]
    post_processing(config, chosen_clustering_variables, clustering_output)
