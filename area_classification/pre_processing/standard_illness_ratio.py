# Expected input
# area_code   |  age_group   |  Population  |  Disability_count
#---------------------------------------------------------------
# E06000001   |  0-14        |  1000        |  50
#             |              |              |

# ^^ Areas code for all of UK, age groups = 0_14_65_over and 15_64

import pandas as pd
import os

from utilities.disability_age_group_conversion import (
    convert_disability_age_group_england_wales,
    convert_disability_age_group_northern_ireland,
    convert_disability_age_group_scotland,
)


def sir_processing(config):
    """
    Process disability data to calculate the Standard Illness Ratio (SIR) for each area code.

    Parameters
    -----------
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    pd.DataFrame
        DataFrame with SIR values calculated for each area code.
    """

    # disability files by age -> sharepoint?
    # Check if required files exist in the input directory
    required_files = [
        config["england_wales_disability_file"],
        config["ni_disability_file"],
        config["scotland_disability_file"]
    ]
    missing_files = []
    for file in required_files:
        file_path = os.path.join(config["input_data_directory"], file)
        if not os.path.isfile(file_path):
            missing_files.append(file)

    if config["england_wales_disability_file"] in missing_files:
        print(f"Warning: The file {config['england_wales_disability_file']} was not found in the input directory.")
        convert_disability_age_group_england_wales(config["input_data_directory"] + config["england_wales_disability_input"], config)
    if config["ni_disability_file"] in missing_files:
        print(f"Warning: The file {config['ni_disability_file']} was not found in the input directory.")
        convert_disability_age_group_northern_ireland(config["input_data_directory"] + config["ni_disability_input"], config)
    if config["scotland_disability_file"] in missing_files:
        convert_disability_age_group_scotland(config["input_data_directory"] + config["scotland_disability_input"], config)
        print(f"Warning: The file {config['scotland_disability_file']} was not found in the input directory.")        


        print(f"Warning: The following files were not found: {missing_files}")

    ew_disability_df = pd.read_csv(config["input_data_directory"]+config["england_wales_disability_file"])
    ni_disability_df = pd.read_csv(config["input_data_directory"]+config["ni_disability_file"])
    scotland_disability_df = pd.read_csv(config["input_data_directory"]+config["scotland_disability_file"])
    combined_disability_df = pd.concat(
        [ew_disability_df, ni_disability_df, scotland_disability_df])
    # Scotland excluded because it doesnt have council area codes 
    sir_output_df = SIR_calculation(combined_disability_df, config)
    return sir_output_df

def SIR_calculation(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate the Standard Illness Ratio (SIR) for a given DataFrame containing disability data.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame containing columns 'Area_Code', 'local_authority', 'age_group', 'Count', 'Population',
        UK coverage
                        
    Returns
    -------
    DataFrame
        DataFrame with SIR values calculated. Output is not grouped by age
    """

    
    # Get Ran (proportion of ill or disabled people for each age group at the national UK level)
    df_nat_summary = df.groupby('age_group').agg(
        sum_population=('total_population', 'sum'),
        sum_disability_count=('total_disabled', 'sum')).reset_index()
 
    df_nat_summary['nat_prop'] = df_nat_summary['sum_disability_count'] / df_nat_summary['sum_population']


    # Join the national proportions back to the original DataFrame
    df = df.merge(df_nat_summary[['age_group', 'nat_prop']], on='age_group', how='left', suffixes=('', '_nat'))

    # Exp_ill for each age group (ill_prop * pop) 
    df['exp_ill'] = df['nat_prop'] * df['total_population']    

    # Sum exp ill and diisability count (across age groups, to get one value per geog)
    df_all = df.groupby(['area_code']).agg(exp_ill_all=('exp_ill', 'sum'),
                                                          disability_count=('total_disabled', 'sum')).reset_index()

    # Calculate SIR for each Area Code
    df_all['SIR'] = df_all.apply(lambda row: round((row['disability_count'] / row['exp_ill_all']) * 100, 4), axis=1)

    # QA check the SIR dataframe before returning
    sir_qa_checks(df_all, config)
    print("SIR_DF_ALL", df_all.head())
    return df_all

def sir_qa_checks(df: pd.DataFrame, config: dict) -> None:
    """
    Perform QA checks on the SIR DataFrame.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame containing SIR values.
        
    Returns
    -------
        None
    """
    # Check if disability_count is int
    
    assert df['disability_count'].dtype == 'int64', "Disability count should be of type int64"

    # Check expected spatial distribution
    print("SIR values distribution:")
    print(df['SIR'].describe())

    for country_code_starts_with in [["E", "W"], ['S'], ['N']]:
        df_subset = df[df["area_code"].str.startswith(tuple(country_code_starts_with))]
        print(df_subset['SIR'].describe())

    # Ensure QA directory exists
    os.makedirs(os.path.dirname(config["qa_folder_path"]), exist_ok=True)

    # Save to data QA folder
    output_file_path = config["qa_folder_path"] + "sir_calculation_qa_output.csv"
    df.to_csv(output_file_path, index=False)

    # check that all records contain all of uk
    # Can add once we are working with all data
    # df["total_population"].sum() == sum(ew+scotland+ni)


if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    EW_df = pd.read_csv("data/inputs/ew_disability_age_group.csv") 
    EW_df.rename(columns={'Area Code': 'area_code'}, inplace=True)
    EW_df.rename(columns={'Local Authority': 'local_authority'}, inplace=True)

    x = sir_processing(config)
    sir_qa_checks(x)

# QA checks - Checked disability_count is int, checked SIR is %, Checked expected spatial distribution
# Reasonably sure this is correct, but will need to be check once we use combined UK data as input.





















#import pandas as pd

# Read the Excel file containing the disability data from disabilitycensus2021.xlsx from the link in line 4, skips the first 4 rows (removes metadata. data starts on row 5)
#ill_prop_2021 = pd.read_excel("D:/Repos/Area_Classification/disabilitycensus2021.xlsx", sheet_name="Table 6", skiprows=4)
#print(ill_prop_2021.head())

# renaming columns using underscores instead of spaces
#ill_prop_2021.rename(columns={
#    'Local Authority': 'local_authority',
#    "Disability status": "Disability_status",
#    "Age-specific Percentage": "Age_specific_perc",
#    "Area Code": "area_code"
#}, inplace=True)


#print(ill_prop_2021.columns)

# Filter and manipulate data
# selecting to include only 'persons' (not split by male/female), the 2-category for Category,
# and Status is 'Disabled'
#ill_prop_2021 = ill_prop_2021[
#    (ill_prop_2021["Sex"] == "Persons") &
#    (ill_prop_2021["Category"] == "Two category") &
#    (ill_prop_2021["Disability_status"] == "Disabled")
#]
#print(ill_prop_2021.head())

# create new column 'sir_age_band' for either "0-14 and 65+"" or "15-64"
#ill_prop_2021["sir_age_band"] = ill_prop_2021["Age"].apply(
#    lambda x: "0_14_65_over" if x in ["Under 1", "1 to 4", "5 to 9", "10 to 14",
#                                      "65 to 69", "70 to 74", "75 to 79",
#                                      "80 to 84", "85 to 89", "90+"] else "15_64"
#)

#print(ill_prop_2021.head() )

# deleting unnecessary columns (those not need for aggregation steps)
#ill_prop_2021 = ill_prop_2021.drop(columns=[
#    "Year", #"Local Authority", 
#    "Notes", 
#    "Lower 95% Confidence Interval", 
#    "Upper 95% Confidence Interval", "Category", "Age_specific_perc"
#])
#print(ill_prop_2021.head() )

# filter out the rows where there is a string ([c]) instead of a number
#ill_prop_2021 = ill_prop_2021[pd.to_numeric(ill_prop_2021['Count'], errors='coerce').notnull()]

# converting the columns to numeric (so next aggregation step works)
#ill_prop_2021['Count'] = pd.to_numeric(ill_prop_2021['Count'], errors='coerce')
#ill_prop_2021['Population'] = pd.to_numeric(ill_prop_2021['Count'], errors='coerce')


#################### CALCULATE SIR ###########################################
# Get Ii (observed count of disabled people in geography i)
# Get Pai (pop size of age group a in area i)

# Count = Ii; Population = Pai

#agg_data = ill_prop_2021.groupby(['area_code', 'local_authority'])[['Count', 'Population']].sum().reset_index()
#print(agg_data.head())

# Get ran (proportion of disabled people in group a (all age groups for now) at the national level)
# 
#nat_disabled_count = ill_prop_2021['Count'].sum()
#nat_pop = ill_prop_2021['Population'].sum()


#nat_disabled_prop = nat_disabled_count / nat_pop 

# Add value to ill+prop df
#agg_data['nat_prop_disabled'] = nat_disabled_prop

#print(nat_disabled_prop)
# Calculate SIR for each LAD (i)

# Count / Population * nat_prop_disabled
#agg_data['SIR'] = agg_data.apply(lambda row: round((row['Count'] / (row['nat_prop_disabled'] * row['Population'])) * 100, 4), axis=1)

# Check SIRs
#print(agg_data.sort_values(by='SIR', ascending=True).head(15))

## OUTPUT (check what output needs to look like)











# aggregating the data to create count and sum of the data by 'area_code' and 'sir_age_band'
#ill_prop_2021 = ill_prop_2021.groupby(["area_code", "sir_age_band"]).agg(
#    count=("Count", "sum"),
#    population=("Population", "sum")
#).reset_index()

#print(ill_prop_2021.head() )

# Create new ill_prop column
#ill_prop_2021["ill_prop"] = ill_prop_2021["count"] / ill_prop_2021["population"]

# Process data sets
# for dat in ["Census_2021_common_var", "Census_2021_oa_changed_common_var"]:
#     tab2 = globals()[dat].copy()
#     tab2["tot_0_14_65_over"] = (
#         tab2["NM_2020_1_1"] + tab2["NM_2020_1_2"] + tab2["NM_2020_1_3"] +
#         tab2["NM_2020_1_14"] + tab2["NM_2020_1_15"] + tab2["NM_2020_1_16"] +
#         tab2["NM_2020_1_17"] + tab2["NM_2020_1_18"]
#     )
#     tab2["tot_15_64"] = tab2["NM_2020_1_0"] - tab2["tot_0_14_65_over"]
#     tab2["Disabled"] = tab2["NM_2056_1_1"] + tab2["NM_2056_1_2"]
#     tab2 = tab2[["Geography_Code", "NM_2020_1_0", "tot_0_14_65_over", "tot_15_64", "Disabled"]]

#     # Calculate SIR values
#     # people within the SIR band (0-14 and 65+) with a disability divided by the total number of people in total population with a disability
#     # times 100 to get a percentage
#     ill_prop_0_14_65_over = ill_prop_2021.loc[ill_prop_2021["sir_age_band"] == "0_14_65_over", "ill_prop"].values[0]
#     ill_prop_15_64 = ill_prop_2021.loc[ill_prop_2021["sir_age_band"] == "15_64", "ill_prop"].values[0]

#     tab2["exp_ill_0_14_65_over"] = ill_prop_0_14_65_over * tab2["tot_0_14_65_over"]
#     tab2["exp_ill_15_64"] = ill_prop_15_64 * tab2["tot_15_64"]
#     tab2["exp_ill"] = tab2["exp_ill_0_14_65_over"] + tab2["exp_ill_15_64"]
#     tab2["SIR"] = round(tab2["Disabled"] / tab2["exp_ill"] * 100, 4)

#     SIR = tab2[["Geography_Code", "SIR"]]

#     # Merge SIR values back into the original data set
#     tab = pd.merge(globals()[dat], SIR, on="Geography_Code", how="outer")
#     globals()[dat] = tab

#     # Additional merging for other variables
#     if dat == "Census_2021_common_var":
#         Census_2021_common_var_prop = pd.merge(Census_2021_common_var_prop, SIR, on="Geography_Code", how="outer")
#     if dat == "Census_2021_oa_changed_common_var":
#         Census_2021_oa_changed_common_var_prop = pd.merge(Census_2021_oa_changed_common_var_prop, SIR, on="Geography_Code", how="outer")

#     # will need to repeat this for Scotland and NI data    
