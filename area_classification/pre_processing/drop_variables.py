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
    pre_clustering_std : pd.DataFrame
         pandas DataFrame containing the preprocessed table.

    Returns
    -------
        None
    """
    
    # Check if 'drop_columns' is set to True in the config
    if config["drop_columns"]:
        return drop_variables_pre_clustering(config, preprocessed_df, config.get('variables_to_drop', [])) 
    else: 
        return preprocessed_df



def drop_variables_pre_clustering(config, preprocessed_df, variables_to_drop):
    """
    Duplicates the preprocessed input table, removes columns listed under 'variables_to_drop' in the config,
    and saves the resulting table as a new CSV file.

    Parameters
    ----------
    config_path : str
        Path to the YAML configuration file.
    pre_clustering_std :
        A pandas DataFrame containing the preprocessed table.
    variables_to_drop : 
        A list of variables which will be dropped (these can be stored in the config)

    Returns
    -------
        None
    """   
    # Duplicate the table the preprocessed input table
    processed_input_table = preprocessed_df.copy()
    
    # Drop the specified columns
    pre_clustering_filtered = processed_input_table.drop(columns=variables_to_drop, errors='ignore')

    # Save the processed table as a new CSV file NAME NEEDS CHNAGIN
    pre_clustering_filtered.to_csv(config["pre_clustering_data_filtered"], index=False)

    return pre_clustering_filtered


# Example usage
if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    pre_clustering_std = pd.read_csv(f"{config['input_directory']}pre_clustering_data_std_means.csv")
    pre_clustering_df = drop_variables_pre_clustering(config, pre_clustering_std, config.get('variables_to_drop', [])) 
    print(pre_clustering_df)

    