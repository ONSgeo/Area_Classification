# The following code is based on Jakub's script: https://github.com/jakubwyszomierski/OAC2021-2/blob/main/Scripts/Transforming_Census_data.R
# It has been translated from R into Python, and (will be) amended to include all UK countries, not just England and Wales.
# EW file referenced is from https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/disability/datasets/disabilityinenglandandwales2021
# TABLE 2 FOR OUTPUT AREAS OR TABLE 6 FOR LOCAL AUTHORITIES

# Expected input
# Area_code   |  age_group   |  Population  |  Disability_count
#---------------------------------------------------------------
# E06000001   |  0-14        |  1000        |  50
#             |              |              |

# ^^ Areas code for all of UK, age groups = 0_14_65_over and 15_64

import pandas as pd

def SIR_calculation(df):
    """
    Calculate the Standard Illness Ratio (SIR) for a given DataFrame containing disability data.
    
    Parameters:
        df (DataFrame): DataFrame containing columns 'Area_Code', 'Local_Authority', 'Count', 'Population',
        UK coverage
                        
    Returns:
        DataFrame: DataFrame with SIR values calculated.
    """

    
    # Get Ran (proportion of ill or disabled people for each age group at the national UK level)
    df_nat_summary = df.groupby('age_group').agg(
        sum_population=('Population', 'sum'),
        sum_disability_count=('total_disabled', 'sum')).reset_index()
 
    df_nat_summary['nat_prop'] = df_nat_summary['sum_disability_count'] / df_nat_summary['sum_population']


    # Join the national proportions back to the original DataFrame
    df = df.merge(df_nat_summary[['age_group', 'nat_prop']], on='age_group', how='left', suffixes=('', '_nat'))

    # Exp_ill for each age group (ill_prop * pop) 
    df['exp_ill'] = df['nat_prop'] * df['Population']    

    # Sum exp ill and diisability count (across age groups, to get one value per geog)
    df_all = df.groupby(['Area_Code', 'Local_Authority']).agg(exp_ill_all=('exp_ill', 'sum'),
                                                          disability_count=('total_disabled', 'sum')).reset_index()

    # Calculate SIR for each Area Code
    df_all['SIR'] = df_all.apply(lambda row: round((row['disability_count'] / row['exp_ill_all']) * 100, 4), axis=1)
    return df_all



EW_df = pd.read_excel("C:/Users/parkes/Downloads/ew_disability_age_group_temp.xlsx") 
EW_df.rename(columns={'Area Code': 'Area_Code'}, inplace=True)
EW_df.rename(columns={'Local Authority': 'Local_Authority'}, inplace=True)

x = SIR_calculation(EW_df)


























#import pandas as pd

# Read the Excel file containing the disability data from disabilitycensus2021.xlsx from the link in line 4, skips the first 4 rows (removes metadata. data starts on row 5)
#ill_prop_2021 = pd.read_excel("D:/Repos/Area_Classification/disabilitycensus2021.xlsx", sheet_name="Table 6", skiprows=4)
#print(ill_prop_2021.head())

# renaming columns using underscores instead of spaces
#ill_prop_2021.rename(columns={
#    'Local Authority': 'Local_Authority',
#    "Disability status": "Disability_status",
#    "Age-specific Percentage": "Age_specific_perc",
#    "Area Code": "Area_Code"
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

#agg_data = ill_prop_2021.groupby(['Area_Code', 'Local_Authority'])[['Count', 'Population']].sum().reset_index()
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











# aggregating the data to create count and sum of the data by 'Area_Code' and 'sir_age_band'
#ill_prop_2021 = ill_prop_2021.groupby(["Area_Code", "sir_age_band"]).agg(
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
