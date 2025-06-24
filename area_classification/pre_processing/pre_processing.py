# from area_classification.pre_processing.SIR import SIR
# from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
# from area_classification.pre_processing.aggregate_variables import aggregate_variables
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table
select_variables_lookup = "area_classification/pre_processing/EW_selected_codes_lookup.csv"


#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    print("placeholder for pre_processing")

    for df in [ew_df, ni_df, scot_df]:
        df_temp = SIR(df)
        df_temp = aggregate_variables(df_temp) #legacy version was aggregate_columns
        if config["count or percent"] == "count":
            # count or percent means we have downloaded the data as a count or a percent
            df_temp = convert_to_percentages(df_temp)
        df_temp = select_columns_from_lookup(df_temp, select_variables_lookup, output_file)

   # need to find a way to overwrite ew_df, ni_df, scot_df with the processed data

    combined_df = combine_table(ew_df, ni_df, scot_df)
    return combined_df