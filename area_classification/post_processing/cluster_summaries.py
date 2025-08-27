import pandas as pd

def analyze_cluster_means(means_table):
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

import pandas as pd

def identify_cluster_drivers_with_lookup_and_area(means_table, lookup_file, restructured_table, top_n=5):
    """
    Identifies the variables that drive the allocation of each cluster and make it different
    from the other clusters by comparing the mean values of variables in a cluster to the
    mean values of the same variables across all other clusters. Converts column names
    using a lookup file, displaying variable names with new_code in brackets. Also prints
    the name of one area within the cluster.

    Parameters:
        means_table (pd.DataFrame): A DataFrame where rows represent clusters
                                    and columns are the variable means.
        lookup_file (str): Path to the CSV file containing the lookup table.
        restructured_table (pd.DataFrame): A DataFrame containing the `supergroup` and `LAD_name` columns.
        top_n (int): The number of top driving variables to identify for each cluster.

    Returns:
        None: Prints the top driving variables for each cluster and an example area name.
    """
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
    
    # Identify cluster drivers
    for cluster_name, row in means_table.iterrows():
        # Calculate the mean of each variable across all other clusters
        other_clusters_means = means_table.drop(index=cluster_name).mean()
        
        # Calculate the difference between the cluster's values and the other clusters' means
        differences = row - other_clusters_means
        
        # Sort variables by the absolute difference in descending order
        sorted_differences = differences.abs().sort_values(ascending=False)
        
        # Select the top N driving variables
        top_drivers = sorted_differences.head(top_n)
        
        # Find an example area from the restructured table
        example_area = restructured_table[restructured_table['supergroup'] == cluster_name]
        area_name = example_area['LAD_name'].iloc[0] if not example_area.empty else "No area found"
        
        # Print the results for the cluster
        print(f"Cluster {cluster_name}:")
        print(f"  Example area: {area_name}")
        for variable in top_drivers.index:
            print(f"  {variable}: {row[variable]} (difference: {differences[variable]:.2f})")
        print()

if __name__ == "__main__":
    means_table = pd.read_csv('data/uk_std_cluster_means_output.csv')
    analyze_cluster_means(means_table)

    # Example Lookup File (CSV)
    lookup_file = './data/lookups/UK_selected_codes_lookup.csv'
    restructured_table = pd.read_csv('data/restructured_subclustering_output_6supergroup.csv')

    # Identify cluster drivers with column name conversion and example area
    identify_cluster_drivers_with_lookup_and_area(means_table, lookup_file, restructured_table, top_n=3)