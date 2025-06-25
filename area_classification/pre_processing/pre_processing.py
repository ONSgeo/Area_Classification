import pandas as pd
from area_classification.utilities.load_config import load_config
from area_classification.pre_processing.standard_illness_ratio import SIR_calculation
from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
from area_classification.pre_processing.Aggregating_variables import batch_ag_columns
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table
select_variables_lookup = "area_classification/pre_processing/EW_selected_codes_lookup.csv"

#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    print("placeholder for pre_processing")
    aggregation_config = load_config('area_classification/aggregation_setup.yaml')
    select_variables_lookup = "area_classification/pre_processing/EW_selected_codes_lookup.csv"
    dfs = {"england_wales": ew_df, "ni": ni_df, "scotland": scot_df}

    ew_disability_df = pd.read_csv("ew...").rename(columns={'Area Code': 'Area_Code', 'Local Authority': 'Local_Authority'})
    ni_disability_df = pd.read_csv("ni...").rename(columns={'lgd_code': 'Area_Code', 'lgd': 'Local_Authority'})
    # scotland_disability_df = pd.read_csv("scotland...").rename(columns={'council_area': 'Area_Code', 'council_area_code': 'Local_Authority'})
    combined_disability_df = pd.concat(
        [ew_disability_df, ni_disability_df])#, scotland_disability_df],)
    # Scotland excluded because it doesnt have council area codes 
    sir_output_df = SIR_calculation(combined_disability_df)
    for key in dfs:
        # make the key to extract the information from config file
        join_column_name = key + "_join_column_name"
        exclude_form_code_key = key + "_exclude_form_code"
        #Calculate the standard illness ratio (SIR) for each census
        df_temp = SIR_calculation(dfs[key])
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

    # Join on sir column to combined df
    combined_df = combined_df.merge(sir_output_df, on='Area_Code', how='left')
    return combined_df