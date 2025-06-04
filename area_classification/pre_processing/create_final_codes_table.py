import csv
from io import StringIO

def parse_raw_data(raw_data):
    """
    Parses raw CSV-like string data into a list of dictionaries.
    
    Args:
        raw_data (str): Multi-line string with CSV-like format.
    
    Returns:
        list: A list of dictionaries representing the rows of data.
    """
    # Use StringIO to treat the string as a file
    csv_reader = csv.DictReader(StringIO(raw_data.strip()))
    return [row for row in csv_reader]

def create_final_code_csv(file_name, columns, rows):
    """
    Creates a CSV file with the specified column names and row data.

    Args:
        file_name (str): The name of the CSV file to create.
        columns (list): A list of column names for the CSV file.
        rows (list): A list of dictionaries, where each dictionary represents a row of data.
    """
    try:
        # Open the file in write mode
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            # Create a DictWriter object
            writer = csv.DictWriter(file, fieldnames=columns)
            
            # Write the header row (column names)
            writer.writeheader()
            
            # Write the data rows
            writer.writerows(rows)
        
        print(f"CSV file '{file_name}' created successfully with columns: {columns}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Define the raw data as a multi-line string
    raw_data = """
    name,table_ID,table_name,variable_code,new_code






    """
    
    # Parse the raw data into row_data
    row_data = parse_raw_data(raw_data)
    
    # Extract column names dynamically from the parsed data
    column_names = list(row_data[0].keys()) if row_data else []
    
    # Specify the output file name
    output_file = "D:/Output_Area_Classification/final_code_test.csv"
    
    # Create the CSV file with data
    create_final_code_csv(output_file, column_names, row_data)


