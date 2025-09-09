import pandas as pd
import numpy as np 

def prepare_clustering_data(dataframe):
    """
    Standardizes the columns of a DataFrame by calculating the z-scores for each column.
    Skips the first column (e.g., area codes) and avoids division by zero for columns with zero standard deviation.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame to standardize with area codes in the first
        column followed by the percentage values of the chosen cluster variables.

    Returns:
        pd.DataFrame: A new DataFrame which has replaced the percentage values with standardized values.
    """

    standardized_data = dataframe.copy()
    for column in dataframe.columns[1:]:  # Skip the first column (e.g., area codes)
        mean = dataframe[column].mean()
        std = dataframe[column].std()
        if std != 0:  # Avoid division by zero
            standardized_data[column] = (dataframe[column] - mean) / std
        else:
            standardized_data[column] = 0  # If std is 0, set standardized values to 0

    # set the index as the first column
    standardized_data.set_index(standardized_data.columns[0], inplace=True)
    transformed_and_standardized_df = np.arcsinh(standardized_data) # Apply inverse hyperbolic sine transformation
    transformed_and_standardized_df = (transformed_and_standardized_df - transformed_and_standardized_df.min()) / (standardized_data.max() - standardized_data.min()) # Apply min-max scaling
   
    return transformed_and_standardized_df


if __name__ == "__main__":
    from utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    pre_clustering_df_path = config["input_data_directory"] + "pre_clustering_data.csv"
    pre_clustering_df = pd.read_csv(pre_clustering_df_path)
    re_clustering_df_std = prepare_clustering_data(pre_clustering_df)
    re_clustering_df_std.to_csv(config["input_data_directory"] + "pre_clustering_data_std_normalized.csv", index=False)
  


 