# UK standardised mean

import os
import pandas as pd
import yaml


def make_unique_columns(columns):
    """
    Ensures column names are unique by appending a suffix to duplicates.
    """
    seen = {}
    unique_columns = []
    for col in columns:
        if col not in seen:
            seen[col] = 0
            unique_columns.append(col)
        else:
            seen[col] += 1
            unique_columns.append(f"{col}_{seen[col]}")
    return unique_columns

def extract_matching_and_partial_columns(inputs_folder, lookup_file, output_file):
    """
    Identifies tables in the inputs folder starting with 'aggregated_variables_output', extracts columns
    matching the 'variable_code' column in the lookup file, and also extracts columns
    whose headers match the 'variable_code' except the last character is replaced with '1'.
    Additionally, handles columns ending with '0001' by matching them to variable codes in the lookup file
    and renaming them to the corresponding 'new_code' with a '_total' suffix.
    The resulting columns are reordered alphabetically (low to high) after bringing the first column to the front.
    Totals each column, appends the totals as a new row, and renames columns using the lookup table.

    Parameters
    ----------
    inputs_folder : str
        Path to the folder containing input files.
    lookup_file : str
        Path to the lookup CSV file containing the 'variable_code' and 'new_code' columns.
    output_file : str
        Path to save the resulting table.
    """
    # Read the lookup file to get the list of variable codes and their corresponding new codes
    lookup_df = pd.read_csv(lookup_file)
    if 'variable_code' not in lookup_df.columns or 'new_code' not in lookup_df.columns:
        raise ValueError("The lookup file must contain 'variable_code' and 'new_code' columns.")
    variable_codes = set(lookup_df['variable_code'].dropna())
    partial_codes = {code[:-1] + '1' for code in variable_codes if len(code) > 1}
    code_mapping = dict(zip(lookup_df['variable_code'], lookup_df['new_code']))
    #v_to_formid = dict(zip(lookup_df['table_ID'].str.lower()+'0001', lookup_df['new_code']+'_total', ))
    
    #Add two new columns to the look up for the totals
    lookup_df["total_code"] = lookup_df["new_code"]+"_total"
    condition = lookup_df["variable_code"].str[-4:].apply(lambda x: x.isdigit())
    lookup_df.loc[condition, "total_column"] = lookup_df.loc[condition, "variable_code"].str[:-4] + "0001"
    lookup_df.loc[~condition, "total_column"] = False

    # Find rows where total_column is False
    false_total_rows = lookup_df[lookup_df['total_column'] == False]

    # Update the values in the 'total_column' to variable_code_total for these rows
    lookup_df.loc[lookup_df['total_column'] == False, 'total_column'] = (
        false_total_rows['variable_code'] + '_total'
    )
    print(lookup_df)

    # Load the YAML file
    with open('area_classification/aggregation_setup.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)

    # # Access the scot_file_configs section
    # ew_file_configs = yaml_data.get('ew_file_configs', {})
    # ni_file_configs = yaml_data.get('ni_file_configs', {})
    # scot_file_configs = yaml_data.get('scot_file_configs', {})

    # # Create a mapping from the codes in the lists to their corresponding keys
    # code_to_key_mapping_ew = {code: key for key, codes in ew_file_configs.items() for code in codes}
    # code_to_key_mapping_ni = {code: key for key, codes in ni_file_configs.items() for code in codes}
    # code_to_key_mapping_scot = {code: key for key, codes in scot_file_configs.items() for code in codes}
    # # Merge the three dictionaries
    # code_to_key_mapping = {**code_to_key_mapping_ew, **code_to_key_mapping_ni, **code_to_key_mapping_scot}

    # Access file configurations and create a combined mapping in one step
    code_to_key_mapping = {
        code: key
        for config_key in ['ew_file_configs', 'ni_file_configs', 'scot_file_configs']
        for key, codes in yaml_data.get(config_key, {}).items()
        for code in codes
    }

    print(code_to_key_mapping)
    # Create a new dictionary with modified keys and values for the totals of those in the aggregation config
    agg_total_code_to_key_mapping = {key[:-4] + '0001': value + '_total' for key, value in code_to_key_mapping.items()}
    print(agg_total_code_to_key_mapping)
    
    # Initialize an empty DataFrame to store the extracted data
    extracted_data = pd.DataFrame()

    # Iterate through files in the inputs folder
    for file_name in os.listdir(inputs_folder):
        # Find the files starting with 'aggregated_variables_output'
        if file_name.startswith("aggregated_variables_output"):  
            file_path = os.path.join(inputs_folder, file_name)
            df = pd.read_csv(file_path)

            # Find columns that match the variable codes
            matching_columns = [col for col in df.columns if col in variable_codes]

            # Find columns in the DataFrame that have header names in code_to_key_mapping
            aggregation_matching_columns = [col for col in df.columns if col in code_to_key_mapping]
            # Handle columns ending with '0001'
            columns_ending_0001 = [
                col for col in df.columns if col.endswith("0001")
            ]
               
            # renamed_columns_ending_0001 = {
            #     col: f"{code_mapping[col[:-4]]}_total" for col in columns_ending_0001
            # }

            # Combine matched columns and total columns
            all_matching_columns = matching_columns + columns_ending_0001 + aggregation_matching_columns

            if all_matching_columns:
                # Extract the matching columns
                extracted_subset = df[all_matching_columns].copy()  # Use .copy() to avoid SettingWithCopyWarning
    
                # Bring the first column of the original table to the front
                first_column = df.iloc[:, 0]  # Get the first column
                extracted_subset.insert(0, df.columns[0], first_column)  # Insert it at the front
                
                # Rename country specific column headers to 'LAD'
                country_code_to_lad_dict = {"CA19":"LAD","LGD":"LAD","LTLA":"LAD"}
                extracted_subset = extracted_subset.rename(columns = country_code_to_lad_dict)
               
                # Ensure the lookup file contains 'total_column' and 'total_code'
                if 'total_column' in lookup_df.columns and 'total_code' in lookup_df.columns:
                    # Create a mapping from total_column to total_code
                    total_column_mapping = dict(zip(lookup_df['total_column'], lookup_df['total_code']))
                #Rename some columns
                # Combine all column mappings into a single dictionary
                combined_mapping = {**code_to_key_mapping, **total_column_mapping, **code_mapping, **agg_total_code_to_key_mapping}
                # Rename columns using the combined mapping and print the result
                extracted_subset.rename(columns=combined_mapping, inplace=True)
                # Ensure unique column names before concatenation
                extracted_subset.columns = make_unique_columns(extracted_subset.columns)
                print(extracted_subset)
                # Concatenate the extracted data
                extracted_data = pd.concat([extracted_data, extracted_subset], ignore_index=True)
    
    # Add a totals row
    if not extracted_data.empty:
        totals_row = extracted_data.iloc[:, 1:].sum(numeric_only=True)  # Sum numeric columns (excluding the first column)
        totals_row[extracted_data.columns[0]] = "Total"  # Add a label for the first column
        extracted_data = pd.concat([extracted_data, pd.DataFrame([totals_row])], ignore_index=True)

    # Reorder the remaining columns alphabetically excluding the first column (LAD)
    # Get the first column
    first_column = extracted_data.columns[0]
    remaining_columns = sorted(extracted_data.columns[1:])
    reordered_columns = [first_column] + remaining_columns
    extracted_data = extracted_data[reordered_columns]
    
    # Save the extracted data to the output file
    extracted_data.to_csv(output_file, index=False)
    print(f"Extracted data saved to: {output_file}")

# Example usage
inputs_folder = "D:/Repos/Area_Classification/data/QA"
lookup_file = "D:/Repos/Area_Classification/data/lookups/UK_selected_codes_lookup.csv"
output_file = "D:/Repos/Area_Classification/data/extracted_data3.csv"

extract_matching_and_partial_columns(inputs_folder, lookup_file, output_file)