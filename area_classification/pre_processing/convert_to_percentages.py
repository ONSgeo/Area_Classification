# -*- coding: utf-8 -*-
"""
Functions to transform and validate CSV data.

Script Name: Area Classification - Convert to Percentages Functions
Script Author: Dan Harris
Collaborators: Jeremy Brocklehurst
Script Purpose: Contains processing and validation functions to
                convert required columns as percentage of total column
"""

import pandas as pd
from typing import List, Optional, Union
from pathlib import Path
import os

def get_metadata_totals(metadata_table: pd.DataFrame,
                        metadata_table_id: str,
                        metadata_variable_id: str,
                        additional_cols: Optional[List[str]] = None) -> pd.DataFrame:
    
    """
    This function returns a pandas dataframe of the Variable IDs (and additional columns passed)
    associated with the total column for each Table ID referenced in the metadata table.
    
    Parameters
    ----------
    metadata_table : pd.DataFrame
        A metadata table associated with a country data download
    metadata_table_id : str
        ID referencing the Table IDs of the metadata table 
    metadata_variable_id: str
        ID referencing the Variable IDs of the metadata table 
    additional_cols: Optional[List[str]]
        List of additional columns names to return from metadata table
    
    Returns
    -------
    pd.DataFrame
        Returns the Totals variable IDs for each Table ID in the metadata table
    
    Raises
    ------
    None
    
    """
    
    return_cols = [metadata_variable_id] + additional_cols if additional_cols else [metadata_variable_id]
    metadata_totals = metadata_table.groupby(metadata_table_id)[return_cols].first()
    
    return metadata_totals.reset_index()

def get_csv_files(csv_folder_path: Union[str, Path],
                  metadata_totals: pd.DataFrame,
                  metadata_table_id: str) -> List[str]:
    
    """
    This function returns a list of CSV files associated with the Metadata Table IDs passed.
    
    Parameters
    ----------
    csv_folder_path : Union[str, Path]
        Path to CSV file country data downloads
    metadata_totals : pd.DataFrame
        Table referencing Total Variable IDs for each Table ID (derived from get_metadata_totals)
    metadata_table_id: str
        ID referencing the Table IDs of the metadata table 
    
    Returns
    -------
    csv_files List[str]
        CSV filenames common to Metadata Table IDs
    
    Raises
    ------
    FileNotFoundError
        If Table ID not found in CSV folder path provided
    
    """
    
    csv_files = os.listdir(csv_folder_path)
    metadata_tables = metadata_totals[metadata_table_id].values
    
    csv_utility_function = lambda string: string.replace('.csv', '')
    
    tables_found = [table for table in metadata_tables if table in map(csv_utility_function, csv_files)]
    tables_not_found = [table for table in metadata_tables if table not in map(csv_utility_function, csv_files)]
    
    csv_files = [table + '.csv' for table in tables_found]
    
    if len(tables_not_found):
        raise FileNotFoundError(f"Tables {tables_not_found} not found in folder path")
            
    return csv_files

def transform_input_data(csv_folder_path: Union[str, Path],
                         metadata_table: pd.DataFrame,
                         metadata_totals: pd.DataFrame,
                         metadata_table_id: str,
                         metadata_variable_id: str,
                         csv_files: List[str],
                         ignore_vars: Optional[List[str]] = None) -> None:
    
    """
    This function scales variables with respect to the total person counts for each geography and
    creates CSV files with _percentages suffix.
    
    Parameters
    ----------
    csv_folder_path : Union[str, Path]
        Path to CSV file country data downloads
    metadata_table: pd.DataFrame
        A metadata table associated with a country data download
    metadata_totals : pd.DataFrame
        Table referencing Total Variable IDs for each Table ID (derived from get_metadata_totals)
    metadata_table_id: str
        ID referencing the Table IDs of the metadata table 
    metadata_variable_id: str
        ID referencing the Variable IDs of the metadata table
    csv_files: List[str]
        CSV filenames common to Metadata Table IDs
    ignore_vars: Optional[List[str]]
        Variable IDs not to scale
    
    Returns
    -------
    None
    
    Raises
    ------
    ValueError
        If additional Variable IDs are present (besides geography) 
        in CSV file that are not present in metadata table.
    
    """
        
    for file in csv_files:
        
        table_name = file.replace('.csv', '')
        
        print(f"Processing {table_name}...")
                
        table = pd.read_csv(os.path.join(csv_folder_path, file))
        csv_metadata_table = metadata_table[metadata_table[metadata_table_id] == table_name]
        csv_metadata_total = metadata_totals[metadata_totals[metadata_table_id] == table_name]
        
        total_var = csv_metadata_total[metadata_variable_id].values[0]
        table_vars = csv_metadata_table[metadata_variable_id].to_list()
        table_vars.remove(total_var)
        
        all_vars = [total_var] + table_vars
        
        additional_vars = [col for col in table.columns if col not in all_vars]
        
        ignore_vars = [] if not ignore_vars else ignore_vars
        
        # sense check (the length of additional vars should be 1 i.e. the geography itself)
        # raise an error if more are detected
        
        if len(additional_vars) > 1:
            raise ValueError(f"Additional variables {additional_vars} found in table {table_name}")
            
        for var in table_vars:
            
            if var not in ignore_vars:
            
                table[var] = 100 * table[var] / table[total_var]
                table[var] = table[var].fillna(0)
                table[var] = table[var].apply(lambda x: round(x, 3))
        
        out_name = table_name + '_percentages.csv'
        table.to_csv(os.path.join(csv_folder_path, out_name), index=None)
        
        print(f"{table_name} converted to percentage of total variable")
        
def validate_output(csv_folder_path: Union[str, Path],
                    metadata_table: pd.DataFrame,
                    metadata_totals: pd.DataFrame,
                    metadata_table_id: str,
                    metadata_variable_id: str,
                    ignore_vars: Optional[List[str]] = None) -> None:
    
    """
    This function validates the output produced by transform_input_data by checking all
    required variables are within range [0,100].
    
    Parameters
    ----------
    csv_folder_path : Union[str, Path]
        Path to CSV file country data downloads
    metadata_table: pd.DataFrame
        A metadata table associated with a country data download
    metadata_totals : pd.DataFrame
        Table referencing Total Variable IDs for each Table ID (derived from get_metadata_totals)
    metadata_table_id: str
        ID referencing the Table IDs of the metadata table 
    metadata_variable_id: str
        ID referencing the Variable IDs of the metadata table
    ignore_vars: Optional[List[str]]
        Variable IDs not to scale
    
    Returns
    -------
    None
    
    Raises
    ------
    ValueError
        If variable values are outside [0,100] range
    
    """
    
    processed_csv_files = [file for file in os.listdir(csv_folder_path) if '_percentages.csv' in file]
    
    for file in processed_csv_files:
        
        table_name = file.replace('_percentages.csv', '')
                
        table = pd.read_csv(os.path.join(csv_folder_path, file))
        csv_metadata_table = metadata_table[metadata_table[metadata_table_id] == table_name]
        csv_metadata_total = metadata_totals[metadata_totals[metadata_table_id] == table_name]
        
        total_var = csv_metadata_total[metadata_variable_id].values[0]
        table_vars = csv_metadata_table[metadata_variable_id].to_list()
        table_vars.remove(total_var)
        
        ignore_vars = [] if not ignore_vars else ignore_vars

        for var in table_vars:
            
            if var not in ignore_vars:
                
                if not ((table[var].all() >= 0) and (table[var].all() <= 100)):
                    raise ValueError(f"Column {var} in {file} file contains values outside range [0,100]")
        
    print("CSV files validated")
    
# def convert_to_percentages(metadata_filepath: Union[str, Path],
#                            metadata_table_id: str,
#                            metadata_variable_id: str,
#                            csv_folder_path: Union[str, Path],
#                            ignore_scaling_vars:  Optional[List[str]] = None) -> None:
    
#     """
#     This function converts variables to percentages of total counts and outputs the
#     CSVs to same directory as csv_folder_path with _percentages suffix.
    
#     Parameters
#     ----------
#     metadata_filepath : Union[str, Path]
#         Path to metadata CSV file
#     metadata_table_id: str
#         Table ID associated with metadata
#     metadata_variable_id: str
#         Variable ID associated with metadata
#     csv_folder_path: Union[str, Path]
#         Path to folder containing CSV data
#     ignore_scaling_vars: Optional[List[str]]
#         Variables to ignore when scaling
    
#     Returns
#     -------
#     None
    
#     Raises
#     ------
#     ValueError
#         If additional Variable IDs are present (besides geography) 
#         in CSV file that are not present in metadata table.
#     ValueError
#         If variable values are outside [0,100] range
#     FileNotFoundError
#         If Table ID not found in CSV folder path provided
    
#     """
    
#     metadata_table = pd.read_csv(metadata_filepath)
    
#     metadata_totals = get_metadata_totals(metadata_table = metadata_table,
#                                           metadata_table_id = metadata_table_id,
#                                           metadata_variable_id = metadata_variable_id)
    
#     csv_files = get_csv_files(csv_folder_path = csv_folder_path,
#                               metadata_totals = metadata_totals,
#                               metadata_table_id = metadata_table_id)

#     transform_input_data(csv_folder_path = csv_folder_path,
#                          metadata_table = metadata_table,
#                          metadata_totals = metadata_totals,
#                          metadata_table_id = metadata_table_id,
#                          metadata_variable_id = metadata_variable_id,
#                          csv_files = csv_files)
    
#     validate_output(csv_folder_path = csv_folder_path,
#                     metadata_table = metadata_table,
#                     metadata_totals = metadata_totals,
#                     metadata_table_id = metadata_table_id,
#                     metadata_variable_id = metadata_variable_id)  

#--------------------- example -------------------#


def convert_to_percentages(df:pd.DataFrame, area_code_column_name: str) -> pd.DataFrame:

    # Get list of column names
    col_names = df.columns.tolist()
    # Remove the last 4 digits from each column name (if present)
    base_names = [col[:-4] if col[-4:].isdigit() else col for col in col_names]
    # Get unique values
    unique_base_names = sorted([name for name in set(base_names) if name != area_code_column_name])
    total_code_suffix = "0001"  # Assuming the total column ends with '0001'
    for form_code in unique_base_names:
        total_column_name = form_code + total_code_suffix
        df["temp_copy_column"] = df[total_column_name]  # Create a temporary copy of the total column
        if total_column_name not in df.columns:
            raise ValueError(f"Total column '{total_column_name}' not found in DataFrame.")
        # Calculate percentages for each column
        for col in df.columns:  
            if col.startswith(form_code):
                # Calculate percentage of the total column
                df[col] = (df[col] / df["temp_copy_column"]) * 100
                # Fill NaN values with 0
                df[col] = df[col].fillna(0)
                # Round to 3 decimal places
                # df[col] = df[col].round(3)
    df.drop(columns=["temp_copy_column"], inplace=True)  # Remove the temporary column

    # Check that all values are within [0, 100]
    for col in df.columns:
        if col != area_code_column_name:
            if not ((df[col] >= 0).all() and (df[col] <= 100).all()):
                raise ValueError(f"Column {col} contains values outside the range [0, 100]")
            
    return df
    
    
if __name__ == "__main__":
    # Example usage

    example_data = pd.read_csv("ew_concat.csv")
    # format of combined data is ts???001 will be total,

    df = convert_to_percentages(
       example_data,
       area_code_column_name = "LTLA"  # Assuming 'LTLA' is the area code column name
    )
    print(df)


