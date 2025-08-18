

def standardize_dataframe(dataframe):
    """
    Standardizes the columns of a DataFrame by calculating the z-scores for each column.
    Skips the first column (e.g., area codes) and avoids division by zero for columns with zero standard deviation.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame to standardize.

    Returns:
        pd.DataFrame: A new DataFrame with standardized values.
    """
    standardized_data = dataframe.copy()
    for column in dataframe.columns[1:]:  # Skip the first column (e.g., area codes)
        mean = dataframe[column].mean()
        std = dataframe[column].std()
        if std != 0:  # Avoid division by zero
            standardized_data[column] = (dataframe[column] - mean) / std
        else:
            standardized_data[column] = 0  # If std is 0, set standardized values to 0
    return standardized_data


if __name__ == "__main__":
    from utilities.load_config import load_config
    import pandas as pd
    config = load_config('area_classification/config.yaml')
    # Load the pre-clustering data into a DataFrame
    pre_clustering_df_path = config["input_data_directory"] + "pre_clustering_data.csv"
    pre_clustering_df = pd.read_csv(pre_clustering_df_path)
    re_clustering_df_std = standardize_dataframe(pre_clustering_df)
    re_clustering_df_std.to_csv(config["input_data_directory"] + "pre_clustering_data_std_mean.csv", index=False)
  


 