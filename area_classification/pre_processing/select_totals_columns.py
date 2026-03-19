import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


def select_totals_columns(config, inputs_folder):
    """
    Extracts select files for England and Wales (ew), Northern Ireland (ni), and Scotland (scot),
    matches variable columns with their corresponding totals using a lookup file, and appends the
    totals to the select files. The processed files are then concatenated into a single DataFrame
    and saved to an output file. This is used to calculate percentages later in the pipeline.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and settings
    inputs_folder : str
        Path to the folder containing the select files and aggregated output tables for each
        country (ew, ni, scot).
            - select files contain the area codes and raw counts for only the variables
            from v1 to v60.
            - aggregated output tables contain the area codes and raw counts and totals for every
            variable using variables codes like ts, ni and uv. Codes ending '001' are the totals.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with the area codes in the first column followed by raw count values for each
        variable from v1 to v60 and the total respondents to the question relating to that variable.
    """

    # Load the lookup file
    lookup_file = config["select_variables_lookup"]
    lookup_df = pd.read_csv(lookup_file)

    # Filter out rows where 'new_code' is 'v12' or 'v33' (population density and SIR)
    # These are already ratios, not counts
    lookup_df = lookup_df[~lookup_df["new_code"].isin(["v12", "v33"])]

    # Append '0001' to the end of the table_ID values in the lookup DataFrame
    lookup_df["table_ID_with_suffix"] = lookup_df["table_ID"].astype(str) + "0001"

    # Initialize an empty list to store processed DataFrames
    processed_dfs = []

    # Loop through all files in the inputs folder
    for file_name in os.listdir(inputs_folder):
        if file_name.endswith(
            "_selected_variables.csv"
        ):  # Process only files ending with '_selected_variables.csv'
            # Determine the country and corresponding aggregated file based on the file name
            if "preprocessing_ew_selected_variables.csv" in file_name:
                country = "ew"
                agg_file = os.path.join(
                    inputs_folder, "preprocessing_aggregated_all_variables_LTLA.csv"
                )
                # Decapitalize the table_ID_with_suffix column for England and Wales
                lookup_df["table_ID_with_suffix"] = lookup_df["table_ID_with_suffix"].str.lower()
            elif "preprocessing_ni_selected_variables.csv" in file_name:
                country = "ni"
                agg_file = os.path.join(
                    inputs_folder, "preprocessing_aggregated_all_variables_LGD.csv"
                )
                # Decapitalize the table_ID_with_suffix column for Northern Ireland
                lookup_df["table_ID_with_suffix"] = lookup_df["table_ID_with_suffix"].str.lower()
            elif "preprocessing_scot_selected_variables" in file_name:
                country = "scot"
                agg_file = os.path.join(
                    inputs_folder, "preprocessing_aggregated_all_variables_CA19.csv"
                )
                # Do not decapitalize the table_ID_with_suffix column for Scotland
                lookup_df["table_ID_with_suffix"] = lookup_df["table_ID"].astype(str) + "0001"
            else:
                continue  # Skip files that don't match the expected pattern

            # Load the select file
            select_df = pd.read_csv(os.path.join(inputs_folder, file_name))

            # Filter the lookup DataFrame for the current country
            country_lookup_df = lookup_df[lookup_df["country"] == country]

            # Load the aggregated variables file
            agg_df = pd.read_csv(agg_file)

            # Iterate through each variable column in the select file
            for variable in select_df.columns[1:]:  # Skip the first column
                # Ignore 'v12' and 'v33' columns as these are already ratios,
                # don't need to be percentages
                if variable in ["v12", "v33"]:
                    continue
                # Only process variable columns
                if variable.startswith("v"):
                    # Special case for v19 in Scotland
                    if country == "scot" and variable == "v19":
                        # Directly set the total column to 'Total'
                        total_column = "Total"
                    else:
                        # Find the corresponding total column in the lookup
                        match = country_lookup_df.loc[
                            country_lookup_df["new_code"] == variable, "table_ID_with_suffix"
                        ]
                        if not match.empty:
                            total_column = match.values[
                                0
                            ]  # Get the matching total column name (e.g., ts0010001)
                        else:
                            logger.warning(
                                f"Warning: No match found for variable '{variable}' "
                                + "in lookup_df for {country}."
                            )
                            continue

                    # Check if the total column exists in the aggregated variables file
                    if total_column in agg_df.columns:
                        # Add the total column to the select DataFrame
                        select_df[f"{variable}_total"] = agg_df[total_column]
                    else:
                        logger.warning(
                            f"Warning: Total column '{total_column}' not found in agg file."
                        )

            # Append the processed DataFrame to the list
            processed_dfs.append(select_df)

    # Concatenate all processed DataFrames
    raw_totals_df = pd.concat(processed_dfs, ignore_index=True)

    # Reorder the remaining columns alphabetically excluding the first column (LAD)
    # Get the first column
    first_column = raw_totals_df.columns[0]
    remaining_columns = sorted(raw_totals_df.columns[1:])
    reordered_columns = [first_column] + remaining_columns
    raw_totals_df = raw_totals_df[reordered_columns]

    # Save the concatenated DataFrame to the output file
    output_file = os.path.join(
        config["qa_directory"], "preprocessing_selected_variables_raw_totals.csv"
    )
    raw_totals_df.to_csv(output_file, index=False)

    return raw_totals_df
