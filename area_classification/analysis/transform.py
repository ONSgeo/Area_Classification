import numpy as np
import pandas as pd

def transform_and_standardize_data(df):
    """
    Apply data transformations to handle non-normality and scale the data:
    1. Apply the inverse hyperbolic sine (arcsinh) transformation to reduce skewness.
    2. Perform min-max scaling to normalize the data to a range of [0, 1].
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with numerical data to transform.
    
    Returns
    -------
    pd.DataFrame
        Transformed and standardized dataframe.
    """
    df = np.arcsinh(df) # Apply inverse hyperbolic sine transformation
    df = (df - df.min()) / (df.max() - df.min()) # Apply min-max scaling
    return df