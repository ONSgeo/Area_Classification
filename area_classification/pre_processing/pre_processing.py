import pandas as pd
import sys
import os
from utilities.load_config import load_config
from pre_processing.standard_illness_ratio import sir_processing
from pre_processing.aggregating_variables import aggregating_variables
from pre_processing.select_variables import select_variables
from pre_processing.totals_columns_select_uk import select_totals_columns
from pre_processing.convert_to_percentages import convert_to_percentages
from pre_processing.standardize_pre_clustering_data import standardize_dataframe

#Assume that the data has been loaded and is in a pandas dataframe (e.g. ran NI / EW bulks and downloaded Scot)
def pre_processing(ew_df, ni_df, scot_df, config):
    """
    Processes to prepare the census data from England, Wales, Northern Ireland, and Scotland to ensure 
    consistency of datasets before being fed into clustering algorithm.

    Parameters
    ----------
    ew_df : pd.DataFrame
        DataFrame containing census data for England and Wales.
    ni_df : pd.DataFrame
        DataFrame containing census data for Northern Ireland.
    scot_df : pd.DataFrame
        DataFrame containing census data for Scotland.
    config : dict
        Configuration dictionary containing paths and settings/

    Returns
    -------
    pd.DataFrame
        Combined and pre-processed DataFrame containing data for England, Wales, Northern Ireland, 
        and Scotland, for the 60 specific variables required for area classification clustering.

    Notes
    -----
    - The function calculates the Standard Illness Ratio (SIR) for each census.
    - Converts counts to percentages for England, Wales and Northern Ireland.
    - Aggregates variables based on the configuration for each country individually.
    - Joins SIR data to the main DataFrame and handles cases where area codes do not match exactly.
    - Selects the specific 60 variables based on a lookup table.
    - Saves intermediate and final outputs to CSV files.

    Raises
    ------
    FileNotFoundError
        If any of the required configuration files or paths are missing.
    KeyError
        If required keys are missing in the `config` dictionary.
    ValueError
        If there are issues with data merging or transformations.

    """
    aggregation_config = load_config('area_classification/aggregation_setup.yaml')
    select_variables_lookup = pd.read_csv(config["select_variables_lookup"])
    dfs = {"ew": ew_df, "ni": ni_df, "scot": scot_df}

    #Calculate the standard illness ratio (SIR) for each census
    sir_output_df = sir_processing(config)

    for key in dfs:
        # make the key to extract the information from config file
        join_column_name = key + "_join_column_name"
        exclude_form_code_key = key + "_excluded_form_code"

        df_temp = dfs[key]

        #Aggregate variables which need to be combined categories
        aggregation_configs = aggregation_config[key + '_file_configs']
        df_temp = aggregating_variables(df_temp, aggregation_configs, config)

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
        country_variables_lookup = select_variables_lookup[select_variables_lookup["country"] == key]
        df_temp = select_variables(df_temp, country_variables_lookup, config)
        df_temp.rename(columns={config[join_column_name]: "LAD_code"},inplace=True)

        # Write the DataFrame to a CSV file
        os.makedirs(os.path.dirname(config["qa_folder_path"]), exist_ok=True)
        output_csv_path = os.path.join(config["qa_folder_path"], f"{key}_select.csv")
        df_temp.to_csv(output_csv_path, index=False)

        # overwriting original df with processed df
        dfs[key] = df_temp


    # Call select_totals_columns after all _select.csv files are created
    raw_totals_df = select_totals_columns(config)

    # Convert counts to percentages
    percentages_df = convert_to_percentages(raw_totals_df)
    pre_processed_data_ew_ni_scot = percentages_df
    pre_processed_data_ew_ni_scot.to_csv(config["pre_clustering_data"], index=False)

    pre_clustering_std = standardize_dataframe(percentages_df)

    # Ensure QA directory exists
    os.makedirs(os.path.dirname(config["qa_folder_path"]), exist_ok=True)

    pre_processed_data_ew_ni_scot.to_csv(config["qa_folder_path"] + "pre_processed_data_ew_ni_scot.csv", index=False)

    # Save the standardized data to a new file
    pre_clustering_std.to_csv(config["pre_clustering_data_std_mean"], index=False)

    return pre_clustering_std

if __name__ == "__main__":
    # Example usage
    config = load_config('area_classification/config.yaml')
    ew_df = pd.read_csv('./data/inputs/LTLA_concat.csv')  
    ni_df = pd.read_csv('./data/inputs/LGD_concat.csv')
    scot_df = pd.read_csv('./data/inputs/CA19_concat.csv')

    processed_df = pre_processing(ew_df, ni_df, scot_df, config)
    print("pre-processing complete. Processed DataFrame shape:", processed_df.shape)