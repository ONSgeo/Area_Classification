
import pandas as pd
import os

def batch_ag_columns(file_configs):
    """
    This function loops through multiple CSV files, aggregates specified columns,
    adds new columns, renames the original CSV file, and saves the updated file
    with a new name.

    Parameters:
    - file_configs (list of dict): A list of dictionaries where each dictionary contains:
        - 'file_path' (str): Path to the CSV file to update.
        - 'col_names' (list): List of column names to aggregate.
        - 'new_col_name' (str): Name of the new column to create.
    """
    for config in file_configs:
        file_path = config['file_path']
        col_names = config['col_names']
        new_col_name = config['new_col_name']
        
        # Derive a new name for the '_derived' file
        base, ext = os.path.splitext(file_path)
        derived_name = f"{base}_derived{ext}"
        
        # Check if the '_derived' file already exists
        if os.path.exists(derived_name):
            # Read the existing '_derived' file
            df = pd.read_csv(derived_name)
            print(f"Updating existing file: {derived_name}")
        else:
            # Read the original file to create a new '_derived' file
            df = pd.read_csv(file_path)
            print(f"Creating new file: {derived_name}")
        
        # Add the new column by summing the specified columns
        df[new_col_name] = df[col_names].sum(axis=1)
        
        # Save the updated DataFrame to the '_derived' file
        df.to_csv(derived_name, index=False)
        print(f"Updated '{derived_name}' with new column '{new_col_name}'.")

# Example usage
file_configs = [
    {
        'file_path': "D:/Output_Area_Classification/csv/ts045.csv",
        'col_names': ['ts0450004', 'ts0450005'],
        'new_col_name': 'cars_2_or_more'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts002.csv",
        'col_names': ['ts0020010', 'ts0020013'],
        'new_col_name': 'separated_divorced'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts003.csv",
        'col_names': ['ts0030009', 'ts0030013', 'ts0030016' ,'ts0030021'],
        'new_col_name': 'dependant_children'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts029.csv",
        'col_names': ['ts0290006', 'ts0290007'],
        'new_col_name': 'cannot_speak_English'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts039.csv",
        'col_names': ['ts0390003', 'ts0390006','ts0390009'],
        'new_col_name': 'provides_unpaid_care'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts044.csv",
        'col_names': ['ts0440005', 'ts0440006','ts0440008'],
        'new_col_name': 'flat'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts053.csv",
        'col_names': ['ts0530002', 'ts0530003'],
        'new_col_name': 'under_occupation'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts053.csv",
        'col_names': ['ts0530005', 'ts0530006'],
        'new_col_name': 'overcrowding'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts054.csv",
        'col_names': ['ts0540002', 'ts0540005'],
        'new_col_name': 'ownership_or_shared'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts067.csv",
        'col_names': ['ts0670003', 'ts0670004','ts0670005'],
        'new_col_name': 'level_1_2_and_appr'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts007a.csv",
        'col_names': ['ts007a0003','ts007a0004'],
        'new_col_name': 'age_5_14'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts007a.csv",
        'col_names': ['ts007a0007','ts007a0008','ts007a0009','ts007a0010'],
        'new_col_name': 'age_25_44'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts007a.csv",
        'col_names': ['ts007a0011','ts007a0012','ts007a0013','ts007a0014'],
        'new_col_name': 'age_45_64'
    },

    {
        'file_path': "D:/Output_Area_Classification/csv/ts007a.csv",
        'col_names': ['ts007a0015','ts007a0016','ts007a0017','ts007a0018'],
        'new_col_name': 'age_65_84'
    },
    

]

# Update multiple CSV files
batch_ag_columns(file_configs)




# separated_divorced - DONE
# dependant_children - DONE
# cannot_speak_English - DONE
# provides_unpaid_care - DONE
# flat - DONE
# cars_2_or_more - DONE
# under_occupation - DONE
# overcrowding - DONE
# ownership_or_shared - DONE
# level_1_2_and_appr - DONE
# age_5_14 - DONE
# age_25_44 - DONE
# age_45_64 - DONE
# age_65_84 - DONE