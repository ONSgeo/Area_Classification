# Creating print statements about the clusters

import logging
logger = logging.getLogger(__name__)
import pandas as pd
import numpy as np
import os
import re

from area_classification.utilities.load_config import load_config

def cluster_summaries_wrapper(config, restructured_cluster_table_long, uk_std_cluster_means, lookup_file, cluster_column):
    """
    Wrapper function to execute a series of cluster summary operations post clustering.

    This function calculates the cluster variances, population percentages, 
    cluster summaries, and the identification of key drivers for each cluster.

    Parameters
    ----------
    config : dict
        main pipeline config dictionary containing output directory.
    restructured_cluster_table_long : pd.DataFrame
        A DataFrame containing detailed information about clusters, including the clustering results 
        and associated variables.
    uk_std_cluster_means : pd.DataFrame
        A DataFrame containing the mean standardised values of clustering variables for each cluster.
    lookup_file : str
        Path to the lookup file used for identifying cluster drivers.
    cluster_column : str
        The name of the column in `restructured_cluster_table_long` that identifies the cluster assignments.

    Steps
    -----
    1. Calculate the variance for each cluster.
    2. Compute the population percentages and population densities for each cluster.
    3. Generate detailed summaries for each cluster.
    4. Identify the key drivers for each cluster.

    Returns
    -------
    None
        This function does not return a value. It performs operations that generate summaries 
        and insights about the clusters.
    """

    # Step 1 - Variance: 
    variance_df = calculate_cluster_variance(restructured_cluster_table_long, cluster_column)

    # Step 2 - Population statistics: 
    df_populations_sam_long = population_sam_preprocessing(
        restructured_cluster_table_long,
        f"{config['input_directory']}population_density/population_2021.xls",
        f"{config['input_directory']}population_density/population_2022.xlsx",
        f"{config['input_directory']}population_density/SAM_LAD_DEC_2021_UK.csv",
        f"{config['input_directory']}population_density/SAM_LAD_DEC_2022_UK_V2.csv"
    )
    pop_sums = cluster_population_percentages(df_populations_sam_long, cluster_column)
    pop_densities = output_population_densities(config, df_populations_sam_long)

    # Step 3 - Cluster summaries: 
    cluster_info = cluster_summary(restructured_cluster_table_long, uk_std_cluster_means, variance_df, pop_sums, pop_densities,  cluster_column)

    # Step 4 - Cluster drivers: 
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

    print("VARIANCE DF:", variance_df)
    return variance_df

def population_sam_preprocessing(restructured_cluster_table_long, population_estimates_filepath_2021, population_estimates_filepath_2022, sam_2021_filepath, sam_2022_filepath):
    """
    Data preprocessing steps before running cluster_population_percentages and output_population_densities functions. 

    This function removes superfluous columns, removes 'total' row in population_estimates, and renames 
    primary key columns ready for joining the restructured_cluster_table_long and df_populations together. 

    NOTE: This function edits the dataframes in place, then returns them.

    Parameters
    ----------
    restructured_cluster_table_long : pd.DataFrame
        A DataFrame containing the data, including columns for LAD code / names, the cluster allocation at different levels 
    population_estimates_filepath_2021 : str
        The file path of where to find the .xls for the LAD estimate population for 2021.
    population_estimates_filepath_2022 : str
        The file path of where to find the .xlsx for the LAD estimate population for 2022.
    sam_2021_filepath : str
        The file path of where to find the csv for the Standard Area Measurements (SAM) in hectares by LAD code for 2021.
    sam_2022_filepath : str
        The file path of where to find the csv for the Standard Area Measurements (SAM) in hectares by LAD code for 2022.    

    Returns
    -------
    Three pandas.DataFrames
        - The first DataFrame is a cleaned version of the `restructured_cluster_table_long` and `population_estimates` joined.
        - The second DataFrame is cleaned version of Standard Area Measurements (SAM) for 2021.
        - The third DataFrame is cleaned version of Standard Area Measurements (SAM) for 2021.
        These are ready for running cluster_population_percentages and output_population_densities functions functions. 
    """
    #Pre-process the populations table
    # Import the .xls file and open the 'MYE2 - Persons' tab
    df_populations_2021 = pd.read_excel(population_estimates_filepath_2021, sheet_name='MYE2 - Persons', engine='xlrd')  

    # Import the .xlsx file
    df_populations_2022 = pd.read_excel(population_estimates_filepath_2022, sheet_name='MYE2 - Persons', engine='openpyxl')  # Use 'openpyxl' for .xlsx files
    
    # List of DataFrames to process
    dataframes = [df_populations_2021, df_populations_2022]

    # Process each DataFrame in the list
    for index, df in enumerate(dataframes):
        # Remove the first 7 rows and keep only the first 4 columns
        df = df.iloc[7:, :4]
        # Rename the columns
        df.columns = ['LAD_code', 'LAD_name', 'Geography', 'population']
        
        # Drop rows where 'Geography' column contains 'country' or 'region'
        df = df[~df['Geography'].str.lower().isin(['country', 'region'])]
        
        # Update the original DataFrame in the list
        dataframes[index] = df

    # Assign the processed DataFrames back to their original variables
    df_populations_2021, df_populations_2022 = dataframes
    # Filter rows where the first character of 'LAD_code' is 'E', 'N', or 'W'
    df_populations_2021 = df_populations_2021[df_populations_2021['LAD_code'].str[0].isin(['E', 'N', 'W'])]

    # Filter rows where the first character of 'LAD_code' is 's'
    df_populations_2022 = df_populations_2022[df_populations_2022['LAD_code'].str[0].str.lower() == 's']

    # Pre-process the SAM tables
    # Read in the population estimates CSV file and do some initial formatting
    sam_2021 = pd.read_csv(sam_2021_filepath)
    sam_2022 = pd.read_csv(sam_2022_filepath)
    
    # Keep only required columns 
    sam_2021.drop(columns=['LAD21NM', 'AREAEHECT', 'AREACHECT', 'AREAIHECT'], inplace=True)
    sam_2022.drop(columns=['LAD22NM', 'LAD22NMW', 'AREAEHECT', 'AREACHECT', 'AREAIHECT'], inplace=True)

    # Rename columns in place
    sam_2021.rename(columns={'LAD21CD': 'LAD_code'}, inplace=True)
    sam_2022.rename(columns={'LAD22CD': 'LAD_code'}, inplace=True)
    
    # Merge the sam_2021 DataFrame with df_populations_2021 on the 'LAD_code' column
    merged_2021 = pd.merge(df_populations_2021, sam_2021, on='LAD_code', how='inner')
    merged_2022 = pd.merge(df_populations_2022, sam_2022, on='LAD_code', how='inner')

    # Concatenate merged_2021 and merged_2022
    merged_all = pd.concat([merged_2021, merged_2022], axis=0, ignore_index=True)

    # Perform the join with an indicator column to track the source of rows
    df_populations_sam_long = pd.merge(merged_all, restructured_cluster_table_long, 
        on='LAD_code', how='outer', indicator=True)

    return df_populations_sam_long

def cluster_population_percentages (df_populations_sam_long, cluster_column):
    """
    Calculates the total population of the LAD combined for each cluster at the level specificed (supergroup, 
    group or subgroup) as well as calculating the precentage of population for that cluster based on population
    estimates for the years 2021 and 2022. The function reads the merged population and cluster data, and 
    calculates the total and percentage population for each supergroup, group or subgroup as specified.
    
    Parameters
    ----------
    df_populations_sam_long : pd.DataFrame
        A DataFrame containing the merged restructured_cluster_table_long, population estimates (for 2021 for EW and
        NI, and 2022 for Scot), and standard area measurement (AREALHECT for 2021 for EW and NI, and 2022 for Scot). 
        This function requires at least the columns 'LAD_code', 'supergroup' and 'population'
    cluster_column : str
        The name of the column in the DataFrame that contains cluster allocations (likely supergroup, group, and subgroup).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the population totals and percentages for each supergroup.
        The columns include:
        - 'supergroup': The unique cluster supergroup identifier.
        - 'supergroup_population': Total population for the supergroup (population for EW and NI is 2021 but for Scot is from 2022).
        - 'supergroup_percentage': Percentage of the total population (population for EW and NI is 2021 but for Scot is from 2022).

    Notes
    -----
    - Percentages are rounded to two decimal places for clarity.
    """
    # Sum the population for each unique subgroup
    df_populations_sam_long['population'] = pd.to_numeric(df_populations_sam_long['population'], errors='coerce').astype('Int64')
    pop_sums = df_populations_sam_long.groupby(cluster_column)[['population']].sum().reset_index()
    # Sum the total population column in merged_df
    total_population = df_populations_sam_long['population'].sum()

    # Add population columns for 2021 and 2022
    pop_sums['percentage'] = (pop_sums['population'] / total_population) * 100

    # Ensure the 'percentage' column is numeric
    pop_sums['percentage'] = pd.to_numeric(pop_sums['percentage'], errors='coerce')

    # Round the percentages to 2 decimal places
    pop_sums['percentage'] = pop_sums['percentage'].round(2)

    # Rename columns for clarity
    pop_sums.rename(columns={'population': f'{cluster_column}_population', 'percentage': f'{cluster_column}_percentage'}, inplace=True)

    return pop_sums


def output_population_densities(config, df_populations_sam_long ):
    """
    Calculate population densities by cluster and output to CSV. This function splits LAD codes into those 
    which conducted census in 2021 (England, Wales and Northern Ireland) and those which conducted census 
    in 2022 (Scotland). It then applies 2021 population and area to the 2021 group and applies 2022 
    population and area to LAD codes in Scotland. The function then groups all the variables by their cluster 
    (e.g. supergroup 1 or subgroup 1a1) and aggregates the population and area values so there is one population
    value and one area value for each cluster. Then population density is calculated (population / area) and saved
    as a csv.  
    
    Data must be cleaned using population_sam_preprocessing function before running this function. 

    Parameters
    ----------
    config : dict
        A configuration dictionary containing the output directory path.
    df_populations_sam_long : pd.DataFrame
        A DataFrame containing the merged restructured_cluster_table_long and population estimates, containing at 
        least the columns 'LAD_code', 'supergroup', 'population' and 'AREALHECT'

    Returns
    -------
    pandas.DataFrame
        A combined DataFrame containing population densities for supergroups, groups, and subgroups.    
    """    
    # Define the clusters and their corresponding columns
    clusters = {
        'supergroup': 'supergroup',
        'group': 'group',
        'subgroup': 'subgroup'
    }

    # Initialize an empty list to store the processed DataFrames
    dataframes = []

    # Process each cluster
    for cluster, column in clusters.items():
        df = df_populations_sam_long[[column, 'population', 'AREALHECT']]
        df = df.groupby(by=column).sum()
        df['population_density'] = df['population'] / df['AREALHECT']
        df['cluster'] = cluster
        df = df[['cluster'] + [col for col in df.columns if col != 'cluster']]
        dataframes.append(df)

    # Concatenate all three DataFrames (supergroup, group and subgroup) into one
    pop_densities = pd.concat(dataframes)
    # Reset the index to turn the cluster allocation into a column
    pop_densities.reset_index(inplace=True)
    # Rename the first column to cluster_allocation
    pop_densities.rename(columns={pop_densities.columns[0]: 'cluster_allocation'}, inplace=True)

    # Save the combined DataFrame to a single CSV file
    pop_densities_filepath = os.path.join(config['output_directory'], 'population_densities.csv')
    pop_densities.to_csv(pop_densities_filepath, index=False)
    
    # Return the combined dataframe
    return pop_densities

def cluster_summary(restructured_cluster_table_long, uk_std_cluster_means, variance_df, pop_sums, pop_densities, cluster_column):
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
 
        # Find example areas from the restructured_cluster_table_long table
        example_areas = restructured_cluster_table_long[restructured_cluster_table_long[cluster_column] == cluster]
        if not example_areas.empty:
            area_names = example_areas['LAD_name'].sample(n=min(3, len(example_areas)), random_state=42).tolist()
        else:
            area_names = ["No area found"]

        # Extract the percentage for the current cluster
        cluster_data = pop_sums.loc[pop_sums[cluster_column] == cluster]  # Filter for the current cluster
        percentage_column = f'{cluster_column}_percentage'
        percentage = cluster_data[percentage_column].values[0]  

        ## Population density
        # Ensure both 'cluster_allocation' values and 'cluster' are strings
        pop_densities['cluster_allocation'] = pop_densities['cluster_allocation'].astype(str)
        cluster = str(cluster)

        # Find the row where 'cluster_allocation' matches the defined cluster
        matching_row = pop_densities[pop_densities['cluster_allocation'] == cluster]

        # Extract the 'population_density' value from the matching row
        if not matching_row.empty:
            cluster_pop_density = matching_row['population_density'].values[0]
        else:
            print(f"No matching row found for cluster_allocation: {cluster}")

        # Print the summary for the cluster
        # Combine the print statements into a single string
        output = (
            f"Cluster {cluster} contains {num_local_authorities} local authorities which is {percentage_local_authorities:.2f}% of UK local authorities, "
            f"this included {percentage:.2f}% of the UK population (values are taken for 2021 for EW and NI, but 2022 for Scot, due to times of the census)."
            f" This cluster has a population density of {cluster_pop_density:.2f} people per hectare.\n"
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
        # cluster_number = int(row['cluster'])
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

                    variance_value = variance_df.loc[cluster_number_str, v_code] # if running through main un hash
                    # variance_value = variance_df.loc[cluster_number_int, v_code] # if running through main hash this!

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
    filepath_long = os.path.join(config["output_directory"], "cluster_assignments/restructured_subclustering_output_long.csv")
    restructured_cluster_table_long = pd.read_csv(filepath_long)
    uk_std_cluster_means_filepath = os.path.join(config["output_directory"], "std_means/uk_std_means/uk_std_cluster_means_output.csv")
    uk_std_cluster_means = pd.read_csv(uk_std_cluster_means_filepath)

    lookup_file = config["select_variables_lookup"]

    cluster_summaries_wrapper(config, restructured_cluster_table_long, uk_std_cluster_means, lookup_file,  cluster_column='subgroup')
