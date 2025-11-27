# Cluster variables mean averages
import pandas as pd
import os

def cluster_variable_means(config, restructured_cluster_table, standardised_data):
    """
    Calculates the mean of each variable for different hierarchical clusters (supergroup, group, subgroup),
    and outputs the results in a structured format. 
    
    Parameters
    ----------
    config : dict
        Configuration dictionary containing the filepath and name to the cluster data
    
    restructured_cluster_table_df : pd.DataFrame
        DataFrame of cluster assignments. Data will have the following format:
        
        LAD_name    | LAD_code  | supergroup| group | subgroup
        -------------------------------------------
        Hartlepool  | E06000001 | 1         | 1c    | 1c1
    
    standardised_data : pd.DataFrame
        DataFrame containing standardised variable values for each LAD_code.

    Returns
    -------

    pd.DataFrame 
        Dataframe containing the mean of each variable for each cluster, structured as:
        Cluster_code  | Hierarchy_level   |  variable_name  |  variable_mean
        -----------------------------------------------------------------
        1             | supergroup        | TS001           | 100.0
        1a            | group             | TS001           | 120.0
        1a1           | subgroup          | TS001           | 130.0
    """
    
    # Merge cluster results with standardised means census data
    merged_data = pd.merge(restructured_cluster_table, standardised_data, on="LAD_code", how="left")

    # Reshape from wide to long format to create one variable_name column (rather than 61 columns, one for each)
    long_data = pd.melt(merged_data, id_vars=["LAD_code", "LAD_name", "supergroup", "group", "subgroup"],
                        var_name="variable_name", value_name="variable_value")
        
    # Reshape to even longer by making one hierarchy_level column (rather than supergroup, group, subgroup)
    long_data = pd.melt(long_data, id_vars=["LAD_code", "LAD_name", "variable_name", "variable_value"],
                        value_vars=["supergroup", "group", "subgroup"],
                        var_name="hierarchy_level", value_name="cluster")
        
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


if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    cluster_variable_means(config)

 