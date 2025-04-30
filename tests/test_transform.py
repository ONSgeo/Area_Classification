from area_classification.analysis.transform import transform_and_standardize_data

# def test_____():

# def transform_and_standardize_data(df):
#     """
#     Apply data transformations to handle non-normality and scale the data:
#     1. Apply the inverse hyperbolic sine (arcsinh) transformation to reduce skewness.
#     2. Perform min-max scaling to normalize the data to a range of [0, 1].
    
#     Args:
#         df (pd.DataFrame): Input dataframe with numerical data to transform.
    
#     Returns:
#         pd.DataFrame: Transformed and standardized dataframe.
#     """
#     df = np.arcsinh(df) # Apply inverse hyperbolic sine transformation
#     df = (df - df.min()) / (df.max() - df.min()) # Apply min-max scaling
#     return df


import pandas as pd
import numpy as np
import pytest

# Are all values in output df between 0 and 1? No neg values
def test_min():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    })

    df2 = transform_and_standardize_data(df)

    assert(df2.min() >= 0).all()

def test_max():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    })

    df2 = transform_and_standardize_data(df)

    assert(df2.max() <= 1).all()


# What happens with any non-numeric columns?

def test_no_num_input():
    with pytest.raises(TypeError):  # Replace Exception with the specific exception type
        df = pd.DataFrame({
        'A': ['a', 'b', 'c'],
        'B': ['d', 'e', 'f'],
        'C': ['g', 'h', 'i']})

        transform_and_standardize_data(df)

# Does the function fail when you give it an input that isn't a pd df?
@pytest.mark.xfail(reason="Function has not been updated to raise value errors")
def test_null_values():
    with pytest.raises(ValueError):  # Replace Exception with the specific exception type
        # Write a dummy numpy array
         df = pd.DataFrame({
             'A': [np.nan],
             'B': [np.nan]})
         
         transform_and_standardize_data(df)





    