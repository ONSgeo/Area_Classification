import pandas as pd
import os
import numpy as np
import csv

# these functions are set up to reformat the Scotland tables to be consistent with Eng/Wales/NI 
# extract metadata from them to create a metadata table for Scotland


# Function to reformat the UV101b CSV file
def reformat_uv101b(input_directory, CA_lookup_file_path):
    """
    Function to reformat the UV101b CSV file so it has rows removed and CA codes instead of names.
    
    Args:
        input_directory (str): Path to the directory containing the input CSV files.
        CA_lookup_file_path (str): Path to the lookup file containing LAD codes and names.
    """
    # Look for UV101b.csv in the directory
    file_path = os.path.join(input_directory, "UV101b.csv")
    if not os.path.exists(file_path):
        print("No file named UV101b.csv found in the directory.")
        return

    # Load the CSV file and skip the first 12 rows
    df = pd.read_csv(file_path, skiprows=12, header=None, names=['A', 'B', 'C', 'D', 'E', 'F'])
    
    # Remove the empty column (F)
    df = df.dropna(axis=1, how='all')

    # List to store results
    results = []

    # Iterate through rows to extract relevant data
    for index, row in df.iterrows():
        if str(row['A']).strip().lower() == 'sex':
            # Get the council area name (two rows above the 'sex' row)
            council_area = df.iloc[index - 2]['A'] if index - 2 >= 0 else None

            # Get the 'All people' row (next row after 'sex')
            all_people_row = df.iloc[index + 1] if index + 1 < len(df) else None
            if all_people_row is not None and str(all_people_row['A']).strip().lower() == 'all people':
                # Extract the values from columns C, D, and E
                all_people_value = all_people_row['C']
                household_value = all_people_row['D']
                communal_value = all_people_row['E']
                
                # Append the extracted values to the results
                results.append({
                    'CA19': council_area,
                    'All people': all_people_value,
                    'Lives in a household': household_value,
                    'Lives in a communal establishment': communal_value
                })

    # Convert results to a DataFrame
    if results:
        output_df = pd.DataFrame(results)
        # Add Clackmannanshire to the first row, first column
        output_df.iloc[0, 0] = "Clackmannanshire"

        # Load the LAD codes and names lookup file
        lookup_df = pd.read_csv(CA_lookup_file_path)
        lookup_dict = dict(zip(lookup_df['LAD22NM'].str.lower().str.strip(), lookup_df['LAD22CD']))

        # Replace council area names with LAD codes
        output_df['CA19'] = output_df['CA19'].str.strip().str.lower().map(lookup_dict).fillna(output_df['CA19'])

        # Save the final DataFrame to a new CSV file
        output_file_path = os.path.join(input_directory, "reformat_UV101b.csv")
        output_df.to_csv(output_file_path, index=False)
        print("Data formatting complete. Results saved to:", output_file_path)
    else:
        print("No relevant data found in UV101b.csv.")




def reformat_uv103(input_directory, CA_lookup_file_path):
    """
    Function to reformat the UV103 CSV file so it has rows removed and CA codes instead of names.

    Args:
        input_directory (str): Path to the directory containing the input CSV file.
        CA_lookup_file_path (str): Path to the lookup file containing LAD codes and names.
    """
    # Look for UV103.csv in the directory
    file_path = os.path.join(input_directory, "UV103.csv")
    if not os.path.exists(file_path):
        print("No file named UV103.csv found in the directory.")
        return

    # Load the CSV file
    df = pd.read_csv(file_path, skiprows=11, header=None)

    # Extract headers for columns B to CY (row 2 in the original file)
    headers = ["Council Area 2019"] + df.iloc[1, 1:].tolist()

    # Extract council area names and corresponding data
    reformatted_data = []
    for i in range(0, len(df), 6):  # Step by 6 rows
        council_area = df.iloc[i, 0] if pd.notna(df.iloc[i, 0]) else None
        data_row_index = i + 3  # Data row is 2 rows below the header row
        if data_row_index < len(df):
            data_row = df.iloc[data_row_index, 1:].tolist()
            if any(pd.notna(value) for value in data_row):  # Skip rows where all data columns are blank
                reformatted_data.append([council_area] + data_row)

    # Create the new DataFrame
    reformatted_df = pd.DataFrame(reformatted_data, columns=headers)

    # Remove rows where all columns except column A are blank
    reformatted_df = reformatted_df.dropna(how='all', subset=headers[1:])

    # Load the LAD codes and names lookup file
    lookup_df = pd.read_csv(CA_lookup_file_path)
    lookup_dict = dict(zip(lookup_df['LAD22NM'].str.lower().str.strip(), lookup_df['LAD22CD']))

    # Replace council area names with LAD codes
    reformatted_df['Council Area 2019'] = (
        reformatted_df['Council Area 2019']
        .str.strip()
        .str.lower()
        .map(lookup_dict)
        .fillna(reformatted_df['Council Area 2019'])
    )
    
    # Replace the column name 'Council Area 2019' with 'CA19'
    reformatted_df.rename(columns={'Council Area 2019': 'CA19'}, inplace=True)

    # Save the reformatted DataFrame to a new CSV file
    output_file_path = os.path.join(input_directory, "reformat_UV103.csv")
    reformatted_df.to_csv(output_file_path, index=False)
    print(f"Data formatting complete. Results saved to: {output_file_path}")



def reformat_migrant_indicator(input_directory, CA_lookup_file_path):
    """
    Reformat the migrant indicator CSV file to move the last column of the DataFrame which contains total percentages
    to be the second column so that it is consistent with other tables.
    Replace CA names with codes.

    Args:
        input_directory (str): Path to the directory containing the input CSV file

    Returns:
        None
    """
    # Look for migrant_indicator.csv in the directory
    file_path = os.path.join(input_directory, "migrant_indicator_percentage.csv")
    if not os.path.exists(file_path):
        print("No file named migrant_indicator.csv found in the directory.")
        return

    # Load the CSV file
    df = pd.read_csv(file_path, skiprows=10, header=None)

    # Remove the last 3 rows
    df = df.iloc[:-3, :]

    # Remove the row where column A contains 'Total'
    df = df[df.iloc[:, 0] != 'Total']

    # Remove columns where all rows except column 1 are blank
    empty_columns_removed_df = df.dropna(axis=1, how='all')
    
    # Look to see if there are more than two columns
    columns = list(empty_columns_removed_df.columns)
    if len(columns) < 2:
        # If there are less than 2 columns, no change is needed
        return df  
    # Identify the last column
    last_column = columns[-1] 
    # Rearrange the columns to move the last column which it totals to the second position 
    new_order = [columns[0], last_column] + columns[1:-1]
    reformatted_df = empty_columns_removed_df[new_order]
    
    # Remove value from cell A1
    reformatted_df.iloc[0, 0] = ""  # Remove the value in A1 (table name)
    
    if len(reformatted_df) > 1 and reformatted_df.shape[1] > 1:
        # Move the values from row 1 (index 0) in columns B onward (index 1 onward) to row 2 (index 1)
        reformatted_df.iloc[1, 1:] = reformatted_df.iloc[0, 1:].values
    
        # Clear the original values in row 1 (index 0) from column B onward (index 1 onward)
        reformatted_df.iloc[0, 1:] = np.nan
    
        # Drop the first (empty) row and reset the index
        reformatted_df = reformatted_df.drop(index=0).reset_index(drop=True)
    
    # Remove the row with default integer headers if it exists
    reformatted_df.columns = reformatted_df.iloc[0]  # Set the first row as column headers
    reformatted_df = reformatted_df[1:].reset_index(drop=True)  # Drop the first row and reset the index

    # Load the LAD codes and names lookup file
    lookup_df = pd.read_csv(CA_lookup_file_path)
    lookup_dict = dict(zip(lookup_df['LAD22NM'].str.lower().str.strip(), lookup_df['LAD22CD']))

    # Replace council area names with LAD codes
    reformatted_df['Council Area 2019'] = (
        reformatted_df['Council Area 2019']
        .str.strip()
        .str.lower()
        .map(lookup_dict)
        .fillna(reformatted_df['Council Area 2019'])
    )

    # Replace the column name 'Council Area 2019' with 'CA19'
    reformatted_df.rename(columns={'Council Area 2019': 'CA19'}, inplace=True)

    # Save the new DataFrame to a CSV file
    output_file_path = os.path.join(input_directory, "reformat_migrant_indicator_percentage.csv")
    reformatted_df.to_csv(output_file_path, index=False)

    print("Data formatting complete. Results saved to:", output_file_path)





def extract_metadata_from_files(input_directory):
    """
    Extracts metadata from CSV files in the specified input directory.
    Special handling is applied for the 'migrant_indicator_percentage.csv' file. 

    Returns:
        A list of dictionaries, where each dictionary contains metadata for a file, including:
        - table_id: The unique identifier for the table.
        - table_name: The name of the table.
        - unit: The unit of measure (e.g., "Person", "Household").
    """
    print("Running extract_metadata_from_files...")
    la_files = os.listdir(input_directory)
    metadata = []  # List to store metadata for each file

    
    for file in la_files:
        # Skip files that contain 'reformat' in their name
        if 'reformat' in file:
            continue

        # Check for migrant_indicator table and explicitly define its metadata
        if file == "migrant_indicator_percentage.csv":  
            metadata.append({
                "table_id": "migrant_indicator", 
                "table_name": "Migrant Indicator",  
                "unit": "Person"  
            })
            continue  # Skip further processing for this specific table

    
        t_tab_loc = file
        # Extract the table id
        table_id = os.path.splitext(t_tab_loc)[0]

        # Open the CSV file and extract row 5
        with open(os.path.join(input_directory, t_tab_loc), "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            table_name = None  # Initialize table_name
            # Ensure there are at least 4 rows in the file
            if len(rows) >= 4:
                row_4 = rows[3][0]  # Extract the first column of row 4
                
                # Extract the portion after the second hyphen
                parts = row_4.split('-')
                if len(parts) > 2:
                    # Extract the portion after the second hyphen
                    table_name = parts[2].strip()
                    
                    # If there's a third hyphen, extract only the part before it
                    if len(parts) > 3:
                        table_name = parts[2].split('-', 1)[0].strip()
                    
                    # If the word 'All' is present, extract only the part before 'All'
                    if 'All' in table_name:
                        table_name = table_name.split('All', 1)[0].strip()
    

            # Initialize table_includes with a default value
            table_includes = []
            # Ensure there are at least 9 rows in the file
            if len(rows) > 8:
                table_includes = rows[8]  # Directly point to the 9th row
            
            # Find the unit of measure
            unit = "-"
            if "Households" in table_includes:
                unit = "Household"
            elif "Individuals" in table_includes:
                unit = "Person"   

            # Append the metadata for the current file to the list
            metadata.append({
                "table_id": table_id,
                "table_name": table_name,
                "unit": unit
            })
    
    # Check if metadata list is populated correctly
    if not metadata:
        print("Warning: Metadata list is empty. No files were processed or metadata extraction failed.")
    else:
        print(f"Metadata extraction completed successfully. Extracted {len(metadata)} entries.")
        for entry in metadata:
            if not all(key in entry for key in ["table_id", "table_name", "unit"]):
                print(f"Warning: Incomplete metadata entry found: {entry}")
            else:
                print(f"Valid metadata entry: {entry}")

    return metadata





def replace_ca19_names_with_codes(input_directory, lookup_file_path):
    """
    Replace council area names with council area codes in CSV files.

    Parameters:
    - input_directory (str): Path to the directory containing input CSV files.
    - lookup_file_path (str): Path to the lookup CSV file containing council area names and codes.
    """
    # Load the LAD codes and names lookup file
    lookup_df = pd.read_csv(lookup_file_path)  # Assuming the file has headers
    lookup_dict = dict(zip(lookup_df['LAD22NM'].str.lower().str.strip(), lookup_df['LAD22CD']))  # Create a dictionary for lookup (place names -> place codes)


    # Process each CSV file in the input directory
    # Process each CSV file in the input directory, skipping uv101b.csv
    for file_name in os.listdir(input_directory):
        if file_name.lower() == "uv101b.csv" and "uv103.csv" and "migrant_indicator_percentage.csv":
            continue
        file_path = os.path.join(input_directory, file_name)
            
        # Read the input CSV file
        if "UV604" in file_name or "UV606" in file_name:
            df = pd.read_csv(file_path, header=None, skiprows=11)
        else:
            df = pd.read_csv(file_path, header=None, skiprows=10)
        
        # Locate the row where 'Council Area 2019' appears in column 1
        if 0 in df.columns:  # Ensure column 0 exists in the input DataFrame
            council_area_row_index = df[df.iloc[:, 0] == 'Council Area 2019'].index
            if not council_area_row_index.empty:  # Check if the value exists
                start_index = council_area_row_index[0] + 1  # Start processing rows below this index
                
                # Slice the DataFrame to include only rows below the specified cell
                df_below = df.iloc[start_index:]
                
                # Strip spaces and convert to lowercase for consistent matching
                df_below.iloc[:, 0] = df_below.iloc[:, 0].str.strip().str.lower()
                
                # Replace values in column 0 using the lookup dictionary
                df_below.iloc[:, 0] = df_below.iloc[:, 0].map(lookup_dict).fillna(df_below.iloc[:, 0])  # Replace matching values, keep original if no match
                
                # Update the original DataFrame with the modified rows
                df.iloc[start_index:] = df_below
            else:
                print(f"'Council Area 2019' not found in {file_name}. Skipping replacement.")
        else:
            print(f"Column 0 not found in {file_name}. Skipping replacement.")
        # Save the reformat DataFrame to a new CSV file
        reformat_file_path = os.path.join(input_directory, f"reformat_{file_name}")
        df.to_csv(reformat_file_path, index=False, header=False)




def remove_rows(input_directory):
    """
    Processes all CSV files in the input directory that start with 'reformat_'.
    Modifies the files in place by performing specific preprocessing steps.

    Parameters:
    - input_directory (str): Path to the directory containing the CSV files.
    """

    # Process only files starting with "reformat_" and ending with ".csv", skipping uv101b.csv
    for file_name in os.listdir(input_directory):
        if file_name.lower() == "uv101b.csv" and "uv103.csv" and "migrant_indicator_percentage.csv":
            continue
        if file_name.startswith("reformat_"):
            file_path = os.path.join(input_directory, file_name)
            
            try:
                # Read the CSV file
                df = pd.read_csv(file_path, on_bad_lines='warn', header=None)
                
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
                
                # Save the modified DataFrame back to the same file (edit in place)
                df.to_csv(file_path, index=False, header=False)
                print(f"Processed and reformat: {file_name}")
            
            except pd.errors.ParserError as e:
                print(f"Error processing {file_name}: {e}")
        else:
            print(f"Skipping non-reformat file: {file_name}")





def replace_variable_names_with_codes(input_directory):
    """
    Replace the variable names with the variable ids.
    Extract the variable name and variable ids for use in the metadata table. 

    Parameters:
    - input_directory (str): Path to the directory containing the CSV files.

    Returns:
    - List of tuples containing variable_names and variable_ids for each processed file.
    """
    variable_names_ids = []  # Initialize a list to store variable_names and variable_ids for each file

    # Iterate through each file in the input directory
    for file_name in os.listdir(input_directory):
        print(f"Checking file: {file_name}")  # Debugging print statement
        if "reformat_" in file_name and file_name.endswith(".csv"):  # Target only relevant CSV files
            file_path = os.path.join(input_directory, file_name)
            
            # Read the CSV file
            df = pd.read_csv(file_path, on_bad_lines='warn', header=0)

            # Create new column names with zero padding, excluding the first column
            variable_names = df.columns

            # Check if the file is 'reformat_migrant_indicator_percentage'
            if file_name == "reformat_migrant_indicator_percentage.csv":
                # For this specific table, keep variable IDs the same as variable names
                # Replace whitespaces and slashes with underscores in variable IDs
                variable_ids = [name.replace(" ", "_").replace("/", "_") for name in variable_names[1:]]  # Exclude the first column
            else:
                # Extract the table_id from the file name after "reformat_"
                table_id = file_name.split("reformat_")[1].split(".")[0]

                # Create a list of new column names
                variable_ids = [f"{table_id}{str(i).zfill(4)}" for i in range(1, len(variable_names))]

            # Replace the existing column names of the df from column B onward with the variable IDs
            df.columns = [df.columns[0]] + list(variable_ids)  # Keep column A unchanged, replace column B onward
            # Print the new column names
            print("Updated column names:", df.columns.tolist())

            # Drop the last column unless the file name is "reformat_UV101b.csv"
            df = df.iloc[:, :-1] if file_name != "reformat_UV101b.csv" else df

            # Save the modified DataFrame 
            df.to_csv(file_path, index=False, header=True)
            print(f"Processed and saved as: {file_path}")

            # Append the variable_names and variable_ids to the results list
            variable_names_ids.append((variable_names.tolist(), variable_ids))
        else:
            print(f"Skipping file: {file_name}")
    
    # Return the list of results
    return variable_names_ids

