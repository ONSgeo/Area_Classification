
import pandas as pd
import os

def batch_ag_columns(file_configs):
    """
    This function loops through multiple CSV files, aggregates specified columns,
    adds new columns, renames the original CSV file, and saves the updated file
    with a new name.

    Parameters:
    - main_path (str): The main directory path where the CSV files are located.
    - file_configs (list of dict): A list of dictionaries where each dictionary contains:
        - 'file_name' (str): Path to the CSV file to update.
        - 'col_names' (list): List of column names to aggregate.
        - 'new_col_name' (str): Name of the new column to create.
    """
    for config in file_configs:
        file_name = config['file_name']
        col_names = config['col_names']
        new_col_name = config['new_col_name']
        
        # Construct the full file path
        file_name = os.path.join(main_path, file_name)

        # Derive a new name for the '_derived' file
        base, ext = os.path.splitext(file_name)
        derived_name = f"{base}_derived{ext}"
        
        # Check if the '_derived' file already exists
        if os.path.exists(derived_name):
            # Read the existing '_derived' file
            df = pd.read_csv(derived_name)
            print(f"Updating existing file: {derived_name}")
        else:
            # Read the original file to create a new '_derived' file
            df = pd.read_csv(file_name)
            print(f"Creating new file: {derived_name}")
        
        # Add the new column by summing the specified columns
        df[new_col_name] = df[col_names].sum(axis=1)
        
        # Save the updated DataFrame to the '_derived' file
        df.to_csv(derived_name, index=False)
        print(f"Updated '{derived_name}' with new column '{new_col_name}'.")


# Define the main path and file name
main_path = ""

# Example usage
file_configs = [

    {
        'file_name': "uv104.csv",
        'col_names': ['UV1040004', 'UV1040005'],
        'new_col_name': 'separated_divorced'
    },


    {
        'file_name': "uv112.csv",
        'col_names': ['UV1120009', 'UV1120010','UV1120022','UV1120023'],
        'new_col_name': 'dependent_children'
    },

    {
        'file_name': "uv210.csv",
        'col_names': ['UV2100010', 'UV2100011'], 
        'new_col_name': 'cannot_speak_English'
    },


    {
        'file_name': "uv405.csv",
        'col_names': ['UV4050004', 'UV4050005','UV4050006'],
        'new_col_name': 'cars_2_or_more'
    },

    {
        'file_name': "uv415.csv",
        'col_names': ['UV4150002', 'UV4150003'],
        'new_col_name': 'under_occupation'
    },

    {
        'file_name': "uv501.csv",
        'col_names': ['UV5010003','UV5010004', 'UV5010005'],
        'new_col_name': 'level_1_2_and_appr'
    },


    {
        'file_name': "uv102b.csv",
        'col_names': ['UV102b0003','UV102b0004'],
        'new_col_name': 'age_5_14'
    },

    {
        'file_name': "uv102b.csv",
        'col_names': ['UV102b0009','UV102b0010','UV102b0011','UV102b0012'],
        'new_col_name': 'age_25_44'
    },

    {
        'file_name': "uv102b.csv",
        'col_names': ['UV102b0013','UV102b0014','UV102b0015','UV102b0016'],
        'new_col_name': 'age_45_64'
    },

    {
        'file_name': "uv102b.csv",
        'col_names': ['UV102b0017','UV102b0018','UV102b0019','UV102b0020'],
        'new_col_name': 'age_65_84'
    },

    
    {
        'file_name': "uv112.csv",
        'col_names': ['UV1120008','UV1120013'],
        'new_col_name': 'no_children'
    },

    {
        'file_name': "uv601.csv",
        'col_names': ['UV6010012','UV6010023'],
        'new_col_name': 'economically_active'
    },
    

]

# Update multiple CSV files
batch_ag_columns(file_configs)



# separated_divorced - DONE
# dependant_children - DONE
# cannot_speak_English - DONE
# provides_unpaid_care - this already has one variable (All unpaid carers - UV3010003) 
# flat - this already has one variable (Flat, maisonette or apartment: total - UV4010006)
# cars_2_or_more - DONE
# under_occupation - DONE
# overcrowding - this already has one variable (Occupancy rating of bedrooms: -1 or less - UV4150005)
# ownership_or_shared - this already has one variable (Owned: Total	UV4030002)
# level_1_2_and_appr - DONE
# age_5_14 - DONE
# age_25_44 - DONE
# age_45_64 - DONE
# age_65_84 - DONE
# no_children - DONE
# economically_active - DONE this is a single variable for EW