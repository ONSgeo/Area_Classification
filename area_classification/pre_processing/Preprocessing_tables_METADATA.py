# Top section removes unneeded lines of cotnent from CSVs, and puts CA19 instead of "Council Area 2019" 
# the top section doesnt work for any tables that are further categorized e.g., uv101b or uv102b. the top metadata rows and bottom 3 rows may have to manually removed from these.
# manually rename uv101b.csv to row_removal_UV101b.csv in the input directory before running this script

#Spreadsheets downloaded from table builder
#pip install os
import os
import pandas as pd
import numpy as np
from reformat_Scot_tables_functions import reformat_uv101b, reformat_uv103 

# Paths to the folder and metadata file
# input_directory = 'C:\\Users\\goodme\\Office for National Statistics\\Geospatial - LAD_data_downloaded\\Scotland_LA\\Percentages'  # Replace with your folder path
input_directory = 'D:/Output_Area_Classification/Scotland_downloaded/test_sample_percentages/metadata_creation_samples' 


# Loop through all files in the folder
for file_name in os.listdir(input_directory):
    # Skip files containing "UV101b" or "UV102b" because they require different formatting to remove rows and headers
    if 'UV101b' in file_name or 'UV102b' in file_name or 'UV204' in file_name:
        print(f"Skipping file: {file_name}")
        continue


    # Process only CSV files
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_directory, file_name)
        
        # Check if the file name contains "row_removal"
        if 'row_removal' in file_name:
            print(f"{file_name} not had rows removed")
            continue
        
        # Determine the number of rows to skip
        if 'UV' in file_name:
            skip_rows = 11  # Skip the first 11 rows for UV tables
        else:
            # This should be for migrant indicator and population density
            skip_rows = 10

        try:
            # Read the CSV file, skipping the determined number of rows
            # Use on_bad_lines='skip' to handle rows with inconsistent fields
            df = pd.read_csv(file_path, skiprows=skip_rows, on_bad_lines='warn', header=None)
            
            # Remove the last 3 rows
            df = df.iloc[:-3, :]

            # Replace any cell in the DataFrame that says "Council Area 2019" with "CA19"
            df.replace("Council Area 2019", "CA19", inplace=True)
            

            # Remove value from cell A1 
            df.iloc[0, 0] = ""  # Remove the value in A1 (table name)

            # Move the values from row 1 (index 0) in columns B onward (index 1 onward) to row 2 (index 1)
            df.iloc[1, 1:] = df.iloc[0, 1:]

            # Clear the original values in row 1 (index 0) from column B onward (index 1 onward)
            df.iloc[0, 1:] = np.nan

            # Drop the first (empty) row and reset the index
            df = df.drop(index=0).reset_index(drop=True)

            # Save the modified DataFrame to a new CSV file
            cleaned_file_path = os.path.join(input_directory, 'row_removal_' + file_name)
            df.to_csv(cleaned_file_path, index=False, header=False)
        
        except pd.errors.ParserError as e:
            print(f"Error processing {file_name}: {e}")


        print(f"Processed: {file_name} -> Saved as: removed_metadata_rows_{file_name}")
        


# run the functions to reformat these tables to be consistent with the others
reformat_uv103(input_directory)
reformat_uv101b(input_directory)




# PART 2

import os
input_directory = 'D:/Output_Area_Classification/Scotland_downloaded/test_sample_percentages/metadata_creation_samples/raw_data_sample' 

# create metadata table
meta_data_table = pd.DataFrame(
    columns=[
        "Table_Name",
        "Table_ID",
        "Variable_Name",
        "Type",
    ]
)


# Loop through all files in the folder
for file_name in os.listdir(input_directory):
    # Skip files that do not start with 'row_removal_' 
    #if not file_name.startswith('row_removal_'):
        #continue 

    # Construct the full file path
    file_path = os.path.join(input_directory, file_name)
    
    print(f"Processing file: {file_name}")
    
    # Open the file and read its lines
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list

    table_includes = lines[3].strip()

    # find the unit of measure
    # if table includes had  'people' in it, Unit of measure is Person
    # if table includes had  'households' in it, Unit of measure is Household
    # if table has both, Unit of measure is Person
    unit = "-"
    if "Household Reference Persons " in table_includes:
        unit = "Household Reference Person"
    elif "people" in table_includes or "Persons" in table_includes:
        unit = "Person"
    elif "household" in table_includes and "people" not in table_includes:
        unit = "Household"
    else:
        print(f"Unit of measure not found for {table_id}, table includes: {table_includes}")

    # Extract the table name (the part after the second underscore)
    table_name = table_name = os.path.splitext(file_name)[0]
    parts = file_name.split('_')  # Split the file name by underscores
    table_id = parts[2].split('.')[0]  # Extract the part after the second underscore and remove the file extension
    print(f"Extracted table name: {table_id}")
    # Create new column names with zero padding
    variable_names = df.columns
    # create a list of new column names
    # combine the t_id prefix adding a 4 digit zero padded number to the end 
    # so 1 becomes 0001 for example 
    var_ids = [f"{table_id}{str(i).zfill(4)}" for i in range(1, len(variable_names) + 1)]
    # replace the exsiting column names of the df with the newly generated column names stored in var_ids
    df.columns = var_ids
    # save to new csv and parquet
    df.to_csv(f"{input_directory}/{table_id}.csv")
    # add to metadata table
    meta_data_table = pd.concat(
        [
            meta_data_table,
            pd.DataFrame(
                {
                    "Variable_Name": variable_names,
                    "Variable_ID": var_ids,
                    "Table_ID": [table_id] * len(variable_names),
                    "Table_Name": [table_name] * len(variable_names),
                    "Unit": [unit] * len(variable_names),
                }
            ),
        ]
    )

# save metadata table
# create full name column
meta_data_table["Full_Name"] = (
    meta_data_table["Table_Name"] + " - " + meta_data_table["Variable_Name"]
)
meta_data_table = meta_data_table[["Variable_Name", "Variable_ID", "Table_ID", "Table_Name", "Type", "Unit", "Full_Name"]]
#manually set Type to 'Count' for all tables
meta_data_table['Type'] = 'Count'
meta_data_table.to_csv(f"{input_directory}/Table_Metadata_test.csv", index=False)
