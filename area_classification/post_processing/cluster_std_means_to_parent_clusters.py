
# This script creates means standardized to the parent cluster
# group means standardised to the supergroup mean
# subgroup means standardised to the group mean


def cluster_std_means_to_parent_clusters(config, restructured_cluster_table_df):
    """
    This function reads the clustering output CSV file and the pre-clustering data CSV file.
    It creates standardized means of the values in a cluster to their parent cluster. It then saves the standardized means
    to a new CSV file.
    Once it has the standardized means, it creates means for each cluster. 

    Parameters
    ----------
    config : dict
        Configuration dictionary containing the filepath and name to the cluster data.
    restructured_cluster_table_df : pd.DataFrame
        DataFrame of cluster assignments. Data will have the following format:
        
        LAD_name    | LAD_code  | supergroup| group | subgroup
        -------------------------------------------
        Hartlepool  | E06000001 | 1         | 1c    | 1c1

    Returns:
        pd.DataFrame: DataFrame containing standardized means for each cluster.

    """

    import os
    import pandas as pd
    from collections import defaultdict

    # Load the clustering output data
    restructured_subclustering_output_df = restructured_cluster_table_df
    print("This is restructured", restructured_cluster_table_df)

    # Define the paths to the pre-clustering data files (not standardized) 
    pre_clustering_data = (config["pre_clustering_data"])
    filtered_pre_clustering_data = (config["pre_clustering_data_filtered"])

    # Check if the filtered (variables dropped) file exists
    # if it does, use it; otherwise, use the full pre_clustering_data
    pre_clustering_data_to_use = filtered_pre_clustering_data if os.path.exists(filtered_pre_clustering_data) else pre_clustering_data
    
    pre_clustering_data_to_use = pd.read_csv(pre_clustering_data_to_use)
    
    # Merge the two DataFrames on the LAD CODE column
    merged_df = restructured_subclustering_output_df.merge(
        pre_clustering_data_to_use , on="LAD_code", how="left"
    )
    
    
    
    # Define the output directory
    output_directory = config["output_directory"]
    
    # Create a subfolder named 'std_means' in the output directory
    output_directory = os.path.join(output_directory, "std_means")
    os.makedirs(output_directory, exist_ok=True)
    
    # --- Generate CSVs for supergroups ---
    # Sort the data by the supergroup column
    merged_df = merged_df.sort_values(by=["supergroup"])
    print("merged_df supergroup", merged_df.head)
    
    # Group by supergroup and save each supergroup's data to a separate CSV
    for supergroup, supergroup_data in merged_df.groupby("supergroup"):
        # Sort the data by 'group'
        supergroup_data = supergroup_data.sort_values(by=["group"])
        # Drop the 'subgroup' column
        supergroup_data = supergroup_data.drop(columns=["subgroup"])
        # Save the supergroup's data to a CSV file
        output_file = os.path.join(output_directory, f"{supergroup}_data.csv")
        supergroup_data.to_csv(output_file, index=False)
      

        # Identify columns starting with 'v'
        v_columns = [col for col in supergroup_data.columns if col.startswith("v")]

        # Standardize mean of each value in the 'v' columns
        for col in v_columns:
            mean = supergroup_data[col].mean()
            std = supergroup_data[col].std()
            supergroup_data[col] = (supergroup_data[col] - mean) / std

        # Save the standardized data to a CSV file
        output_file = os.path.join(output_directory, f"{supergroup}_std_means.csv")
        supergroup_data.to_csv(output_file, index=False)
     

        # Group by 'group' and calculate the mean for each group
        group_means = supergroup_data.groupby("group").mean(numeric_only=True).reset_index()

        # Identify columns starting with 'v'
        v_columns = [col for col in supergroup_data.columns if col.startswith("v")]

        # Filter the group_means DataFrame to include only the 'group' column and 'v' columns
        group_means_filtered = group_means[["group"] + v_columns]

        # Save the group means to a CSV file
        output_file = os.path.join(output_directory, f"{supergroup}_means.csv")
        group_means_filtered.to_csv(output_file, index=False)



    
    # --- Generate CSVs for groups ---
    # Sort the data by group and subgroup
    merged_df = merged_df.sort_values(by=["group", "subgroup"])
    print("merged_df group", merged_df.head)
    # Group by group and save each group's data (ordered by subgroup) to a separate CSV
    for group, group_data in merged_df.groupby("group"):
        # Save the group's data to a CSV file
        output_file = os.path.join(output_directory, f"{group}_data.csv")
        group_data.to_csv(output_file, index=False)


        # Identify columns starting with 'v'
        v_columns = [col for col in group_data.columns if col.startswith("v")]

        # Standardize means of each value in the 'v' columns
        for col in v_columns:
            mean = group_data[col].mean()
            std = group_data[col].std()
            group_data[col] = (group_data[col] - mean) / std

        # Save the standardized data to a CSV file
        output_file = os.path.join(output_directory, f"{group}_std_means.csv")
        group_data.to_csv(output_file, index=False)
       

        # Group by 'subgroup' and calculate the mean for each group
        subgroup_means = group_data.groupby("subgroup").mean(numeric_only=True).reset_index()
        
        # Identify columns starting with 'v'
        v_columns = [col for col in group_data.columns if col.startswith("v")]
        
        # Filter the group_means DataFrame to include only the 'group' column and 'v' columns
        subgroup_means_filtered = subgroup_means[["subgroup"] + v_columns]
        
        # Save the group means to a CSV file
        output_file = os.path.join(output_directory, f"{group}_means.csv")
        subgroup_means_filtered.to_csv(output_file, index=False)



    # --- Combine CSVs into Excel files ---
    # List all CSV files in the output directory
    csv_files = [f for f in os.listdir(output_directory) if f.endswith(".csv")]

    # Group files by their names after the first underscore
    grouped_files = defaultdict(list)
    for file in csv_files:
        prefix, suffix = file.split("_", 1)  # Split into prefix and suffix
        grouped_files[(len(prefix), suffix)].append(file)  # Group by prefix length and suffix

    # Combine files into Excel files
    for (prefix_length, suffix), files in grouped_files.items():
        # Determine the file name based on prefix length
        if prefix_length == 1:
            file_type = "group"
        elif prefix_length == 2:
            file_type = "subgroup"
        else:
            file_type = "other"  # Fallback for unexpected cases

        # Create the Excel file name
        excel_file = os.path.join(output_directory, f"{file_type}_{suffix.replace('.csv', '')}.xlsx")

        # Write the grouped CSVs into the Excel file
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            for file in files:
                file_path = os.path.join(output_directory, file)
                df = pd.read_csv(file_path)
                sheet_name = os.path.splitext(file)[0]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Saved combined Excel file: {excel_file}")

    # --- Remove all CSV files in the output directory ---
    for file in csv_files:
        file_path = os.path.join(output_directory, file)
        os.remove(file_path)



    
if __name__ == "__main__":
    from utilities.load_config import load_config
    # Load the configuration
    config = load_config('area_classification/config.yaml')
    
    # Run the function
    cluster_std_means_to_parent_clusters(config)









