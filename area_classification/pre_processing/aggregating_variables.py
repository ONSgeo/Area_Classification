import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def aggregating_variables(df_temp, aggregation_configs, config):
    """
    This function aggregates specified columns in a temporary DataFrame and adds the aggregated
    data as new columns.

    Parameters
    ----------
    df_temp : pd.DataFrame 
        The temporary DataFrame to update.
    aggregation_configs : list of dict
        A list of dictionaries, one each for EW, NI and Scot. Each dictionary contains:
            - 'col_names' (list): List of column codes to aggregate.
            - 'new_col_name' (str): Name of the new column to create.
            For example: 
                cars_2_or_more: [ts0450004, ts0450005]
    config : dict
        A dictionary containing user configuration settings, including the QA path.

    Returns
    -------
    pd.DataFrame
        The updated DataFrame with new aggregated columns.
    """
    for key in aggregation_configs:
        col_names = aggregation_configs[key]
        new_col_name = key

         # Check if all columns in col_names exist in df_temp
        missing_cols = [col for col in col_names if col not in df_temp.columns]
        if missing_cols:
            logging.warning(f"Warning: Missing columns {missing_cols} in DataFrame. Skipping aggregation for {new_col_name}.")
            continue

        # Add the new column by summing the specified columns
        df_temp[new_col_name] = df_temp[col_names].sum(axis=1)

    # Extract the header of column 1 (the country area code type e.g. LTLA, LGD or CA19)
    if not df_temp.empty:
        # Convert to string for use in the file name
        country_lad_code = str(df_temp.columns[0])  
    else:
        # Handle empty DataFrame case
        country_lad_code = "N/A" 

    # Ensure QA directory exists
    os.makedirs(os.path.dirname(config["qa_folder_path"]), exist_ok=True)

    # Save to data QA folder with country area code type in the file name
    output_file_path = f"{config['qa_folder_path']}aggregated_variables_output_{country_lad_code}.csv"
    df_temp.to_csv(output_file_path, index=False)
        
    return df_temp

if __name__ == "__main__":
    from utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    aggregation_config = load_config('area_classification/aggregation_setup.yaml')
    #aggregation_configs = aggregation_config['scot_file_configs']
    #df_temp = 
    df = aggregating_variables(df_temp, aggregation_config, config )
    print(df)
