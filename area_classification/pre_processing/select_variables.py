import pandas as pd
import re  
import os
import logging

logger = logging.getLogger(__name__)

def select_variables(df_temp, lookup_df, config):
    """
    Selects specific columns from a main DataFrame based on a lookup table
    and returns a new DataFrame with only the specified columns. It also takes
    the variable_codes (which start either TS, ni or UV, based on the country) 
    and converts these all into new_codes which all start 'v'.

    Parameters
    ----------
    df_temp : pd.DataFrame
        The temp DataFrame containing all data.
    lookup_df : str
        Path to the CSV file containing the variable_codes and new_codes to 
        select columns and convert all codes to new 'v' codes.
    config : dict
        A configuration dictionary containing the QA file paths.
    
    Returns
    -------
    pd.DataFrame 
        A new DataFrame with only the specified columns, with area codes in the first column followed by
        raw count values for each vairable from v1 to v60.
        
    """

    # Extract the columns to select and their new names
    selected_columns = lookup_df['variable_code'].dropna().tolist()
    new_code = dict(zip(lookup_df['variable_code'], lookup_df['new_code']))
    
    # Check for missing columns and log them
    valid_columns = []
    for col in selected_columns:
        if col not in df_temp.columns:
            logger.warning(f"Warning: Column '{col}' is missing in the temp DataFrame.")
        else:
            valid_columns.append(col)
    
    # Ensure the first column (area codes) of df_temp is included as the first column
    first_column = df_temp.columns[0]
    if first_column not in valid_columns:
        valid_columns.insert(0, first_column)
    
    logger.info(f"Columns to be selected: {valid_columns}")
    
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

if __name__ == "__main__":
    # Example usage
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    lookup_df = pd.read_csv(config['select_variables_lookup'])
    df_temp = pd.read_csv(os.path.join(config['input_data_directory'], 'CA19_concat.csv'))
    
    select_variables(df_temp, lookup_df, config)