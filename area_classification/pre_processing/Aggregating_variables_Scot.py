
import pandas as pd
import os

from aggregating_variables import batch_ag_columns


# Define the main directory path
main_path = ""

# variables to aggregate
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
        'file_name': "uv103.csv",
        'col_names': ['UV1030002','UV1030003','UV1030004','UV1030005','UV1030006'],
        'new_col_name': 'age_4_and_under'
    },

    {
        'file_name': "uv103.csv",
        'col_names': [
            'uv1030007','uv1030008','uv1030009','uv1030010',
            'uv1030011','uv1030012','uv1030013','uv1030014',
            'uv1030015','uv1030016'
        ],
        'new_col_name': 'age_5_14'
    },

    {
        'file_name': "uv103.csv",
        'col_names': [
            'uv1030027', 'uv1030028', 'uv1030029', 'uv1030030', 'uv1030031', 
            'uv1030032', 'uv1030033', 'uv1030034', 'uv1030035', 'uv1030036', 
            'uv1030037', 'uv1030038', 'uv1030039', 'uv1030040', 'uv1030041', 
            'uv1030042', 'uv1030043', 'uv1030044', 'uv1030045', 'uv1030046'
        ],
        'new_col_name': 'age_25_44'
    },

    {
        'file_name': "uv103.csv",
        'col_names': [
            'uv1030047','uv1030048','uv1030049','uv1030050','uv1030051',
            'uv1030052','uv1030053','uv1030054','uv1030055','uv1030056',
            'uv1030057','uv1030058','uv1030059','uv1030060','uv1030061',
            'uv1030062','uv1030063','uv1030064','uv1030065','uv1030066'
        ],
        'new_col_name': 'age_45_64'
    },

    {
        'file_name': "uv103.csv",
        'col_names': [
            'uv1030067','uv1030068','uv1030069','uv1030070','uv1030071',
            'uv1030072','uv1030073','uv1030074','uv1030075','uv1030076',
            'uv1030077','uv1030078','uv1030079','uv1030080','uv1030081',
            'uv1030082','uv1030083','uv1030084','uv1030085','uv1030086'
        ],
        'new_col_name': 'age_65_84'
    },


    {
        'file_name': "uv103.csv",
        'col_names': [
            'uv1030087','uv1030088','uv1030089','uv1030090','uv1030091',
            'uv1030092','uv1030093','uv1030094','uv1030095','uv1030096',
            'uv1030097','uv1030098','uv1030099','uv1030100','uv1030101',
            'uv1030102'
        ],
        'new_col_name': 'age_85_and_over'
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

    {
        'file_name': "uv205.csv",
        'col_names': ['UV2050002','UV2050003','UV2050004'],
        'new_col_name': 'christian'
    },
    

]

# Update multiple CSV files
batch_ag_columns(main_path, file_configs)



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
# age_4_years_and_under - DONE
# age_5_14 - DONE
# age_25_44 - DONE
# age_45_64 - DONE
# age_65_84 - DONE
# age_85_and_over - DONE 
# no_children - DONE
# economically_active - DONE this is a single variable for EW
# christian - DONE