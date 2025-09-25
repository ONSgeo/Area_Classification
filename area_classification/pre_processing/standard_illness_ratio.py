# Expected input
# area_code   |  age_group   |  Population  |  Disability_count
#---------------------------------------------------------------
# E06000001   |  0-14        |  1000        |  50
#             |              |              |

# ^^ Areas code for all of UK, age groups = 0_14_65_over and 15_64

import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

from area_classification.utilities.disability_age_group_conversion import (
    convert_disability_age_group_england_wales,
    convert_disability_age_group_northern_ireland,
    convert_disability_age_group_scotland,
)


def sir_processing(config):
    """
    Process disability data to calculate the Standard Illness Ratio (SIR) for each area code.

    Parameters
    -----------
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    pd.DataFrame
        DataFrame with SIR values calculated for each area code.
    """

    # disability files by age -> sharepoint?
    # Check if required files exist in the input directory
    required_files = [
        config["england_wales_disability_file"],
        config["ni_disability_file"],
        config["scotland_disability_file"]
    ]
    missing_files = []
    for file in required_files:
        file_path = os.path.join(config["input_directory"], file)
        if not os.path.isfile(file_path):
            missing_files.append(file)

    if config["england_wales_disability_file"] in missing_files:
        logger.warning(f"Warning: The file {config['england_wales_disability_file']} was not found in the input directory.")
        convert_disability_age_group_england_wales(config["input_directory"] + config["england_wales_disability_input"], config)
    if config["ni_disability_file"] in missing_files:
        logger.warning(f"Warning: The file {config['ni_disability_file']} was not found in the input directory.")
        convert_disability_age_group_northern_ireland(config["input_directory"] + config["ni_disability_input"], config)
    if config["scotland_disability_file"] in missing_files:
        convert_disability_age_group_scotland(config["input_directory"] + config["scotland_disability_input"], config)
        logger.warning(f"Warning: The file {config['scotland_disability_file']} was not found in the input directory.")        


        logger.warning(f"Warning: The following files were not found: {missing_files}")

    ew_disability_df = pd.read_csv(config["input_directory"]+config["england_wales_disability_file"])
    ni_disability_df = pd.read_csv(config["input_directory"]+config["ni_disability_file"])
    scotland_disability_df = pd.read_csv(config["input_directory"]+config["scotland_disability_file"])
    combined_disability_df = pd.concat(
        [ew_disability_df, ni_disability_df, scotland_disability_df])
    # Scotland excluded because it doesnt have council area codes 
    sir_output_df = SIR_calculation(combined_disability_df, config)
    return sir_output_df

def SIR_calculation(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate the Standard Illness Ratio (SIR) for a given DataFrame containing disability data.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame containing columns 'Area_Code', 'local_authority', 'age_group', 'Count', 'Population',
        UK coverage
                        
    Returns
    -------
    DataFrame
        DataFrame with SIR values calculated. Output is not grouped by age
    """

    
    # Get Ran (proportion of ill or disabled people for each age group at the national UK level)
    df_nat_summary = df.groupby('age_group').agg(
        sum_population=('total_population', 'sum'),
        sum_disability_count=('total_disabled', 'sum')).reset_index()
 
    df_nat_summary['nat_prop'] = df_nat_summary['sum_disability_count'] / df_nat_summary['sum_population']


    # Join the national proportions back to the original DataFrame
    df = df.merge(df_nat_summary[['age_group', 'nat_prop']], on='age_group', how='left', suffixes=('', '_nat'))

    # Exp_ill for each age group (ill_prop * pop) 
    df['exp_ill'] = df['nat_prop'] * df['total_population']    

    # Sum exp ill and diisability count (across age groups, to get one value per geog)
    df_all = df.groupby(['area_code']).agg(exp_ill_all=('exp_ill', 'sum'),
                                                          disability_count=('total_disabled', 'sum')).reset_index()

    # Calculate SIR for each Area Code
    df_all['SIR'] = df_all.apply(lambda row: round((row['disability_count'] / row['exp_ill_all']) * 100, 4), axis=1)

    # QA check the SIR dataframe before returning
    sir_qa_checks(df_all, config)
    logger.info(f"SIR_DF_ALL: {df_all.head()}")
    return df_all

def sir_qa_checks(df: pd.DataFrame, config: dict) -> None:
    """
    Perform QA checks on the SIR DataFrame.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame containing SIR values.
        
    Returns
    -------
        None
    """
    # Check if disability_count is int
    
    assert df['disability_count'].dtype == 'int64', "Disability count should be of type int64"

    # Check expected spatial distribution
    logger.info("SIR values distribution:")
    logger.info(df['SIR'].describe())

    for country_code_starts_with in [["E", "W"], ['S'], ['N']]:
        df_subset = df[df["area_code"].str.startswith(tuple(country_code_starts_with))]
        logger.info(df_subset['SIR'].describe())

    # Ensure QA directory exists
    os.makedirs(os.path.dirname(config["qa_directory"]), exist_ok=True)

    # Save to data QA folder
    output_file_path = config["qa_directory"] + "sir_calculation_qa_output.csv"
    df.to_csv(output_file_path, index=False)

    # check that all records contain all of uk
    # Can add once we are working with all data
    # df["total_population"].sum() == sum(ew+scotland+ni)


if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    EW_df = pd.read_csv(f"{config['input_directory']}ew_disability_age_group.csv") 
    EW_df.rename(columns={'Area Code': 'area_code'}, inplace=True)
    EW_df.rename(columns={'Local Authority': 'local_authority'}, inplace=True)

    x = sir_processing(config)
    sir_qa_checks(x)

# QA checks - Checked disability_count is int, checked SIR is %, Checked expected spatial distribution
# Reasonably sure this is correct, but will need to be check once we use combined UK data as input.