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