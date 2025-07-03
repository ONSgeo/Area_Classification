import pandas as pd
import os

def batch_ag_columns(df_temp, file_configs, user_config):
    """
    This function aggregates specified columns in a temporary DataFrame, aggregates specified columns,
    adds new columns, and updates the DataFrame in-memory.

    Parameters:
    - df_temp (pd.DataFrame): The temporary DataFrame to update.
    - file_config (list of dict): A list of dictionaries where each dictionary contains:
        - 'col_names' (list): List of column names to aggregate.
        - 'new_col_name' (str): Name of the new column to create.
    - user_config (dict): A dictionary containing user configuration settings, including the path to save the output file or QA.

    Returns:
    - pd.DataFrame: The updated DataFrame with new aggregated columns.
    """
    for key in file_configs:
        col_names = file_configs[key]
        new_col_name = key

         # Check if all columns in col_names exist in df_temp
        missing_cols = [col for col in col_names if col not in df_temp.columns]
        if missing_cols:
            print(f"Warning: Missing columns {missing_cols} in DataFrame. Skipping aggregation for {new_col_name}.")
            continue

        # Add the new column by summing the specified columns
        df_temp[new_col_name] = df_temp[col_names].sum(axis=1)
        print(f"Added new column '{new_col_name}' to the DataFrame.")

    # Ensure QA directory exists
    os.makedirs(os.path.dirname(user_config["qa_folder_path"]), exist_ok=True)

    # Save to data QA folder
    output_file_path = user_config["qa_folder_path"] + "aggregated_variables_output.csv"
    df_temp.to_csv(output_file_path, index=False)
        
    return df_temp
