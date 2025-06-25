import pandas as pd
import os
# Import the re module for regular expressions
import re  

def select_variables(df_temp, select_variables_lookup):
    """
    Selects specific columns from a main DataFrame based on a lookup table
    and returns a new DataFrame with only the specified columns.

    Parameters:
    - df_temp (pd.DataFrame): The main DataFrame containing all data.
    - select_variables_lookup (str): Path to the CSV file containing the lookup information.

    Returns:
    - pd.DataFrame: A new DataFrame with only the specified columns.
    """
    # Load the lookup table
    lookup_df = pd.read_csv(select_variables_lookup)

    # Extract the columns to select and their new names
    selected_columns = lookup_df['variable_code'].dropna().tolist()
    new_code = dict(zip(lookup_df['variable_code'], lookup_df['new_code']))
    
    # Check for missing columns and log them
    valid_columns = []
    for col in selected_columns:
        if col not in df_temp.columns:
            print(f"Warning: Column '{col}' is missing in the temp DataFrame.")
        else:
            valid_columns.append(col)
    
    # Ensure the first column (area codes) of df_temp is included as the first column
    first_column = df_temp.columns[0]
    if first_column not in valid_columns:
        valid_columns.insert(0, first_column)
    
    print(f"Columns to be selected: {valid_columns}")
    
    # Filter the main DataFrame to include only the valid columns
    filtered_df = df_temp[valid_columns].copy()

    # Rename the columns based on lookup table (V codes)
    filtered_df.rename(columns=new_code, inplace=True)

    # Keep the first column (area codes) in place and reorder the remaining columns
    first_column = filtered_df.columns[0]
    remaining_columns = filtered_df.columns[1:]

    # Order the remaining columns based on the numeric value following 'v'
    def extract_numeric_value(col_name):
        match = re.search(r'v(\d+)', col_name)
        # Default to infinity if no match
        return int(match.group(1)) if match else float('inf')  

    ordered_remaining_columns = sorted(remaining_columns, key=extract_numeric_value)

    # Combine the first column (area codes) with the reordered remaining columns
    ordered_columns = [first_column] + ordered_remaining_columns
    filtered_df = filtered_df[ordered_columns]

    # Define the folder path and file name
    folder_path = "data/QA"
    file_name = "select_variables_output.csv"

    # Ensure the folder exists, create it if it doesn't
    os.makedirs(folder_path, exist_ok=True)

    # Construct the full file path
    output_file_path = os.path.join(folder_path, file_name)

    # Save the DataFrame to the constructed path
    filtered_df.to_csv(output_file_path, index=False)
    # Save the resulting DataFrame as a CSV file
    #filtered_df.to_csv("/data/QA/select_variables_output", index=False)

    return filtered_df