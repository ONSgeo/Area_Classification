# This is an optional script which does not include all 60 variables in the clustering.
# Instead this focuses on using the same as academics used for the 2021/22 OAC.

from utilities.load_config import load_config

import pandas as pd
import yaml

def drop_variables_pre_clustering(config):
    """
    Duplicates the preprocessed input table, removes columns listed under 'variables_to_drop' in the config,
    and saves the resulting table as a new CSV file.

    Parameters
    ----------
        config_path (str): Path to the YAML configuration file.

    Parameters
    ----------
        None
    """   
    # Get the list of variables to drop from the config
    variables_to_drop = config.get('variables_to_drop', [])

    # Load the preprocessed input table
    preprocessed_input_path = (config["qa_folder_path"]+"pre_processed_data_ew_ni_scot.csv")
    preprocessed_input_table = pd.read_csv(preprocessed_input_path)
    
    # Duplicate the table
    processed_input_table = preprocessed_input_table.copy()
    
    # Drop the specified columns
    processed_input_table = processed_input_table.drop(columns=variables_to_drop, errors='ignore')

    # Save the processed table as a new CSV file
    processed_input_table.to_csv(config["pre_clustering_data"], index=False)

    

    # Calculate standardized means for each variable
    standardized_data = processed_input_table.copy()
    for column in processed_input_table.columns[1:]:  # Skip the first column (e.g., area codes)
        mean = processed_input_table[column].mean()
        std = processed_input_table[column].std()
        if std != 0:  # Avoid division by zero
            standardized_data[column] = (processed_input_table[column] - mean) / std
        else:
            standardized_data[column] = 0  # If std is 0, set standardized values to 0

    # Save the standardized data to a new file
    standardized_data.to_csv(config["pre_clustering_data_std_mean"], index=False)

    return standardized_data
    

# Example usage
if __name__ == "__main__":
    # Example usage
    config = load_config('area_classification/config.yaml')
    pre_clustering_df = drop_variables_pre_clustering(config)