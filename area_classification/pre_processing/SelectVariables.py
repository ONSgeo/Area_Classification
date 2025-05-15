import os
import pandas as pd

def select_variables(input_dir, base_file, selected_variables, new_names, join_column, join_type):
    """
    This function iterates through all CSV files in a directory and performs multiple join operations
    with an existing base CSV file using specified columns.

    Parameters:
    - input_dir (str): The directory containing the input CSV files to join.
    - base_file (str): The path to the base CSV file to join with.
    - selected_variables (list): A list of column names to add from the input files.
    - join_column (str): The column name to join on.
    - join_type (str): The type of join to perform. Options: 'left', 'inner', 'outer', 'right'.
    """
    # Load the base file
    base_df = pd.read_csv(base_file)

    # Process each CSV file in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_dir, file_name)
            current_df = pd.read_csv(file_path)
            # Select only the required columns
            selected_columns = [join_column] + [col for col in selected_variables if col in current_df.columns]
            
            # Perform the join if there are columns to add
            if len(selected_columns) > 1:  # Ensure at least one column (besides join_column) is added
                base_df = base_df.merge(current_df[selected_columns], on=join_column, how=join_type)
                print(f"Columns added from file: {file_name}")

    # Rename columns in the base file based on the new_names dictionary
    base_df.rename(columns=new_names, inplace=True)

    # Save the updated base file
    base_df.to_csv(base_file, index=False)
    print(f"Updated base file: {base_file}")

# Parameters
input_dir = "D:/Output_Area_Classification/EW_csv_samples"
base_file = "D:/Repos/Area_Classification/Area_Classification_Project/area_classification/pre_processing/base_file.csv"
config_file = "D:/Repos/Area_Classification/Area_Classification_Project/area_classification/pre_processing/config_file.csv"
join_column = "LTLA"
join_type = "left"

# Load columns and their new names from the configuration file
config_df = pd.read_csv(config_file)
selected_variables = config_df['selected_variables'].dropna().tolist()
new_names = dict(zip(config_df['selected_variables'], config_df['new_name']))

# Call the function
select_variables(input_dir, base_file, selected_variables, new_names, join_column, join_type)