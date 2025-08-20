# Cluster variables mean averages


import pandas as pd
import os


def cluster_variable_means(config, restructured_cluster_table, chosen_clustering_variables):
    """
    Function calculates the mean of each variable and cluster (supergroup, group, subgroup)
    
    Parameters
    ----------
    config : dict
        Configuration dictionary containing the filepath and name to the cluster data
    
    restructured_cluster_table_df : pd.DataFrame
        DataFrame of cluster assignments. Data will have the following format:
        
        LAD_name    | LAD_code  | supergroup| group | subgroup
        -------------------------------------------
        Hartlepool  | E06000001 | 1         | 1c    | 1c1

    Returns
    -------
    pd.DataFrame
        Dataframe containing the mean of each variable for each cluster, structured as:
        cluster_code  | Hierarchy_level   |  TS001_mean      | TS002_mean      | ... | xxx_mean
        -----------------------------------------------------------------------------------------------
        1             | supergroup        | 100.0            | 200.0           | ... | 150.0
        1a            | group             | 120.0            | 180.0           | ... | 160.0
        1a1           | subgroup          | 130.0            | 170.0           | ... | 155.0

    OR LONG FORMAT? ... (SP - which is easier for comparison with national averages)

    pd.DataFrame  <---- currently outputs this option
        Dataframe containing the mean of each variable for each cluster, structured as:
        Cluster_code  | Hierarchy_level   |  variable_name  |  variable_mean
        -----------------------------------------------------------------
        1             | supergroup        | TS001           | 100.0
        1a            | group             | TS001           | 120.0
        1a1           | subgroup          | TS001           | 130.0
    """
    
    # Load the restructured cluster table (restrucutred_cluster_table / restructured_sublustering_output.csv) 
    
    cluster_results = restructured_cluster_table

    # load in the pre clustering data
    pre_clustering_data = chosen_clustering_variables


    # Merge cluster results with standardized means census data
    merged_data = pd.merge(cluster_results, pre_clustering_data, on="LAD_code", how="left")

    # Reshape from wide to long format to create one variable_name column (rather than 61 columns, one for each)
    long_data = pd.melt(merged_data, id_vars=["LAD_code", "LAD_name", "supergroup", "group", "subgroup"],
                        var_name="variable_name", value_name="variable_value")
    
    print("long_data first reshape", long_data.head())
    
    # Reshape to even longer by making one hierarchy_level column (rather than supergroup, group, subgroup)
    long_data = pd.melt(long_data, id_vars=["LAD_code", "LAD_name", "variable_name", "variable_value"],
                        value_vars=["supergroup", "group", "subgroup"],
                        var_name="hierarchy_level", value_name="cluster")
    
    print("long_data second reshape", long_data.head())
    
    # Group by cluster and variable, and calculate the mean
    uk_std_cluster_means = long_data.groupby(["variable_name", "hierarchy_level", "cluster"]).mean("variable_value").reset_index()

    # Pivot the data to create the wide format
    uk_std_cluster_means = uk_std_cluster_means.pivot(index=["cluster", "hierarchy_level"], 
                                             columns="variable_name", 
                                             values="variable_value").reset_index()


  
    # Create the 'std_means' folder in the output directory
    std_means_directory = os.path.join(config["output_directory"], "std_means")
    os.makedirs(std_means_directory, exist_ok=True)

    # Create the 'uk_std_means' subfolder within 'std_means'
    uk_std_means_directory = os.path.join(std_means_directory, "uk_std_means")
    os.makedirs(uk_std_means_directory, exist_ok=True)

    # Define the output file path within the 'uk_std_means' folder
    output_file_path = os.path.join(uk_std_means_directory, "uk_std_cluster_means_output.csv")

    # Save the output as a CSV file
    uk_std_cluster_means.to_csv(output_file_path, index=False)
    
    return uk_std_cluster_means

# Run the function if the script is executed directly
if __name__ == "__main__":
    # import the config file
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    # Run the function
    cluster_variable_means(config)

 