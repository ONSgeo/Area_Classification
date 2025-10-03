import pandas as pd

def compare_csvs(file1, file2):
    """
    Compare two CSV files for differences in headers, structure, and values.

    Args:
        file1 (str): Path to the first CSV file.
        file2 (str): Path to the second CSV file.

    Returns:
        dict: A dictionary containing the differences found.
    """
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    differences = {}

    # Compare headers
    if list(df1.columns) != list(df2.columns):
        differences['header_differences'] = {
            'file1_headers': list(df1.columns),
            'file2_headers': list(df2.columns)
        }

    # Compare shapes
    if df1.shape != df2.shape:
        differences['shape_differences'] = {
            'file1_shape': df1.shape,
            'file2_shape': df2.shape
        }

    # Compare values in matching columns
    common_columns = set(df1.columns).intersection(set(df2.columns))
    value_differences = {}
    for column in common_columns:
        # Normalize values to ignore '.0' differences
        col1 = df1[column].apply(lambda x: int(x) if isinstance(x, float) and x.is_integer() else x)
        col2 = df2[column].apply(lambda x: int(x) if isinstance(x, float) and x.is_integer() else x)

        # Compare normalized values
        if not col1.equals(col2):
            value_differences[column] = {
                'file1_values': col1.tolist(),
                'file2_values': col2.tolist()
            }

    if value_differences:
        differences['value_differences_in_common_columns'] = value_differences

    return differences

# Main script
if __name__ == "__main__":
    file1 = "D:/Area_Classification/data/inputs/CA19_concat.csv"
    file2 = "D:/Area_Classification/data/inputs/CA19_concat_pre_redownload.csv"

    differences = compare_csvs(file1, file2)

    if differences:
        print("Differences found:")
        for key, value in differences.items():
            print(f"{key}: {value}")
    else:
        print("The two CSV files are identical.")