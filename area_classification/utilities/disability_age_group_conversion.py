import pandas as pd
from pathlib import Path

def define_age_bands_and_bools(df, lower_age_band_col="lower_age_band"):
     """
     Function to define age bands and their corresponding boolean conditions based on the lower age band column.

     Parameters
     ----------
        df : pd.DataFrame
            DataFrame containing the lower age band column.
        lower_age_band_col : str
            Name of the column containing the lower age band values.

    Returns
    -------
        dict
            Dictionary with age band names as keys and boolean conditions as values.

     """
     age_band_names_and_bools = {
            "<15 and >=65": (df[lower_age_band_col]<15)|(df[lower_age_band_col]>=65),
            "15-64": (df[lower_age_band_col]>=15) & (df[lower_age_band_col]<65),
        }
     return age_band_names_and_bools
     

      
def convert_disability_age_group_scotland(filepath:str, config: dict) -> pd.DataFrame:
    """
    Function to convert disability age group data from Scotland into a standard format,
    iterating based on council areas.
    As mentioned in the main README for this repo, disability data for Scotland needs to be downloaded manually 
    from the Scotland's Census Flexible Table Builder (UV303a) and saved into the 'data/inputs/scot_downloads folder.
    The file should be named 'UV303a.csv'.

    Output is written to a csv file in the input_directory

    Parameters
    ----------
    filepath : str
        filepath to the csv file containing the disability age group data.
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    pd.DataFrame
        disability data combined into two age groups: "<15 and >=65" and "15-64".
        Columns: council_area, age_group, total_population, total_disabled.
    
    """    

    # Read the CSV file
    # Specify number of columns to read from the CSV
    n = 6
    df = pd.read_csv(filepath, skiprows=10, header=1 ,  usecols=range(n))
    
    df.columns = ["A", "B", "C", "D", "E", "F"]

    # Initialize an empty DataFrame to store results
    result_df = pd.DataFrame()

    # Iterate through rows to extract relevant data
    for index, row in df.iterrows():
        if str(row.iloc[0]).strip().lower() == 'sex':  
            # Get the council area name
            if index == 0:
                # If the index is 0, set council_area to "Clackmannanshire" (as this CA was removed in skip rows reformat)
                council_area = "Clackmannanshire"  # Set to "Clackmannanshire" for index 1
            else:
                # If it's not the first one, instead get the area name from two rows above
                council_area = df.iloc[index - 2, 0] if index - 2 >= 0 else None  # Get value from two rows above

            
            # Ensure council_area is not None before proceeding
            if council_area is None:
                raise ValueError(f"Council area could not be determined at row {index}.")
            
            # Process the current council area
            sex_row_index = index
            
            # Keep only the 21 rows after the 'Sex' row (all people rows)
            council_df = df.iloc[sex_row_index + 1 : sex_row_index + 22].copy()
            
            # Rename columns for clarity
            council_df = council_df.rename(columns={'A': "Sex", 'B': "age_band"})
            
            # Extract 'age_band' column
            age_band_list = council_df["age_band"].tolist()[1:]
            
            # Extract the first number from each age band string
            first_element_list = [int(s.split()[0]) if isinstance(s, str) and len(s.split()) > 0 else '' for s in age_band_list]
            
            # Map each age band to its lower boundary
            mapping_dictionary = dict(zip(age_band_list, first_element_list))
            council_df["lower_age_band"] = council_df["age_band"].map(mapping_dictionary)
            
            # Select columns to convert to numeric
            columns_to_convert = council_df.columns[2:]  # Select all columns starting from the 3rd column onward

            # Convert the selected columns to numeric
            for col in columns_to_convert:
                council_df[col] = pd.to_numeric(council_df[col], errors="coerce")
            
            # Call the function to define age bands and conditions
            age_band_names_and_bools = define_age_bands_and_bools(council_df, lower_age_band_col="lower_age_band")

            # Define columns that contain 'limited a' in their name
            limited_a_cols = ["D", "E"]
    
            for age_band_name, condition in age_band_names_and_bools.items():
                new_row = {
                    "CA19": council_area,
                    "age_group": age_band_name,
                    "total_population": council_df.loc[condition, "C"].sum(),
                    "total_disabled": council_df.loc[condition, limited_a_cols].sum(axis=1).sum()
                }
                if 'result_df' not in locals():
                    result_df = pd.DataFrame([new_row])
                else:
                    result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)

    # Load the LAD codes and names lookup file
    lookup_file_path = config["LAD_lookup_file_path"]
    lookup_df = pd.read_csv(lookup_file_path)
    lookup_dict = dict(zip(lookup_df['LAD22NM'].str.lower().str.strip(), lookup_df['LAD22CD']))

    # Replace council area names with LAD codes
    result_df["CA19"] = result_df["CA19"].str.strip().str.lower().map(lookup_dict).fillna(result_df["CA19"])

    result_df.rename(columns={'CA19': 'area_code'}, inplace=True)
    output_path = Path(config["input_directory"]) / "scot_disability_age_group.csv"
    result_df.to_csv(output_path, index=False)

    return result_df

def convert_disability_age_group_england_wales(filepath: str, config: dict) -> pd.DataFrame:
    """
    function to convert disability age group data from England and Wales into a standard format.
    As mentioned in the main README for this repo, disability data for England and Wales needs to be downloaded 
    manually from the Office for National Statistics (ONS) website as it is not available in the bulk download. 
    It should have been manually saved into the 'data/inputs/ew_downloads folder. The file name should be 
    'disabilitycensus2021.xlsx'.

    Output is written to a csv file in the input_directory

    Parameters
    ----------
    filepath : str
        path to downloaded excel file
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    pd.DataFrame
        disability data combined into two age groups: "<15 and >=65" and "15-64".
        Columns: local_authority, area_code, age_group, total_population, total_disabled.
    """    
    df_ew = pd.read_excel(filepath, sheet_name="Table 6", skiprows=4)
    # Filter for persons and age bands; exclude gender breakdown
    df_ew = df_ew.loc[(df_ew["Sex"]=="Persons")&(df_ew["Category"] == "Two category")] 
    df_ew = df_ew[["Year", "Local Authority", "Area Code", "Category", "Disability status", "Age","Count","Population"]]
    df_ew = df_ew.rename(columns={"Local Authority": "local_authority", "Area Code": "area_code"})
    df_ew["Count"] = df_ew["Count"].replace({'[c]': 0, '[x]': 0})
    df_ew["Population"] = df_ew["Population"].replace({'[c]': 0, '[x]': 0})
    # Extract the first integer from the Age column for comparison
    df_ew["lower_age_band"] = df_ew["Age"].str.extract(r'(\d+)').astype(float)

    age_band_names_and_bools = define_age_bands_and_bools(df_ew, lower_age_band_col="lower_age_band")
    for age_band_name, condition in age_band_names_and_bools.items():
        df_ew.loc[condition, "age_group"] = age_band_name

    result_df_list = []
    for (geo_name, geo_code), group_df in df_ew.groupby(["local_authority", "area_code"]):
        for age_band_name, condition in age_band_names_and_bools.items():
            new_row = {
                "area_code": geo_code,
                "local_authority": geo_name,
                "age_group": age_band_name,
                "total_disabled": group_df.loc[
                    (group_df["age_group"] == age_band_name) &
                    (group_df["Disability status"] == "Disabled"),
                    "Count"
                ].astype(int).sum(),
                "total_population": group_df.loc[(group_df["age_group"] == age_band_name) , "Count"].sum()

            }
            result_df_list.append(new_row)

    result_df = pd.DataFrame(result_df_list)
    output_path = Path(config["input_directory"]) / "ew_disability_age_group.csv"
    result_df.to_csv(output_path, index=False)
        
    return result_df

def convert_disability_age_group_northern_ireland(filepath:str, config:dict) -> pd.DataFrame:
    """
    function to convert disability age group data from Northern Ireland into a standard format.
    As mentioned in the main README for this repo, disability data for Northern Ireland needs to be downloaded 
    manually from the Northern Ireland Statistics and Research Agency (NISRA) website as it is not available in
    the bulk download. It should have been manually saved into the 'data/inputs/ni_downloads folder. The file 
    should be named 'census-2021-ms-d02.xlsx'.
    Output is written to a csv file in the input_directory

    Parameters
    ----------
    filepath : str
        filepath to the excel file containing the disability age group data.
    config : str
        Configuration dictionary containing paths and file names.
        
    Returns
    -------
    pd.DataFrame
        disability data combined into two age groups: "<15 and >=65" and "15-64".
        Columns: lgd_code, lgd, age_group, total_population, total_disabled.
    """    

    # Read and preprocess the Excel file
    ni_df = pd.read_excel(filepath, sheet_name="LGD", skiprows=8).iloc[0:-14]
    ni_df.columns = ni_df.columns.str.replace('\n', '').str.lower()
    ni_df.columns = ni_df.columns.str.replace("usual residents aged ", "", regex=False)
    ni_df.columns = ni_df.columns.str.replace(r":\s*day-to-day activities\s*", " ", regex=True)

    # Reshape the DataFrame to long format
    ni_long_df = ni_df.melt(
        id_vars=["geography code", "geography"],
        var_name="age_disability_group",
        value_name="count"
    )

    # Extract lower age band from the group name
    ni_long_df["lower_age_band"] = ni_long_df["age_disability_group"].str.extract(r'(\d*)').replace('',None).astype(float)
    # Define age band conditions
    age_band_names_and_bools = {
            "<15 and >=65": (ni_long_df["lower_age_band"]<15)|(ni_long_df["lower_age_band"]>=65),
            "15-64": (ni_long_df["lower_age_band"]>=15) & (ni_long_df["lower_age_band"]<65),
        }
    
    disability_condition = ni_long_df["age_disability_group"].str.contains(r"limited a l.*", case=False, regex=True)
    non_disability_condition = ni_long_df["age_disability_group"].str.contains(r"not limited", case=False, regex=True)
    
    # Aggregate results for each area and age band
    result_df_list = []
    for (geo_code, geo_name), group_df in ni_long_df.groupby(["geography code", "geography"]):
        for age_band_name, condition in age_band_names_and_bools.items():
            new_row = {
                "area_code": geo_code,
                "local_authority": geo_name,
                "age_group": age_band_name,
                "total_disabled": group_df.loc[condition & disability_condition, "count"].sum(),
                "total_population": group_df.loc[condition & (disability_condition | non_disability_condition), "count"].sum()
            }
            result_df_list.append(new_row)

    # Create the result DataFrame and write to CSV        
    result_df = pd.DataFrame(result_df_list)
    output_path = Path(config["input_directory"]) / "ni_disability_age_group.csv"
    result_df.to_csv(output_path, index=False)
    return result_df


if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    LAD_lookup_file_path = (config["LAD_lookup_file_path"]) 
    
    df_scot = convert_disability_age_group_scotland(config["input_directory"] + config["scotland_disability_input"], config)
    df_scot.to_csv(config["input_directory"]+"scot_disability_age_group.csv", index=False)
    print(df_scot)

    df_ni = convert_disability_age_group_northern_ireland(config["input_directory"] + config["ni_disability_input"], config)
    df_ni.to_csv(config["input_directory"]+"ni_disability_age_group.csv", index=False)
    print(df_ni)

    df_ew = convert_disability_age_group_england_wales(config["input_directory"] + config["england_wales_disability_input"], config)
    df_ew.to_csv(config["input_directory"]+"ew_disability_age_group.csv", index=False)

    print(df_ew)
    print("all saved to csv")


