import pandas as pd
import os
import glob
from functools import reduce

def load_data(filepath):
    """
    Input some docstring here ....
    """
    input_df = pd.read_csv(filepath, index_col=0)
    
    # Check for missing values
    missing_values = input_df.isnull().sum().sum()
    if missing_values > 0:
        print(f"Warning: {missing_values} missing values found in input data. Missing values will be replaced with 0.")
        input_df.fillna(0, inplace=True)
    
    return input_df

def load_format_data(filepath:str, file_pattern:str, join_column_name:str) -> pd.DataFrame:
    """
    function to load and format data downloaded from API calls

    Parameters
    ----------
    filepath : str
        path to the directory containing the data files
    file_pattern : str
        pattern to match the files to be loaded, e.g. "ts*.csv" for England and Wales data
    join_column_name : str
        column name to join the dataframes on, e.g. "LTLA" for England and Wales data

    Returns
    -------
    pd.DataFrame
        A combined dataframe contaiing all data question codes and values for each geo code

    Raises
    ------
    FileNotFoundError
        raises error if no files matching the pattern are found in the given filepath
    ValueError
        raises error if the number of columns in the merged dataframe does not match the expected number
        expected number is the sum of columns in all files minus the join column which is only present in the first file
        (i.e. len(file_list) - 1)
    """    

    # load all of the data from the different tables, combine them into the format like example data 
    # first column will be geo code, others be questions and rows indicate responses 
    # Find all files matching the pattern "ts" followed by any three digits and ".csv" in the given filepath
    pattern = os.path.join(filepath, file_pattern)
    file_list = glob.glob(pattern)
    if not file_list:
        raise FileNotFoundError(f"No files matching {file_pattern} found in {filepath}")
    dfs = []
    # Read all files and store them in dfs
    num_columns = 0
    for file in file_list:
        df = pd.read_csv(file)
        num_columns += df.shape[1]
        dfs.append(df)
    num_columns -= (len(file_list) - 1) # removing the join column from count, only added in first df
    # Merge all dataframes on join_column_name column
    merged_df = reduce(lambda left, right: pd.merge(left, right, on=join_column_name, how='outer'), dfs)
    if num_columns != merged_df.shape[1]:
        raise ValueError(f"Expected {num_columns} columns, but got {merged_df.shape[1]} columns after merging.")

    return merged_df

if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config()
    filepath = "C:/Users/dayj1/Office for National Statistics/Geospatial - LAD_data_downloaded/EW_LAD"
    ew_df = load_format_data(filepath, config["england_wales_file_pattern"],config["england_wales_join_column_name"])
    # ew_df.to_csv("test_ew_concat.csv", index=False)

    filepath = "C:/Users/dayj1/Office for National Statistics/Geospatial - LAD_data_downloaded/NI_LAD"
    ni_df = load_format_data(filepath, config["ni_file_pattern"],config["ni_join_column_name"])
    ni_df.to_csv("ni_concat.csv", index=False)

