# Post processing of the cluster assignments
import os
import pandas as pd

def post_process_cluster_table(output_folder, file_name, keep_column, split_column):
    """
    Finds a the cluster output, then keeps the data in one column (LAD_codes), and separates all
    characters in another column (cluster codes) into seperate columns for supergroup, group and 
    subgroup.

    Parameters
    ----------
    output_folder : str
        Path to the folder containing the file.
    file_name : str
        Name of the file to process.
    keep_column : str
        Name of the column to keep as-is.
    split_column : str
        Name of the column to split into separate characters.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the kept column and characters from the split column in custom-named columns.
    """
    # Construct the file path
    file_path = os.path.join(output_folder, file_name)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_name}' not found in folder '{output_folder}'.")

    # Read the file into a DataFrame
    df = pd.read_csv(file_path)

    # Check if the specified columns exist
    if keep_column not in df.columns:
        raise ValueError(f"Column '{keep_column}' not found in the file '{file_name}'.")
    if split_column not in df.columns:
        raise ValueError(f"Column '{split_column}' not found in the file '{file_name}'.")

    # Keep the specified column
    kept_data = df[[keep_column]]

    # Split the characters in the specified column into separate columns
    split_data = df[split_column].apply(lambda x: list(str(x)))  # Ensure the value is treated as a string
    split_df = pd.DataFrame(split_data.tolist())

    # Rename the first three columns with custom names and the rest dynamically
    column_names = ['supergroup', 'group', 'subgroup'] + [f"char_{i+4}" for i in range(split_df.shape[1] - 3)]
    split_df.columns = column_names[:split_df.shape[1]]

    # Combine the kept column with the split columns
    result_df = pd.concat([kept_data, split_df], axis=1)

    # Convert 'subgroup' column values from letters to numbers (a=1, b=2, c=3, etc.)
    if 'subgroup' in result_df.columns:
        result_df['subgroup'] = result_df['subgroup'].str.lower().map(lambda x: ord(x) - ord('a') + 1 if isinstance(x, str) else x)

    # Save the resulting DataFrame to a new file
    output_file = os.path.join(output_folder, f"processed_{file_name}")
    result_df.to_csv(output_file, index=False)
    print(f"Processed file saved to: {output_file}")

    return result_df

# Example usage
output_folder = "D:/Repos/Area_Classification/data/output_data/subgroup"
post_process_cluster_table(
    output_folder=output_folder, 
    file_name="subgroups_clusteroutput.csv", 
    keep_column='LAD_code', 
    split_column='subsubcluster'
)

