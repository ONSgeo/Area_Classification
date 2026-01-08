# This script which does not include all 60 variables in the clustering.
import pandas as pd
import yaml


def check_drop_columns_true(config, preprocessed_df):
    """
    This function checks if the 'drop_columns' key in the config is set to True.
    If it is, it calls the drop_variables_pre_clustering function to drop specified columns
    from the preprocessed input table.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and parameters.
    preprocessed_df : pd.DataFrame
         pandas DataFrame containing the preprocessed table.

    Returns
    -------
    pd.DataFrame
        DataFrame with specified columns dropped if 'drop_columns' is True; otherwise, the original DataFrame.
    """
    
    # Check if 'drop_columns' is set to True in the config
    if config["drop_columns"]:
        return drop_variables_pre_clustering(config, preprocessed_df, config.get('variables_to_drop', [])) 
    else: 
        return preprocessed_df



def drop_variables_pre_clustering(config, preprocessed_df, variables_to_drop):
    """
    Duplicates the preprocessed input table, removes columns listed in 'variables_to_drop',
    and saves the resulting table as a new CSV file.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing the output file path under 'pre_clustering_data_filtered'.
    preprocessed_df : pd.DataFrame
        DataFrame containing the preprocessed table.
    variables_to_drop : list
        List of variable names (columns) to drop.

    Returns
    -------
    pd.DataFrame
        The filtered DataFrame with specified columns removed.
    """  
    # Duplicate the preprocessed input table
    processed_input_table = preprocessed_df.copy()
    
    # Drop the specified columns
    pre_clustering_filtered = processed_input_table.drop(columns=variables_to_drop, errors='ignore')

    # Save the filtered table as a new CSV file 
    pre_clustering_filtered.to_csv(config["pre_clustering_data_filtered"], index=False)

    return pre_clustering_filtered


    