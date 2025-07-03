import pandas as pd
import os
from area_classification.utilities.load_config import load_config
from area_classification.pre_processing.standard_illness_ratio import sir_processing
from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
from area_classification.pre_processing.Aggregating_variables import batch_ag_columns
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table

import sys
import os


#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    aggregation_config = load_config('area_classification/aggregation_setup.yaml')
    select_variables_lookup = config["select_variables_lookup"]
    # Load the lookup table
    lookup_df = pd.read_csv(select_variables_lookup)
    dfs = {"england_wales": ew_df, "ni": ni_df}#, "scotland": scot_df}

    sir_output_df = sir_processing(config)

    for key in dfs:
        # make the key to extract the information from config file
        join_column_name = key + "_join_column_name"
        exclude_form_code_key = key + "_excluded_form_code"
        #Calculate the standard illness ratio (SIR) for each census
        #Convert counts to percentages
        df_temp = convert_to_percentages(
            dfs[key].copy(), 
            area_code_column_name=config[join_column_name], 
            excluded_form_code=config[exclude_form_code_key]
        )
        #Aggregate variables which need to be combined categories (for just England)
        file_config = aggregation_config[key + '_file_configs']
        df_temp = batch_ag_columns(df_temp, file_config, config)

        # Joining to add SIR column into main df
        # needed for select_variable function
        # look at output of sir, split area codes which contain and
        # fuzzy match - E4378949315 -> E4378949315 and E4383415436
        df_temp = pd.merge(df_temp,sir_output_df[["area_code","SIR"]],how = "left", left_on = config[join_column_name], right_on = "area_code").drop(columns=["area_code"])
        
        # Check cases where SIR is NaN and try to match with sir_output_df
        # This is a workaround for cases where the area code in the main df does not match exactly with the area code in the sir_output_df
        # Occurs where Area code is combined for small areas 
        for idx, row in df_temp[df_temp["SIR"].isna()].iterrows():
            area_code = row[config[join_column_name]]
            match_in_sir = sir_output_df[sir_output_df["area_code"].str.contains(str(area_code), na=False)]
            if not match_in_sir.empty:
                df_temp.at[idx, "SIR"] = match_in_sir["SIR"].values[0]
        #Select the 60 variables a used in previous itterations of the area classification
        select_variables_lookup = lookup_df[lookup_df["country"] == key]
        df_temp = select_variables(df_temp, select_variables_lookup, config)
        df_temp.rename(columns={config[join_column_name]: "LAD_code"},inplace=True)

        # overwriting original df with processed df
        dfs[key] = df_temp
    
    #Combine the three dataframes for censuses into one
    combined_df = pd.concat([dfs["england_wales"], dfs["ni"], dfs["scotland"]], ignore_index=True)

    # setting combined to england and wales for testing only!
    # combined_df = dfs["england_wales"]
    
    # Ensure QA directory exists
    os.makedirs(os.path.dirname(config["qa_folder_path"]), exist_ok=True)

    combined_df.to_csv(config["qa_folder_path"]+"pre_processed_data_ew_ni_scot.csv", index=False)

    return combined_df


if __name__ == "__main__":
    # Example usage
    config = load_config('area_classification/config.yaml')
    ew_df = pd.read_csv('D:/Output_Area_Classification/All_tables/ew_concat.csv')  # Replace with actual path
    ni_df = pd.read_csv('D:/Output_Area_Classification/All_tables/ni_concat.csv')
    scot_df = pd.read_csv("D:/Output_Area_Classification/All_tables/scot_concatenated_result.csv")

    processed_df = pre_processing(ew_df, ni_df, scot_df, config)
    print("pre-processing complete. Processed DataFrame shape:", processed_df.shape)