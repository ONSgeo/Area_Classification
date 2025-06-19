import pandas as pd
from area_classification.utilities.load_config import load_config

# from area_classification.pre_processing.SIR import SIR
# from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
# from area_classification.pre_processing.aggregate_variables import aggregate_variables
from area_classification.pre_processing.Aggregating_variables import batch_ag_columns
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table

#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    print("placeholder for pre_processing")

    # Config stuff needs to go here: 
    # with open('area_classification/aggregation_setup.yaml', 'r') as file:
    #     content = file.read()
    # ew_file_configs = yaml.safe_load(content)
    # file_configs = ew_file_configs['ew_file_configs']
    # Think this will work easier
    file_configs = load_config('area_classification/aggregation_setup.yaml')


    for df in [ew_df, ni_df, scot_df]:
        df_temp = SIR(df)
        # currently file_configs is just for EW, needs NI and Scot variations also
        df_temp = batch_ag_columns(df_temp, file_configs)
        df_temp = aggregate_variables(df_temp) #legacy version was aggregate_columns
        if config["count or percent"] == "count":
            # count or percent means we have downloaded the data as a count or a percent
            df_temp = convert_to_percentages(df_temp)
        df_temp = select_variables(df_temp)
   # need to find a way to overwrite ew_df, ni_df, scot_df with the processed data

    combined_df = combine_table(ew_df, ni_df, scot_df)
    return combined_df