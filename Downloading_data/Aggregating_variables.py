import pandas as pd

#Aggregating ages for England and Wales
def ag_columns(df, col_names, new_col_name):
    """
    This function takes a dataframe, a list of column names, and a new column name as input.
    It sums the values of the specified columns and stores the result in the new column.
    """
    # Create a copy of the dataframe to avoid modifying the original
    df_copy = df.copy()
    
    # Sum the values of the specified columns and store the result in the new column
    df_copy[new_col_name] = df_copy[col_names].sum(axis=1)
    
    # Return the modified dataframe
    return df_copy

 # Create a dataframe
df = pd.DataFrame({'col_1': [1, 1, 2, 2, 5],
                'col_2': [6, 7, 8, 9, 10],
                'col_3': [20, 30, 40, 50, 60]})
print(df)
# Call the ag_columns() function
aggregated_df = ag_columns(df, ['col_1', 'col_2', 'col_3'], 'col_4_total')

print(aggregated_df)

#table = "C:/Users/goodme/Office for National Statistics/Geospatial - NI_LAD/ni001.csv"
#df1 = pd.read_csv(table)
#print(df1)

# NI AGES
table = "C:/Users/goodme/Office for National Statistics/Geospatial - NI_LAD/ni012.csv"
age_table = pd.read_csv(table)
print(age_table)

# Select the columns to aggregate
#age 5 to 14
age_table = ag_columns(age_table, ['ni0120003', 'ni0120004'], 'age_5_14')
print(age_table)
#age 25 to 44 
age_table = ag_columns(age_table, ['ni0120007', 'ni0120008', 'ni0120009', 'ni0120010'], 'age_25_44')
print(age_table)
#age 45 to 64
age_table = ag_columns(age_table, ['ni0120011', 'ni0120012', 'ni0120013', 'ni0120014'], 'age_45_64')
print(age_table)
#age 65 to 84
age_table = ag_columns(age_table, ['ni0120015', 'ni0120016', 'ni0120017', 'ni0120018'], 'age_65_84')
print(age_table)

# separated_divorced
# dependant_children
# cannot_speak_English
# provides_unpaid_care
# flat
# cars_2_or_more
# under_occupation
# overcrowding
# ownership_or_shared
# level_1_2_and_appr