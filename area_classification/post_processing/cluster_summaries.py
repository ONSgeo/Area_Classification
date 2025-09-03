import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import pandas as pd
import numpy as np
import os
import re

from area_classification.utilities.load_config import load_config

def cluster_summaries_wrapper(restructured_cluster_table_long, uk_std_cluster_means, lookup_file, cluster_column):
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
    variance_df = calculate_cluster_variance(restructured_cluster_table_long, cluster_column)
    
    # Step 2: 
    cluster_info = cluster_summary(restructured_cluster_table_long, uk_std_cluster_means, variance_df)

    # Step 3: 
    identify_cluster_drivers(uk_std_cluster_means, lookup_file, cluster_info, variance_df, top_n=3)

    # Step 4: 
    

    return 


def calculate_cluster_variance(restructured_cluster_table_long, cluster_column):
    """
    Calculate the variance for all columns starting with 'v' for each cluster, compute the average variance, and print it.

    Parameters:
        restructured_cluster_table_long (pd.DataFrame): The first DataFrame containing the data.
        cluster_column (str): The name of the column containing cluster identifiers.

    Returns:
        None
    """
    import numpy as np
    import pandas as pd

    data = restructured_cluster_table_long

    # Identify columns starting with 'v'
    v_columns = [col for col in data.columns if col.startswith('v')]

    # Initialize a dictionary to store variances
    cluster_variances = {}

    # Get unique clusters
    unique_clusters = data[cluster_column].unique()

    # Loop through each cluster and calculate variance for 'v' columns
    for cluster_number in unique_clusters:
        # Filter the data for the current cluster
        cluster_data = data[data[cluster_column] == cluster_number]
        # Initialize a dictionary for the current cluster
        cluster_variances[cluster_number] = {}

        # Calculate variance for each 'v' column
        for v_col in v_columns:
            if not cluster_data.empty:
                variance = np.var(cluster_data[v_col], ddof=1)  # Sample variance
                cluster_variances[cluster_number][v_col] = variance
            else:
                cluster_variances[cluster_number][v_col] = None  # Handle empty clusters

    # Calculate the average variance for each cluster
    cluster_average_variance = {}
    for cluster_number, variances in cluster_variances.items():
        # Filter out None values and calculate the mean
        valid_variances = [v for v in variances.values() if v is not None]
        if valid_variances:
            cluster_average_variance[cluster_number] = np.mean(valid_variances)
        else:
            cluster_average_variance[cluster_number] = None

    variance_df = pd.DataFrame.from_dict(cluster_variances, orient='index')
    variance_df.index.name = cluster_column
    variance_df = variance_df.sort_index()
    # Add the average variance as an additional column
    variance_df['cluster_average_variance'] = variance_df.index.map(cluster_average_variance)
    
    # Save the detailed variance table for reference
    variance_df.to_csv('./data/output_data/cluster_variance/detailed_cluster_variances.csv')
    return variance_df

def cluster_summary(restructured_cluster_table_long, uk_std_cluster_means, variance_df):
    # Get unique clusters
    clusters = restructured_cluster_table_long['supergroup'].unique()
    # Sort clusters in ascending order
    clusters = sorted(clusters)

    # Filter rows where 'hierarchy_level' is 'supergroup' and convert 'cluster' column to integers
    filtered_df = (
        uk_std_cluster_means.loc[uk_std_cluster_means['hierarchy_level'] == 'supergroup']
        .assign(cluster=lambda df: pd.to_numeric(df['cluster'], errors='coerce').astype(int))
    )

    # Initialize a list to store outputs for all clusters
    cluster_info = []

    # Iterate through each cluster
    for cluster in clusters:
        # Filter rows for the current cluster
        cluster_data = restructured_cluster_table_long[restructured_cluster_table_long['supergroup'] == cluster]
        
        # Number of local authorities in the current cluster
        num_local_authorities = cluster_data['LAD_name'].nunique()
        
        # Total number of unique local authorities in the dataset
        total_local_authorities = restructured_cluster_table_long['LAD_name'].nunique()
        
        # Percentage of local authorities in the current cluster
        percentage_local_authorities = (num_local_authorities / total_local_authorities) * 100
                        
        # Population density using restructured_cluster_table_long (V12 values for the cluster)
        cluster_v12_mean = cluster_data['v12'].mean()
        
        # Extract the mean value for v12 for the current cluster
        uk_mean_v12 = filtered_df.loc[filtered_df['cluster'] == cluster, 'v12']

        # Check if uk_mean_v12 is not empty before accessing .iloc[0]
        if not uk_mean_v12.empty:
            uk_mean_v12 = uk_mean_v12.iloc[0]  # Use .iloc[0] to get the first value
        else:
            uk_mean_v12 = None  # Or set a default value, e.g., 0 or np.nan
            logging.warning(f"No data found for cluster {cluster} in filtered_df.")

        # uk_mean_v12 = filtered_df.loc[filtered_df['cluster'] == cluster, 'v12']
        # print(uk_mean_v12)
        # # Extract the scalar value from the Series
        # uk_mean_v12 = uk_mean_v12.iloc[0]  # Use .iloc[0] to get the first value
  
        # Find example areas from the restructured_cluster_table_long table
        example_areas = restructured_cluster_table_long[restructured_cluster_table_long['supergroup'] == cluster]
        if not example_areas.empty:
            area_names = example_areas['LAD_name'].sample(n=min(3, len(example_areas)), random_state=42).tolist()
        else:
            area_names = ["No area found"]
               
        # Print the summary for the cluster
        # Combine the print statements into a single string
        output = (
            f"Cluster {cluster} contains {num_local_authorities} local authorities which is {percentage_local_authorities:.2f}% of UK local authorities, "
            f"and has a population density of {cluster_v12_mean:.2f}.\n"
        )
        # Check if the cluster exists in the DataFrame
        if cluster in variance_df.index:
            cluster_avg_variance = variance_df.loc[cluster, 'cluster_average_variance']
            output += f"The average variance for cluster {cluster} is {cluster_avg_variance:.2f}. Example areas: {', '.join(area_names)}"
        else:
            output += f"Cluster {cluster} not found in the DataFrame.\n"

        # Append the output to the list
        cluster_info.append(output)

    return cluster_info

def identify_cluster_drivers(uk_std_cluster_means, lookup_file, cluster_info, variance_df, top_n=5):
    """
    Identifies the variables that drive the allocation of each cluster and make it different
    from the other clusters by comparing the mean values of variables in a cluster to the
    mean values of the same variables across all other clusters. Converts column names
    using a lookup file, displaying variable names with new_code in brackets. Also prints
    the names of three random areas within the cluster.

    Parameters:
        uk_std_cluster_means (pd.DataFrame): A DataFrame where rows represent clusters
                                    and columns are the variable means.
        lookup_file (str): Path to the CSV file containing the lookup table.
        top_n (int): The number of top driving variables to identify for each cluster.

        cluster_info:list

    Returns:
        None: Prints the top driving variables for each cluster and three example area names.
    """
    # Filter the uk_std_cluster_means_output to include only the top row and rows with 'supergroup' in the hierarchy_level column
    if 'hierarchy_level' not in uk_std_cluster_means.columns:
        raise ValueError("Means table must contain a 'hierarchy_level' column.")
    
    uk_std_cluster_means = pd.concat([
        uk_std_cluster_means[uk_std_cluster_means['hierarchy_level'] == 'supergroup']  # Select rows with 'supergroup'
    ])

    # Remove the hierarchy_level column
    uk_std_cluster_means = uk_std_cluster_means.drop(columns=['hierarchy_level'])

    # Load the lookup file
    lookup_df = pd.read_csv(lookup_file)
    
    # Ensure the lookup file has the required columns
    if 'new_code' not in lookup_df.columns or 'variable_name' not in lookup_df.columns:
        raise ValueError("Lookup file must contain 'new_code' and 'variable_name' columns.")
    
    # Create a mapping dictionary for variable names with new_code in brackets
    code_to_variable = {
        row['new_code']: f"{row['variable_name']} ({row['new_code']})"
        for _, row in lookup_df.iterrows()
    }
    
    # Replace column names in the uk_std_cluster_means
    uk_std_cluster_means = uk_std_cluster_means.rename(columns=code_to_variable)

    for index, row in uk_std_cluster_means.iterrows():
        
        # Use the value in the 'cluster' column as the cluster_number
        cluster_number = int(row['cluster'])
        
        # Create a Pandas Series of the mean values of all numeric columns in uk_std_cluster_means, excluding rows where the cluster column equals cluster_number.
        other_clusters_means = uk_std_cluster_means[uk_std_cluster_means['cluster'] != cluster_number].select_dtypes(include='number').mean()

        # Calculate the difference between the cluster's values and the other clusters' means (which excludes the row of the current cluster_number)
        differences = row.drop('cluster') - other_clusters_means

        # Sort variables by the absolute difference in descending order
        # The variable at the top of the list will then have the greatest difference between the current cluster and the other clusters
        sorted_differences = differences.abs().sort_values(ascending=False)
        
        # Select the top N variables with the greatest difference
        variables_with_greatest_differnce = sorted_differences.head(top_n)
        
        # Print the results for the cluster
        print(f"Cluster {cluster_number}")
        if cluster_number is not None:
            for output in cluster_info:
                if f"Cluster {cluster_number}" in output:
                    print(output)
        print(f"""Values in the brackets below are the difference between the mean of the variable for this cluster
compared with the mean of the other clusters combined. The population of cluster {cluster_number} has a:""")      
        
        for variable in variables_with_greatest_differnce.index:
            # Remove anything in brackets from the variable name
            variable_name = re.sub(r'\(.*?\)', '', variable).strip()

            # Determine if the difference is "higher" or "lower"
            if differences[variable] > 0:
                difference_status = "higher"
            else:
                difference_status = "lower"
            
            # Extract the "V" followed by two digits using regex
            match = re.search(r'v\d{2}', variable)
            if match:
                v_code = match.group(0)  # Extracted code (e.g., "v22")
                
                # Find the first row in the lookup table where the code matches
                domain_value = lookup_df.loc[lookup_df['new_code'].str.contains(v_code, na=False), 'domain'].head(1)
                
                # Define a dictionary to map domains to their specific message logic
                domain_logic = {
                    "Demography and Migration": lambda table_name_value, variable_name: (
                        f"proportion of households comprised of {variable_name}" if "Household composition" in table_name_value else
                        f"proportion of people who live in a communal establishment" if "Residency type" in table_name_value else
                        f"proportion of people whose address one year ago is the same as the address of enumeration" if "Migrant Indicator" in table_name_value else
                        f"proportion of people who are {variable_name}" if "Age structure" in table_name_value or "Legal partnership status" in table_name_value else
                        f"proportion of people with a country of birth in {variable_name}" if "Country of birth" in table_name_value else
                        f"{variable_name}" if "Population density" in table_name_value else
                        f"people {variable_name}"
                    ),
                    "Labour Market": lambda table_name_value, variable_name: (
                        f"proportion of people working jobs which are {variable_name}" if "hours worked" in table_name_value else
                        "proportion of full-time students" if "NS-SeC" in table_name_value else
                        f"proportion of people who work in {variable_name.lstrip('0123456789. ').strip()}" if "occupation" in table_name_value else
                        f"proportion of people who work in {variable_name}"
                    ),
                    "Health, Disability and Unpaid Care": lambda table_name_value, variable_name: (
                        variable_name if "Disability" in table_name_value else
                        f"proportion of people who provide unpaid care" if "Provision of unpaid care" in table_name_value else
                        f"proportion of people {variable_name}"
                    ),
                    "Housing": lambda table_name_value, variable_name: (
                        f"proportion of people who live in a flat" if "Accommodation type" in table_name_value and "flat" in variable_name.lower() else
                        f"proportion of people living in a {variable_name}" if "Accommodation type" in table_name_value else
                        f"proportion of dwellings which are {variable_name}" if "Occupancy rating for rooms" in table_name_value else
                        f"proportion of people who own {variable_name}" if "Car or van availability" in table_name_value else
                        f"proportion of people living in {variable_name} accommodation" if "Tenure" in table_name_value else
                        f"proportion of people {variable_name}"
                    ),
                    "Ethnicity, Identity, Language and Religion": lambda table_name_value, variable_name: (
                        f"proportion of people who are {variable_name}" if "Ethnic group" in table_name_value else
                        f"proportion ofhouseholds where all household members have the same ethnic group" if "Multiple ethnic group" in table_name_value else
                        f"proportion of whose religion is {variable_name}" if "Religion" in table_name_value else
                        f"proportion of people who {variable_name}" if "Proficient in English" in table_name_value else
                        f"proportion of people {variable_name}"
                    ),
                    "Education": lambda table_name_value, variable_name: (
                        f" proportion of people whose highest level of qualification is {variable_name}"
                    )
                }

                # Check if a match is found and print the domain-specific message and variance value
                if not domain_value.empty:
                    domain = domain_value.iloc[0]
                    # Retrieve the table_name value for the specific variable
                    table_name_value = lookup_df.loc[lookup_df['new_code'].str.contains(v_code, na=False), 'table_name'].head(1).iloc[0]
                    
                    variance_value = variance_df.loc[cluster_number, v_code]

                    # Generate the specific message based on the domain logic
                    if domain in domain_logic:
                        specific_message = domain_logic[domain](table_name_value, variable_name)
                        message = f"• {difference_status} ({differences[variable]:.2f}) {specific_message}. Variance:{variance_value:.2f} ({domain} domain)"
                        print(message)
                    else:
                        # Default message for unrecognized domains
                        message = f"Domain {domain} not recognized for variable {variable_name}."

        print("-" * 40)

if __name__ == "__main__":
    config = load_config()
    uk_std_cluster_means_filepath = os.path.join(config["output_directory"], "std_means/uk_std_means/uk_std_cluster_means_output.csv")
    uk_std_cluster_means = pd.read_csv(uk_std_cluster_means_filepath)

    lookup_file = config["select_variables_lookup"]
    filepath_long = os.path.join(config["output_directory"], "restructured_subclustering_output_long.csv")
    restructured_cluster_table_long = pd.read_csv(filepath_long)
    
    cluster_summaries_wrapper(restructured_cluster_table_long, uk_std_cluster_means, lookup_file, cluster_column='supergroup')


#PROBABLY DELETE BELOW
# def analyze_cluster_means(uk_std_cluster_means_output):
#     """
#     Analyzes a table of means and prints the cluster name along with any means
#     that are lower than -2 or higher than 2 for that cluster. If a value is an
#     outlier, it groups the column names as having a "large effect."
#     If a value is between -1.25 and -2.00 or between 1.25 and 2.00, it groups
#     the column names as having a "medium effect."
#     Additionally, it groups variables by the cluster that contains the highest value
#     and prints the 5 most extreme variables from the "large effect" group for each cluster.

#     Parameters:
#         means_table (pd.DataFrame): A DataFrame where rows represent clusters
#                                     and columns are the variable means.
#     """
#     # Iterate through each cluster
#     for cluster_number, row in means_table.iterrows():
#         # Initialize lists to store variables with large and medium effects
#         large_effect_vars = []
#         medium_effect_vars = []
        
#         # Iterate through each value in the row
#         for feature, value in row.items():
#             if value < -2 or value > 2:
#                 large_effect_vars.append((feature, value))
#             elif -2.00 < value <= -1.25 or 1.25 <= value < 2.00:
#                 medium_effect_vars.append(feature)
        
#         # Construct the output message
#         output = f"Cluster {cluster_number} variables which have a large effect include: {', '.join([var[0] for var in large_effect_vars])}."
#         if medium_effect_vars:
#             output += f" Variables which have a medium effect are: {', '.join(medium_effect_vars)}."
        
#         # Print the output
#         print(output)
    
#     # Group variables by the cluster with the highest value
#     print("\nClusters with the highest value for each variable:")
#     cluster_highest_values = {}
#     for column in means_table.columns:
#         max_cluster = means_table[column].idxmax()
#         max_value = means_table[column].max()
#         if max_cluster not in cluster_highest_values:
#             cluster_highest_values[max_cluster] = []
#         cluster_highest_values[max_cluster].append(f"{column} ({max_value})")
    
#     # Print the grouped results in the order they appear in the DataFrame
#     for cluster, variables in cluster_highest_values.items():
#         print(f"Cluster {cluster} contains the highest value for: {', '.join(variables)}")
    
#     # Print the 5 most extreme variables for each cluster
#     print("\nTop 5 most extreme variables in the 'large effect' group for each cluster:")
#     for cluster_number, row in means_table.iterrows():
#         # Filter the "large effect" variables and sort by absolute value
#         large_effect_vars = [(feature, value) for feature, value in row.items() if value < -2 or value > 2]
#         large_effect_vars_sorted = sorted(large_effect_vars, key=lambda x: abs(x[1]), reverse=True)
        
#         # Select the top 5 most extreme variables
#         top_5_extreme = large_effect_vars_sorted[:5]
#         if top_5_extreme:
#             print(f"Cluster {cluster_number}: {', '.join([f'{var[0]} ({var[1]})' for var in top_5_extreme])}")
#         else:
#             print(f"Cluster {cluster_number}: No variables in the 'large effect' group.")
      
#     # Print the 5 most extreme variables for each cluster in the range above 1.25 or below -1.25
#     print("\nTop 5 most extreme variables above 1.25 or below -1.25 for each cluster:")
#     for cluster_number, row in means_table.iterrows():
#         # Filter the variables in the range above 1.25 or below -1.25 and sort by absolute value
#         extreme_vars = [(feature, value) for feature, value in row.items() if value < -1.25 or value > 1.25]
#         extreme_vars_sorted = sorted(extreme_vars, key=lambda x: abs(x[1]), reverse=True)
        
#         # Select the top 5 most extreme variables
#         top_5_extreme = extreme_vars_sorted[:5]
#         if top_5_extreme:
#             print(f"Cluster {cluster_number}: {', '.join([f'{var[0]} ({var[1]})' for var in top_5_extreme])}")
#         else:
#             print(f"Cluster {cluster_number}: No variables above 1.25 or below -1.25.")
