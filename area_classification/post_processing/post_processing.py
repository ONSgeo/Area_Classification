# Post clustering wrapper
import os
import pandas as pd
from area_classification.utilities.load_config import load_config
from area_classification.post_processing.cluster_table_restructure import cluster_table_restructure  
from area_classification.post_processing.cluster_variables_mean import cluster_variable_means
from area_classification.post_processing.cluster_std_means_to_parent_clusters import cluster_std_means_to_parent_clusters  
from area_classification.post_processing.create_radial_plots import create_radial_plots_wrapper
from area_classification.post_processing.cluster_summaries import cluster_summaries_wrapper
from area_classification.pre_processing.prepare_clustering_data import standardise_data

def post_processing(config, clustering_output, chosen_clustering_variables):
    """
    Wrapper function to standardise the data and restructure the table created when clustering. 
    Calculates means of each cluster, based on the restructured table and standardised data.
    Creates radial plots and drafts cluster summaries.
    
    Parameters
    ----------
    config : dict
        main pipeline config dictionary containing output directory.
    clustering_output : pd.DataFrame
        the output from running the clustering algorithm
    chosen_clustering_variables : pd.DataFrame
        A DataFrame containing LAD_codes and data for each variable prior to standardisation.

    Returns
    -------
    tuple of pd.DataFrame
        (combined_group_means, combined_subgroup_means): DataFrames containing means for group and subgroup clusters.
    """

    # Run the standardise_data function on chosen_clustering_variables
    standardised_data = standardise_data(chosen_clustering_variables)

    # Step 1: Restructure the cluster table to have separate columns for supergroup, group and subgroup
    restructured_cluster_table, restructured_cluster_table_long = cluster_table_restructure(
    config, clustering_output, config["split_column"], config["keep_column"], standardised_data
    )

    # Step 2: Calculate means for each variable for each cluster 
    uk_std_cluster_means = cluster_variable_means(config, restructured_cluster_table, standardised_data)

    # Step 3: Run cluster_std_means_to_parent_clusters and capture the returned means
    combined_group_means, combined_subgroup_means = cluster_std_means_to_parent_clusters(
        config, restructured_cluster_table, chosen_clustering_variables
    )

    # Step 4: Create radial plots for the clusters using the combined means
    create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means)

    # Step 5: Draft cluster summaries
    cluster_summaries_wrapper(config, restructured_cluster_table_long, uk_std_cluster_means, config["select_variables_lookup"], cluster_column = 'supergroup')
    cluster_summaries_wrapper(config, restructured_cluster_table_long, uk_std_cluster_means, config["select_variables_lookup"], cluster_column = 'group')
    cluster_summaries_wrapper(config, restructured_cluster_table_long, uk_std_cluster_means, config["select_variables_lookup"], cluster_column = 'subgroup')
    
    # Return the combined means for further use if needed
    return combined_group_means, combined_subgroup_means