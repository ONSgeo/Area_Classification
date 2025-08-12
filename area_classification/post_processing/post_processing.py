# Post clustering wrapper
#INITAL PLACE HOLDER SCRIPT - NOTE DOES NOT RUN!
import os

from utilities.load_config import load_config
from post_processing.table_restructure import post_process_cluster_table  
#from post_processing.UK_standardised_means import create_UK_means
from post_processing.cluster_variables_mean import get_cluster_means
from post_processing.cluster_std_means_to_parent_clusters import cluster_std_means_to_parent_clusters  


def post_processing(config):
    """
    Wrapper function to run post_process_cluster_table, 
    extract_matching_and_partial_columns, and get_cluster_means in sequence.

    Args:
        post_process_args (tuple): Arguments for post_process_cluster_table.
        extract_columns_args (tuple): Arguments for extract_matching_and_partial_columns.
        cluster_means_args (tuple): Arguments for get_cluster_means.

    Returns:
        The result of get_cluster_means.
    """


    # Step 1: Run post_process_cluster_table
    post_process_cluster_table(config)

    # Step 2: Create the means for all area codes and UK, EW, NI and Scot
    #create_UK_means(post_process_cluster_df)

    # Step 2: Run get_cluster_means to calculate means on the already standardized data
    get_cluster_means(config)

    # Step 3: Run cluster_std_means_to_parent_clusters
    cluster_std_means_to_parent_clusters(config)

    # Step 4: Significance testing
    


# Run the function if the script is executed directly
if __name__ == "__main__":
    config = load_config('area_classification/config.yaml')
    post_processing(config)
