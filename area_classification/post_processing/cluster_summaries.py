import pandas as pd
import numpy as np
import os

from area_classification.utilities.load_config import load_config

def cluster_summaries(config,):
    """
    Wrapper function to run the cluster summary functions post clustering 
    
    Parameters
    ----------
    config : dict
        main pipeline config dictionary containing output directory.
    chosen_clustering_variables

    clustering_output : pd.DataFrame
        the output from running the clustering algroithm

    Returns
    ----------
        The result of get_cluster_means.
    """

    # Step 1: 

    # Step 2: 

    # Step 3: 

    # Step 4: C
    
    # Return the combined means for further use if needed
    return 


def analyze_cluster_means(uk_std_cluster_means_output):
    """
    Analyzes a table of means and prints the cluster name along with any means
    that are lower than -2 or higher than 2 for that cluster. If a value is an
    outlier, it groups the column names as having a "large effect."
    If a value is between -1.25 and -2.00 or between 1.25 and 2.00, it groups
    the column names as having a "medium effect."
    Additionally, it groups variables by the cluster that contains the highest value
    and prints the 5 most extreme variables from the "large effect" group for each cluster.

    Parameters:
        means_table (pd.DataFrame): A DataFrame where rows represent clusters
                                    and columns are the variable means.
    """
    # Iterate through each cluster
    for cluster_name, row in means_table.iterrows():
        # Initialize lists to store variables with large and medium effects
        large_effect_vars = []
        medium_effect_vars = []
        
        # Iterate through each value in the row
        for feature, value in row.items():
            if value < -2 or value > 2:
                large_effect_vars.append((feature, value))
            elif -2.00 < value <= -1.25 or 1.25 <= value < 2.00:
                medium_effect_vars.append(feature)
        
        # Construct the output message
        output = f"Cluster {cluster_name} variables which have a large effect include: {', '.join([var[0] for var in large_effect_vars])}."
        if medium_effect_vars:
            output += f" Variables which have a medium effect are: {', '.join(medium_effect_vars)}."
        
        # Print the output
        print(output)
    
    # Group variables by the cluster with the highest value
    print("\nClusters with the highest value for each variable:")
    cluster_highest_values = {}
    for column in means_table.columns:
        max_cluster = means_table[column].idxmax()
        max_value = means_table[column].max()
        if max_cluster not in cluster_highest_values:
            cluster_highest_values[max_cluster] = []
        cluster_highest_values[max_cluster].append(f"{column} ({max_value})")
    
    # Print the grouped results in the order they appear in the DataFrame
    for cluster, variables in cluster_highest_values.items():
        print(f"Cluster {cluster} contains the highest value for: {', '.join(variables)}")
    
    # Print the 5 most extreme variables for each cluster
    print("\nTop 5 most extreme variables in the 'large effect' group for each cluster:")
    for cluster_name, row in means_table.iterrows():
        # Filter the "large effect" variables and sort by absolute value
        large_effect_vars = [(feature, value) for feature, value in row.items() if value < -2 or value > 2]
        large_effect_vars_sorted = sorted(large_effect_vars, key=lambda x: abs(x[1]), reverse=True)
        
        # Select the top 5 most extreme variables
        top_5_extreme = large_effect_vars_sorted[:5]
        if top_5_extreme:
            print(f"Cluster {cluster_name}: {', '.join([f'{var[0]} ({var[1]})' for var in top_5_extreme])}")
        else:
            print(f"Cluster {cluster_name}: No variables in the 'large effect' group.")
      
    # Print the 5 most extreme variables for each cluster in the range above 1.25 or below -1.25
    print("\nTop 5 most extreme variables above 1.25 or below -1.25 for each cluster:")
    for cluster_name, row in means_table.iterrows():
        # Filter the variables in the range above 1.25 or below -1.25 and sort by absolute value
        extreme_vars = [(feature, value) for feature, value in row.items() if value < -1.25 or value > 1.25]
        extreme_vars_sorted = sorted(extreme_vars, key=lambda x: abs(x[1]), reverse=True)
        
        # Select the top 5 most extreme variables
        top_5_extreme = extreme_vars_sorted[:5]
        if top_5_extreme:
            print(f"Cluster {cluster_name}: {', '.join([f'{var[0]} ({var[1]})' for var in top_5_extreme])}")
        else:
            print(f"Cluster {cluster_name}: No variables above 1.25 or below -1.25.")



def calculate_cluster_variance(restructured_table_long, cluster_column):
    """
    Calculate the variance for all columns starting with 'v' for each cluster, compute the average variance, and print it.

    Parameters:
        restructured_table (pd.DataFrame): The first DataFrame containing the data.
        pre_clustering_data_std_mean (pd.DataFrame): The second DataFrame to merge.
        cluster_column (str): The name of the column containing cluster identifiers.

    Returns:
        None
    """
    import numpy as np
    import pandas as pd

    # Identify columns starting with 'v'
    v_columns = [col for col in data.columns if col.startswith('v')]

    # Initialize a dictionary to store variances
    cluster_variances = {}

    # Get unique clusters
    unique_clusters = data[cluster_column].unique()

    # Loop through each cluster and calculate variance for 'v' columns
    for cluster_name in unique_clusters:
        # Filter the data for the current cluster
        cluster_data = data[data[cluster_column] == cluster_name]

        # Initialize a dictionary for the current cluster
        cluster_variances[cluster_name] = {}

        # Calculate variance for each 'v' column
        for v_col in v_columns:
            if not cluster_data.empty:
                variance = np.var(cluster_data[v_col], ddof=1)  # Sample variance
                cluster_variances[cluster_name][v_col] = variance
            else:
                cluster_variances[cluster_name][v_col] = None  # Handle empty clusters

    # Calculate the average variance for each cluster
    average_variances = {}
    for cluster_name, variances in cluster_variances.items():
        # Filter out None values and calculate the mean
        valid_variances = [v for v in variances.values() if v is not None]
        if valid_variances:
            average_variances[cluster_name] = np.mean(valid_variances)
        else:
            average_variances[cluster_name] = None

    # Print the average variance for each cluster
    print("Average Variance for Each Cluster:")
    for cluster_name, avg_variance in average_variances.items():
        print(f"Cluster {cluster_name}: {avg_variance}")

    # Optional: Save the detailed variance table for reference
    variance_df = pd.DataFrame.from_dict(cluster_variances, orient='index')
    variance_df.index.name = cluster_column
    variance_df.to_csv('detailed_cluster_variances.csv')
    print("Detailed variances saved to 'detailed_cluster_variances.csv'")
    


def identify_cluster_drivers_with_lookup_and_area(means_table, lookup_file, restructured_table, top_n=5):
    """
    Identifies the variables that drive the allocation of each cluster and make it different
    from the other clusters by comparing the mean values of variables in a cluster to the
    mean values of the same variables across all other clusters. Converts column names
    using a lookup file, displaying variable names with new_code in brackets. Also prints
    the names of three random areas within the cluster.

    Parameters:
        means_table (pd.DataFrame): A DataFrame where rows represent clusters
                                    and columns are the variable means.
        lookup_file (str): Path to the CSV file containing the lookup table.
        restructured_table (pd.DataFrame): A DataFrame containing the `supergroup` and `LAD_name` columns.
        top_n (int): The number of top driving variables to identify for each cluster.

    Returns:
        None: Prints the top driving variables for each cluster and three example area names.
    """
    
    # Filter the means_table to include only the top row and rows with 'supergroup' in the hierarchy_level column
    if 'hierarchy_level' not in means_table.columns:
        raise ValueError("Means table must contain a 'hierarchy_level' column.")
    
    means_table = pd.concat([
        means_table[means_table['hierarchy_level'] == 'supergroup']  # Select rows with 'supergroup'
    ])

    # Remove the hierarchy_level column
    means_table = means_table.drop(columns=['hierarchy_level'])

    # Load the lookup file
    lookup_df = pd.read_csv(lookup_file)
    
    # Ensure the lookup file has the required columns
    if 'new_code' not in lookup_df.columns or 'variable name' not in lookup_df.columns:
        raise ValueError("Lookup file must contain 'new_code' and 'variable name' columns.")
    
    # Create a mapping dictionary for variable names with new_code in brackets
    code_to_variable = {
        row['new_code']: f"{row['variable name']} ({row['new_code']})"
        for _, row in lookup_df.iterrows()
    }
    
    # Replace column names in the means_table
    means_table = means_table.rename(columns=code_to_variable)
    
    # Ensure the restructured table has the required columns
    if 'supergroup' not in restructured_table.columns or 'LAD_name' not in restructured_table.columns:
        raise ValueError("Restructured table must contain 'supergroup' and 'LAD_name' columns.")
    
    for index, row in means_table.iterrows():
        # Use the value in the 'cluster' column as the cluster_name
        cluster_name = int(row['cluster'])
        
        # Calculate the mean of each variable across all other clusters
        other_clusters_means = means_table[means_table['cluster'] != cluster_name].select_dtypes(include='number').mean()
        
        # Calculate the difference between the cluster's values and the other clusters' means
        differences = row.drop('cluster') - other_clusters_means
        
        # Sort variables by the absolute difference in descending order
        sorted_differences = differences.abs().sort_values(ascending=False)
        
        # Select the top N driving variables
        top_drivers = sorted_differences.head(top_n)
        
        # Find example areas from the restructured table
        example_areas = restructured_table[restructured_table['supergroup'] == cluster_name]
        if not example_areas.empty:
            area_names = example_areas['LAD_name'].sample(n=min(3, len(example_areas)), random_state=42).tolist()
        else:
            area_names = ["No area found"]
        
        # Print the results for the cluster
        print(f"Cluster {cluster_name}:")
        print(f"  Example areas: {', '.join(area_names)}")
        for variable in top_drivers.index:
            print(f"  {variable}: {row[variable]} (difference: {differences[variable]:.2f})")
        print()



def cluster_summary(restructured_table_long, uk_std_cluster_means_output):
    # Get unique clusters
    clusters = restructured_table_long['supergroup'].unique()
    
    # Filter rows where 'hierarchy_level' is 'supergroup' and convert 'cluster' column to integers
    filtered_df = (
        uk_std_cluster_means_output.loc[uk_std_cluster_means_output['hierarchy_level'] == 'supergroup']
        .assign(cluster=lambda df: pd.to_numeric(df['cluster'], errors='coerce').astype(int))
    )

    # Iterate through each cluster
    for cluster in clusters:
        # Filter rows for the current cluster
        cluster_data = restructured_table_long[restructured_table_long['supergroup'] == cluster]
        
        # Number of local authorities
        num_local_authorities = cluster_data['LAD_name'].nunique()
                        
        # Population density using restructured_table_long (V12 values for the cluster)
        cluster_v12_mean = cluster_data['v12'].mean()
        
        uk_mean_v12 = filtered_df.loc[filtered_df['cluster'] == cluster, 'v12']
        # Extract the scalar value from the Series
        uk_mean_v12 = uk_mean_v12.iloc[0]  # Use .iloc[0] to get the first value

        # Placeholder for percentage of UK population
        uk_population_percentage = "?"

        # Find example areas from the restructured table
        example_areas = restructured_table_long[restructured_table_long['supergroup'] == cluster]
        if not example_areas.empty:
            area_names = example_areas['LAD_name'].sample(n=min(3, len(example_areas)), random_state=42).tolist()
        else:
            area_names = ["No area found"]
               
        # Print the summary for the cluster
        print(
            f"Cluster {cluster} contains {num_local_authorities} local authorities which is % of UK population, "
            f"population density {cluster_v12_mean:.2f}."
        )
        print(
            f"The population of this supergroup typically live in XXXXXX areas - "
            f"Example areas: {', '.join(area_names)}"
        )

        print("-" * 40)

if __name__ == "__main__":
    config = load_config()
    uk_std_cluster_means_output_filepath = os.path.join(config["output_directory"], "std_means/uk_std_means/uk_std_cluster_means_output.csv")
    uk_std_cluster_means_output = pd.read_csv(uk_std_cluster_means_output_filepath)

    # Example Lookup File (CSV)
    lookup_file = config["select_variables_lookup"]
    filepath = os.path.join(config["output_directory"], "restructured_subclustering_output.csv")
    restructured_table = pd.read_csv(filepath)
    filepath_long = os.path.join(config["output_directory"], "restructured_subclustering_output_long.csv")
    restructured_table_long = pd.read_csv(filepath_long)
    pre_clustering_data_std_mean_path = config["pre_clustering_data_std_mean"]
    pre_clustering_data_std_mean = pd.read_csv(pre_clustering_data_std_mean_path)

    cluster_summary(restructured_table_long, uk_std_cluster_means_output)
    # Identify cluster drivers with column name conversion and example area
    #identify_cluster_drivers_with_lookup_and_area(means_table, lookup_file, restructured_table, top_n=3)
    #calculate_cluster_variance(restructured_table, pre_clustering_data_std_mean, cluster_column='supergroup')