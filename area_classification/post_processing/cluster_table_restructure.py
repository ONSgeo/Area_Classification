# Restructuring of cluster assignments table
import os
import pandas as pd
from area_classification.utilities.load_config import load_config
config = load_config('area_classification/config.yaml')

def cluster_table_restructure(config, clustering_output):
    """
    Using the cluster output column one (LAD_codes) is kept, but column two containing cluster codes are 
    seperated out into seperate columns for supergroup, group, and subgroup. The final character in the 
    subgroup column is then converted to a number (a=1, b=2, c=3, etc.).

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and file names.
    clustering_output : pd.DataFrame
        DataFrame of cluster assignments which have been output from running the clustering algroithm. 
        Data will have the following format:
        
        LAD_code   | subsub cluster 
        ----------------------------
        S12000005  |  1c1
        
    Returns
    -------
    pd.DataFrame
        A DataFrame with the LAD_codes, followed by columsn for supergroup (number e.g. 1), group (number and 
        letter e.g. 1c) and subgroup (number letter number e.g. 1c1).
    """
    df = clustering_output

    # Reset the LAD_codes column so it is no longer an index and can be used to merge a table
    df = df.reset_index()

    keep_column= config["keep_column"]
    split_column= config["split_column"]
   
    # Check if the specified columns exist
    if keep_column not in df.columns:
        raise ValueError(f"Column '{keep_column}' not found in the dataframe.")
    if split_column not in df.columns:
        raise ValueError(f"Column '{split_column}' not found in the dataframe.")

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
    restructured_cluster_table = pd.concat([kept_data, supergroup.rename('supergroup'), group.rename('group'), subgroup.rename('subgroup')], axis=1)

    # Load the LAD lookup file into a DataFrame
    lad_lookup_file_path = config["LAD_lookup_file_path"]
    lad_lookup = pd.read_csv(lad_lookup_file_path)

    # Add in the LAD names
    restructured_cluster_table = restructured_cluster_table.merge(
        lad_lookup[['LAD22CD', 'LAD22NM']],  # Select only the necessary columns
        left_on='LAD_code',                      # Column in restructured_cluster_table
        right_on='LAD22CD',                 # Column in lad_lookup
        how='left'                          # Use a left join to keep all rows in restructured_cluster_table
    )

    # Drop the LAD22CD column after the join if it's no longer needed
    restructured_cluster_table = restructured_cluster_table.drop(columns=['LAD22CD'])

    # Rename the LAD22NM column to LAD_name
    restructured_cluster_table = restructured_cluster_table.rename(columns={'LAD22NM': 'LAD_name'})

    # Move the LAD_name column to the first position
    columns = ['LAD_name'] + [col for col in restructured_cluster_table.columns if col != 'LAD_name']
    restructured_cluster_table = restructured_cluster_table[columns]

    # Save the resulting DataFrame to a new file
    output_file = os.path.join(config["output_directory"], f"restructured_subclustering_output.csv")
    restructured_cluster_table.to_csv(output_file, index=False)
    print(f"Restructured file saved to: {output_file}")

    return restructured_cluster_table

if __name__ == "__main__":
    # Example usage
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    clustering_output_filepath = os.path.join(config["output_directory"], "subgroup", "subclustering_output.csv")
    clustering_output = pd.read_csv(clustering_output_filepath)
    cluster_table_restructure(config, clustering_output) 
