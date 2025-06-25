import pandas as pd
from area_classification.utilities.load_config import load_config
# from area_classification.pre_processing.SIR import SIR
from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
from area_classification.pre_processing.Aggregating_variables import batch_ag_columns
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table

#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    print("placeholder for pre_processing")
    aggregation_config = load_config('area_classification/aggregation_setup.yaml')
    select_variables_lookup = "area_classification/pre_processing/EW_selected_codes_lookup.csv"
    dfs = {"england_wales": ew_df, "ni": ni_df, "scotland": scot_df}

    for key in dfs:
        # make the key to extract the information from config file
        join_column_name = key + "_join_column_name"
        exclude_form_code_key = key + "_exclude_form_code"
        #Calculate the standard illness ratio (SIR) for each census
        df_temp = SIR(dfs[key])
        #Convert counts to percentages
        df_temp = convert_to_percentages(
            df_temp, 
            area_code_column_name=config[join_column_name], 
            excluded_form_code=config[exclude_form_code_key]
        )
        #Aggregate variables which need to be combined categories (for just England)
        file_config = aggregation_config[key + 'file_configs']
        df_temp = batch_ag_columns(df_temp, file_config, config)
        
        #Select the 60 variables a used in previous itterations of the area classification
        df_temp = select_variables(df_temp, select_variables_lookup, config)
   
  # need to find a way to overwrite ew_df, ni_df, scot_df with the processed data

    # Update and overwrite the dataframes
    #ew_df = dfs["england_wales"]
    
    #Combine the three dataframes for censuses into one
    combined_df = combine_table(ew_df, ni_df, scot_df)
    return combined_df