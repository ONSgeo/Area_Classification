import os
import pandas as pd

def select_variables(input_dir, base_file, config_file, join_column, join_type):
    """
    This function iterates through all CSV files in a directory, reads column names to add
    from a configuration CSV file, and performs multiple join operations with an existing base CSV file.

    Parameters:
    - input_dir (str): The directory containing the input CSV files to join.
    - base_file (str): The path to the base CSV file to join with.
    - config_file (str): The path to the configuration CSV file containing the columns to add.
    - join_column (str): The column name to join on.
    - join_type (str): The type of join to perform (default is 'left'). Options: 'left', 'inner', 'outer', 'right'.
    """
    # Load configuration and base file
    selected_variables = pd.read_csv(config_file)['selected_variables'].dropna().tolist()
    base_df = pd.read_csv(base_file)

    # Process each CSV file in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_dir, file_name)
            current_df = pd.read_csv(file_path)
            selected_columns = [join_column] + [col for col in selected_variables if col in current_df.columns]
            base_df = base_df.merge(current_df[selected_columns], on=join_column, how=join_type)
            print(f"Joined {file_name} on column '{join_column}' and added columns {selected_columns}.")

    # Save the updated base file
    base_df.to_csv(base_file, index=False)
    print(f"Updated base file: {base_file}")

# Example usage
input_dir = "D:/Output_Area_Classification/EW_csv_samples"
base_file = "D:/Repos/Area_Classification/Area_Classification_Project/area_classification/pre_processing/base_file.csv"
config_file = "D:/Repos/Area_Classification/Area_Classification_Project/area_classification/pre_processing/config_file.csv" 
join_column = "LTLA"  
join_type = "left"  

select_variables(input_dir, base_file, config_file, join_column, join_type)