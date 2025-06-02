#Top section removes unneeded lines of cotnent from CSVs, and puts CA19 in and tells you how many columns
#Second section tells you how many variables assoicated to each table ID and prints them (UV)
#Current issue - the columns are reporting to have 2 more columns in the CSV than in the varaible list, however only really one more in the actual CSV (for LAD code)
#Think the difference in the lengths is preventing puttting the varables into the sheets?
#Is migrant indicator missing from the percentages folder?

#Spreadsheets downloaded from table builder
#pip install os
import os
import pandas as pd
from reformat_Scot_tables_functions import reformat_uv101b, reformat_uv103 

# Paths to the folder and metadata file
#folder_path = 'C:\\Users\\goodme\\Office for National Statistics\\Geospatial - LAD_data_downloaded\\Scotland_LA\\Percentages'  # Replace with your folder path
folder_path = "D:/Output_Area_Classification/Scotland_downloaded/test_sample_percentages/general_reformat_sample/"
metadata_file = 'Downloading_data/Scotland_Census_2022_OA-download/output_data/Table_Metadata.csv'

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
     # Process only CSV files
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file name contains "UV101b" or "UV103"
        if 'UV101b' in file_name or 'UV103' in file_name or 'UV204' in file_name:
            print("Use Tyde's code")
            #This is where Tyde's functions could be called
            continue

        # Check if the file name contains "row_removal"
        if 'row_removal' in file_name:
            print(f"{file_name} not had rows removed")
            continue
        
        # Determine the number of rows to skip
        if 'UV' in file_name:
            skip_rows = 11

        else:
            #This should be for migrant indicator and population density
            skip_rows = 10

        
        # Read the CSV file, skipping the determined number of rows
        df = pd.read_csv(file_path, skiprows=skip_rows)
        
        # Remove the last 3 rows
        df = df.iloc[:-3, :]

        #Printing some info to support with trouble shooting - can be removed when resolved.
        # Get the number of columns
        num_columns = df.shape[1]
        # Print the number of columns
        print(f"The number of columns in {file_name} is: {num_columns}") 
        # Get the first row
        first_row = df.iloc[0]
        # Count the number of populated (non-empty) cells in the first row
        populated_cells = first_row.notna().sum()
        # Print the number of populated cells
        print(f"The number of populated cells in the first row is: {populated_cells}")
        
        # Rename "Council Area 2019" in first row to "CA19"
        if "Council Area 2019" in df.iloc[:, 0].values:
            df.iloc[:, 0] = df.iloc[:, 0].replace("Council Area 2019", "CA19")  # Replace "Council Area 2019" with "CA19"
        else:
            print(f"Unknown geography level in file: {file_name}")
        
        # Save the modified DataFrame to a new CSV file
        cleaned_file_path = os.path.join(folder_path, 'row_removal_' + file_name)
        df.to_csv(cleaned_file_path, index=False, header=False)

        print(f"Processed: {file_name} -> Saved as: removed_metadata_rows_{file_name}")


#ADD UV CODES TO THE COLUMN HEADERS
# Load the metadata file
metadata_df = pd.read_csv(metadata_file)

# Ensure the 'Table_ID' column exists in the metadata table
if "Table_ID" not in metadata_df.columns:
    raise ValueError("The metadata table does not contain a 'Table_ID' column.")

# Get the list of file names in the folder
file_names = os.listdir(folder_path)

# Loop through the file names and check if they exist in the 'Table_ID' column
for file_name in file_names:
    # Remove the file extension to match the Table_ID
    table_id = os.path.splitext(file_name)[0]
    
    # Skip files with names 'UV101b' or 'UV103' - doesn't need to be skipped if Tyde's stuff added 
    if table_id in ["UV101b", "UV103"]:
        print(f"Skipping file: {file_name}")
        continue
    
    # Full path to the file
    file_path = os.path.join(folder_path, file_name)
    
    # Check if the file name exists in the Table_ID column
    if table_id in metadata_df["Table_ID"].values:
        print(f"File '{file_name}' exists in the Table_ID column.")
        
        #Printing some info to support with trouble shooting - can be removed when resolved.
        # Get the corresponding Variable_ID values for the Table_ID
        variable_ids = metadata_df.loc[metadata_df["Table_ID"] == table_id, "Variable_ID"].values
        # Print the number of Variable_IDs and the Variable_IDs themselves
        print(f"Number of Variable_IDs for '{table_id}': {len(variable_ids)}")
        print(f"Variable_IDs for '{table_id}': {list(variable_ids)}")
    else:
        print(f"File '{file_name}' does NOT exist in the Table_ID column.")

    #ONCE UV VALUES THEY COULD THEN BE SAVED AS (folder_path, 'cleaned_' + file_name)