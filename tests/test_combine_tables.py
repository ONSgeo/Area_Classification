import pandas as pd
import numpy as np
import pytest
from pandas.testing import assert_frame_equal
from area_classification.pre_processing.combine_tables import combine_table

# Test_1 - positive values, zero values, negative values, NaNs, duplicates
table1 = [
    [1, 0, -1],
    ["NaN", 5, 6]
]
 
table2 = [
    [1, 0, -1],
    [-1, 11, "NaN"]
]
 
table3 = [
    ["Belfast", 14, 15],
    ["Belfast", 14, 15]
]
result_tables123 = [
    [1, 0, -1],
    ["NaN", 5, 6],
    [1, 0, -1],
    [-1, 11, "NaN"],
    ["Belfast", 14, 15],
    ["Belfast", 14, 15]
]

# Test_2 with counts and strings
EnglWales = [
    ["City", "Females", "Males"],
    ["London", 2, 3],
    ["Manchester", 5, 6]
]

Scotland = [
    ["City", "Females","Males"],
    ["Edinburgh", 8, 9],
    ["Glasgow", 11, 12]
]
 
NI = [
    ["City", "Females", "Males"],
    ["Belfast", 14, 15]
]
results_UK = [
    ["City", "Females", "Males"],
    ["London", 2, 3],
    ["Manchester", 5, 6],
    ["City", "Females","Males"],
    ["Edinburgh", 8, 9],
    ["Glasgow", 11, 12],
    ["City", "Females", "Males"],
    ["Belfast", 14, 15]
]
# Test_3 with different row numbers and columns
table_A = [
    ["London", 2, 3, 4],
    ["Manchester", 5, 6, 7]
]
 
table_B = [
    ["Edinburgh", 9],
    ["Glasgow", 12]
]
 
table_C = [
    ["Belfast", 14, 15]
]
tablesABC = [
    ["London", 2, 3, 4],
    ["Manchester", 5, 6, 7],
    ["Edinburgh", 9],
    ["Glasgow", 12],
    ["Belfast", 14, 15]
]



UK_result = combine_table(EnglWales, Scotland, NI)
for row in UK_result:
    print(row)

def test_combine_tables_values():
    df_actual = combine_table(table1, table2, table3)
    assert_frame_equal(df_actual, result_tables123, check_dtype=False)

def test_combine_tables_strings_and_counts():
    df_actual = combine_table(EnglWales, Scotland, NI)
    assert_frame_equal(df_actual, results_UK, check_dtype=False)

def test_combine_tables_columns():
    df_actual = combine_table(table_A, table_B, table_C)
    assert_frame_equal(df_actual, tablesABC, check_dtype=False)
