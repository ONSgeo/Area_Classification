import pandas as pd
# Import the re module for regular expressions
import re  
import os

def select_variables(df_temp, lookup_df, config):
    """
    Selects specific columns from a main DataFrame based on a lookup table
    and returns a new DataFrame with only the specified columns.

    Parameters
    ----------
    df_temp : pd.DataFrame
        The main DataFrame containing all data.
    select_variables_lookup : str
        Path to the CSV file containing the lookup information.
    config : dict
        A dictionary containing user configuration settings, including the path to save the output file or QA.
    
    Returns
    -------
    pd.DataFrame 
        A new DataFrame with only the specified columns.
    """

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
    # Rename the columns based on lookup table (V codes)
    filtered_df = df_temp[valid_columns].copy().rename(columns=new_code)

    # Keep the first column (area codes) in place and reorder the remaining columns
    first_column = filtered_df.columns[0]
    remaining_columns = filtered_df.columns[1:]    

    # Combine the first column (area codes) with the reordered remaining columns
    ordered_columns = [first_column] +  sorted(remaining_columns)
    filtered_df = filtered_df[ordered_columns]

    # Ensure QA directory exists
    os.makedirs(os.path.dirname(config["qa_folder_path"]), exist_ok=True)

    # Save to data QA folder
    output_file_path = config["qa_folder_path"] + "select_variables_output.csv"
    filtered_df.to_csv(output_file_path, index=False)

    return filtered_df

# Order the remaining columns based on the numeric value following 'v'
def extract_numeric_value(col_name):
    match = re.search(r'v(\d+)', col_name)
    # Default to infinity if no match
    return int(match.group(1)) if match else float('inf')  




