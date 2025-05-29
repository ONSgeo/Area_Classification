
import pandas as pd
import os

from aggregating_variables import batch_ag_columns


# Define the main directory path
main_path = "D:/Output_Area_Classification/csv/"

# Variables to aggregate
file_configs = [
    {
        'file_name': "ts045.csv",
        'col_names': ['ts0450004', 'ts0450005'],
        'new_col_name': 'cars_2_or_more'
    },

    {
        'file_name': "ts002.csv",
        'col_names': ['ts0020010', 'ts0020013'],
        'new_col_name': 'separated_divorced'
    },

    {
        'file_name': "ts003.csv",
        'col_names': ['ts0030009', 'ts0030013', 'ts0030016', 'ts0030021'],
        'new_col_name': 'dependant_children'
    },

    {
        'file_name': "ts029.csv",
        'col_names': ['ts0290006', 'ts0290007'],
        'new_col_name': 'cannot_speak_English'
    },

    {
        'file_name': "ts039.csv",
        'col_names': ['ts0390003', 'ts0390006', 'ts0390009'],
        'new_col_name': 'provides_unpaid_care'
    },

    {
        'file_name': "ts044.csv",
        'col_names': ['ts0440005', 'ts0440006', 'ts0440008'],
        'new_col_name': 'flat'
    },

    {
        'file_name': "ts053.csv",
        'col_names': ['ts0530002', 'ts0530003'],
        'new_col_name': 'under_occupation'
    },

    {
        'file_name': "ts053.csv",
        'col_names': ['ts0530005', 'ts0530006'],
        'new_col_name': 'overcrowding'
    },

    {
        'file_name': "ts054.csv",
        'col_names': ['ts0540002', 'ts0540005'],
        'new_col_name': 'ownership_or_shared'
    },

    {
        'file_name': "ts067.csv",
        'col_names': ['ts0670003', 'ts0670004', 'ts0670005'],
        'new_col_name': 'level_1_2_and_appr'
    },

    {
        'file_name': "ts007a.csv",
        'col_names': ['ts007a0003', 'ts007a0004'],
        'new_col_name': 'age_5_14'
    },

    {
        'file_name': "ts007a.csv",
        'col_names': ['ts007a0007', 'ts007a0008', 'ts007a0009', 'ts007a0010'],
        'new_col_name': 'age_25_44'
    },

    {
        'file_name': "ts007a.csv",
        'col_names': ['ts007a0011', 'ts007a0012', 'ts007a0013', 'ts007a0014'],
        'new_col_name': 'age_45_64'
    },

    {
        'file_name': "ts007a.csv",
        'col_names': ['ts007a0015', 'ts007a0016', 'ts007a0017', 'ts007a0018'],
        'new_col_name': 'age_65_84'
    },

    {
        'file_name': "ts003.csv",
        'col_names': ['ts0030008', 'ts0030012'],
        'new_col_name': 'no_children'
    },
]

# Update multiple CSV files
batch_ag_columns(main_path, file_configs)




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
# no_children -DONE