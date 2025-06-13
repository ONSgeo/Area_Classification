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
            "<16 and >=65": (df["lower_age_band"]<16)|(df["lower_age_band"]>=65),
            "16-64": (df["lower_age_band"]>=16) & (df["lower_age_band"]<65),
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

def convert_disability_age_group_northern_ireland(df: pd.DataFrame) -> pd.DataFrame:

    return df


if __name__ == "__main__":
    filepath = 'C:/Users/dayj1/Downloads/table_2025-06-11_15-20-42.xlsx'
    df = convert_disability_age_group_scotland(filepath)
    print(df)

    # print(all_sheets[first_key])
    # df = all_sheets[first_key].iloc[:-5]
    # df = df.rename(columns={"Unnamed: 1" : "Sex", "Unnamed: 2":"age_band"}).drop(columns= 'Disability')
    # df["sex"] = df["Sex"].ffill()
    # df["council_area"] = first_key.split(". ")[1]
    # df2 = df.loc[df["sex"] == "All people"].drop(columns = "Sex")
    # # Create a mapping dictionary from age_band values (excluding the first) to the specified numbers
    # age_band_list = df2["age_band"].tolist()[1:]
    # first_element_list = [int(s.split()[0]) if isinstance(s, str) and len(s.split()) > 0 else '' for s in age_band_list]
    # mapping_dictionary = dict(zip(age_band_list, first_element_list))
    # df2["lower_age_band"] = df2["age_band"].map(mapping_dictionary)
    # result_df = pd.DataFrame(columns=["local_authority", "age_band", "total_population","total_disabled"])
    # # Example: Append a new row to result_df
    # age_band_names_and_bools = {
    #     "<16 and >=65": (df2["lower_age_band"]<16)|(df2["lower_age_band"]>=65),
    #     "16-64": (df2["lower_age_band"]>=16) & (df2["lower_age_band"]<65),
    # }
    # for age_band_name, condition in age_band_names_and_bools.items():

    #     new_row = {
    #         "local_authority": first_key.split(". ")[1],
    #         "age_band": age_band_name,
    #         "total_population": df2.loc[df2["age_band"] == "Total", "All people"].values[0],
    #         "total_disabled": df2.loc[condition,"All people"].sum()
    #     }
    #     if 'result_df' not in locals():
    #         result_df = pd.DataFrame([new_row])
    #     else:
    #         result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)
    # print(result_df)


#### CURRENT ISSUE WITH SUMS AND TOTALS. THE TOTAL OF ALL AGE COLUMNS DOES NOT EQUAL TOTAL GIVEN IN DF


    # config = load_config()
    # england_wales_disability_age_filepath = config["england_wales_disability_age_filepath"]
    # convert_disability_age_group_england_wales(england_wales_disability_age_filepath)
    # scotland_disability_age_filepath = config["scotland_disability_age_filepath"]
    # northern_ireland_disability_age_filepath = config["northern_ireland_disability_age_filepath"]


