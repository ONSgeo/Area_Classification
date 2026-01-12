import pandas as pd
import os

def cluster_table_wrapper(config, restructured_cluster_table, cluster_name_lookup):
    """
    Wrapper function to create the excel doc from the csv tables

    Parameters
    ----------
    config : dict
        Configuration dictionary containing filepaths.
    restructured_cluster_table : DataFrame
        DataFrame containing cluster allocations for each local authority.
    cluster_name_lookup : DataFrame
        Look up containing cluster numbers and cluster names.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with the clusters and the number of local authorities in each.
    pandas.DataFrame
        DataFrame with the cluster names and numbers.
    """
    non_zero_table = replace_zero_with_six(config, restructured_cluster_table)
    cluster_codes_and_counts_table = create_cluster_totals_table(config, non_zero_table, cluster_name_lookup)
    cluster_names_table = create_cluster_names_table(config, non_zero_table, cluster_name_lookup)
    return cluster_codes_and_counts_table , cluster_names_table

def replace_zero_with_six(config, restructured_cluster_table):
    """
    Updates cluster numbers ('supergroup', 'group', or 'subgroup') in Supergroup 0 to be Supergroup 6
    and saves the modified DataFrame. e.g. 0c1 becomes 6c1 
    
    Parameters
    ----------
    config : dict
        Configuration dictionary containing filepaths.
    restructured_cluster_table : str
        Path to the CSV cluster assignments dataframe with the columns 'LAD_name', 'LAD_code', 'supergroup', 
        'group', and 'subgroup' columns.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame the same as restructured_cluster_table but supergroup 0 is now supergroup 6.
    """
    df = pd.read_csv(restructured_cluster_table)
    for col in ['supergroup', 'group', 'subgroup']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'^0', '6', regex=True)
    output_path = os.path.join(config['output_directory'], 'cluster_no_zeros.csv')
    df.to_csv(output_path, index=False)
    return df

def create_cluster_totals_table(config, non_zero_table, cluster_name_lookup):
    """
    Calculates the number of LADs allocated to each unique cluster code (e.g. supergroup 1, subgroup 1c1 etc.)
    Then creates a dataframe which adds 'cluster_name' column and filled using the cluster_name_lookup.
    The resulting table is sorted by 'cluster_code' and saved as a CSV.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing filepaths.
    non_zero_table : DataFrame
        DataFrame containing cluster allocations for each local authority, for supergroup 1 to 6.
    cluster_name_lookup : DataFrame
        Look up containing cluster numbers and cluster names.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with columns 'cluster_code', 'cluster_name' and 'number_of_LADs'.
    """

    # Combine all unique values from the three columns
    cluster_codes = pd.concat([
        non_zero_table['supergroup'],
        non_zero_table['group'],
        non_zero_table['subgroup']
    ]).dropna().astype(str)

    # Count occurrences of each unique value
    totals = cluster_codes.value_counts().reset_index()
    totals.columns = ['cluster_code', 'number_of_LADs']
    
    # Insert 'cluster_name' column between 'cluster_code' and 'total'
    totals.insert(1, 'cluster_name', '')
    totals = totals.sort_values('cluster_code').reset_index(drop=True)
    # Read the lookup table (assuming it has columns 'cluster_code' and 'cluster_name')
    lookup_df = pd.read_csv(cluster_name_lookup)

    # Create a mapping dictionary from the lookup table
    name_map = dict(zip(lookup_df['cluster_code'].astype(str), lookup_df['cluster_name']))

    # Map the names into the totals DataFrame
    totals['cluster_name'] = totals['cluster_code'].map(name_map).fillna('')

    # Print cluster codes with missing names
    missing_names = totals[totals['cluster_name'] == '']['cluster_code'].tolist()
    if missing_names:
        print("Warning: The following cluster codes are missing names in the lookup:")
        for code in missing_names:
            print(f"  {code}")
    output_path = os.path.join(config['output_directory'], 'cluster_totals.csv')
    totals.to_csv(output_path, index=False)
    return totals

def create_cluster_names_table(config, non_zero_table, cluster_name_lookup):
    """
    This adds an extra columns for the cluster names which is filled using the cluster_name_lookup
    and sorts the data frame based on subgroup and saved as a CSV.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing filepaths.
    non_zero_table : DataFrame
        DataFrame containing cluster allocations for each local authority, for supergroup 1 to 6.
    cluster_name_lookup : DataFrame
        Look up containing cluster numbers and cluster names.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with name columns added and sorted by 'subgroup' if present.
    """
    df = non_zero_table.copy()

    # Read the lookup table (assuming it has columns 'cluster_code' and 'cluster_name')
    lookup_df = pd.read_csv(cluster_name_lookup)
    name_map = dict(zip(lookup_df['cluster_code'].astype(str), lookup_df['cluster_name']))

    # Insert name columns immediately after their parent columns
    for col in ['supergroup', 'group', 'subgroup']:
        if col in df.columns:
            name_col = f"{col}_name"
            # Compute the index to insert after the parent column
            insert_idx = df.columns.get_loc(col) + 1
            df.insert(insert_idx, name_col, df[col].astype(str).map(name_map).fillna(''))
            # Print missing names for this column
            missing = df[df[name_col] == ''][col].unique()
            if len(missing) > 0:
                print(f"Warning: The following {col} codes are missing names in the lookup:")
                for code in missing:
                    print(f"  {code}")

    # Reorder by the subgroup codes
    if 'subgroup' in df.columns:
        df = df.sort_values('subgroup').reset_index(drop=True)
    output_path = os.path.join(config['output_directory'], 'cluster_names.csv')
    df.to_csv(output_path, index=False)
    return df