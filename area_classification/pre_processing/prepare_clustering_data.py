import pandas as pd
import numpy as np 

def prepare_clustering_data(dataframe):
    """
    Transforms and standardizes the input DataFrame for clustering.
    This function creates standardized means per varaible column
    followed by an inverse hyperbolic sine transformation and min-max scaling.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame for clustering

    Returns:
        pd.DataFrame: A new DataFrame with the transformed and standardized numeric values,
                      and the first column set as the index.
    """

    standardized_data = dataframe.copy()
    for column in dataframe.columns[1:]:  # Skip the first column (e.g., area codes)
        mean = dataframe[column].mean()
        std = dataframe[column].std()
        if std != 0:  # Avoid division by zero
            standardized_data[column] = (dataframe[column] - mean) / std
        else:
            standardized_data[column] = 0  # If std is 0, set standardized values to 0

   # Apply inverse hyperbolic sine transformation to all columns except the first
    standardized_data.iloc[:, 1:] = np.arcsinh(standardized_data.iloc[:, 1:])

    # Apply min-max scaling to all columns except the first
    standardized_data.iloc[:, 1:] = (standardized_data.iloc[:, 1:] - standardized_data.iloc[:, 1:].min()) / (
        standardized_data.iloc[:, 1:].max() - standardized_data.iloc[:, 1:].min()
    )

    # The first column remains untouched, and the transformations are applied in place to the numeric columns.
    transformed_and_standardized_df = standardized_data

    return transformed_and_standardized_df


if __name__ == "__main__":
    from utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    pre_clustering_df_path = config["input_data_directory"] + "pre_clustering_data.csv"
    pre_clustering_df = pd.read_csv(pre_clustering_df_path)
    re_clustering_df_std = prepare_clustering_data(pre_clustering_df)
    re_clustering_df_std.to_csv(config["input_data_directory"] + "pre_clustering_data_std_normalized.csv", index=False)
  


 