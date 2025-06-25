import pandas as pd
import yaml
import os

def batch_ag_columns(df_temp, file_configs):
    """
    This function aggregates specified columns in a temporary DataFrame, aggregates specified columns,
    adds new columns, and updates the DataFrame in-memory.

    Parameters:
    - df_temp (pd.DataFrame): The temporary DataFrame to update.
    - file_config (list of dict): A list of dictionaries where each dictionary contains:
        - 'col_names' (list): List of column names to aggregate.
        - 'new_col_name' (str): Name of the new column to create.

    Returns:
    - pd.DataFrame: The updated DataFrame with new aggregated columns.
    """
    for config in file_configs:
        col_names = config['col_names']
        new_col_name = config['new_col_name']

         # Check if all columns in col_names exist in df_temp
        missing_cols = [col for col in col_names if col not in df_temp.columns]
        if missing_cols:
            print(f"Warning: Missing columns {missing_cols} in DataFrame. Skipping aggregation for {new_col_name}.")
            continue

        # Add the new column by summing the specified columns
        df_temp[new_col_name] = df_temp[col_names].sum(axis=1)
        print(f"Added new column '{new_col_name}' to the DataFrame.")
        
        # Need to save using config instead!
        #config["qa_folder_path"]
        #output_file_path = config["qa_folder_path"] + "/name.csv"
        #df_temp.to_csv(output_file_path, index=False)

        # Define the folder path and file name
        folder_path = "data/QA"
        file_name = "aggregated_variables_output.csv"

        # Ensure the folder exists, create it if it doesn't
        os.makedirs(folder_path, exist_ok=True)

        # Construct the full file path
        output_file_path = os.path.join(folder_path, file_name)

        # Save the DataFrame to the constructed path
        df_temp.to_csv(output_file_path, index=False)
        # Temp dataframe saved out for QA
        #df_temp.to_csv("/data/QA/aggregated_variables_output.csv", index=False)
        
    return df_temp
