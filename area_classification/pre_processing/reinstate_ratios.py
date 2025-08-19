# V12 population density and V33 SIR are removed before percentage creation
# as these are already ratios. They need to be added back into the table
# before clustering.

# NOTE THIS FUNCTION CURRENTLY IS HARD CODED TO USE THE _SELECT.CSV FILES,
# IF THESE ARE NOT SAVED OUT IN EARLIER SCTIPY THEN THIS WILL NOT WORK

import os
import pandas as pd

def reinstate_v12_v33(percentages_df, config):
    """
    Looks in the QA folder for files ending with '_select', extracts V12 and V33 columns,
    and joins them into percentages_df on the first column.

    Parameters
    ----------
    percentages_df : pd.DataFrame
        The DataFrame to join the data into.
    config : dict
        main pipeline config dictionary containing output directory.

    Returns
    --------
    pd.DataFrame
        The updated percentages_df with V12 and V33 columns joined.
    
    """
    # List all files in the QA folder ending with '_select'
    select_files = [f for f in os.listdir(config["qa_folder_path"]) if f.endswith('_select.csv')]

    # Initialize an empty DataFrame to store all extracted data
    all_extracted_data = pd.DataFrame()

    for file in select_files:
        file_path = os.path.join(config["qa_folder_path"], file)
        df = pd.read_csv(file_path)
        
        # Ensure the required columns exist
        if 'v12' in df.columns and 'v33' in df.columns and 'LAD_code' in df.columns:
            # Extract LAD_code, v12, and v33
            extracted_data = df[['LAD_code', 'v12', 'v33']]
            
            # Append the extracted V12, V33 and LAD_code data to the combined DataFrame
            all_extracted_data = pd.concat([all_extracted_data, extracted_data], ignore_index=True)
        else:
            print(f"Skipping file {file} as it does not contain LAD_code, v12, or v33 columns.")

    # Merge V12, V33 columns with percentages_df on the 'LAD_code' column
    if 'LAD_code' in percentages_df.columns:
        percentages_df = percentages_df.merge(all_extracted_data, on='LAD_code', how='left')
    else:
        raise KeyError("The 'LAD_code' column is missing in percentages_df.")

    # Reorder the columns: keep LAD_code as the first column and sort the rest
    columns_to_sort = [col for col in percentages_df.columns if col != 'LAD_code']
    sorted_columns = ['LAD_code'] + sorted(columns_to_sort)
    percentages_df = percentages_df[sorted_columns]

    # Ensure QA directory exists
    os.makedirs(os.path.dirname(config["qa_folder_path"]), exist_ok=True)

    # Save to data QA folder
    output_file_path = os.path.join(config["qa_folder_path"], "V12_33_added_output.csv")
    percentages_df.to_csv(output_file_path, index=False)

    return percentages_df


# Run the function if the script is executed directly
from utilities.load_config import load_config
if __name__ == "__main__":
    config = load_config('area_classification/config.yaml')
    percentages_df = pd.read_csv('./data/QA/pre_processed_data_ew_ni_scot.csv')  
    updated_df = reinstate_v12_v33(percentages_df, config)
    print(updated_df)