# This script creates a metadata for Scotland's Local Authority Districts (LAD) tables.
# It cleans/preprocesses the tables to a consistent format
# This script has been ran on a sample of tables; needs to be ran on all of the (normal) tables
# note that the functions are hard coded to our scotland tables

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
input_directory = 'D:/Repos/Area_Classificaiton_data/Percentages' 
# LAD code and names table
CA_lookup_file_path = "D:/Repos/Area_Classificaiton_data/Local_Authority_Districts_2022_Names_and_Codes_UK.csv"  


#### NEED TO ACCOUNT FOR THE UV101b and UV103 and population density and migrant indictor in this script ###
#### make use of functions: reformat_uv101b and reformat_uv103 in reformat_Scot_tables_functions.py ####
### CHECK the outputs of the two functions above; at what point do they feed into this script? ####
### migrant indicator and population density need functions; not yet created ####
### Tables UV606 and UV604 are formatted slightly different, with an extra line at the top - need to account for these


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
# Debug: Print the metadata list to verify its structure
print("Metadata extracted from files:")
print(metadata)

# call in the function to replace council area names with their codes using the lookup file
replace_ca19_names_with_codes(input_directory, CA_lookup_file_path)

# call in the function to remove rows with metadata/no data (first 10 and bottom 3 rows)
remove_rows(input_directory)

# call in the function to replace variable names with their codes
# 'variable_names_ids' is a list of variable_names and variable_ids variables
variable_names_ids = replace_variable_names_with_codes(input_directory)




# add to metadata table
# Iterate over the metadata dict and variable_names_ids list and add to the metadata table

for (meta, (variable_names, variable_ids)) in zip(metadata, variable_names_ids):
    # Extract table_id, table_name, and unit from the metadata dictionary
    table_id = meta.get("table_id", "")
    table_name = meta.get("table_name", "")
    unit = meta.get("unit", "")

    print(f"Table ID: {table_id}, Table Name: {table_name}")
    print(f"Variable Names: {variable_names}, Variable IDs: {variable_ids}")

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
                    "Table_ID": table_id,
                    "Table_Name": table_name,
                    "Unit": unit,
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
