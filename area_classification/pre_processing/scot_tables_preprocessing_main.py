# This script creates a metadata for Scotland's Local Authority Districts (LAD) tables.
# It cleans/preprocesses the tables to a consistent format
# certain tables have their own re-formatting functions 
# note that the functions are hard coded to our scotland tables

import os
import pandas as pd
import numpy as np
from scot_tables_preprocessing_functions import (
    extract_metadata_from_files, 
    replace_ca19_names_with_codes, 
    remove_rows,
    reformat_uv101b,
    reformat_uv103,
    reformat_migrant_indicator,
    reformat_pop_density,
    replace_variable_names_with_codes, 
)

# path to input directory containing the csv files to be processed
input_directory = input_directory = "D:/Output_Area_Classification/Scotland_downloaded/test_sample_percentages/metadata_creation_samples/All_tables_test2" 
# LAD code and names table
CA_lookup_file_path = "D:/Output_Area_Classification/Local_Authority_Districts_2022_Names_and_Codes_UK.csv"  


#### NEED TO ACCOUNT FOR population density in this script ###
### population density need functions; not yet created ####


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
replace_ca19_names_with_codes(input_directory, CA_lookup_file_path)

# call in the function to remove rows with metadata/no data (first 10 and bottom 3 rows)
remove_rows(input_directory)

reformat_uv101b(input_directory, CA_lookup_file_path)  # reformat the UV101b table
reformat_uv103(input_directory, CA_lookup_file_path) # reformat the UV103 table
reformat_migrant_indicator(input_directory, CA_lookup_file_path) # reformat the migrant indicator table
reformat_pop_density(input_directory) # reformat the population density table

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
