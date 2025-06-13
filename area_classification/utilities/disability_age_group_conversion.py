import pandas as pd
from area_classification.utilities.load_config import load_config


def convert_disability_age_group_scotland(filepath:str) -> pd.DataFrame:
    all_sheets = pd.read_excel(filepath, sheet_name=None,skiprows=11)
    for key in ["template_rse", "format"]:
        # Removing unwanted sheets from the dictionary
        all_sheets.pop(key, None)
    # Loop over each la and dataframe to sum number of disabled in each age band
    for la, df in all_sheets.items():
        df = df.iloc[:-5].rename(columns={"Unnamed: 1" : "Sex", "Unnamed: 2":"age_band"}).drop(columns= 'Disability')
        df["sex"] = df["Sex"].ffill()
        df["council_area"] = la.split(". ")[1]
        df = df.loc[df["sex"] == "All people"].drop(columns = "Sex")
        age_band_list = df["age_band"].tolist()[1:]
        first_element_list = [int(s.split()[0]) if isinstance(s, str) and len(s.split()) > 0 else '' for s in age_band_list]
        mapping_dictionary = dict(zip(age_band_list, first_element_list))
        df["lower_age_band"] = df["age_band"].map(mapping_dictionary)
        age_band_names_and_bools = {
            "<15 and >=65": (df["lower_age_band"]<15)|(df["lower_age_band"]>=65),
            "15-64": (df["lower_age_band"]>=15) & (df["lower_age_band"]<65),
        }
        for age_band_name, condition in age_band_names_and_bools.items():

            new_row = {
                "council_area": la.split(". ")[1],
                "age_group": age_band_name,
                "total_population": df.loc[df["age_band"] == "Total", "All people"].values[0],
                "total_disabled": df.loc[condition,"All people"].sum()
            }
            if 'result_df' not in locals():
                result_df = pd.DataFrame([new_row])
            else:
                result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)

    # need to load metadata table to convert council_area to code
    # Use Function to convert these.
    # scot_metadata = pd.read_csv("area_classification/downloading_data/")

    return result_df

def convert_disability_age_group_england_wales(df: pd.DataFrame) -> pd.DataFrame:

    return df

def convert_disability_age_group_northern_ireland(filepath:str) -> pd.DataFrame:
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
    result_df_list = []
    for (geo_code, geo_name), group_df in ni_long_df.groupby(["geography code", "geography"]):
        for age_band_name, condition in age_band_names_and_bools.items():
            new_row = {
                "lgd_code": geo_code,
                "lgd": geo_name,
                "age_group": age_band_name,
                "total_population": group_df.loc[group_df["age_disability_group"] == "all usual residents", "count"].values[0] if not group_df.loc[group_df["age_disability_group"] == "all usual residents", "count"].empty else None,
                "total_disabled": group_df.loc[condition & disability_condition, "count"].sum()
            }
            result_df_list.append(new_row)
    result_df = pd.DataFrame(result_df_list)
    return result_df


if __name__ == "__main__":
    filepath_scot = 'C:/Users/dayj1/Downloads/table_2025-06-11_15-20-42.xlsx'
    df_scot = convert_disability_age_group_scotland(filepath_scot)
    print(df_scot)

    filepath_ni = "C:/Users/dayj1/Downloads/census-2021-ms-d02.xlsx"
    df_ni = convert_disability_age_group_northern_ireland(filepath_ni)
    print(df_ni)


#### CURRENT ISSUE WITH SUMS AND TOTALS. THE TOTAL OF ALL AGE COLUMNS DOES NOT EQUAL TOTAL GIVEN IN DF


    # config = load_config()
    # england_wales_disability_age_filepath = config["england_wales_disability_age_filepath"]
    # convert_disability_age_group_england_wales(england_wales_disability_age_filepath)
    # scotland_disability_age_filepath = config["scotland_disability_age_filepath"]
    # northern_ireland_disability_age_filepath = config["northern_ireland_disability_age_filepath"]


