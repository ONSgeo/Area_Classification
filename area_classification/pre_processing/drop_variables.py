# This script which does not include all 60 variables in the clustering.
import pandas as pd
import yaml
from pre_processing.standardize_pre_clustering_data import standardize_dataframe

def check_drop_columns_true(config, pre_clustering_std):
    """
    This function checks if the 'drop_columns' key in the config is set to True.
    If it is, it calls the drop_variables_pre_clustering function to drop specified columns
    from the preprocessed input table.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and parameters.
    pre_clustering_std : pd.DataFrame
         pandas DataFrame containing the preprocessed table.

    Returns:
        None
    """
    
    # Check if 'drop_columns' is set to True in the config
    if config["drop_columns"]:
        return drop_variables_pre_clustering(config, pre_clustering_std, config.get('variables_to_drop', [])) 
    else: 
        return pre_clustering_std



def drop_variables_pre_clustering(config, pre_clustering_std, variables_to_drop):
    """
    Duplicates the preprocessed input table, removes columns listed under 'variables_to_drop' in the config,
    and saves the resulting table as a new CSV file.

    Parameters:
    config_path : str
        Path to the YAML configuration file.
    pre_clustering_std :
        A pandas DataFrame containing the preprocessed table.
    variables_to_drop : 
        A list of variables which will be dropped (these can be stored in the config)

    Returns:
        None
    """   
    # Duplicate the table the preprocessed input table
    processed_input_table = pre_clustering_std.copy()
    
    # Drop the specified columns
    pre_clustering_filtered_df = processed_input_table.drop(columns=variables_to_drop, errors='ignore')

    # Save the processed table as a new CSV file
    pre_clustering_filtered_df.to_csv(config["pre_clustering_data_filtered"], index=False)

    # Standardize the data
    pre_clustering_filtered_std = standardize_dataframe(pre_clustering_filtered_df)

    # Save the standardized data to a new file
    pre_clustering_filtered_std.to_csv(config["pre_clustering_data_filtered_std_mean"], index=False)


    return pre_clustering_filtered_std


# Example usage
if __name__ == "__main__":
    from utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    pre_clustering_std = pd.read_csv('data/inputs/pre_clustering_data_std_means.csv')
    pre_clustering_df = drop_variables_pre_clustering(config, pre_clustering_std, config.get('variables_to_drop', [])) 
    print(pre_clustering_df)