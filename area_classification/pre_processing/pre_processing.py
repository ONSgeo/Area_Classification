# from area_classification.pre_processing.SIR import SIR
# from area_classification.pre_processing.convert_to_percentages import convert_to_percentages
# from area_classification.pre_processing.aggregate_variables import aggregate_variables
from area_classification.pre_processing.select_variables import select_variables
from area_classification.pre_processing.combine_tables import combine_table

#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    print("placeholder for pre_processing")

    for df in [ew_df, ni_df, scot_df]:
        #Calculate the standard illness ratio (SIR) for each census
        df_temp = SIR(df)
        # For each census aggregate varaiables which require aggregating
        df_temp = aggregate_variables(df_temp) #legacy version was aggregate_columns
        #Convert values to counts
        if config["count or percent"] == "count":
            # count or percent means we have downloaded the data as a count or a percent
            df_temp = convert_to_percentages(df_temp)
        #Aggregate variables
        # this needs to be an if statement - as different scrips for each census
        if df = ew_df:
            df_temp = Aggregating_variables_EW(df_temp)
        if df = ni_df:
            df_temp = Aggregating_variables_NI(df_temp)
        if df = scot_df:
            df_temp = Aggregating_variables_Scot(df_temp)
        #Select the same 60 variables a used in previous itterations
        df_temp = select_variables(df_temp)
   # need to find a way to overwrite ew_df, ni_df, scot_df with the processed data

    #Put all three census tables into one dataframe
    combined_df = combine_table(ew_df, ni_df, scot_df)
    return combined_df