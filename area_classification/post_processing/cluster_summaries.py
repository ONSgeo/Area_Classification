# If using population counts / step 2 in final outputs, check correct input data!! 
import logging
logger = logging.getLogger(__name__)

import pandas as pd
import numpy as np
import os
import re

from area_classification.utilities.load_config import load_config

def cluster_summaries_wrapper(config, restructured_cluster_table_long, uk_std_cluster_means, chosen_clustering_variables, lookup_file, cluster_column, ):
    """
    Wrapper function to execute a series of cluster summary operations post clustering.

    This function calculates the cluster variances, population percentages, 
    cluster summaries, and the identification of key drivers for each cluster.

    Parameters
    ----------
    restructured_cluster_table_long : pd.DataFrame
        A DataFrame containing detailed information about clusters, including the clustering results 
        and associated variables.
    uk_std_cluster_means : pd.DataFrame
        A DataFrame containing the mean standardised values of clustering variables for each cluster.
    chosen_clustering_variables : pd.DataFrame
        A DataFrame containing LAD_codes and data for each variable prior to standardisation.
    lookup_file : str
        Path to the lookup file used for identifying cluster drivers.
    cluster_column : str
        The name of the column in `restructured_cluster_table_long` that identifies the cluster assignments.

    Steps
    -----
    1. Calculate the variance for each cluster.
    2. Compute the population percentages for each cluster.
    3. Generate detailed summaries for each cluster.
    4. Identify the key drivers for each cluster.

    Returns
    -------
    None
        This function does not return a value. It performs operations that generate summaries 
        and insights about the clusters.
    """

    # Step 1: 
    variance_df = calculate_cluster_variance(restructured_cluster_table_long, cluster_column)

    # Step 2: 
    pop_sums = cluster_population_percentages (restructured_cluster_table_long, f"{config['input_data_directory']}population_estimates.csv", cluster_column)

    # Step 3: 
    cluster_info = cluster_summary(restructured_cluster_table_long, uk_std_cluster_means, variance_df, pop_sums, chosen_clustering_variables, cluster_column)

    # Step 4: 
    identify_cluster_drivers(uk_std_cluster_means, lookup_file, cluster_info, variance_df, cluster_column, top_n=3)

    return 


def calculate_cluster_variance(restructured_cluster_table_long, cluster_column):
    """
    Calculates the variance for all columns starting with 'v' for each cluster, computes the average variance 
    for each cluster

    Parameters
    ----------
    restructured_cluster_table_long : pd.DataFrame
        A DataFrame containing the data, including columns for LAD code / names, the cluster allocation at different levels 
        (supergroup, group, and subgroup) and columns starting with 'v' for which variance will be calculated.
    cluster_column : str
        The name of the column in the DataFrame that contains cluster allocations (likely supergroup, group, and subgroup).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the cluster allocation column called (supergroup, group or subgroup) the variance of each 
        'v' column for each cluster, along with an additional column 'cluster_average_variance' that represents the average 
        variance of all 'v' columns for each cluster. The cluster column becomes the index for the dataframe.

    Notes
    -----
    - Variance is calculated using the sample variance formula (degrees of freedom = 1).
    - The average variance for each cluster is computed by excluding None values from the variance calculations.
    """
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
    # Make the cluster column the index
    variance_df.index.name = cluster_column
    variance_df = variance_df.sort_index()
    # Add the average variance as an additional column
    variance_df['cluster_average_variance'] = variance_df.index.map(cluster_average_variance)
    
    return variance_df

def cluster_population_percentages (restructured_cluster_table_long, population_estimates_filepath, cluster_column):
    """
    Calculates the total population of the LAD combined for each cluster at the level specificed (supergroup, 
    group or subgroup) as well as calculating the precentage of population for that cluster based on population
    estimates for the years 2021 and 2022. The function reads population data from a CSV file, merges it with
    the cluster data, and calculates the total and percentage population for each supergroup, group or subgroup
    as specified.
    
    Parameters
    ----------
    restructured_cluster_table_long : pd.DataFrame
        A DataFrame containing cluster data with at least the columns 'LAD_code' and 'supergroup'.
    population_estimates_filepath : str
        The file path of where to find the csv for the LAD estimate population for 2021 and 2022.
    cluster_column : str
        The name of the column in the DataFrame that contains cluster allocations (likely supergroup, group, and subgroup).


    Returns
    -------
    pd.DataFrame
        A DataFrame containing the population totals and percentages for each supergroup.
        The columns include:
        - 'supergroup': The unique cluster supergroup identifier.
        - '2021_supergroup_population': Total population for the supergroup in 2021.
        - '2022_supergroup_population': Total population for the supergroup in 2022.
        - '2021_percentage': Percentage of the total population for the supergroup in 2021.
        - '2022_percentage': Percentage of the total population for the supergroup in 2022.

    Notes
    -----
    - Percentages are rounded to two decimal places for clarity.
    """
    # Read in the population estimates CSV file and do some initial formatting
    df_populations = pd.read_csv(population_estimates_filepath, skiprows=7)
    # Rename the first two columns
    df_populations.rename(columns={df_populations.columns[0]: 'LAD_name', df_populations.columns[1]: 'LAD_code'}, inplace=True)
    # Remove the last row
    df_populations = df_populations.iloc[:-1, :]

    # Merge the two cluster dataframe and population dataframe on LAD code
    merged_df = pd.merge(restructured_cluster_table_long, df_populations, on='LAD_code', how='inner')
    
    # Sum the population for each unique subgroup
    pop_sums = merged_df.groupby(cluster_column)[['2021', '2022']].sum().reset_index()

    # Sum the total population column in merged_df
    total_population_2021 = merged_df['2021'].sum()
    total_population_2022 = merged_df['2022'].sum()

    # Add population columns for 2021 and 2022
    pop_sums['2021_percentage'] = (pop_sums['2021'] / total_population_2021) * 100
    pop_sums['2022_percentage'] = (pop_sums['2022'] / total_population_2022) * 100

    # Round the percentages to 2 decimal places
    pop_sums['2021_percentage'] = pop_sums['2021_percentage'].round(2)
    pop_sums['2022_percentage'] = pop_sums['2022_percentage'].round(2)

    # Rename columns for clarity
    pop_sums.rename(columns={'2021': f'2021_{cluster_column}_population', '2022': f'2022_{cluster_column}_population'}, inplace=True)

    return pop_sums

def cluster_summary(restructured_cluster_table_long, uk_std_cluster_means, variance_df, pop_sums, chosen_clustering_variables, cluster_column,):
    """
    Generate a text summary for each cluster based on various metrics and data sources.

    Parameters
    ----------
    restructured_cluster_table_long : pd.DataFrame
        A DataFrame containing detailed information about clusters,
            including columns such as 'supergroup', 'LAD_name', and 'v12'.
    uk_std_cluster_means : pd.DataFrame
        A DataFrame containing mean values for various metrics at the cluster level,
            including columns such as 'hierarchy_level', 'cluster', and 'v12'.
    variance_df : pd.DataFrame
        A DataFrame containing variance information for clusters, indexed by cluster IDs,
            with a column 'cluster_average_variance'.
    pop_sums: pd.DataFrame
        A DataFrame containing population percentages for clusters, including columns
            such as 'supergroup', '2021_percentage', and '2022_percentage'.
    chosen_clustering_variables : pd.DataFrame
        A DataFrame containing LAD_codes and data for each variable prior to standardisation.
    cluster_column : str
        The name of the column in the DataFrame that contains cluster allocations (likely supergroup, group, and subgroup).

    Returns
    ----------
        list: A list of strings, where each string contains a detailed summary for a cluster, including:
            - The number and percentage of local authorities in the cluster.
            - The population percentages for 2021 and 2022.
            - The population density (mean of 'v12' values).
            - The average variance for the cluster.
            - Example areas (up to 3 randomly sampled local authority names).

    Notes
    ----------
        - Random sampling of example areas is performed with a fixed random seed for reproducibility.
    """
    # Get unique clusters
    clusters = restructured_cluster_table_long[cluster_column].unique()

    # This if statment is needed as supergroup is int, where as group and subgroup are str
    if cluster_column == "supergroup":
        # Sort clusters in ascending order
        clusters = sorted(clusters)
        # Filter rows where 'hierarchy_level' is the same as the cluster_column specified and convert 'cluster' column to integers
        filtered_df = (
            uk_std_cluster_means.loc[uk_std_cluster_means['hierarchy_level'] == cluster_column]
            .assign(cluster=lambda df: pd.to_numeric(df['cluster'], errors='coerce').astype(int))
        )
    elif cluster_column in ["group", "subgroup"]:
        # Sort based on the numeric part
        clusters = sorted(clusters, key=lambda x: int(''.join(filter(str.isdigit, str(x)))))
        # Filter rows where 'hierarchy_level' is the same as the cluster_column specified and ensure 'cluster' column is treated as strings
        filtered_df = (
            uk_std_cluster_means.loc[uk_std_cluster_means['hierarchy_level'] == cluster_column]
            .assign(cluster=lambda df: df['cluster'].astype(str))
        )

    # Rename the V12 column to pop_density in chosen_clustering_variables
    chosen_clustering_variables = chosen_clustering_variables.rename(columns={'v12': 'raw_pop_density'})

    # Merge the pop_density column from chosen_clustering_variables into restructured_cluster_table_long
    restructured_cluster_table_long = restructured_cluster_table_long.merge(
        chosen_clustering_variables[['LAD_code', 'raw_pop_density']],  # Select only LAD_code and pop_density columns
        on='LAD_code',                                 # Join on the LAD_code column
        how='left'                                     # Use a left join to preserve all rows in restructured_cluster_table_long
    )

    # Initialize a list to store outputs for all clusters
    cluster_info = []

    # Iterate through each cluster
    for cluster in clusters:

        # Filter rows for the current cluster
        cluster_data = restructured_cluster_table_long[restructured_cluster_table_long[cluster_column] == cluster]

        # Number of local authorities in the current cluster
        num_local_authorities = cluster_data['LAD_name'].nunique()
        
        # Total number of unique local authorities in the dataset
        total_local_authorities = restructured_cluster_table_long['LAD_name'].nunique()
        
        # Percentage of local authorities in the current cluster
        percentage_local_authorities = (num_local_authorities / total_local_authorities) * 100
                        
        # Calculate the mean population density using raw_pop_density column
        cluster_v12_mean = cluster_data['raw_pop_density'].mean()
 
        # Find example areas from the restructured_cluster_table_long table
        example_areas = restructured_cluster_table_long[restructured_cluster_table_long[cluster_column] == cluster]
        if not example_areas.empty:
            area_names = example_areas['LAD_name'].sample(n=min(3, len(example_areas)), random_state=42).tolist()
        else:
            area_names = ["No area found"]

        # Extract the 2021 and 2022 percentages for the current cluster
        cluster_data = pop_sums.loc[pop_sums[cluster_column] == cluster]  # Filter for the current cluster
        percentage_2021 = cluster_data['2021_percentage'].values[0]  # Get the 2021 percentage
        percentage_2022 = cluster_data['2022_percentage'].values[0]  # Get the 2022 percentage
   
        # Print the summary for the cluster
        # Combine the print statements into a single string
        output = (
            f"Cluster {cluster} contains {num_local_authorities} local authorities which is {percentage_local_authorities:.2f}% of UK local authorities, "
            f"in 2021 this was {percentage_2021:.2f}% of the UK population and in 2022 it was {percentage_2022:.2f}%. It has a mean population density of {cluster_v12_mean:.2f}.\n"
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

def identify_cluster_drivers(uk_std_cluster_means, lookup_file, cluster_info, variance_df, cluster_column, top_n=5):
    """
    Identifies the key variables that differentiate each cluster from others by analyzing
    the mean values of variables within a cluster compared to the mean values across all
    other clusters. The function also maps variable names using a lookup file and provides
    detailed descriptions of the differences for each cluster.
    
    Parameters
    ----------
        uk_std_cluster_means (pd.DataFrame): A DataFrame where rows represent clusters
            and columns represent the mean values of variables for each cluster.
        lookup_file (str): Path to a CSV file containing a lookup table with columns
            'new_code', 'variable_name', and 'domain' for mapping variable codes to
            descriptive names and domains.
        cluster_info (list): A list of strings containing information about each cluster,
            such as example area names or additional metadata.
        variance_df (pd.DataFrame): A DataFrame containing variance values for each variable
            and cluster, indexed by cluster number and variable code.
        top_n (int, optional): The number of top driving variables to identify for each
            cluster. Defaults to 5.

    Returns
    ----------
        None: The function prints the top driving variables for each cluster, along with
        detailed descriptions and variance values.

    """
    # Filter the uk_std_cluster_means_output to include only the top row and rows with the specified cluster_column  
    # in the hierarchy_level column
    if 'hierarchy_level' not in uk_std_cluster_means.columns:
        raise ValueError("Means table must contain a 'hierarchy_level' column.")
    
    uk_std_cluster_means = pd.concat([
        uk_std_cluster_means[uk_std_cluster_means['hierarchy_level'] == cluster_column]
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
        #cluster_number = int(row['cluster'])
        cluster_number = row['cluster']
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
                    
                    # Convert cluster_number to string to match the index type
                    cluster_number_str = str(cluster_number)
                    #cluster_number_int = int(cluster_number_str) # if running through main hash this!

                    variance_value = variance_df.loc[cluster_number_str, v_code] #if running through main un hash
                    #variance_value = variance_df.loc[cluster_number_int, v_code] # if running through main hash this!

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
    filepath_long = os.path.join(config["output_directory"], "restructured_subclustering_output_long.csv")
    restructured_cluster_table_long = pd.read_csv(filepath_long)
    uk_std_cluster_means_filepath = os.path.join(config["output_directory"], "std_means/uk_std_means/uk_std_cluster_means_output.csv")
    uk_std_cluster_means = pd.read_csv(uk_std_cluster_means_filepath)
    chosen_clustering_variables = pd.read_csv(os.path.join(config["input_data_directory"], "pre_clustering_data.csv"))

    lookup_file = config["select_variables_lookup"]

    cluster_summaries_wrapper(config, restructured_cluster_table_long, uk_std_cluster_means, chosen_clustering_variables, lookup_file, cluster_column='supergroup')

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
