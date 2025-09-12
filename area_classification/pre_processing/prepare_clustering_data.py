import pandas as pd
import numpy as np


def prepare_clustering_data(dataframe):
    """
    Wrapper function that applies standardization, arcsinh transformation,
    and min-max scaling to the input DataFrame.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame for clustering.

    Returns:
        pd.DataFrame: A new DataFrame with the transformed and standardized numeric values,
                      and the first column set as the index.
    """
    # Step 1: Standardize the data
    standardized_data = standardize_data(dataframe)

    # Step 2: Apply arcsinh transformation
    transformed_data = apply_arcsinh_transformation(standardized_data)

    # Step 3: Apply min-max scaling
    transformed_standardized_data = apply_min_max_scaling(transformed_data)

    return transformed_standardized_data


def standardize_data(dataframe):
    """
    Standardizes the numeric columns of the DataFrame by subtracting the mean
    and dividing by the standard deviation (z-score normalization).

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with standardized numeric columns.
    """
    standardized_data = dataframe.copy()
    for column in dataframe.columns[1:]:  # Skip the first column (e.g., area codes)
        mean = dataframe[column].mean()
        std = dataframe[column].std(ddof=0)  # Use population standard deviation
        if std != 0:  # Avoid division by zero
            standardized_data[column] = (dataframe[column] - mean) / std
        else:
            standardized_data[column] = 0  # If std is 0, set standardized values to 0
    return standardized_data


def apply_arcsinh_transformation(dataframe):
    """
    Applies the inverse hyperbolic sine (arcsinh) transformation to numeric columns.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with arcsinh-transformed numeric columns.
    """
    transformed_data = dataframe.copy()
    transformed_data.iloc[:, 1:] = np.arcsinh(transformed_data.iloc[:, 1:])
    return transformed_data


def apply_min_max_scaling(dataframe):
    """
    Applies min-max scaling to numeric columns, scaling values to the range [0, 1].

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with min-max scaled numeric columns.
    """
    scaled_data = dataframe.copy()
    scaled_data.iloc[:, 1:] = (scaled_data.iloc[:, 1:] - scaled_data.iloc[:, 1:].min()) / (
        scaled_data.iloc[:, 1:].max() - scaled_data.iloc[:, 1:].min()
    )
    return scaled_data


if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    pre_clustering_df_path = config["input_data_directory"] + "pre_clustering_data.csv"
    pre_clustering_df = pd.read_csv(pre_clustering_df_path)
    pre_clustering_df_std = prepare_clustering_data(pre_clustering_df)
    pre_clustering_df_std.to_csv(config["input_data_directory"] + "pre_clustering_data_std_normalized.csv", index=False)
  


 