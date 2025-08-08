
# This script creates means standardized to the parent cluster
# group means standardised to the supergroup mean
# subgroup means standardised to the group mean

import pandas as pd
import os

from utilities.load_config import load_config
config = load_config('area_classification/config.yaml')

def cluster_std_means_to_parent_clusters(config):
    """
    This function reads the clustering output CSV file, calculates the means for each cluster,
    and standardizes these means to their parent clusters. It then saves the standardized means
    to a new CSV file.

    Parameters:
        config (dict): Configuration dictionary containing paths and parameters.
        processed_subclustering_output_df: DataFrame containing the clustering output data.
        pre_clustering_data_df: DataFrame containing the input data used for clustering, in percentages.

    Returns:
        pd.DataFrame: DataFrame containing standardized means for each cluster.

standardized means group structure:
        group code	  LAD CODE	 v01 
            0a	        E001	34.56
	                    E002	34.56
	                    E003	34.56
            0b	        E007	34.56
            	        E012	34.56
            	        E019	34.56

standardized means subgroup structure:
        subgroup code  LAD CODE	 v01 
            0a1	        E001	34.56
	                    E002	34.56
	                    E003	34.56
            0a2	        E007	34.56
            	        E012	34.56
            	        E019	34.56
               

    """

    import os
    import pandas as pd

    # Load in the pre-clustering percentages data
    pre_clustering_data = config["pre_clustering_data"]
    pre_clustering_data_df = pd.read_csv(pre_clustering_data)
    
    # Load the clustering output data
    processed_subclustering_output = config["processed_subclustering_output"]
    processed_subclustering_output_df = pd.read_csv(processed_subclustering_output)
    
    # Merge the two DataFrames on the LAD CODE column
    merged_df = processed_subclustering_output_df.merge(
        pre_clustering_data_df, on="LAD_code", how="left"
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
        print(f"Saved {output_file}")

        # Identify columns starting with 'v'
        v_columns = [col for col in supergroup_data.columns if col.startswith("v")]

        # Standardize each value in the 'v' columns
        for col in v_columns:
            mean = supergroup_data[col].mean()
            std = supergroup_data[col].std()
            supergroup_data[col] = (supergroup_data[col] - mean) / std

        # Save the standardized data to a CSV file
        output_file = os.path.join(output_directory, f"{supergroup}_std_means.csv")
        supergroup_data.to_csv(output_file, index=False)
        print(f"Saved standardized means for supergroup {supergroup} to {output_file}")

        # Group by 'group' and calculate the mean for each group
        group_means = supergroup_data.groupby("group").mean(numeric_only=True).reset_index()

        # Identify columns starting with 'v'
        v_columns = [col for col in supergroup_data.columns if col.startswith("v")]

        # Filter the group_means DataFrame to include only the 'group' column and 'v' columns
        group_means_filtered = group_means[["group"] + v_columns]

        # Save the group means to a CSV file
        output_file = os.path.join(output_directory, f"{supergroup}_group_means.csv")
        group_means_filtered.to_csv(output_file, index=False)
        print(f"Saved group means for supergroup {supergroup} to {output_file}")






    
    # --- Generate CSVs for groups ---
    # Sort the data by group and subgroup
    merged_df = merged_df.sort_values(by=["group", "subgroup"])
    print("merged_df group", merged_df.head)
    # Group by group and save each group's data (ordered by subgroup) to a separate CSV
    for group, group_data in merged_df.groupby("group"):
        # Save the group's data to a CSV file
        output_file = os.path.join(output_directory, f"{group}_data.csv")
        group_data.to_csv(output_file, index=False)
        print(f"Saved {output_file}")

        # Identify columns starting with 'v'
        v_columns = [col for col in group_data.columns if col.startswith("v")]

        # Standardize each value in the 'v' columns
        for col in v_columns:
            mean = group_data[col].mean()
            std = group_data[col].std()
            group_data[col] = (group_data[col] - mean) / std

        # Save the standardized data to a CSV file
        output_file = os.path.join(output_directory, f"{group}_std_means.csv")
        group_data.to_csv(output_file, index=False)
        print(f"Saved standardized means for group {group} to {output_file}")

        # Group by 'subgroup' and calculate the mean for each group
        subgroup_means = group_data.groupby("subgroup").mean(numeric_only=True).reset_index()
        
        # Identify columns starting with 'v'
        v_columns = [col for col in group_data.columns if col.startswith("v")]
        
        # Filter the group_means DataFrame to include only the 'group' column and 'v' columns
        subgroup_means_filtered = subgroup_means[["subgroup"] + v_columns]
        
        # Save the group means to a CSV file
        output_file = os.path.join(output_directory, f"{group}_group_means.csv")
        subgroup_means_filtered.to_csv(output_file, index=False)
        print(f"Saved subgroup means for group {group} to {output_file}")




    
if __name__ == "__main__":
    from utilities.load_config import load_config
    # Load the configuration
    config = load_config('area_classification/config.yaml')
    
    # Run the function
    cluster_std_means_to_parent_clusters(config)









