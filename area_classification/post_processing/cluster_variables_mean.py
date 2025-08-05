# Cluster variables mean averages

import pandas as pd
import os


def get_cluster_means(config):
    """
    Function calculates the mean of each variable and cluster (supergroup, group, subgroup)
    
    Parameters
    ----------
    config : dict
        Configuration dictionary containing the filepath and name to the cluster data
        Data will have the following format:
        LAD_code  | supergroup | group | subgroup
        -------------------------------------------
        E06000001 | 1          | 1c     | 1c1

    agg_census_data : pd.DataFrame
        Dataframe containing the data (as counts rather than percentages) for each LAD and variable, structured as:
        LAD_code  | variable_1 | variable_2 | ... | variable_n
        --------------------------------------------------------
        E06000001 | 100        | 200        | ... | 150

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

    # Load the cluster results (processed_sublustering_output.csv/post_process_cluster_df) 
    # and the aggregated census data (select_raw_totals.csv/raw_totals_df)
    cluster_results_file_path = os.path.join(config["output_directory"], "subgroup", "processed_subclustering_output.csv")
    cluster_results = pd.read_csv(cluster_results_file_path)
    agg_census_data_filepath = os.path.join(config["qa_folder_path"], "select_raw_totals.csv")
    agg_census_data = pd.read_csv(agg_census_data_filepath)

    # Merge cluster results with census data
    merged_data = pd.merge(cluster_results, agg_census_data, on="LAD_code", how="left")

    # Reshape from wide to long format to create one variable_name column (rather than 61 columns, one for each)
    long_data = pd.melt(merged_data, id_vars=["LAD_code", "LAD_name", "supergroup", "group", "subgroup"],
                        var_name="variable_name", value_name="variable_value")
    
    # Reshape to even longer by making one hierarchy_level column (rather than supergroup, group, subgroup)
    long_data = pd.melt(long_data, id_vars=["LAD_code", "LAD_name", "variable_name", "variable_value"],
                        value_vars=["supergroup", "group", "subgroup"],
                        var_name="hierarchy_level", value_name="cluster")
    
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
    
    # save out as a csv

# Run the function if the script is executed directly
if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    get_cluster_means(config)