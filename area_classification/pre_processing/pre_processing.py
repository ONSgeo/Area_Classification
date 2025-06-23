# from area_classification.pre_processing.SIR import SIR
from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
# from area_classification.pre_processing.aggregate_variables import aggregate_variables
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table

#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    print("placeholder for pre_processing")

    dfs = {"england_wales": ew_df, "ni": ni_df, "scotland": scot_df}

    for key in dfs:
        # make the key to extract the information from config file
        join_column_name = key + "_join_column_name"
        exclude_form_code_key = key + "_exclude_form_code"
        df_temp = SIR(dfs[key])
        df_temp = aggregate_variables(df_temp)

        df_temp = convert_to_percentages(
            df_temp, 
            area_code_column_name=config[join_column_name], 
            excluded_form_code=config[exclude_form_code_key]
        )

        df_temp = select_variables(df_temp)
        dfs[key] = df_temp

    combined_df = combine_table(ew_df, ni_df, scot_df)
    return combined_df