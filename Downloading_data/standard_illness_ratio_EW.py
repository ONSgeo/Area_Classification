# The following code has been taken from Jakub's script: https://github.com/jakubwyszomierski/OAC2021-2/blob/main/Scripts/Transforming_Census_data.R
# It has been translated from R into Python
# This script will not run as the tables and headings are not standard 
# The file referenced is from https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/disability/datasets/disabilityinenglandandwales2021
# TABLE 2 FOR OUTPUT AREAS OR TABLE 6 FOR LOCAL AUTHORITIES


# we have run up to line 50 and this runs ok so far
# Line 50 - this line is trying to filter out the rows where there is a string ([c]) instead of a number



import pandas as pd

# Read the Excel file containing the disability data from disabilitycensus2021.xlsx from the link in line 4, skips the first 4 rows (removes metadata. data starts on row 5)
ill_prop_2021 = pd.read_excel("D:/Repos/Area_Classification/disabilitycensus2021.xlsx", sheet_name="Table 6", skiprows=4)
#print(ill_prop_2021.head())

# renaming columns using underscores instead of spaces
ill_prop_2021.rename(columns={
    "Disability status": "Disability_status",
    "Age-specific Percentage": "Age_specific_perc",
    "Area Code": "Area_Code"
}, inplace=True)

#print(ill_prop_2021.columns)

# Filter and manipulate data
# selecting to include only 'persons' (not split by male/female), the 2-category for Category,
# and Status is 'Disabled'
ill_prop_2021 = ill_prop_2021[
    (ill_prop_2021["Sex"] == "Persons") &
    (ill_prop_2021["Category"] == "Two category") &
    (ill_prop_2021["Disability_status"] == "Disabled")
]
#print(ill_prop_2021.head())

# create new column 'sir_age_band' for either "0-14 and 65+"" or "15-64"
ill_prop_2021["sir_age_band"] = ill_prop_2021["Age"].apply(
    lambda x: "0_14_65_over" if x in ["Under 1", "1 to 4", "5 to 9", "10 to 14",
                                      "65 to 69", "70 to 74", "75 to 79",
                                      "80 to 84", "85 to 89", "90+"] else "15_64"
)

#print(ill_prop_2021.head() )

# deleting unnecessary columns (those not need for aggregation steps)
ill_prop_2021 = ill_prop_2021.drop(columns=[
    "Year", "Local Authority", "Notes", 
    "Lower 95% Confidence Interval", 
    "Upper 95% Confidence Interval", "Category", "Age_specific_perc"
])
#print(ill_prop_2021.head() )

# filter out the rows where there is a string ([c]) instead of a number
ill_prop_2021 = ill_prop_2021[pd.to_numeric(ill_prop_2021['Count'], errors='coerce').notnull()]

# converting the columns to numeric (so next aggregation step works)
ill_prop_2021['Count'] = pd.to_numeric(ill_prop_2021['Count'], errors='coerce')
ill_prop_2021['Population'] = pd.to_numeric(ill_prop_2021['Count'], errors='coerce')

# aggregating the data to create count and sum of the data by 'Area_Code' and 'sir_age_band'
ill_prop_2021 = ill_prop_2021.groupby(["Area_Code", "sir_age_band"]).agg(
    count=("Count", "sum"),
    population=("Population", "sum")
).reset_index()

print(ill_prop_2021.head() )

# Create new ill_prop column
ill_prop_2021["ill_prop"] = ill_prop_2021["count"] / ill_prop_2021["population"]

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
