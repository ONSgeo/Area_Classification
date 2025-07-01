import pandas as pd
from area_classification.utilities.load_config import load_config

def define_age_bands_and_bools(df, lower_age_band_col="lower_age_band"):
     age_band_names_and_bools = {
            "<15 and >=65": (df[lower_age_band_col]<15)|(df[lower_age_band_col]>=65),
            "15-64": (df[lower_age_band_col]>=15) & (df[lower_age_band_col]<65),
        }
     return age_band_names_and_bools
     

def convert_disability_age_group_scotland(filepath:str, LAD_lookup_filepath:str) -> pd.DataFrame:
    """
    function to convert disability age group data from Scotland into a standard format.
    Data needs to be downloaded manually from Scotland Census website.

    Parameters
    ----------
    filepath : str
        filepath to the excel file containing the disability age group data.
    LAD_lookup_filepath : str
        filepath to the csv file containing the Local Authority Districts Names and CodesUK.

    Returns
    -------
    pd.DataFrame
        disability data combined into two age groups: "<15 and >=65" and "15-64".
        Columns: council_area, age_group, total_population, total_disabled.
    -----------
    Notes
    """    
    all_sheets = pd.read_excel(filepath, sheet_name=None,skiprows=11)
    for key in ["template_rse", "format"]:
        # Removing unwanted sheets from the dictionary
        all_sheets.pop(key, None)
    # Loop over each lad and dataframe to sum number of disabled in each age band
    for lad, df in all_sheets.items():
        df = df.iloc[:-5].rename(columns={"Unnamed: 1" : "Sex", "Unnamed: 2":"age_band"}).drop(columns= 'Disability')
        df["sex"] = df["Sex"].ffill()
        # Getting council area from the sheet name
        df["council_area"] = lad.split(". ")[1]
        df = df.loc[df["sex"] == "All people"].drop(columns = "Sex")
        # only needing all people not separated by sex 
        age_band_list = df["age_band"].tolist()[1:]
        first_element_list = [int(s.split()[0]) if isinstance(s, str) and len(s.split()) > 0 else '' for s in age_band_list]
        mapping_dictionary = dict(zip(age_band_list, first_element_list))
        df["lower_age_band"] = df["age_band"].map(mapping_dictionary)
        age_band_names_and_bools = define_age_bands_and_bools(df, lower_age_band_col="lower_age_band")
        limited_a_cols = [col for col in df.columns if "limited a" in str(col).lower()]
        for age_band_name, condition in age_band_names_and_bools.items():

            new_row = {
                "council_area": lad.split(". ")[1],
                "age_group": age_band_name,
                "total_population": df.loc[condition, "All people"].sum(),
                "total_disabled": df.loc[condition, limited_a_cols].sum(axis=1).sum()
            }
            if 'result_df' not in locals():
                result_df = pd.DataFrame([new_row])
            else:
                result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)

    # Load the LAD codes and names lookup file
    lookup_file_path = LAD_lookup_filepath

    # Load the LAD codes and names lookup file
    lookup_df = pd.read_csv(lookup_file_path)  # Assuming the file has headers
    lookup_dict = dict(zip(lookup_df['LAD22NM'].str.lower().str.strip(), lookup_df['LAD22CD']))  # Create a dictionary for lookup (place names -> place codes)

    # Strip spaces and convert to lowercase for consistent matching in the first column
    result_df.iloc[:, 0] = result_df.iloc[:, 0].str.strip().str.lower()

    # Replace values in the first column using the lookup dictionary
    result_df.iloc[:, 0] = result_df.iloc[:, 0].map(lookup_dict).fillna(result_df.iloc[:, 0])  # Replace matching values, keep original if no match

    return result_df

def convert_disability_age_group_england_wales(filepath: str) -> pd.DataFrame:
    """
    function to convert disability age group data from England and Wales into a standard format.
    Data needs to be downloaded manually from the Office for National Statistics website.

    Parameters
    ----------
    filepath : str
        path to downloaded excel file

    Returns
    -------
    pd.DataFrame
        disability data combined into two age groups: "<15 and >=65" and "15-64".
        Columns: Local Authority, Area Code, age_group, total_population, total_disabled.
    """    
    df_ew = pd.read_excel(filepath, sheet_name="Table 6", skiprows=4)
    df_ew = df_ew.loc[(df_ew["Sex"]=="Persons")&(df_ew["Category"] == "Two category")] # Only want persons and age bands, dont need gender
    df_ew = df_ew[["Year", "Local Authority", "Area Code", "Category", "Disability status", "Age","Count","Population"]]
    df_ew["Count"] = df_ew["Count"].replace({'[c]': 0, '[x]': 0})
    df_ew["Population"] = df_ew["Population"].replace({'[c]': 0, '[x]': 0})
    # Extract the first integer from the Age column for comparison
    df_ew["lower_age_band"] = df_ew["Age"].str.extract(r'(\d+)').astype(float)

    age_band_names_and_bools = define_age_bands_and_bools(df_ew, lower_age_band_col="lower_age_band")
    for age_band_name, condition in age_band_names_and_bools.items():
        df_ew.loc[condition, "age_group"] = age_band_name

    result_df_list = []
    for (geo_name, geo_code), group_df in df_ew.groupby(["Local Authority", "Area Code"]):
        for age_band_name, condition in age_band_names_and_bools.items():
            new_row = {
                "Area Code": geo_code,
                "Local Authority": geo_name,
                "age_group": age_band_name,
                "total_disabled": group_df.loc[
                    (group_df["age_group"] == age_band_name) &
                    (group_df["Disability status"] == "Disabled"),
                    "Count"
                ].astype(int).sum(),
                "total_population": group_df.loc[(group_df["age_group"] == age_band_name) , "Count"].sum()

            }
            result_df_list.append(new_row)
    return pd.DataFrame(result_df_list)

def convert_disability_age_group_northern_ireland(filepath:str) -> pd.DataFrame:
    """
    function to convert disability age group data from Northern Ireland into a standard format.
    Data needs to be downloaded manually from the Northern Ireland Statistics and Research Agency website.

    Parameters
    ----------
    filepath : str
        filepath to the excel file containing the disability age group data.

    Returns
    -------
    pd.DataFrame
        disability data combined into two age groups: "<15 and >=65" and "15-64".
        Columns: lgd_code, lgd, age_group, total_population, total_disabled.
    """    
    ni_df = pd.read_excel(filepath, sheet_name="LGD", skiprows=8).iloc[0:-14]
    ni_df.columns = ni_df.columns.str.replace('\n', '').str.lower()
    ni_df.columns = ni_df.columns.str.replace("usual residents aged ", "", regex=False)
    ni_df.columns = ni_df.columns.str.replace(r":\s*day-to-day activities\s*", " ", regex=True)
    ni_long_df = ni_df.melt(
        id_vars=["geography code", "geography"],
        var_name="age_disability_group",
        value_name="count"
    )
    ni_long_df["lower_age_band"] = ni_long_df["age_disability_group"].str.extract(r'(\d*)').replace('',None).astype(float)
    age_band_names_and_bools = {
            "<15 and >=65": (ni_long_df["lower_age_band"]<15)|(ni_long_df["lower_age_band"]>=65),
            "15-64": (ni_long_df["lower_age_band"]>=15) & (ni_long_df["lower_age_band"]<65),
        }
    disability_condition = ni_long_df["age_disability_group"].str.contains(r"limited a l.*", case=False, regex=True)
    non_disability_condition = ni_long_df["age_disability_group"].str.contains(r"not limited", case=False, regex=True)
    result_df_list = []
    for (geo_code, geo_name), group_df in ni_long_df.groupby(["geography code", "geography"]):
        for age_band_name, condition in age_band_names_and_bools.items():
            new_row = {
                "lgd_code": geo_code,
                "lgd": geo_name,
                "age_group": age_band_name,
                "total_disabled": group_df.loc[condition & disability_condition, "count"].sum(),
                "total_population": group_df.loc[condition & (disability_condition | non_disability_condition), "count"].sum()
            }
            result_df_list.append(new_row)
    result_df = pd.DataFrame(result_df_list)
    return result_df


if __name__ == "__main__":
    config = load_config('area_classification/config.yaml')
    LAD_lookup_file_path = (config["LAD_lookup_file_path"]) 
    filepath_scot = 'C:/Users/dayj1/Downloads/table_2025-06-11_15-20-42.xlsx'
    df_scot = convert_disability_age_group_scotland(filepath_scot, LAD_lookup_file_path)
    df_scot.to_csv(config["output_directory"]+"scot_disability_age_group.csv", index=False)
    print(df_scot)

    filepath_ni = "C:/Users/dayj1/Downloads/census-2021-ms-d02.xlsx"
    df_ni = convert_disability_age_group_northern_ireland(filepath_ni)
    df_ni.to_csv(config["output_directory"]+"ni_disability_age_group.csv", index=False)
    print(df_ni)

    filepath_ew = "disabilitycensus2021.xlsx"
    df_ew = convert_disability_age_group_england_wales(filepath_ew)
    df_ew.to_csv(config["output_directory"]+"ew_disability_age_group.csv", index=False)
    print(df_ew)
    print("all saved to csv")


#### CURRENT ISSUE WITH SUMS AND TOTALS. THE TOTAL OF ALL AGE COLUMNS DOES NOT EQUAL TOTAL GIVEN IN DF


    # config = load_config()
    # england_wales_disability_age_filepath = config["england_wales_disability_age_filepath"]
    # convert_disability_age_group_england_wales(england_wales_disability_age_filepath)
    # scotland_disability_age_filepath = config["scotland_disability_age_filepath"]
    # northern_ireland_disability_age_filepath = config["northern_ireland_disability_age_filepath"]


