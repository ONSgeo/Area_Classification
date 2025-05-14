# -*- coding: utf-8 -*-
"""
Created on Wed May 14 13:05:13 2025

@author: harrid3
"""

import pandas as pd
from typing import List, Optional, Union
from pathlib import Path
import os

def get_metadata_totals(metadataTable: pd.DataFrame, 
                        metadataTableID: str,
                        metadataVariableID: str,
                        additionalCols: Optional[List[str]] = None) -> pd.DataFrame:
    
    returnCols = [metadataVariableID] + additionalCols if additionalCols else [metadataVariableID]
    metadataTotals = metadataTable.groupby(metadataTableID)[returnCols].first()
    
    return metadataTotals.reset_index()

def get_csv_files(csvFolderPath: Union[str, Path],
                  metadataTotals: pd.DataFrame,
                  metadataTableID: str) -> List[str]:
    
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
                         ignoreVars: Optional[List[str]] = None):
        
    for file in csvFiles:
        
        tableName = file.replace('.csv','')
        
        table = pd.read_csv(os.path.join(csvFolderPath, file))
        csvMetadataTable = metadataTable[metadataTable[metadataTableID]==tableName]
        csvMetadataTotal = metadataTotals[metadataTotals[metadataTableID]==tableName]
        
        totalVar = csvMetadataTotal[metadataVariableID].values[0]
        tableVars = csvMetadataTable[metadataVariableID].to_list().remove(totalVar)
        allVars = [totalVar] + tableVars
        
        additionalVars = [col for col in table.columns if col not in allVars]
        
        #sense check (the length of additional vars should be 1 i.e. the geography itself)
        #raise an error if more are detected
        
        if len(additionalVars) > 1:
            raise ValueError(f"Additional variables {additionalVars} found in table {tableName}")
        
        for var in tableVars:
            
            if var not in ignoreVars:
            
                table[var] = table[var] / table[totalVar]
        
        outName = tableName + '_percentages.csv'
        table.to_csv(os.path.join(csvFolderPath, outName))
        
        
            
        
        
        
        
        
        
        
        
    
    








csvFiles = get_csv_files(r"C:\Users\harrid3\OneDrive - Office for National Statistics\Area_Classification\Downloading_data\EW_LAD",
                         test,
                         'Table_ID')





def transform_input_data( 
                    
                    metadataTotals: pd.DataFrame,
                    metadataTableID: str,
                    metadataTotalID: str,
                    scale100Cols: Optional[List[str]] = None, 
                    scale1Cols: Optional[List[str]] = None,
                    ignoreCols: Optional[List[str]] = None) -> pd.DataFrame:
    
    totalCols = metadataTable.groupby(metadataTableIDColname)[metadataVariableColname].first().reset_index()
    
    
