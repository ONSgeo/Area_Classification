# from area_classification.pre_processing.SIR import SIR
# from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
# from area_classification.pre_processing.aggregate_variables import aggregate_variables
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table

#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    print("placeholder for pre_processing")

    for df in [ew_df, ni_df, scot_df]:
        #Standard Illness Ratio calculation
        df_temp = SIR(df)
        #Convert counts to percentages
        df_temp = convert_to_percentages(df_temp)
        #Aggregate variables which need to be combined categories
        df_temp = aggregate_variables(df_temp)
        ##Select the 60 variables which are needed for the area classification             
        df_temp = select_variables(df_temp)

    #Combine the three data frames for censuses into one
    combined_df = combine_table(ew_df, ni_df, scot_df)
    return combined_df