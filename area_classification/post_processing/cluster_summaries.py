# Creating print statements about the clusters

import logging

logger = logging.getLogger(__name__)
import re

import numpy as np
import pandas as pd


def cluster_summaries_wrapper(
    config, restructured_cluster_table_long, uk_std_cluster_means, lookup_file, cluster_column
):
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
    2. Generate detailed summaries for each cluster.
    3. Identify the key drivers for each cluster.

    Returns
    -------
    None
        This function does not return a value. It performs operations that generate summaries
        and insights about the clusters.
    """

    # Step 1 - Variance:
    variance_df = calculate_cluster_variance(restructured_cluster_table_long, cluster_column)

    # Step 2 - Cluster summaries:
    cluster_info = cluster_summary(
        restructured_cluster_table_long, uk_std_cluster_means, variance_df, cluster_column
    )

    # Step 3 - Cluster drivers:
    identify_cluster_drivers(
        uk_std_cluster_means, lookup_file, cluster_info, variance_df, cluster_column, top_n=3
    )

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
    v_columns = [col for col in data.columns if col.startswith("v")]

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

    variance_df = pd.DataFrame.from_dict(cluster_variances, orient="index")
    # Make the cluster column the index
    variance_df.index.name = cluster_column
    variance_df = variance_df.sort_index()
    # Add the average variance as an additional column
    variance_df["cluster_average_variance"] = variance_df.index.map(cluster_average_variance)

    return variance_df


def cluster_summary(
    restructured_cluster_table_long, uk_std_cluster_means, variance_df, cluster_column
):
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
    cluster_column : str
        The name of the column in the DataFrame that contains cluster allocations (likely supergroup, group, and subgroup).

    Returns
    ----------
    list: A list of strings, where each string contains a detailed summary for a cluster, including:
        - The number and percentage of local authorities in the cluster.
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
        filtered_df = uk_std_cluster_means.loc[
            uk_std_cluster_means["hierarchy_level"] == cluster_column
        ].assign(cluster=lambda df: pd.to_numeric(df["cluster"], errors="coerce").astype(int))
    elif cluster_column in ["group", "subgroup"]:
        # Sort based on the numeric part
        clusters = sorted(clusters, key=lambda x: int("".join(filter(str.isdigit, str(x)))))
        # Filter rows where 'hierarchy_level' is the same as the cluster_column specified and ensure 'cluster' column is treated as strings
        filtered_df = uk_std_cluster_means.loc[
            uk_std_cluster_means["hierarchy_level"] == cluster_column
        ].assign(cluster=lambda df: df["cluster"].astype(str))

    # Initialize a list to store outputs for all clusters
    cluster_info = []

    # Iterate through each cluster
    for cluster in clusters:
        # Filter rows for the current cluster
        cluster_data = restructured_cluster_table_long[
            restructured_cluster_table_long[cluster_column] == cluster
        ]

        # Number of local authorities in the current cluster
        num_local_authorities = cluster_data["LAD_name"].nunique()

        # Total number of unique local authorities in the dataset
        total_local_authorities = restructured_cluster_table_long["LAD_name"].nunique()

        # Percentage of local authorities in the current cluster
        percentage_local_authorities = (num_local_authorities / total_local_authorities) * 100

        # Find example areas from the restructured_cluster_table_long table
        example_areas = restructured_cluster_table_long[
            restructured_cluster_table_long[cluster_column] == cluster
        ]
        if not example_areas.empty:
            area_names = (
                example_areas["LAD_name"]
                .sample(n=min(3, len(example_areas)), random_state=42)
                .tolist()
            )
        else:
            area_names = ["No area found"]

        # Print the summary for the cluster
        # Combine the print statements into a single string
        output = f"Cluster {cluster} contains {num_local_authorities} local authorities which is {percentage_local_authorities:.2f}% of UK local authorities. "
        # Check if the cluster exists in the DataFrame
        if cluster in variance_df.index:
            cluster_avg_variance = variance_df.loc[cluster, "cluster_average_variance"]
            output += f"The average variance for cluster {cluster} is {cluster_avg_variance:.3f}. Example areas: {', '.join(area_names)}"
        else:
            output += f"Cluster {cluster} not found in the DataFrame.\n"

        # Append the output to the list
        cluster_info.append(output)

    return cluster_info


def identify_cluster_drivers(
    uk_std_cluster_means, lookup_file, cluster_info, variance_df, cluster_column, top_n=5
):
    """
    Identifies the key variables that differentiate each cluster from others by analyzing
    the mean values of variables within a cluster compared to the mean values across all
    other clusters. The function also maps variable names using a lookup file and provides
    detailed descriptions of the differences for each cluster.

    Parameters
    ----------
    uk_std_cluster_means : pd.DataFrame
        A DataFrame where rows represent clusters and columns represent the mean values
        of variables for each cluster.
    lookup_file : str
        Path to a CSV file containing a lookup table with columns
        'new_code', 'variable_name', and 'domain' for mapping variable codes to
        descriptive names and domains.
    cluster_info : list
        A list of strings containing information about each cluster,
        such as example area names or additional metadata.
    variance_df : pd.DataFrame
        A DataFrame containing variance values for each variable
        and cluster, indexed by cluster number and variable code.
    cluster_column : str
        The name of the column in the DataFrame that contains cluster allocations (likely supergroup,
        group, and subgroup).
    top_n : int (optional)
        The number of top driving variables to identify for each
        cluster. Defaults to 5.

    Returns
    ----------
    None
        The function prints the top driving variables for each cluster, along with
        detailed descriptions and variance values.

    """
    # Filter the uk_std_cluster_means_output to include only the top row and rows with the specified cluster_column
    # in the hierarchy_level column
    if "hierarchy_level" not in uk_std_cluster_means.columns:
        raise ValueError("Means table must contain a 'hierarchy_level' column.")

    uk_std_cluster_means = pd.concat(
        [uk_std_cluster_means[uk_std_cluster_means["hierarchy_level"] == cluster_column]]
    )

    # Remove the hierarchy_level column
    uk_std_cluster_means = uk_std_cluster_means.drop(columns=["hierarchy_level"])

    # Load the lookup file
    lookup_df = pd.read_csv(lookup_file)

    # Ensure the lookup file has the required columns
    if "new_code" not in lookup_df.columns or "variable_name" not in lookup_df.columns:
        raise ValueError("Lookup file must contain 'new_code' and 'variable_name' columns.")

    # Create a mapping dictionary for variable names with new_code in brackets
    code_to_variable = {
        row["new_code"]: f"{row['variable_name']} ({row['new_code']})"
        for _, row in lookup_df.iterrows()
    }

    # Replace column names in the uk_std_cluster_means
    uk_std_cluster_means = uk_std_cluster_means.rename(columns=code_to_variable)

    for index, row in uk_std_cluster_means.iterrows():
        # Use the value in the 'cluster' column as the cluster_number
        # cluster_number = int(row['cluster'])
        cluster_number = row["cluster"]

        # Create a Pandas Series of the mean values of all numeric columns in uk_std_cluster_means, excluding rows where the cluster column equals cluster_number.
        other_clusters_means = (
            uk_std_cluster_means[uk_std_cluster_means["cluster"] != cluster_number]
            .select_dtypes(include="number")
            .mean()
        )

        # Calculate the difference between the cluster's values and the other clusters' means (which excludes the row of the current cluster_number)
        differences = row.drop("cluster") - other_clusters_means

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
            variable_name = re.sub(r"\(.*?\)", "", variable).strip()
            # Determine if the difference is "higher" or "lower"
            if differences[variable] > 0:
                difference_status = "higher"
            else:
                difference_status = "lower"

            # Extract the "V" followed by two digits using regex
            match = re.search(r"v\d{2}", variable)
            if match:
                v_code = match.group(0)  # Extracted code (e.g., "v22")

                # Find the first row in the lookup table where the code matches
                domain_value = lookup_df.loc[
                    lookup_df["new_code"].str.contains(v_code, na=False), "domain"
                ].head(1)

                # Define a dictionary to map domains to their specific message logic
                domain_logic = {
                    "Demography and Migration": lambda table_name_value, variable_name: (
                        f"proportion of households comprised of {variable_name}"
                        if "Household composition" in table_name_value
                        else "proportion of people who live in a communal establishment"
                        if "Residency type" in table_name_value
                        else "proportion of people whose address one year ago is the same as the address of enumeration"
                        if "Migrant Indicator" in table_name_value
                        else f"proportion of people who are {variable_name}"
                        if "Age structure" in table_name_value
                        or "Legal partnership status" in table_name_value
                        else f"proportion of people with a country of birth in {variable_name}"
                        if "Country of birth" in table_name_value
                        else f"{variable_name}"
                        if "Population density" in table_name_value
                        else f"people {variable_name}"
                    ),
                    "Labour Market": lambda table_name_value, variable_name: (
                        f"proportion of people working jobs which are {variable_name}"
                        if "hours worked" in table_name_value
                        else "proportion of full-time students"
                        if "NS-SeC" in table_name_value
                        else f"proportion of people who work in {variable_name.lstrip('0123456789. ').strip()}"
                        if "occupation" in table_name_value
                        else f"proportion of people who work in {variable_name}"
                    ),
                    "Health, Disability and Unpaid Care": lambda table_name_value, variable_name: (
                        variable_name
                        if "Disability" in table_name_value
                        else "proportion of people who provide unpaid care"
                        if "Provision of unpaid care" in table_name_value
                        else f"proportion of people {variable_name}"
                    ),
                    "Housing": lambda table_name_value, variable_name: (
                        "proportion of people who live in a flat"
                        if "Accommodation type" in table_name_value
                        and "flat" in variable_name.lower()
                        else f"proportion of people living in a {variable_name}"
                        if "Accommodation type" in table_name_value
                        else f"proportion of dwellings which are {variable_name}"
                        if "Occupancy rating for rooms" in table_name_value
                        else f"proportion of people who own {variable_name}"
                        if "Car or van availability" in table_name_value
                        else f"proportion of people living in {variable_name} accommodation"
                        if "Tenure" in table_name_value
                        else f"proportion of people {variable_name}"
                    ),
                    "Ethnicity, Identity, Language and Religion": lambda table_name_value,
                    variable_name: (
                        f"proportion of people who are {variable_name}"
                        if "Ethnic group" in table_name_value
                        else "proportion of households where all household members have the same ethnic group"
                        if "Multiple ethnic group" in table_name_value
                        else f"proportion of whose religion is {variable_name}"
                        if "Religion" in table_name_value
                        else f"proportion of people who {variable_name}"
                        if "Proficient in English" in table_name_value
                        else f"proportion of people {variable_name}"
                    ),
                    "Education": lambda table_name_value, variable_name: (
                        f"proportion of people whose highest level of qualification is {variable_name}"
                    ),
                }

                # Check if a match is found and print the domain-specific message and variance value
                if not domain_value.empty:
                    domain = domain_value.iloc[0]
                    # Retrieve the table_name value for the specific variable
                    table_name_value = (
                        lookup_df.loc[
                            lookup_df["new_code"].str.contains(v_code, na=False), "table_name"
                        ]
                        .head(1)
                        .iloc[0]
                    )

                    # Convert cluster_number to string to match the index type
                    cluster_number_str = str(cluster_number)
                    # cluster_number_int = int(cluster_number_str) # if running through main hash this!

                    variance_value = variance_df.loc[
                        cluster_number_str, v_code
                    ]  # if running through main un hash
                    # variance_value = variance_df.loc[cluster_number_int, v_code] # if running through main hash this!

                    # Generate the specific message based on the domain logic
                    if domain in domain_logic:
                        specific_message = domain_logic[domain](table_name_value, variable_name)
                        message = f"• {difference_status} ({differences[variable]:.3f}) {specific_message}. Variance:{variance_value:.3f} ({domain} domain)"
                        print(message)
                    else:
                        # Default message for unrecognized domains
                        message = f"Domain {domain} not recognized for variable {variable_name}."

        print("-" * 40)
