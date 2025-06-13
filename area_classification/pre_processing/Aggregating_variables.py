import pandas as pd
import os


def batch_ag_columns(main_path, file_configs):
    """
    This function loops through multiple CSV files, aggregates specified columns,
    adds new columns, renames the original CSV file, and saves the updated file
    with a new name.

    Parameters:
    - file_configs (list of dict): A list of dictionaries where each dictionary contains:
        - 'file_name' (str): Path to the CSV file to update.
        - 'col_names' (list): List of column names to aggregate.
        - 'new_col_name' (str): Name of the new column to create.
    """
    for config in file_configs:
        file_name = config['file_name']
        col_names = config['col_names']
        new_col_name = config['new_col_name']

        # Construct the full file path
        file_name = os.path.join(main_path, file_name)
        
        # Derive a new name for the '_derived' file
        base, ext = os.path.splitext(file_name)
        derived_name = f"{base}_derived{ext}"
        
        # Check if the '_derived' file already exists
        if os.path.exists(derived_name):
            # Read the existing '_derived' file
            df = pd.read_csv(derived_name)
            print(f"Updating existing file: {derived_name}")
        else:
            # Read the original file to create a new '_derived' file
            df = pd.read_csv(file_name)
            print(f"Creating new file: {derived_name}")
        
        # Add the new column by summing the specified columns
        df[new_col_name] = df[col_names].sum(axis=1)
        
        # Save the updated DataFrame to the '_derived' file
        df.to_csv(derived_name, index=False)
        print(f"Updated '{derived_name}' with new column '{new_col_name}'.")

