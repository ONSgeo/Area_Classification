#Table_restructure

# Post processing of the cluster assignments
import os
import pandas as pd
from utilities.load_config import load_config

def post_process_cluster_table(config: dict,
                                output_folder: str,
                                file_name: str):
    """
    Finds the cluster output, then keeps the data in one column (LAD_codes), and separates all
    characters in another column (cluster codes) into separate columns for supergroup, group, and 
    subgroup. Converts the final character in the subgroup column to a number (a=1, b=2, c=3, etc.).

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and file names.
    output_folder : str
        Path to the folder containing the file.
    file_name : str
        Name of the file to process.
    Returns
    -------
    pd.DataFrame
        A DataFrame with the kept column and characters from the split column in custom-named columns.
    """
    
    keep_column= config["keep_column"]
    split_column= config["split_column"]

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

    # Load the LAD lookup file into a DataFrame
    lad_lookup_file_path = config["LAD_lookup_file_path"]
    lad_lookup = pd.read_csv(lad_lookup_file_path)

    # Add in the LAD names
    result_df = result_df.merge(
        lad_lookup[['LAD22CD', 'LAD22NM']],  # Select only the necessary columns
        left_on='LAD_code',                      # Column in result_df
        right_on='LAD22CD',                 # Column in lad_lookup
        how='left'                          # Use a left join to keep all rows in result_df
    )

    # Drop the LAD22CD column after the join if it's no longer needed
    result_df = result_df.drop(columns=['LAD22CD'])

    # Rename the LAD22NM column to LAD_name
    result_df = result_df.rename(columns={'LAD22NM': 'LAD_name'})

    # Move the LAD_name column to the first position
    columns = ['LAD_name'] + [col for col in result_df.columns if col != 'LAD_name']
    result_df = result_df[columns]

    # Save the resulting DataFrame to a new file
    output_file = os.path.join(output_folder, f"Processed_{file_name}")
    result_df.to_csv(output_file, index=False)
    print(f"Processed file saved to: {output_file}")

    return result_df

# Example usage
config = load_config('area_classification/config.yaml')
output_folder = os.path.join(config["output_directory"], "subgroup")
post_process_cluster_table(config,
    output_folder=output_folder, 
    file_name="subclustering_output.csv", 
)
