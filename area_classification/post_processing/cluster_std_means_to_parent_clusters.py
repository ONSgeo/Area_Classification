# This script creates means standardized to the parent cluster
# group means standardised to the supergroup mean
# subgroup means standardised to the group mean

import pandas as pd
import os
from collections import defaultdict

def cluster_std_means_to_parent_clusters(config, restructured_cluster_table_df, chosen_clustering_variables):
    """
    This function reads the clustering output CSV file and the pre-clustering data CSV file.
    It creates standardized means of the values in a cluster to their parent cluster. It then 
    saves the standardized means to a new CSV file.
    Once it has the standardized means, it creates means for each cluster. 

    Parameters
    ----------
    config : dict
        Configuration dictionary containing the filepath and name to the cluster data.
    chosen_clustering_variables : pd.DataFrame
        DataFrame containing the pre-clustering data with the chosen clustering variables.
    restructured_cluster_table_df : pd.DataFrame
        DataFrame of cluster assignments. Data will have the following format:
        
        LAD_name    | LAD_code  | supergroup| group | subgroup
        -------------------------------------------
        Hartlepool  | E06000001 | 1         | 1c    | 1c1

    Returns:
        pd.DataFrame: DataFrame containing standardized means for each cluster.

    """
    # Load the clustering output data
    #restructured_subclustering_output_df = restructured_cluster_table_df

    ## Define the paths to the pre-clustering data files (not standardized) 
    #pre_clustering_data = (config["pre_clustering_data"])
    #filtered_pre_clustering_data = (config["pre_clustering_data_filtered_std_mean"])

    ## Check if the filtered (variables dropped) file exists
    ## if it does, use it; otherwise, use the full pre_clustering_data
    #pre_clustering_data_to_use = filtered_pre_clustering_data if os.path.exists(filtered_pre_clustering_data) else pre_clustering_data
    #
    #pre_clustering_data_to_use = pd.read_csv(pre_clustering_data_to_use)
    
    # Merge the two DataFrames on the LAD CODE column
    merged_df = restructured_cluster_table_df.merge(
        chosen_clustering_variables , on="LAD_code", how="left"
    )
    
    # Define the output directory
    output_directory = config["output_directory"]
    
    # Define the path for the existing folder
    output_directory = os.path.join(output_directory, "std_means")
    
    # --- Generate CSVs for supergroups ---
    # Sort the data by the supergroup column
    merged_df = merged_df.sort_values(by=["supergroup"])

    # Initialize lists to store all group_means and subgroup_means DataFrames
    all_group_means = []
    all_subgroup_means = []

    # Group by supergroup and process each supergroup's data
    for supergroup, supergroup_data in merged_df.groupby("supergroup"):
        # Sort the data by 'group'
        supergroup_data = supergroup_data.sort_values(by=["group"])
        # Drop the 'subgroup' column
        supergroup_data = supergroup_data.drop(columns=["subgroup"])

        # Identify columns starting with 'v'
        v_columns = [col for col in supergroup_data.columns if col.startswith("v")]

        # Standardize mean of each value in the 'v' columns
        for col in v_columns:
            mean = supergroup_data[col].mean()
            std = supergroup_data[col].std()
            supergroup_data[col] = (supergroup_data[col] - mean) / std

        # Group by 'group' and calculate the mean for each group
        group_means = supergroup_data.groupby("group").mean(numeric_only=True).reset_index()

        # Filter the group_means DataFrame to include only the 'group' column and 'v' columns
        group_means = group_means[["group"] + v_columns]

        # Append the group_means DataFrame to the list
        all_group_means.append(group_means)

    # --- Generate CSVs for groups ---
    # Sort the data by group and subgroup
    merged_df = merged_df.sort_values(by=["group", "subgroup"])

    # Group by group and process each group's data
    for group, group_data in merged_df.groupby("group"):
        # Identify columns starting with 'v'
        v_columns = [col for col in group_data.columns if col.startswith("v")]

        # Standardize means of each value in the 'v' columns
        for col in v_columns:
            mean = group_data[col].mean()
            std = group_data[col].std()
            group_data[col] = (group_data[col] - mean) / std

        # Group by 'subgroup' and calculate the mean for each group
        subgroup_means = group_data.groupby("subgroup").mean(numeric_only=True).reset_index()

        # Filter the subgroup_means DataFrame to include only the 'subgroup' column and 'v' columns
        subgroup_means = subgroup_means[["subgroup"] + v_columns]

        # Append the subgroup_means DataFrame to the list
        all_subgroup_means.append(subgroup_means)

    # Concatenate all group_means and subgroup_means DataFrames into single DataFrames
    combined_group_means = pd.concat(all_group_means, ignore_index=True)
    combined_subgroup_means = pd.concat(all_subgroup_means, ignore_index=True)

    # CHECK WITH TYDE AFTER LEAVE BUT DON'T THINK THIS IS NEEDED ANY LONGER!
    # # Group files by their names after the first underscore
    # grouped_files = defaultdict(list)
    # for file in csv_files:
    #     prefix, suffix = file.split("_", 1)  # Split into prefix and suffix
    #     grouped_files[(len(prefix), suffix)].append(file)  # Group by prefix length and suffix

    # # Combine files into Excel files
    # for (prefix_length, suffix), files in grouped_files.items():
    #     # Determine the file name based on prefix length
    #     if prefix_length == 1:
    #         file_type = "group"
    #     elif prefix_length == 2:
    #         file_type = "subgroup"
    #     else:
    #         file_type = "other"  # Fallback for unexpected cases

    #     # Create the Excel file name
    #     excel_file = os.path.join(output_directory, f"{file_type}_{suffix.replace('.csv', '')}.xlsx")

    #     # Write the grouped CSVs into the Excel file
    #     with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
    #         for file in files:
    #             file_path = os.path.join(output_directory, file)
    #             df = pd.read_csv(file_path)
    #             sheet_name = os.path.splitext(file)[0]
    #             df.to_excel(writer, sheet_name=sheet_name, index=False)
    #     print(f"Saved combined Excel file: {excel_file}")

    #INSTEAD SAVING THE FULL DATAFRAME AS A CSV FILE
    # Create the 'parent_std_means' subfolder within 'std_means'
    parent_std_means_directory = os.path.join(config["output_directory"], "std_means", "parent_std_means")
    os.makedirs(parent_std_means_directory, exist_ok=True)

    # Save the group output file path within the 'parent_std_means' folder
    group_output_file_path = os.path.join(parent_std_means_directory, "parent_std_cluster_group_means_output.csv")
    combined_group_means.to_csv(group_output_file_path, index=False)

    # Save the group output file path within the 'parent_std_means' folder
    subgroup_output_file_path = os.path.join(parent_std_means_directory, "parent_std_cluster_subgroup_means_output.csv")
    combined_subgroup_means.to_csv(subgroup_output_file_path, index=False)

    print("combined_group_means DataFrame:", combined_group_means)
    print("combined_subgroup_means DataFrame:", combined_subgroup_means)
    
    # Return the concatenated DataFrames
    return combined_group_means, combined_subgroup_means
    

if __name__ == "__main__":
    from utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    restructured_cluster_table_df = pd.read_csv('data/output_data/restructured_subclustering_output.csv')
    chosen_clustering_variables = pd.read_csv('data/inputs/pre_clustering_data_filtered.csv')
    cluster_std_means_to_parent_clusters(config, restructured_cluster_table_df, chosen_clustering_variables)