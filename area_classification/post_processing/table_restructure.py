#Table_restructure

# Post processing of the cluster assignments
import os
import pandas as pd
from utilities.load_config import load_config

def post_process_cluster_table(output_folder, file_name, keep_column, split_column):
    """
    Finds the cluster output, then keeps the data in one column (LAD_codes), and separates all
    characters in another column (cluster codes) into separate columns for supergroup, group, and 
    subgroup. Converts the final character in the subgroup column to a number (a=1, b=2, c=3, etc.).

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

    # Process the split_column to create the required columns
    supergroup = df[split_column].apply(lambda x: str(x)[0] if pd.notna(x) else "")
    group = df[split_column].apply(lambda x: str(x)[:2] if pd.notna(x) else "")
    subgroup = df[split_column].apply(lambda x: str(x) if pd.notna(x) else "")

    # Convert the final character in the subgroup column to a number
    def convert_final_char_to_number(value):
        if pd.notna(value) and len(value) > 0:
            final_char = value[-1].lower()
            if 'a' <= final_char <= 'z':  # Check if it's a letter
                return value[:-1] + str(ord(final_char) - ord('a') + 1)
        return value

    subgroup = subgroup.apply(convert_final_char_to_number)

    # Combine the kept column with the processed columns
    result_df = pd.concat([kept_data, supergroup.rename('supergroup'), group.rename('group'), subgroup.rename('subgroup')], axis=1)

    # Save the resulting DataFrame to a new file
    output_file = os.path.join(output_folder, f"Processed_{file_name}")
    result_df.to_csv(output_file, index=False)
    print(f"Processed file saved to: {output_file}")

    return result_df

# Example usage
config = load_config('area_classification/config.yaml')
output_folder = os.path.join(config["output_directory"], "/subgroup")
post_process_cluster_table(
    output_folder=output_folder, 
    file_name="subclustering_output.csv", 
    keep_column='LAD_code', 
    split_column='subsubcluster'
)

