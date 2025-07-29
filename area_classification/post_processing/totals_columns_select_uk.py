# Create a totals table for counts
# only runs when in the 'area_classification' directory - working document 
import os
import pandas as pd

from utilities.load_config import load_config

def select_totals_columns(inputs_folder, lookup_file, output_file):
    """
    Extract and generate a totals table for counts by processing _select files for UK countries.

    This function processes select files for England and Wales (ew), Northern Ireland (ni), and Scotland (scot),
    matches variable columns with their corresponding totals using a lookup file, and appends the totals to the
    select files. The processed files are then concatenated into a single DataFrame and saved to an output file.

    Args:
        inputs_folder (str): Path to the folder containing input files (select files and aggregated variables files).
        lookup_file (str): Path to the lookup CSV file containing table_ID, country, and new_code mappings.
        output_file (str): Path to save the final concatenated output CSV file.
    """

    # Load the lookup file
    lookup_df = pd.read_csv(lookup_file)

    # Filter out rows where 'new_code' is 'v12' or 'v33' (population density and SIR)
    lookup_df = lookup_df[~lookup_df["new_code"].isin(["v12", "v33"])]

    # Append '0001' to the end of the table_ID values in the lookup DataFrame
    lookup_df["table_ID_with_suffix"] = lookup_df["table_ID"].astype(str) + "0001"

    # Initialize an empty list to store processed DataFrames
    processed_dfs = []

    # Loop through all files in the inputs folder
    for file_name in os.listdir(inputs_folder):
        if file_name.endswith("_select.csv"):  # Process only files ending with '_select.csv'
            # Determine the country and corresponding aggregated file based on the file name
            if "ew_select" in file_name:
                country = "ew"
                agg_file = os.path.join(inputs_folder, "aggregated_variables_output_LTLA.csv")
                # Decapitalize the table_ID_with_suffix column for England and Wales
                lookup_df["table_ID_with_suffix"] = lookup_df["table_ID_with_suffix"].str.lower()
            elif "ni_select" in file_name:
                country = "ni"
                agg_file = os.path.join(inputs_folder, "aggregated_variables_output_LGD.csv")
                # Decapitalize the table_ID_with_suffix column for Northern Ireland
                lookup_df["table_ID_with_suffix"] = lookup_df["table_ID_with_suffix"].str.lower()
            elif "scot_select" in file_name:
                country = "scot"
                agg_file = os.path.join(inputs_folder, "aggregated_variables_output_CA19.csv")
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
                if variable in ["v12", "v33"]:  # Remove 'v12' and 'v33' columns
                    select_df.drop(columns=[variable], inplace=True)
                    continue
                if variable.startswith("v"):  # Only process variable columns
                    # Find the corresponding total column in the lookup
                    match = country_lookup_df.loc[country_lookup_df["new_code"] == variable, "table_ID_with_suffix"]
                    if not match.empty:
                        total_column = match.values[0]  # Get the matching total column name (e.g., ts0010001)

                        # Debug: Check if the total column exists in the aggregated variables file
                        if total_column in agg_df.columns:
                            # Add the total column to the select DataFrame
                            select_df[f"{variable}_total"] = agg_df[total_column]
                        else:
                            print(f"Warning: Total column '{total_column}' not found in agg file.")
                    else:
                        print(f"Warning: No match found for variable '{variable}' in lookup_df for {country}.")

            # Append the processed DataFrame to the list
            processed_dfs.append(select_df)

    # Concatenate all processed DataFrames
    final_df = pd.concat(processed_dfs, ignore_index=True)

    # Reorder the remaining columns alphabetically excluding the first column (LAD)
    # Get the first column
    first_column = final_df.columns[0]
    remaining_columns = sorted(final_df.columns[1:])
    reordered_columns = [first_column] + remaining_columns
    final_df = final_df[reordered_columns]

    totals_row = final_df.iloc[:, 1:].sum(numeric_only=True)  # Sum numeric columns (excluding the first column)
    totals_row[final_df.columns[0]] = "Total"  # Add a label for the first column
    final_df = pd.concat([final_df, pd.DataFrame([totals_row])], ignore_index=True)

    # Save the concatenated DataFrame to the output file
    final_df.to_csv(output_file, index=False)
    print(f"Final concatenated file saved to: {output_file}")

# Example usage
config = load_config('area_classification/config.yaml')
inputs_folder = config["qa_folder_path"]
lookup_file = config["select_variables_lookup"]
output_file = os.path.join(config["output_directory"], "select_raw_totals.csv")

select_totals_columns(inputs_folder, lookup_file, output_file)