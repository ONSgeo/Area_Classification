# UK standardised mean

import pandas as pd
import os

from utilities.load_config import load_config

def create_UK_means(config):
    """
    Processes a CSV file by removing specific columns, calculating totals, 
    percentages, and filtering rows and columns based on conditions.

    Args:
        input_file (str): Path to the input CSV file.
        config (dict): Configuration dictionary containing the filepath and name to the cluster data
    """
    # Load the CSV file into a DataFrame
    input_file = os.path.join(config["qa_folder_path"], "select_raw_totals.csv")
    raw_totals_df = pd.read_csv(input_file)

    # Remove V12 (population density) and V33 (SIR) as these are already proportions by definition
    columns_to_remove = ['V12', 'V33']
    standardised_means_df = raw_totals_df.drop(columns=columns_to_remove, errors='ignore')

    # Define the row names and corresponding first letter of the area codes
    conditions = {
        'EW_total': ['E', 'W'],  # Codes starting with 'E' or 'W'
        'NI_total': ['N'],      # Codes starting with 'NI'
        'Scot_total': ['S']     # Codes starting with 'UV'
    }

    # Calculate totals for each condition and append them
    total_rows = []
    first_column = standardised_means_df.columns[0]

    for row_name, prefixes in conditions.items():
        # Filter rows where the first column starts with any of the specified prefixes
        filtered_rows = standardised_means_df[standardised_means_df[first_column].str.startswith(tuple(prefixes), na=False)]
        
        # Sum the values for each column
        total_row = filtered_rows.sum(numeric_only=True)
        total_row[first_column] = row_name  # Set the value for the first column
        
        # Collect the total row for later concatenation
        total_rows.append(total_row)

    # Append all total rows to the DataFrame
    standardised_means_df = pd.concat([standardised_means_df, pd.DataFrame(total_rows)], ignore_index=True)

    v_columns = [col for col in standardised_means_df.columns if col.startswith('v') and not col.endswith('_total')]

    # Dictionary to store new columns
    new_columns = {}

    # Calculate percentages for columns based on V code and V_totals
    for column in v_columns:
        total_column = f"{column}_total"  # Find the corresponding total column
        if total_column in standardised_means_df.columns:  # Ensure the total column exists
            # Calculate the percentage and store it in the dictionary
            percentage_column = f"{column}_percentage"
            new_columns[percentage_column] = (standardised_means_df[column] / standardised_means_df[total_column]) * 100

    # Add all new columns to the DataFrame
    standardised_means_df = pd.concat([standardised_means_df, pd.DataFrame(new_columns)], axis=1)

    # Sort the columns alphabetically excluding the first column (area code)
    first_column = standardised_means_df.columns[0]
    sorted_columns = sorted(standardised_means_df.columns[1:])
    standardised_means_df = standardised_means_df[[first_column] + sorted_columns]

    # Keep the rows which are for totals (UK, EW, NI and Scot)
    rows_to_keep = standardised_means_df.iloc[:, 0].astype(str).str.contains('_total')
    standardised_means_df = standardised_means_df[rows_to_keep]

    # Retain the first column and the columns which are '_percentage'
    columns_to_keep = standardised_means_df.columns[1:][standardised_means_df.columns[1:].str.endswith('_percentage')]   
    standardised_means_df = standardised_means_df[[standardised_means_df.columns[0]] + list(columns_to_keep)]

    output_file = (os.path.join(config["output_directory"], "percentages_select_raw_totals.csv"))
    # Save the updated DataFrame back to a CSV file
    standardised_means_df.to_csv(output_file, index=False)

    return standardised_means_df


# Run the function if the script is executed directly
if __name__ == "__main__":
    config = load_config('area_classification/config.yaml')
    #input_file = os.path.join(config["qa_folder_path"], "select_raw_totals.csv")
    create_UK_means(config)