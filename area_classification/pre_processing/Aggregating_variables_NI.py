
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
main_path = "D:/Repos/Area_Classification/Area_Classification_Project/Downloading_data/Northern_Ireland_Census_2022_Data_Zone-download/NI_downloaded_csv/csv"

# Example usage
file_configs = [

    {
        'file_name': "ni137.csv",
        'col_names': ['ni1370005', 'ni1370006'],
        'new_col_name': 'separated_divorced'
    },


    {
        'file_name': "ni003.csv",
        'col_names': ['ni0030005', 'ni0030006','ni0030007'],
        'new_col_name': 'flat'
    },

    {
        'file_name': "ni153.csv",
        'col_names': ['ni1530002', 'ni1530003'],
        'new_col_name': 'under_occupation'
    },


    {
        'file_name': "ni110.csv",
        'col_names': ['ni1100003', 'ni1100004','ni1100005'],
        'new_col_name': 'level_1_2_and_appr'
    },

    {
        'file_name': "ni012.csv",
        'col_names': ['ni0120003','ni0120004'],
        'new_col_name': 'age_5_14'
    },

    {
        'file_name': "ni012.csv",
        'col_names': ['ni0120007','ni0120008','ni0120009','ni0120010'],
        'new_col_name': 'age_25_44'
    },

    {
        'file_name': "ni012.csv",
        'col_names': ['ni0120011','ni0120012','ni0120013','ni0120014'],
        'new_col_name': 'age_45_64'
    },

    {
        'file_name': "ni012.csv",
        'col_names': ['ni0120015','ni0120016','ni0120017','ni0120018'],
        'new_col_name': 'age_65_84'
    },

    {
        'file_name': "ni033.csv",
        'col_names': ['ni0330002','ni0330003'],
        'new_col_name': 'united_kingdom'
    },


    {
        'file_name': "ni033.csv",
        'col_names': ['ni0330004','ni0330005'],
        'new_col_name': 'eu_countries'
    },


    {
        'file_name': "ni050.csv",
        'col_names': ['ni0500005','ni0500007'],
        'new_col_name': 'economically_active'
    },

]

# Update multiple CSV files
batch_ag_columns(file_configs)



# separated_divorced - DONE
# dependant_children - this already has one variable (household with dependent children - ni2390003)
# cannot_speak_English - this already has one variable (Main language is not English: cannot speak English or cannot speak English well - ni0570004)
# provides_unpaid_care - this already has one variable (provides 1 or more hours of unpaid care per week - ni1270003)
# flat - DONE
# cars_2_or_more - this already has the one variable (2 or more cars or van available - ni2210004)
# under_occupation - DONE
# overcrowding - this already has the one variavle (Occupancy rating (rooms) of -1 or less - ni1520003)
# ownership_or_shared - this already has one variable (Owner occupied - ni1070002)
# level_1_2_and_appr - DONE
# age_5_14 - DONE
# age_25_44 - DONE
# age_45_64 - DONE
# age_65_84 - DONE
# no_children - this already has one variable (Single family household: Couple family household: No children - ni2520004)
# united_kingdom - DONE. This has to be derived for NI only
# eu_countries - DONE. This has to be derived for NI only
# economically_active - DONE 