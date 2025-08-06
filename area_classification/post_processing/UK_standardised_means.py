# UK standardised mean
# THIS COULD BE BROKEN DOWN BETTER, PERHAPS ADDING THE PERCENTAGES COULD BE DONE IN THE EARLIER SCRIPT
# WHERE THE TABLE IS CREATED, AND THEN REMOVED FROMT THIS ONE?

import pandas as pd
import os

from utilities.load_config import load_config

def create_UK_means(config):
    """
    Processes a CSV file by removing specific columns, calculating totals, 
    percentages, and filtering rows and columns based on conditions.

    Parameters:
        input_file (str): Path to the input CSV file.
        config (dict): Configuration dictionary containing the filepath and name to the cluster data
    """
    # Load the CSV file into a DataFrame
    config = load_config('area_classification/config.yaml')
    input_file = os.path.join(config["qa_folder_path"], "select_raw_totals.csv")
    raw_totals_df = pd.read_csv(input_file)

    # Remove V12 (population density) and V33 (SIR) as these are already proportions by definition
    # DONT THINK WE NEED TO REMOVE THESE ANYMORE?
    columns_to_remove = ['V12', 'V33']
    df = raw_totals_df.drop(columns=columns_to_remove, errors='ignore')

    # Add columns for the percentages of each V code
    v_columns = [col for col in df.columns if col.startswith('v') and not col.endswith('_total')]

    # Dictionary to store new columns
    new_columns = {}

    # Calculate percentages for columns based on V code and V_totals
    for column in v_columns:
        total_column = f"{column}_total"  # Find the corresponding total column
        if total_column in df.columns:  # Ensure the total column exists
            # Calculate the percentage and store it in the dictionary
            percentage_column = f"{column}_percentage"
            new_columns[percentage_column] = (df[column] / df[total_column]) * 100

    # Add all new columns to the DataFrame
    df = pd.concat([df, pd.DataFrame(new_columns)], axis=1)

    # Sort the columns alphabetically excluding the first column (area code)
    first_column = df.columns[0]
    sorted_columns = sorted(df.columns[1:])
    df = df[[first_column] + sorted_columns]

    percentages_output_file = (os.path.join(config["output_directory"], "percentages_select_raw_totals.csv"))
    # # Save the updated DataFrame back to a CSV file
    df.to_csv(percentages_output_file, index=False)

    # Calculate the standardised mean for each column
    standardised_means = {}
    for column in df.columns[1:]:
        mean = df[column].mean()
        std_dev = df[column].std()
        standardised_values = (df[column] - mean) / std_dev
        standardised_means[column] = standardised_values.mean()

    # Append the standardised means as a new row
    standardised_means_row = pd.DataFrame([standardised_means], index=["Standardised Mean"])
    df_with_standardised_mean = pd.concat([df, standardised_means_row], axis=0)

    # Set the value in the first column of the new row to "Standardised_mean"
    df_with_standardised_mean.iloc[-1, 0] = "Standardised_mean"

    # Creating the devolved countries standardised means
    # Exclude rows where the first column ends with '_total'
    filtered_df = df_with_standardised_mean[~df_with_standardised_mean.iloc[:, 0].str.endswith('_total')]

    # Calculate the standardised mean for each column (excluding the first column)
    overall_standardised_means = {}
    for column in filtered_df.columns[1:]:
        mean = filtered_df[column].mean()
        std_dev = filtered_df[column].std()
        standardised_values = (filtered_df[column] - mean) / std_dev
        overall_standardised_means[column] = standardised_values.mean()

    # Add a label for the overall standardised mean row
    overall_standardised_means[filtered_df.columns[0]] = "Overall_UK_standardised_mean"

    # Append the overall standardised mean as a new row
    UK_standardised_means_df = pd.DataFrame([overall_standardised_means])

    # Iterate over the prefixes (E, S, N, W)
    for prefix, label in [('E', 'E_standardised_mean'), ('S', 'S_standardised_mean'), ('N', 'N_standardised_mean'), ('W', 'W_standardised_mean')]:
        # Filter rows where the first column starts with the prefix
        filtered_rows = df_with_standardised_mean[df_with_standardised_mean.iloc[:, 0].str.startswith(prefix)]
        
        # Calculate the standardised mean for each column (excluding the first column)
        standardised_means = {}
        for column in df_with_standardised_mean.columns[1:]:
            mean = filtered_rows[column].mean()
            std_dev = filtered_rows[column].std()
            standardised_values = (filtered_rows[column] - mean) / std_dev
            standardised_means[column] = standardised_values.mean()
        
        # Add the prefix label to the first column
        standardised_means[df_with_standardised_mean.columns[0]] = label
        
        # Append the standardised means as a new row
        UK_standardised_means_df = pd.concat([UK_standardised_means_df, pd.DataFrame([standardised_means])], ignore_index=True)

    # Append the standardised means DataFrame to the original DataFrame
    UK_standardised_means_df = pd.concat([df, UK_standardised_means_df], ignore_index=True)

    # Filter and save rows where the first column ends with '_mean'
    UK_standardised_mean_summary = UK_standardised_means_df[UK_standardised_means_df.iloc[:, 0].str.endswith('_mean')]
    UK_standardised_mean_output_file = (os.path.join(config["output_directory"], "UK_standardised_means.csv"))
    UK_standardised_mean_summary.to_csv(UK_standardised_mean_output_file, index=False)

    return UK_standardised_mean_summary


# Run the function if the script is executed directly
if __name__ == "__main__":
    from utilities.load_config import load_config

    # Load configuration
    config = load_config('area_classification/config.yaml')

    # Call the main function
    create_UK_means(config)