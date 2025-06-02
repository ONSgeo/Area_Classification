import pandas as pd
import os

# these functions are set up to reformat the tables once the excess information at the top and bottom have been removed

def reformat_uv101b(input_directory):
    """
    Function to reformat the UV101b CSV file in the given directory.
    
    Args:
        input_directory (str): Path to the directory containing the input CSV files.
    """
    # Look for UV101b.csv in the directory
    file_path = os.path.join(input_directory, "row_removal_UV101b.csv")
    if not os.path.exists(file_path):
        print("No file named UV101b.csv found in the directory.")
        return

    # Load the CSV file
    df = pd.read_csv(file_path, header=None)  # No header assumed for processing
    df.columns = ['A', 'B', 'C', 'D', 'E']  # Assign column names for clarity

    # List to store results
    results = []

    # Iterate through rows to extract relevant data
    for index, row in df.iterrows():
        # Check if the row contains the word 'sex' in column A
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

    # Save the results to a new CSV file
    if results:
        output_df = pd.DataFrame(results)
        output_file_path = os.path.join(input_directory, "row_removal_UV101b_cleaned.csv")
        output_df.to_csv(output_file_path, index=False)
        print("Data formatting complete. Results saved to:", output_file_path)
    else:
        print("No relevant data found in UV101b.csv.")

# Run the function
# input_directory = "D:/Output_Area_Classification/Scotland_downloaded/test_sample_percentages/uv101b_uv103/"
# reformat_uv101b(input_directory)








def reformat_uv103(input_directory):
    """
    Reformat the UV103 CSV file according to the specified requirements.
    
    Args:
        input_directory (str): Path to the directory containing the input CSV file.
    """
    # Look for UV103.csv in the directory
    file_path = os.path.join(input_directory, "row_removal_UV103.csv")
    if not os.path.exists(file_path):
        print("No file named UV103.csv found in the directory.")
        return

    # Load the CSV file
    df = pd.read_csv(file_path, header=None)

    # Extract headers for columns B to CY (row 2 in the original file)
    headers = ["CA19"] + df.iloc[1, 1:].tolist()

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

    # Save the new DataFrame to a CSV file
    output_file_path = os.path.join(input_directory, "row_removal_UV103_cleaned.csv")
    reformatted_df.to_csv(output_file_path, index=False)

    print("Data formatting complete. Results saved to:", output_file_path)


# Run the function
# input_directory = "D:/Output_Area_Classification/Scotland_downloaded/test_sample_percentages/uv101b_uv103/"
# reformat_uv103(input_directory)
    

