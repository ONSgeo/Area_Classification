import numpy as np


def prepare_clustering_data(dataframe):
    """
    Wrapper function that applies standardization, arcsinh transformation,
    and min-max scaling to the numerical columns in the input DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The input DataFrame for clustering.

    Returns
    -------
    dataframe : pd.DataFrame
        A new DataFrame with the transformed and standardised numeric values,
        and the first column set as the index.
    """
    # Step 1: standardise the data
    standardised_data = standardise_data(dataframe)

    # Step 2: Apply arcsinh transformation
    transformed_data = apply_arcsinh_transformation(standardised_data)

    # Step 3: Apply min-max scaling
    transformed_standardised_data = apply_min_max_scaling(transformed_data)

    return transformed_standardised_data


def standardise_data(dataframe):
    """
    standardises the numeric columns of the DataFrame by subtracting the mean
    and dividing by the standard deviation (z-score normalization).

    Parameters
    ----------
    dataframe : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    dataframe : pd.DataFrame
        A DataFrame with standardised numeric columns.
    """
    standardised_data = dataframe.copy()
    # Skip the first column (e.g., area codes)
    for column in dataframe.columns[1:]:
        mean = dataframe[column].mean()
        # Use population standard deviation
        std = dataframe[column].std(ddof=0)
        # Avoid division by zero
        if std != 0:
            standardised_data[column] = (dataframe[column] - mean) / std
        else:
            # If std is 0, set standardised values to 0
            standardised_data[column] = 0
    return standardised_data


def apply_arcsinh_transformation(dataframe):
    """
    Applies the inverse hyperbolic sine (arcsinh) transformation to numeric values.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    dataframe : pd.DataFrame
        A DataFrame with arcsinh-transformed numeric columns.
    """
    transformed_data = dataframe.copy()
    transformed_data.iloc[:, 1:] = np.arcsinh(transformed_data.iloc[:, 1:])
    return transformed_data


def apply_min_max_scaling(dataframe):
    """
    Applies min-max scaling to numeric columns, scaling values to the range [0, 1].

    Parameters
    ----------
    dataframe : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    dataframe : pd.DataFrame
        A DataFrame with min-max scaled numeric columns.
    """
    scaled_data = dataframe.copy()
    scaled_data.iloc[:, 1:] = (scaled_data.iloc[:, 1:] - scaled_data.iloc[:, 1:].min()) / (
        scaled_data.iloc[:, 1:].max() - scaled_data.iloc[:, 1:].min()
    )
    return scaled_data
