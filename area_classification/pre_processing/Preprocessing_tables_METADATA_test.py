
import os
import pandas as pd
from io import BytesIO
import numpy as np

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


    try:
        # Combine the lines into a single string, encode it to bytes, and use BytesIO
        csv_data = BytesIO("".join(lines).encode('utf-8'))

        # Read the CSV data into a DataFrame
        df = pd.read_csv(
            csv_data,
            #skiprows=skip_rows,  # Skip the specified number of rows
            on_bad_lines='skip',  # Skip problematic lines
            header=None           # No header row
        )
    except pd.errors.ParserError as e:
        print(f"Error processing {file_name}: {e}")

    table_includes = lines[3].strip()  # Get the third line of the file, which contains the table includes   

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

    # Extract the table id
    table_id = os.path.splitext(file_name)[0]
    # extract the table name
    # Extract the text from row 4 (index 3)
    try:
        row_text = lines[3].strip()  # Get the text on row 4 (index 3) and strip whitespace

        # Extract the portion after the second '-' and before the last 'All'
        after_second_dash = row_text.split('-', 2)[2]
        table_name = after_second_dash.rsplit('All', 1)[0].strip()

        print(f"Extracted Table Name: {table_name}")
    except (IndexError, ValueError):
        print("Error: Unable to extract table name from the given text.")
        print(f"Extracted table name: {table_id}")


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
        #cleaned_file_path = os.path.join(input_directory, 'row_removal_' + file_name)
        #df.to_csv(cleaned_file_path, index=False, header=False)
    
    except pd.errors.ParserError as e:
            print(f"Error processing {file_name}: {e}")
    #print(f"Processed: {file_name} -> Saved as: removed_metadata_rows_{file_name}")

    # Create new column names with zero padding
    variable_names = df.columns
    # create a list of new column names
    # combine the t_id prefix adding a 4 digit zero padded number to the end 
    # so 1 becomes 0001 for example 
    var_ids = [f"{table_id}{str(i).zfill(4)}" for i in range(1, len(variable_names) + 1)]
    # replace the exsiting column names of the df with the newly generated column names stored in var_ids
    df.columns = var_ids
    # save to new csv
    df.to_csv(f"{input_directory}/{table_id}_codes.csv")
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
