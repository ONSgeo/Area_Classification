# Cluster variables mean averages


import pandas as pd
import os


def cluster_variable_means(config, restructured_cluster_table_df):
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
    
    # Load the restructured cluster table (restructured_sublustering_output.csv) 
    # and the aggregated census data (pre_clustering_data_std_means.csv)
    cluster_results = restructured_cluster_table_df
    agg_census_data_filepath = os.path.join(config["input_data_directory"], "pre_clustering_data_std_means.csv")
    agg_census_data = pd.read_csv(agg_census_data_filepath)

    # Merge cluster results with standardized means census data
    merged_data = pd.merge(cluster_results, agg_census_data, on="LAD_code", how="left")

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
    cluster_means = long_data.groupby(["variable_name", "hierarchy_level", "cluster"]).mean("variable_value").reset_index()

    # Pivot the data to create the wide format
    wide_cluster_means = cluster_means.pivot(index=["cluster", "hierarchy_level"], 
                                             columns="variable_name", 
                                             values="variable_value").reset_index()

    # Rename columns to include "_mean" suffix for variable columns
    wide_cluster_means.rename(columns=lambda x: f"{x}_mean" if x not in ["cluster", "hierarchy_level"] else x, inplace=True)

    # Save the output as a CSV file
    output_file_path = os.path.join(config["output_directory"], "cluster_means_output.csv")
    wide_cluster_means.to_csv(output_file_path, index=False)

    print(f"Cluster means saved to {output_file_path}") 
    
    return wide_cluster_means

# Run the function if the script is executed directly
if __name__ == "__main__":
    # import the config file
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    # Run the function
    cluster_variable_means(config)

 