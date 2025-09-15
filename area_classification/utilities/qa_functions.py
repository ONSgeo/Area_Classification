
import pandas as pd 
import os 

def run_qa_checks(df):
    """
    Main function to run QA checks on the provided dataframe. 
    
    The user selects which type of QA checks to perform: an automatic summary or user-input checks 
        - If the user selects automatic summary checks, the function 'quality_checks_all_dfs' is called.
        - If the user selects user-input checks, the function 'user_input_qa' is called
    
    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be checked.

    Returns
    -------
    None
    """

    # Ask the user which QA function(s) to run
    qa_choice = input(
        "Which QA function do you want to run?\n"
        "Type 'auto' for automatic summary checks or'user' for user input checks:"
    ).strip().lower()

    if qa_choice == "auto":
        quality_checks_all_dfs(df)
    elif qa_choice == "user":
        user_input_qa(df)
    else:
        print("Invalid choice. No QA checks run.")

# Ask user to put in standard rows (tailored to whatever use - so for area classifications this would be number of LADs)?

def quality_checks_all_dfs(df):

    """
    Function to perform automatic quality checks on the dataframe.

    The user can select between a basic or a full auto check. Each option will print a summary report of the dataframe but will provide
    a different level of detail. 
    
    Basic Auto Check:
        - Prints the total number of rows and columns.
        - Checks if any column contains a mix of data types and prints a warning if so.
        - Checks for missing values and zero values, printing the total counts if any are found.
        - After completing the basic auto check, the user is prompted to decide if they want to proceed with the full auto check.
    
    Full Auto Check:
        - Prints the total number of rows and columns.
        - Prints the column names and data types of each column.
        - Checks if any column contains a mix of data types. Prints a warning and lists the columns containing mixed data types. 
        - Checks for missing values and zero values - lists the columns containing missing or zero values and the total count found in each.
        - After completing the full auto check, the user is prompted to decide if they want to proceed with the user input checks. 

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be checked.

    Returns 

    Print statement at the specified level of detail. 

    """
    
    # Ask the user if they want a basic or detailed auto check
    auto_check_type = input("Do you want to run a basic or a full auto check? (basic/full): ").strip().lower()

    if auto_check_type == 'basic':
        # Complete basic auto check
        while True:

            print("Summary report for DataFrame:")

            # Print the total number of rows and columns
            print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

            # Check if any column contains a mix of data types
            mixed_type_columns = []
            for col in df.columns:
                types_in_col = set(type(x) for x in df[col].dropna())
                if len(types_in_col) > 1:
                    print(f"Warning: Column '{col}' contains different data types: {types_in_col}")
                    mixed_type_columns.append(col)
            if not mixed_type_columns:
                print('All columns contain a single data type')


            # Check for missing values in the DataFrame
            missing_values = df.isnull().sum().sum()
            if missing_values == 0:
                print("No missing values")
            else:
                print(f"Total missing values in DataFrame: {missing_values}")
            
            # Check for zero values in the DataFrame
            zero_values = (df == 0).sum().sum()
            if zero_values == 0:
                print("No zero values")
            else:
                print(f"Total zero values in DataFrame: {zero_values}")
        
            # Ask the user if they want to complete the full auto check
            run_full = input('Do you want to complete the full auto check? (yes/no) ').strip().lower()
            if run_full == 'yes':
                auto_check_type = 'full'
                break
            
            else:
                print('QA checks complete')
                break
        

    if auto_check_type == 'full': 
        # Complete full auto check

        print("Summary report for DataFrame:")

        # Print the total number of rows and columns
        print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

        # Print column names
        print(f"Column Headings: {df.columns.tolist()}")

        # Print data types of each column
        print(f"Data Types of each column:")
        print(df.dtypes)

        # Check if any column contains a mix of data types
        mixed_type_columns = []
        for col in df.columns:
            types_in_col = set(type(x) for x in df[col].dropna())
            if len(types_in_col) > 1:
                print(f"Warning: Column '{col}' contains different data types: {types_in_col}")
                mixed_type_columns.append(col)
        if not mixed_type_columns:
            print('All columns contain a single data type')

        # Check for missing values in the DataFrame
        missing_values = df.isnull().sum().sum()
        if missing_values == 0:
            print("No missing values")
        else:
            print(f"Total missing values in DataFrame: {missing_values}")

            # Print columns with missing values and their counts
            missing_per_column = df.isnull().sum()
            print("Missing values per column:")
            print(missing_per_column[missing_per_column > 0])

        # Check for zero values in the DataFrame
        zero_values = (df == 0).sum().sum()
        if zero_values == 0:
            print("No zero values")
        else:
            print(f"Total zero values in DataFrame: {zero_values}")

            # Print columns with zero values and their counts
            zero_per_column = (df == 0).sum()
            print("Zero values per column:")
            print(zero_per_column[zero_per_column > 0])
        
        # Ask the user if they want to complete the user input checks
        run_user_input = input('Do you want to complete the user input checks? (yes/no) ').strip().lower()
        if run_user_input == 'yes':
            user_input_qa(df)
        else:
            print('QA checks complete')

    return



def user_input_qa(df):

    """
    Function to perform tailored quality checks on the dataframe based on user inputs.

    The function performs three main checks - the user is prompted at each stage to select if they want to perform or skip the check:

    1. Structure of the dataframe
        - User inputs the expected number of rows and columns. 
        - The function checks if the dataframe matches these expectations and prints a warning if not.

    2. Ranges
        - User selects whether they want to check the value ranges for the entire dataframe or specific columns.
        - For the entire dataframe - the user inputs the expected min and max values. 
          The function checks if any values fall outside this range and prints a warning if so. The duplicate count per column is listed. 
          The user is then prompted to decide if they want to check specific columns.
        - For specific columns - the user specifies which columns to check and inputs the expected min and max for each. 
          The function checks if any values in those columns fall outside the specified ranges and prints a warning if so.
          The user is then prompted to decide if they want to check any further columns.

    3. Unique Values/ Duplicates
        - User selects whether they want to check for duplicate values in the entire dataframe or specific columns.
        - For the entire dataframe - the function checks each column for duplicate values and prints the total number found in each column.
        - For specific columns - the user specifies which columns to check. The function checks each specified column for duplicate values and prints the total number found.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be checked.

    Returns print statements based on the checks performed.
    
    """

    # Check One - Structure of the dataframe
    # Asks the user to input the expected number of rows and columns. Then checks if the dataframe matches these expectations.

    # Ask the user if they want to check the number of rows and columns
    print('Check 1/3 - Structure of the DataFrame')
    check_shape = input("Do you want to check the number of rows and columns? (yes/no): ").strip().lower()
    if check_shape == "yes":
        expected_rows = int(input("Enter the expected number of rows: "))
        expected_cols = int(input("Enter the expected number of columns: "))
        
        # Check if actual shape matches expected shape
        actual_rows, actual_cols = df.shape
        if actual_rows != expected_rows:
            print(f"Warning: DataFrame contains {actual_rows} rows, expected {expected_rows}.")   
        else:
            print("Row count matches expected value.")
        
        if actual_cols != expected_cols:
            print(f"Warning: DataFrame contains {actual_cols} columns, expected {expected_cols}.")
        else: 
            print("Column count matches expected value.")  
    
    else:
        print("Skipping row and column count check.")

 
    # Check Two - Ranges
    # Asks the user to input the expected range for data values (min and max). Then checks if any values fall outside this range.

    
    # Ask the user if they want to check value ranges
    print('Check 2/3 - Ranges')
    check_ranges = input("Do you want to check for values outside a specific range? (yes/no): ").strip().lower()
    if check_ranges == 'yes':
        
        # Ask the user if they want to check ranges for the entire dataframe or only specific columns
        range_scope = input("Do you want to check the ranges for the entire dataframe? (yes/no): ").strip().lower()
        if range_scope == 'yes':
            while True:
                # Ask the user to input the expected min and max values for the dataframe
                min_expected = float(input("Enter the minimum expected value: "))
                max_expected = float(input("Enter the maximum expected value: "))
                
                # Convert all columns to numeric where possible (required to check ranges)
                df_numeric = df.apply(pd.to_numeric, errors='coerce')
                
                # Check for values outside the expected range
                outside_range = df_numeric[(df_numeric < min_expected) | (df_numeric > max_expected)]
                if outside_range.any().any():
                    print("Warning: There are values outside the expected range!")
                
                    # Print columns and counts of out-of-range values
                    out_of_range_counts = ((df_numeric < min_expected) | (df_numeric > max_expected)).sum()
                    print("Out-of-range values per column:")
                    print(out_of_range_counts[out_of_range_counts > 0])
                
                else:
                    print("All values are within the expected range.")
                
                # Ask the user if they want to check the range of any specific columns 
                specific_check = input("Do you want to check the range of any specific columns? (yes/no): ").strip().lower()
                if specific_check == 'yes':
                    range_scope = 'no'
                    break
                else:
                    break
                
        if range_scope == 'no':
            while True:
                # Ask the user to specify which columns to check
                columns_to_check = input("Enter the column heading(s) you want to check, separated by commas: ").split(',')
                columns_to_check = [col.strip() for col in columns_to_check]

                for col in columns_to_check:
                    if col in df.columns:
                        min_expected = float(input(f"Enter the minimum expected value for column '{col}': "))
                        max_expected = float(input(f"Enter the maximum expected value for column '{col}': "))

                        # Convert column to numeric for comparison
                        col_numeric = pd.to_numeric(df[col], errors='coerce')
                        out_of_range_mask = (col_numeric < min_expected) | (col_numeric > max_expected)
                        out_of_range_count = out_of_range_mask.sum()

                        if out_of_range_count > 0:
                            print(f"Warning: Column '{col}' has {out_of_range_count} values outside the expected range [{min_expected}, {max_expected}].")
                        else:
                            print(f"All values in column '{col}' are within the expected range.")
                    else:
                        print(f"Column '{col}' not found in DataFrame.")

                # Ask the user if they want to check the range of any further columns
                more_ranges = input("Do you want to check the range of any more columns? (yes/no): ").strip().lower()
                if more_ranges == 'yes':  
                    continue  
                else:
                    break
           
            
    else: 
        print("Skipping range check.")
            



    # Check Three - Unique Values/ Duplicates
    # Asks the user to specify if a column contains only unique values. Then checks if there are any duplicates in that column.

    # Ask the user if they want to check for duplicate values. 
    print('Check 3/3 - Duplicate Values')
    check_duplicates = input("Do you want to check for duplicate values? (yes/no): ").strip().lower()
    if check_duplicates == 'yes':

        # Ask the user if they want to check  for the entire data frame or only specific columns
        duplicate_scope = input("Do you want to check every column for duplicate values? (yes/no): ").strip().lower()
        if duplicate_scope == 'yes':
            #Check every column for duplicate values
            for col in df.columns:
                duplicate_count = df[col].duplicated().sum()
                if duplicate_count > 0:
                    print(f"Warning: Column '{col}' contains {duplicate_count} duplicated values.")
                else:
                    print(f"Column '{col}' contains no duplicate values.")
                    
        elif duplicate_scope == 'no':
        
            while True:
                # Ask the user to specify which columns to check
                columns_to_check = input("Enter the column heading(s) you want to check, separated by commas: ").split(',')
                columns_to_check = [col.strip() for col in columns_to_check]

                for col in columns_to_check:
                    if col in df.columns:
                        duplicate_count = df[col].duplicated().sum()
                        if duplicate_count > 0:
                            print(f"Warning: Column '{col}' contains {duplicate_count} duplicate values:")
                            # Print each duplicate value and how many times it appears in the column
                            duplicated_values = df[col][df[col].duplicated(keep=False)]
                            value_counts = duplicated_values.value_counts()
                            for value, count in value_counts.items():
                                print(f"Value '{value}' appears {count} times in column '{col}'.")
                        else:
                            print(f"Column '{col}' contains no duplicate values.")
                    else:
                        print(f"Column '{col}' not found in DataFrame.")
                
                # Ask the user if they want to check for duplicates in any further columns
                more_duplicates = input("Do you want to check for duplicate values in any more columns? (yes/no): ").strip().lower()
                if more_duplicates == 'yes':
                    continue
                else:
                    break
         
        
    else:
        print("Skipping duplicate value check.")

    print('QA checks complete')

    return


   

   

if __name__ == "__main__":
    # Example usage
    folder_path = "./data/inputs"
    file_path = os.path.join(folder_path, 'pre_clustering_data_filtered.csv')
    df = pd.read_csv(file_path)

    run_qa_checks(df)


