# Post clustering wrapper

from utilities.load_config import load_config
from post_processing.cluster_table_restructure import cluster_table_restructure  
from post_processing.cluster_variables_mean import cluster_variable_means
from post_processing.cluster_std_means_to_parent_clusters import cluster_std_means_to_parent_clusters  


def post_processing(config):
    """
    Wrapper function to run restrcuture the table created when clustering, 
    
    Parameters
    ----------
    config : dict
        main pipeline config dictionary containing output directory.

    Returns
    ----------
        The result of get_cluster_means.
    """

    # Step 1: Restructure the cluster table to have separate columns for supergroup, group and subgroup
    restructured_cluster_table_df = cluster_table_restructure(config)

    # Step 2: Calculate means for each cluster and each variable
    cluster_variable_means(config, restructured_cluster_table_df)

    # Step 3: Run cluster_std_means_to_parent_clusters
    cluster_std_means_to_parent_clusters(config)
    


# Run the function if the script is executed directly
if __name__ == "__main__":
    config = load_config('area_classification/config.yaml')
    post_processing(config)
