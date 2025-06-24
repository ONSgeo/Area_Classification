import pandas as pd
import re  # Import the re module for regular expressions

def select_columns_from_lookup(main_df, select_variables_lookup, output_file):
    """
    Selects specific columns from a main DataFrame based on a lookup table
    and returns a new DataFrame with only the specified columns.

    Parameters:
    - main_df (pd.DataFrame): The main DataFrame containing all data.
    - select_variables_lookup (str): Path to the CSV file containing the lookup information.
    - output_file (str): Path to save the resulting DataFrame as a CSV file.

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
        if col not in main_df.columns:
            print(f"Warning: Column '{col}' is missing in the main DataFrame.")
        else:
            valid_columns.append(col)
    
    # Ensure the first column of main_df is included as the first column
    first_column = main_df.columns[0]
    if first_column not in valid_columns:
        valid_columns.insert(0, first_column)
    
    print(f"Columns to be selected: {valid_columns}")
    
    # Filter the main DataFrame to include only the valid columns
    filtered_df = main_df[valid_columns].copy()

    # Rename the columns based on the lookup table
    filtered_df.rename(columns=new_code, inplace=True)

    # Keep the first column in place and reorder the remaining columns
    first_column = filtered_df.columns[0]
    remaining_columns = filtered_df.columns[1:]

    # Order the remaining columns based on the numeric value following 'v'
    def extract_numeric_value(col_name):
        match = re.search(r'v(\d+)', col_name)
        return int(match.group(1)) if match else float('inf')  # Default to infinity if no match

    ordered_remaining_columns = sorted(remaining_columns, key=extract_numeric_value)

    # Combine the first column with the reordered remaining columns
    ordered_columns = [first_column] + ordered_remaining_columns
    filtered_df = filtered_df[ordered_columns]

    # Save the resulting DataFrame as a CSV file
    filtered_df.to_csv(output_file, index=False)

    return filtered_df