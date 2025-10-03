import os
from bs4 import BeautifulSoup  # Equivalent to rvest for web scraping
import re  # For string manipulation (similar to stringr)
import pandas as pd  # For data manipulation (similar to tidyverse and vroom)
import requests  # For making HTTP requests
from zipfile import ZipFile
from glob import glob
from shutil import rmtree
import tempfile
import logging

from area_classification.utilities.load_config import load_config

logger = logging.getLogger(__name__)

def ew_lad_bulk_download(config: dict):
    """
    Downloads the latest census 2021 data for England and Wales Local Authority Districts (LADs) from Nomis.
    census data is exported in CSV format to output directory specified in the config.

    Parameters
    ----------
    config : dict
        main config for pipeline
    
    Returns
    -------
    None
        The function saves the downloaded data as CSV files in the specified output directory.
    """
    zip_urls = get_census_table_urls(config)

    meta_data_table = download_and_unzip_data(zip_urls, config)

    format_and_export_metadata_table(meta_data_table, config)


def get_census_table_urls(config: dict) -> list:
    """
    function to configure the HTML pages and extract the URLs for census tables.
    Removes tables that do not have Output Areas (OA) from the list outlined in config.

    Parameters
    ----------
    config : dict
        main config for pipeline

    Returns
    -------
    list
        list of URLs for census tables that contain Output Areas (OA).
    """     
    # Read the HTML page
    html_page = BeautifulSoup(requests.get("https://www.nomisweb.co.uk/sources/census_2021_bulk").content, "html.parser")

    # Get census table zip file names
    zip_urls = [
        link['href'] for link in html_page.find_all('a', href=True) 
        if link['href'].endswith('.zip') and 'extra.zip' not in link['href']
    ]

    # Make zip file names into a full URL
    zip_urls = ["https://www.nomisweb.co.uk" + url for url in zip_urls]

    nomis_address = "https://www.nomisweb.co.uk/output/census/2021/census2021-{table_id}.zip"
    no_oa_tables = [nomis_address.format(table_id=code) for code in config["england_and_wales_table_codes_to_remove"]]

    # Remove the tables without OA
    zip_urls = list(set(zip_urls) - set(no_oa_tables))
    
    return zip_urls

def download_and_unzip_data(zip_urls: list, config: dict) -> pd.DataFrame:
    """
    fucntion to download and unzip the census data files, extract the relevant tables,
    and create a metadata table with the old and new column names.

    Parameters
    ----------
    zip_urls : list
        list of urls to download census data zip files from Nomis.
        produced by the `get_census_table_urls` function.
    config : dict
        main pipeline config dictionary containing output directory.

    Returns
    -------
    pd.DataFrame
        metadata table containing old and new column names, and table IDs.
        downloaded data is saved as CSV files in the specified output directory.
    """
    # Initialize an empty metadata table
    meta_data_table = pd.DataFrame()

    for url in zip_urls:
        # Create a temporary directory for unzipping
        tmp_dir = tempfile.mkdtemp()

        # Download the specified zip file
        response = requests.get(url)
        zip_file_path = os.path.join(tmp_dir, "temp.zip")
        with open(zip_file_path, "wb") as f:
            f.write(response.content)

        # Unzip the file
        with ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)

        # Extract the table name from the URL
        t_code_name_match = re.search(r"ts\d{3}[a-z]?", url)
        t_name = t_code_name_match.group(0) if t_code_name_match else None

        # Extract the LTLA CSV location
        t_tab_loc = glob(os.path.join(tmp_dir, f"*{t_name}-ltla.csv"))
        if not t_tab_loc:
            # Handle typo case
            t_tab_loc = glob(os.path.join(tmp_dir, f"*{t_name}-llta.csv"))

        if not t_tab_loc:
            logger.info(f"No matching file found for {t_name}")
            rmtree(tmp_dir)
            continue

        t_tab_loc = t_tab_loc[0]  # Get the first match

        # Read the CSV file into a DataFrame
        df = pd.read_csv(t_tab_loc)
        df = df.drop(columns=["date", "geography"], errors="ignore")  # Drop unnecessary columns
        df.set_index("geography code", inplace=True)  # Move OA code to row names

        # Get the old column names
        old_names = df.columns.tolist()
        # Create new column names with zero padding
        new_names = [f"{t_name}{i:04d}" for i in range(1, len(old_names) + 1)]

        # Create a metadata table
        n_list = pd.DataFrame({
            "old_names": old_names,
            "new_names": new_names,
            "Table_ID": t_name
        })

        # Append to the metadata table
        meta_data_table = pd.concat([meta_data_table, n_list], ignore_index=True)

        # Rename the columns in the DataFrame
        df.columns = new_names
        df.reset_index(inplace=True)  # Move row names back to a column
        df.rename(columns={"geography code": "LTLA"}, inplace=True)

        # Write the DataFrame to a CSV file
        output_csv_path = os.path.join(config["input_directory"], "./ew_downloads/", f"{t_name}.csv")

        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        df.to_csv(output_csv_path, index=False)

        # Remove all downloaded files for this table
        rmtree(tmp_dir)
    print(type(meta_data_table))
    meta_data_table.to_csv("meta_data_table.csv")
    return meta_data_table




def format_and_export_metadata_table(meta_data_table: pd.DataFrame, config: dict):
    """
    function to format the metadata table and saves it as a CSV to the input directory.

    Parameters
    ----------
    meta_data_table : pd.DataFrame
        metadata table containing old and new column names, and table IDs.
        produced by the `download_and_unzip_data` function.
    config : dict
        main pipeline config dictionary containing output directory.

    Returns
    --------
    None
        The function saves the formatted metadata table as a CSV file in the specified output directory.
    """    
    
    # Format the lookup table
    meta_data_table_full = (
        meta_data_table
        .assign(Table_Name=meta_data_table['old_names'].str.split(':', n=1).str[0])
        #.assign(Type=meta_data_table['old_names'].str.extract(r'; measures: (\w+)')[0])
        .assign(Variable_Name=meta_data_table['old_names'].str.replace(r';.*', '', regex=True))
        .assign(Variable_Name=lambda df: df['Variable_Name'].str.replace(
            df['Table_Name'] + ': ', '', regex=False))
    )
    
    # Ensure input directory exists
    os.makedirs(os.path.dirname(config["input_directory"]), exist_ok=True)

    # Write the resulting DataFrame to a CSV file
    meta_data_table_full.to_csv(os.path.join(config["input_directory"], "ew_lad_table_metadata.csv"), index=False)

    return meta_data_table_full


if __name__ == "__main__":
    # Example usage
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    ew_lad_bulk_download(config)
