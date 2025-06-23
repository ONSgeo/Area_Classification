# Top section removes unneeded lines of content from CSVs, and puts CA19 instead of "Council Area 2019" 
# the top section doesnt work for any tables that are further categorized e.g., uv101b or uv102b. the top metadata rows and bottom 3 rows may have to manually removed from these.
#COMPARE THIS ONE WITH THE OTHER TABLUE BUILDER?!?!

#Spreadsheets downloaded from table builder
#pip install os
import os
import pandas as pd
import numpy as np
from reformat_Scot_tables_functions import reformat_uv101b, reformat_uv103, reformat_migrant_indicator

# Paths to the folder and metadata file
# input_directory = 'C:\\Users\\goodme\\Office for National Statistics\\Geospatial - LAD_data_downloaded\\Scotland_LA\\Percentages'  # Replace with your folder path
input_directory = 'D:/Repos/Area_Classification_data/Percentages' 
metadata_file = 'D:/Repos/Area_Classification_data/scot_legacy_oa_table_metadata.csv'



# Loop through all files in the folder
for file_name in os.listdir(input_directory):
    # Skip files containing "UV101b" or "UV102b" because they require different formatting to remove rows and headers
    if 'UV101b' in file_name or 'UV102b' in file_name:
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
            
            # See if the second row only has CA19 and empty cells
            if df.iloc[1, 1:].isna().all():
                # Remove the second row (index 1)
                df = df.drop(index=1)
                # Put CA19 in the top left cell
                df.at[0, df.columns[0]] = "CA19"

            # Save the modified DataFrame to a new CSV file
            cleaned_file_path = os.path.join(input_directory, 'row_removal_' + file_name)
            df.to_csv(cleaned_file_path, index=False, header=False)
        
        except pd.errors.ParserError as e:
            print(f"Error processing {file_name}: {e}")


        print(f"Processed: {file_name} -> Saved as: removed_metadata_rows_{file_name}")
        

# run the functions to reformat specific tables to be consistent with the others
reformat_uv103(input_directory)
reformat_migrant_indicator(input_directory)
reformat_uv101b(input_directory)


### SECTION 2 ###
# How do we swap out the variable names with variable codes based on the metadata file

# Read the metadata file into a DataFrame
metadata_df = pd.read_csv(metadata_file)

# Loop through all files in the folder
for file_name in os.listdir(input_directory):
    # Process only CSV files starting with 'row_removal'
    if file_name.startswith('row_removal') and file_name.endswith('.csv'):
        file_path = os.path.join(input_directory, file_name)

        # Read the CSV file
        csv_df = pd.read_csv(file_path, header=0)  # Assuming the first row contains headers

        # Iterate through the column headers of the CSV (from column B onwards)
        for col_index, col_name in enumerate(csv_df.columns[1:], start=1):  # Skip the first column (A)
            # Check if the column name exists in the metadata table (exact match)
            match_row = metadata_df[metadata_df.iloc[:, 0] == col_name]  # Exact match in the first column of metadata
            if not match_row.empty:
                # Replace the column name with the value in the column to the right
                new_col_name = match_row.iloc[0, 1]  # Get the value in the second column of the matched row
                csv_df.rename(columns={col_name: new_col_name}, inplace=True)

        # Save the updated CSV file
        updated_file_path = os.path.join(input_directory, f"codes_{file_name}")
        csv_df.to_csv(updated_file_path, index=False)
        print(f"Updated file saved: {updated_file_path}")