# -*- coding: utf-8 -*-
"""
Functions to transform CSV data.

Script Authors: Dan Harris, Jeremy Brocklehurst
"""

import pandas as pd
from typing import List, Optional, Union
from pathlib import Path
import os

def get_metadata_totals(metadataTable: pd.DataFrame, 
                        metadataTableID: str,
                        metadataVariableID: str,
                        additionalCols: Optional[List[str]] = None) -> pd.DataFrame:
    
    """
    This function returns a pandas dataframe of the Variable IDs (and additional columns passed)
    associated with the total column for each Table ID referenced in the metadata table.

    Parameters
    ----------
    metadataTable : pd.DataFrame
    A metadata table associated with a country data download
    metadataTableID : str
    ID referencing the Table IDs of the metadata table 
    metadataVariableID: str
    ID referencing the Variable IDs of the metadata table 
    additionalCols: Optional[List[str]]
    List of additional columns names to return from metadata table

    Returns
    -------
    pd.DataFrame
    Returns the Totals variable IDs for each Table ID in the metadata table

    Raises
    ------
    None
    
    """
    
    returnCols = [metadataVariableID] + additionalCols if additionalCols else [metadataVariableID]
    metadataTotals = metadataTable.groupby(metadataTableID)[returnCols].first()
    
    return metadataTotals.reset_index()

def get_csv_files(csvFolderPath: Union[str, Path],
                  metadataTotals: pd.DataFrame,
                  metadataTableID: str) -> List[str]:
    
    """
    This function returns a list of CSV files associated with the Metadata Table IDs passed.

    Parameters
    ----------
    csvFolderPath : Union[str, Path]
    Path to CSV file country data downloads
    metadataTotals : pd.DataFrame
    Table referencing Total Variable IDs for each Table ID (derived from get_metadata_totals)
    metadataTableID: str
    ID referencing the Table IDs of the metadata table 

    Returns
    -------
    csvFiles List[str]
    CSV filenames common to Metadata Table IDs

    Raises
    ------
    FileNotFoundError
    If Table ID not found in CSV folder path provided
    
    """
    
    csvFiles = os.listdir(csvFolderPath)
    metadataTables = metadataTotals[metadataTableID].values
    
    csvUtilityFunction = lambda string: string.replace('.csv','')
    
    tablesFound = [table for table in metadataTables if table in map(csvUtilityFunction, csvFiles)]
    tablesNotFound = [table for table in metadataTables if table not in map(csvUtilityFunction, csvFiles)]
    
    csvFiles = [table + '.csv' for table in tablesFound]
    
    if len(tablesNotFound):
        raise FileNotFoundError(f"Tables {tablesNotFound} not found in folder path")
            
    return csvFiles

def transform_input_data(csvFolderPath: Union[str, Path],
                         metadataTable: pd.DataFrame,
                         metadataTotals: pd.DataFrame,
                         metadataTableID: str,
                         metadataVariableID: str,
                         csvFiles: List[str],
                         ignoreVars: Optional[List[str]] = None) -> None:
    
    """
    This function scales variables with respect to the total person counts for each geography and
    creates CSV files with _percentages suffix.

    Parameters
    ----------
    csvFolderPath : Union[str, Path]
    Path to CSV file country data downloads
    metadataTable: pd.DataFrame
    A metadata table associated with a country data download
    metadataTotals : pd.DataFrame
    Table referencing Total Variable IDs for each Table ID (derived from get_metadata_totals)
    metadataTableID: str
    ID referencing the Table IDs of the metadata table 
    metadataVariableID: str
    ID referencing the Variable IDs of the metadata table
    csvFiles: List[str]
    CSV filenames common to Metadata Table IDs
    ignoreVars: Optional[List[str]]
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
        
    for file in csvFiles:
        
        tableName = file.replace('.csv','')
                
        table = pd.read_csv(os.path.join(csvFolderPath, file))
        csvMetadataTable = metadataTable[metadataTable[metadataTableID]==tableName]
        csvMetadataTotal = metadataTotals[metadataTotals[metadataTableID]==tableName]
        
        totalVar = csvMetadataTotal[metadataVariableID].values[0]
        tableVars = csvMetadataTable[metadataVariableID].to_list()
        tableVars.remove(totalVar)
        
        allVars = [totalVar] + tableVars
        
        additionalVars = [col for col in table.columns if col not in allVars]
        
        ignoreVars = [] if not ignoreVars else ignoreVars
        
        #sense check (the length of additional vars should be 1 i.e. the geography itself)
        #raise an error if more are detected
        
        if len(additionalVars) > 1:
            raise ValueError(f"Additional variables {additionalVars} found in table {tableName}")
            
        for var in tableVars:
            
            if var not in ignoreVars:
            
                table[var] = table[var] / table[totalVar]
        
        outName = tableName + '_percentages.csv'
        table.to_csv(os.path.join(csvFolderPath, outName), index = None)
        
#Ask Ella/Tyde for which variable names to exclude for processing from each of 
# EW LAD, NI LGD, SCOT CA        

        
        