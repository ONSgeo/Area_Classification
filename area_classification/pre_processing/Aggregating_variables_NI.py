
import pandas as pd
import os

from aggregating_variables import batch_ag_columns


# Define the main directory path
main_path = "D:/Output_Area_Classification/NI_downloaded_csv/csv"

# variables to aggregate
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
batch_ag_columns(main_path, file_configs)



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