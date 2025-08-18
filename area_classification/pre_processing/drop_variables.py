# This is an optional script which does not include all 60 variables in the clustering.
# Instead this focuses on using the same as academics used for the 2021/22 OAC.
# STEPS
# check if the config drop_columns is true or false
# if config["drop_columns"]:
        #drop_variables_pre_clustering(config)


from utilities.load_config import load_config

import pandas as pd
import yaml
from pre_processing.standardize_pre_clustering_data import standardize_dataframe

def check_drop_columns_true(config, pre_clustering_std):
    """
    This function checks if the 'drop_columns' key in the config is set to True.
    If it is, it calls the drop_variables_pre_clustering function to drop specified columns
    from the preprocessed input table.

    Parameters:
        config (dict): Configuration dictionary containing paths and parameters.

    Returns:
        None
    """
    
    # Check if 'drop_columns' is set to True in the config
    if config["drop_columns"]:
        return drop_variables_pre_clustering(config, pre_clustering_std)
    else: 
        return pre_clustering_std



def drop_variables_pre_clustering(config, pre_clustering_std):
    """
    Duplicates the preprocessed input table, removes columns listed under 'variables_to_drop' in the config,
    and saves the resulting table as a new CSV file.

    Parameters:
        config_path (str): Path to the YAML configuration file.

    Returns:
        None
    """   
    # Get the list of variables to drop from the config
    variables_to_drop = config.get('variables_to_drop', [])

    # Load the preprocessed input table
    preprocessed_input_table = pre_clustering_std
    
    # Duplicate the table
    processed_input_table = preprocessed_input_table.copy()
    
    # Drop the specified columns
    pre_clustering_filtered_df = processed_input_table.drop(columns=variables_to_drop, errors='ignore')

    # Save the processed table as a new CSV file
    pre_clustering_filtered_df.to_csv(config["pre_clustering_data_filtered"], index=False)

    # Standardize the data
    pre_clustering_filtered_std = standardize_dataframe(pre_clustering_filtered_df)

    # Save the standardized data to a new file
    pre_clustering_filtered_std.to_csv(config["pre_clustering_data_filtered_std_mean"], index=False)

    # check the data type of pre_clustering_filtered_std 
    print("Data type of pre_clustering_filtered_std:", type(pre_clustering_filtered_std))
    print(pre_clustering_filtered_std)
    csv_version = pd.read_csv(config["pre_clustering_data_filtered_std_mean"])
    print("drop_variables_csv_version:", csv_version)
    print("Data type of csv_version:", type(csv_version))

    return pre_clustering_filtered_std


# Example usage
if __name__ == "__main__":
    # Example usage
    config = load_config('area_classification/config.yaml')
    pre_clustering_df = drop_variables_pre_clustering(config)