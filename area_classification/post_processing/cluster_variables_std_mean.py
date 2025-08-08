# Cluster variables mean averages

# THIS SCRIPT MIGHT NOT BE NEEDED ANYMORE BECAUSE THE INPUT DATA IS ALREADY STANDARDIZED
# SO JUST USE THE CLUSTER_VARIABLES_MEAN SCRIPT TO CREATE CLUSTER MEANS - THESE ARE RELATVIE TO THE UK MEAN


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

    # Load the cluster results and aggregated census data
    cluster_results = pd.read_csv(os.path.join(config["output_directory"], "subgroup", "processed_subclustering_output.csv"))
    #agg_census_data = pd.read_csv(os.path.join(config["qa_folder_path"], "select_raw_totals.csv"))
    agg_census_data = pd.read_csv(os.path.join(config["input_data_directory"], "pre_clustering_data_std_means.csv"))

    # Filter out 'UK_total' rows and columns containing '_total'
    agg_census_data = agg_census_data[agg_census_data["LAD_code"] != "UK_total"]
    agg_census_data = agg_census_data[[col for col in agg_census_data.columns if '_total' not in col]]

    # Merge cluster results with census data
    merged_data = pd.merge(cluster_results, agg_census_data, on="LAD_code", how="left")

    print("merged_data",merged_data.head())
    print("merged_data missing values",merged_data.isna().sum())  # Check for missing values

    # Reshape to long format with one variable_name column
    long_data = pd.melt(merged_data, id_vars=["LAD_code", "LAD_name", "supergroup", "group", "subgroup"],
                        var_name="variable_name", value_name="variable_value")
    
    # Replace missing variable_value with the mean for the same variable_name
    long_data["variable_value"] = long_data.groupby("variable_name")["variable_value"].transform(lambda x: x.fillna(x.mean()))
    
    # Reshape further to include a hierarchy_level column
    long_data = pd.melt(long_data, id_vars=["LAD_code", "LAD_name", "variable_name", "variable_value"],
                        value_vars=["supergroup", "group", "subgroup"],
                        var_name="hierarchy_level", value_name="cluster")
    
    # Group by cluster and variable to calculate mean and standard deviation
    stats = long_data.groupby(["variable_name", "hierarchy_level", "cluster"])["variable_value"].agg(['mean', 'std']).reset_index()
    
    # Merge stats back into the long data
    long_data = pd.merge(long_data, stats, on=["variable_name", "hierarchy_level", "cluster"], how="left")
    
    # Calculate standardized mean (z-score), handling cases where std is NaN or 0 (where there is one LAD in a cluster)
    #long_data["standardized_value"] = long_data.apply(
    #    lambda row: 0 if pd.isna(row["std"]) or row["std"] == 0 else (row["variable_value"] - row["mean"]) / row["std"],
    #    axis=1
    #)

    long_data["standardized_value"] = long_data.apply(
        lambda row: None if pd.isna(row["std"]) or row["std"] == 0 else (row["variable_value"] - row["mean"]) / row["std"],
        axis=1
    )

    print(long_data[["variable_name", "hierarchy_level", "cluster", "variable_value", "mean", "std", "standardized_value"]].head())
    
    # Group by cluster and variable to calculate the mean of standardized values
    cluster_std_means_df = long_data.groupby(["variable_name", "hierarchy_level", "cluster"])["standardized_value"].mean().reset_index()
    
    # Pivot to wide format and rename columns to include "_zscore" suffix
    cluster_std_means_df = cluster_std_means_df.pivot(index=["cluster", "hierarchy_level"], 
                                                       columns="variable_name", 
                                                       values="standardized_value").reset_index()
    cluster_std_means_df.rename(columns=lambda x: f"{x}_zscore" if x not in ["cluster", "hierarchy_level"] else x, inplace=True)
    
    # Save the output as a CSV file
    output_file_path = os.path.join(config["output_directory"], "cluster_standardized_means_output.csv")
    cluster_std_means_df.to_csv(output_file_path, index=False)
    print(f"Cluster standardized means saved to {output_file_path}")
    
    return cluster_std_means_df


# Run the function if the script is executed directly
if __name__ == "__main__":
    from utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    get_cluster_means(config)