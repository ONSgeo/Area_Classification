# Checking that csv ouputs from EW_Census_2021_Output_Areas-download/bulk_data.R and bulk_data.py are identical
# Save output from bulk_data.R to D:/output_data/csv/R_
# Save output from bulk_data.py to D:/output_data/csv/python_
# This script checks if the CSV files in two folders are identical

import csv
import os

# Function to normalize values for comparison
def float_value(value):
    try:
        # Try to convert to float for numeric comparison
        return float(value)
    except ValueError:
        # If conversion fails, return the original value (e.g., for strings)
        return value

# Function that takes 2 csv files and checks that they are identical
def check_csv_files_identical(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        for row_num, (row1, row2) in enumerate(zip(reader1, reader2), start=1):
            # Normalize values in both rows for comparison
            row1 = [float_value(cell) for cell in row1]
            row2 = [float_value(cell) for cell in row2]

            if row1 != row2:
                print(f"Difference found in file '{file1}' and '{file2}' at row {row_num}:")
                print(f"  File 1: {row1}")
                print(f"  File 2: {row2}")
                return False

        # Check if both files have the same number of rows
        remaining_rows1 = list(reader1)
        remaining_rows2 = list(reader2)
        if len(remaining_rows1) != len(remaining_rows2):
            print(f"Files '{file1}' and '{file2}' have different number of rows.")
            print(f"  Remaining rows in File 1: {remaining_rows1}")
            print(f"  Remaining rows in File 2: {remaining_rows2}")
            return False

    return True

# Iterate check_csv_files_identical over all files in 2 folders
def check_csv_files_in_folders(folder1, folder2):
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    if files1 != files2:
        print("Files in folders are not identical.")
        print(f"  Files in Folder 1: {files1}")
        print(f"  Files in Folder 2: {files2}")
        return False

    all_identical = True
    for file in files1:
        file1 = os.path.join(folder1, file)
        file2 = os.path.join(folder2, file)
        if not check_csv_files_identical(file1, file2):
            print(f"Files '{file1}' and '{file2}' are not identical.")
            all_identical = False

    if all_identical:
        print("All files are identical.")
    return all_identical

check_csv_files_in_folders('D:/output_data/csv/R_', 'D:/output_data/csv/python_')