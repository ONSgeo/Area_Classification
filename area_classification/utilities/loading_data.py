import pandas as pd
import os
import glob
from functools import reduce
import logging

logger = logging.getLogger(__name__)

def load_data(filepath):
    """
    Function to load data from a CSV file and handle missing values.

    Parameters
    ----------
    filepath : str
        Path to the CSV file to be loaded.
    
    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the data from the CSV file.
    """
    input_df = pd.read_csv(filepath, index_col=0)
    
    # Check for missing values
    missing_values = input_df.isnull().sum().sum()
    if missing_values > 0:
        logger.warning(f"Warning: {missing_values} missing values found in input data. Missing values will be replaced with 0.")
        input_df.fillna(0, inplace=True)
    
    return input_df

def load_format_data(filepath:str, file_pattern:str, join_column_name:str, config: str) -> pd.DataFrame:
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
    config : dict
        main pipeline config dictionary containing output directory.

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
    
    # Raise an error if no files match the pattern
    if not file_list:
        raise FileNotFoundError(f"No files matching {file_pattern} found in {filepath}")
    
    # Initialize an empty list to store DataFrames
    dfs = []
    num_columns = 0
    
    # Read all files and store them in dfs
    for file in file_list:
        df = pd.read_csv(file)
        num_columns += df.shape[1]
        dfs.append(df)

    # removing the join column from count, only added in first df
    num_columns -= (len(file_list) - 1) 
    
    # Merge all dataframes on join_column_name column
    merged_df = reduce(lambda left, right: pd.merge(left, right, on=join_column_name, how='outer'), dfs)
    if num_columns != merged_df.shape[1]:
        raise ValueError(f"Expected {num_columns} columns, but got {merged_df.shape[1]} columns after merging.")
    
    # Write the DataFrame to a CSV file
    country_lad = join_column_name
    output_csv_path = os.path.join(config["input_data_directory"], f"{country_lad}_concat.csv")
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    merged_df.to_csv(output_csv_path, index=False)
    
    return merged_df

if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    ew_input_csv_path = os.path.join(config["input_data_directory"], "./ew_downloads/")
    ew_df = load_format_data(ew_input_csv_path, config["ew_file_pattern"],config["ew_join_column_name"], config)

    filepath = "C:/Users/dayj1/Office for National Statistics/Geospatial - LAD_data_downloaded/NI_LAD"
    ni_df = load_format_data(filepath, config["ni_file_pattern"],config["ni_join_column_name"])
    ni_df.to_csv("ni_concat.csv", index=False)

