# This script creates a metadata for Scotland's Local Authority Districts (LAD) tables.
# It cleans/preprocesses the tables to a consistent format


import os
import pandas as pd
import numpy as np
from reformat_Scot_tables_functions import (
    extract_metadata_from_files, 
    replace_variable_names_with_codes, 
    replace_ca19_names_with_codes, 
    remove_rows
)

# path to input directory containing the csv files to be processed
input_directory = 'D:/Output_Area_Classification/Scotland_downloaded/test_sample_percentages/metadata_creation_samples/raw_data_sample' 
# LAD code and names table
lookup_file_path = "D:/Output_Area_Classification/Local_Authority_Districts_2022_Names_and_Codes_UK.csv"  


# create metadata table
meta_data_table = pd.DataFrame(
        columns=[
        "Table_Name", 
        "Variable_Name",
        "Variable_id", 
        "Table_ID", 
        "Type", 
        "Unit", 
        "Full_Name"
        ]
)

# function to extract metadata from files into table. 
# 'metadata' is a list of table_name, table_id and unit variables
metadata = extract_metadata_from_files(input_directory)

# call in the function to replace council area names with their codes using the lookup file
replace_ca19_names_with_codes(input_directory, lookup_file_path)

# call in the function to remove rows with metadata/no data
remove_rows(input_directory)

# call in the function to replace variable names with their codes
# 'variable_names_ids' is a list of variable_names and variable_ids variables
variable_names_ids = replace_variable_names_with_codes(input_directory)



# add to metadata table
# Iterate over the metadata list and variable_names_ids list and add to the metadata table
for (table_id, table_name, unit), (variable_names, variable_ids) in zip(metadata, variable_names_ids):
    # Exclude 'CA19' from variable_names and adjust variable_ids accordingly
    if 'CA19' in variable_names:
        variable_names = [name for name in variable_names if name != 'CA19']

    meta_data_table = pd.concat(
        [
            meta_data_table,
            pd.DataFrame(
                {
                    "Variable_Name": variable_names,
                    "Variable_ID": variable_ids,
                    "Table_ID": [table_id] * len(variable_names),
                    "Table_Name": [table_name] * len(variable_names),
                    "Unit": [unit] * len(variable_names),
                }
            ) 
        ]
    )


# create full name column
meta_data_table["Full_Name"] = (
    meta_data_table["Table_Name"] + " - " + meta_data_table["Variable_Name"]
)
meta_data_table = meta_data_table[["Variable_Name", "Variable_ID", "Table_ID", "Table_Name", "Type", "Unit", "Full_Name"]]
#manually set Type to 'Percentage' for all tables
meta_data_table['Type'] = 'Percentage'
# Construct the output file path in the input_directory
output_file_path = os.path.join(input_directory, "scot_LA_table_metadata.csv")

# Save the metadata table to the specified path
meta_data_table.to_csv(output_file_path, index=False)
