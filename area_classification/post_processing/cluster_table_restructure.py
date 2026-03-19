# Restructuring of cluster assignments table
import os

import pandas as pd

from area_classification.utilities.load_config import load_config

config = load_config("area_classification/config.yaml")


def cluster_table_restructure(
    config, clustering_output, split_column, keep_column, standardised_data
):
    """
    Using the cluster output column one (LAD_codes) is kept, but column two containing
    cluster codes are separated out into seperate columns for supergroup, group, and
    subgroup. The final character in the subgroup column is then converted to a number
    (a=1, b=2, c=3, etc.).

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and file names.
    split_column : str
        The column header which the table will be split on
    keep_column : str
        The column header which will be kept in the final output
    clustering_output : pd.DataFrame
        DataFrame of cluster assignments which have been output from running the
        clustering algorithm.
        Data will have the following format:

        LAD_code   | subsub cluster
        ----------------------------
        S12000005  |  1ca

    Returns
    -------
    tuple of pd.DataFrame
        (restructured_cluster_table, restructured_cluster_table_long)
        - restructured_cluster_table: DataFrame with LAD_code, supergroup, group,
        subgroup, and LAD_name.
        - restructured_cluster_table_long: Merged DataFrame with standardised
        data for summaries.
    """

    # Reset the LAD_codes column so it is no longer an index and can be used to merge a table
    df = clustering_output.reset_index()

    # Change the cluster number 0 to 6 (Python indexes to 0, but for cluster number we need 1 to 6)
    for col in ["cluster", "subcluster", "subsubcluster"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"^0", "6", regex=True)

    # Check if the specified columns exist
    if keep_column not in df.columns:
        raise ValueError(f"Column '{keep_column}' not found in the dataframe.")
    if split_column not in df.columns:
        raise ValueError(f"Column '{split_column}' not found in the dataframe.")

    # Keep the specified column
    kept_data = df[[keep_column]]

    # Extract supergroup, group, and subgroup from the split_column
    supergroup = df[split_column].apply(lambda x: str(x)[0] if pd.notna(x) else "")
    group = df[split_column].apply(lambda x: str(x)[:2] if pd.notna(x) else "")
    subgroup = df[split_column].apply(lambda x: str(x) if pd.notna(x) else "")

    # Convert the final character in the subgroup column to a number
    def convert_final_char_to_number(value):
        if pd.notna(value) and len(value) > 0:
            final_char = value[-1].lower()
            if "a" <= final_char <= "z":  # Check if it's a letter
                return value[:-1] + str(ord(final_char) - ord("a") + 1)
        return value

    subgroup = subgroup.apply(convert_final_char_to_number)

    # Combine the kept column with the processed columns
    restructured_cluster_table = pd.concat(
        [
            kept_data,
            supergroup.rename("supergroup"),
            group.rename("group"),
            subgroup.rename("subgroup"),
        ],
        axis=1,
    )

    # Load the LAD lookup file into a DataFrame
    lad_lookup_file_path = config["LAD_lookup_file_path"]
    lad_lookup = pd.read_csv(lad_lookup_file_path)

    # Merge with LAD names from the lookup file
    restructured_cluster_table = restructured_cluster_table.merge(
        lad_lookup[["LAD22CD", "LAD22NM"]], left_on="LAD_code", right_on="LAD22CD", how="left"
    )

    # Drop the LAD22CD column after the join if it's no longer needed
    restructured_cluster_table = restructured_cluster_table.drop(columns=["LAD22CD"])

    # Rename the LAD22NM column to LAD_name
    restructured_cluster_table = restructured_cluster_table.rename(columns={"LAD22NM": "LAD_name"})

    # Move the LAD_name column to the first position
    columns = ["LAD_name"] + [col for col in restructured_cluster_table.columns if col != "LAD_name"]
    restructured_cluster_table = restructured_cluster_table[columns]

    # Save the resulting DataFrame to a new file
    output_file = os.path.join(
        config["output_directory"], "cluster_assignments/restructured_subclustering_output.csv"
    )
    restructured_cluster_table.to_csv(output_file, index=False)

    # Create and save out restructured long table (for use in summaries)
    restructured_cluster_table_long = pd.merge(
        restructured_cluster_table, standardised_data, on="LAD_code", how="inner"
    )
    output_file_long = os.path.join(
        config["output_directory"], "cluster_assignments/restructured_subclustering_output_long.csv"
    )
    restructured_cluster_table_long.to_csv(output_file_long, index=False)

    return restructured_cluster_table, restructured_cluster_table_long
