import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
from io import BytesIO
import os 

logger = logging.getLogger(__name__)

def ni_lgd_download_data(config): 
    """
    Wrapper function to download Northern Ireland Local Government District (LGD) data.
    Data and metadata are downloaded and exported to csv files. 

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    None
        The function saves the downloaded data and metadata as CSV files in the specified input directory.
    """    

    meta_data_table = download_ni_lgd_data(config)
    format_and_export_ni_metadata_table(meta_data_table, config)
    reformat_pop_density_ni(config)



def reformat_pop_density_ni(config):
    """
    Function to reformat Northern Ireland Local Government District (LGD) population density data.
    Data needs to be downloaded manually from Northern Ireland Census website.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    pd.DataFrame
        Table with only rows/columns we need and hectare converted to km2.
        Columns: LGD, population_density
    """

    # Load only the first sheet of the Excel file
    df = pd.read_excel(config["ni_pop_density_filepath"], sheet_name=0, skiprows=5, header=0, index_col=None)

    # Remove unnecessary columns by index
    df = df.drop(df.columns[[0, 2, 3,5]], axis=1)

    # Rename the first remaining column to 'LGD'
    df.columns.values[0] = "LGD" 

    # Convert from per hectare to per km²
    df.iloc[:, 1] = df.iloc[:, 1] * 100  
    df.columns.values[1] = "population_density"  

    # Save to a CSV
    output_csv_path = os.path.join(config["input_directory"], "./ni_downloads/")
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    # save to output_csv_path
    df.to_csv(output_csv_path + "ni_population_density.csv", index=False)
    
    

    

def download_ni_lgd_data(config:dict)-> pd.DataFrame:
    """
    Function to download Northern Ireland Local Government District (LGD) data
    from the NISRA website and format it into a metadata table.
    Data tables are downloaded in CSV format.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    pd.DataFrame
        ni metadata table containing information about the downloaded variables.
        Columns: Variable_Name, Variable_ID, Table_ID, Table_Name, Type, Unit
    """    
    
    variables = get_available_variables()
    meta_data_table = pd.DataFrame(
        columns=[
            "Table_Name",
            "Table_ID",
            "Variable_Name",
            "Type",
        ]
    )
    
    for var in variables:
        t_name = var[0]
        t_dcode = var[1]
        t_unit = var[2]
        # Create a unique table ID (e.g., ni000, ni001, ...)
        t_id = "ni" + str(variables.index(var)).zfill(3)

        # Get data
        data = fetch_data(t_dcode, t_name, t_unit)
        if data is None:
            continue

        # Get metadata (more fields available if needed)
        meta_url = f"https://build.nisra.gov.uk/en/custom/table.csv-metadata.json?d={t_unit}&v=LGD14&v={t_dcode}&p=1"
        r = requests.get(meta_url)
        if r.status_code != 200:
            log_message = (
                f"Failed to fetch metadata for variable {t_name} | "
                f"Status code: {r.status_code} | "
                f"Message: {r.text}"
            )
            logger.error(log_message)
            continue
        type = r.json()["tableSchema"]["columns"][4]["titles"]


        df = pd.read_csv(BytesIO(data), skiprows=1)
        df.rename(columns={"Local Government District 2014 Code": "LGD"}, inplace=True)
        df.set_index("LGD", inplace=True)
        # Drop the label column
        df.drop(columns=["Local Government District 2014 Label"], inplace=True)
        # Drop the "No code required" column if it exists
        if "No code required" in df.columns:
            df.drop(columns=["No code required"], inplace=True)
    
        # Create a total column, that includes everything except "No code required"
        df["All " + t_unit] = df.sum(axis=1)
        # Put the total column first
        df = df[["All " + t_unit] + [col for col in df.columns if col != "All " + t_unit]]
        # Create new column names with zero padding
        variable_names = df.columns
        var_ids = [f"{t_id}{str(i).zfill(4)}" for i in range(1, len(variable_names) + 1)]
        df.columns = var_ids

        output_csv_path = os.path.join(config["input_directory"], "./ni_downloads/")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        # Save to csv
        df.to_csv(output_csv_path + f"/{t_id}.csv")

        meta_data_table = pd.concat(
            [
                meta_data_table,
                pd.DataFrame(
                    {
                        "Variable_Name": variable_names,
                        "Variable_ID": var_ids,
                        "Table_ID": [t_id] * len(variable_names),
                        "Table_Name": [t_name] * len(variable_names),
                        "Type": [type] * len(variable_names),
                        "Unit": [t_unit] * len(variable_names),
                    }
                ),
            ]
        )
    return meta_data_table


def format_and_export_ni_metadata_table(meta_data_table: pd.DataFrame, config:dict):
    """
    Formats and exports ni metadata table to csv.

    Parameters
    ----------
    meta_data_table : pd.DataFrame
        ni metadata table to format and export
    config : dict
        Configuration dictionary containing paths and file names.

    Returns
    -------
    None
        The function saves the formatted metadata table as a CSV file in the specified input directory.
    """    
    # Rename units to match other scripts
    meta_data_table["Unit"] = meta_data_table["Unit"].replace(
        {
            "PEOPLE": "Person",
            "HOUSEHOLD": "Household",
        }
    )
    # Add a 'Full_Name' column combining Table_Name and Variable_Name
    meta_data_table["Full_Name"] = (
        meta_data_table["Table_Name"] + ": " + meta_data_table["Variable_Name"]
    )
    # Reorder columns for output
    meta_data_table = meta_data_table[
        ["Variable_Name", "Variable_ID", "Table_ID", "Table_Name", "Type", "Unit", "Full_Name"]
    ]

    # Set Type to 'Count' for all tables
    meta_data_table["Type"] = "Count"

    meta_data_table.to_csv(os.path.join(config["input_directory"],"ni_lgd_table_metadata.csv"), index=False)



def get_available_variables():
    """
    Fetches available variables from the NISRA dataset metadata page.

    This function sends a GET request to the NISRA metadata page for both the PEOPLE and HOUSEHOLD datasets,
    parses the HTML content to extract table data, and returns the data as a list of lists.
    Each inner list represents a row in the table, containing the text content of each cell.

    Returns
    -------
    list of lists
        A list containing rows of table data, where each row is a list of cell values.
        Each row also includes a column indicating whether the data is for PEOPLE or HOUSEHOLD.
    """
            
    table_data = []

    # Fetch and parse PEOPLE dataset metadata table
    url = "https://build.nisra.gov.uk/en/metadata/dataset?d=PEOPLE"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for row in soup.select("tr"):
        cells = row.find_all(["td", "th"])
        table_data.append([cell.text.strip() for cell in cells] + ['PEOPLE'])

    # Fetch and parse HOUSEHOLD dataset metadata table
    url = "https://build.nisra.gov.uk/en/metadata/dataset?d=HOUSEHOLD"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for row in soup.select("tr"):
        cells = row.find_all(["td", "th"])
        table_data.append([cell.text.strip() for cell in cells] + ['HOUSEHOLD'])

    return table_data


def fetch_data(var_code, var_name, var_unit):
    """
    Fetches data from the Northern Ireland Census 2022 Data Zone.

    Constructs a URL based on the provided variable code, variable name, 
    and variable unit, then sends a GET request to fetch the corresponding data in CSV format.

    Parameters
    ----------
        var_code (str): 
            The code of the variable to fetch.
        var_name (str): 
            The name of the variable to fetch.
        var_unit (str): 
            The unit of the variable to fetch.

    Returns
    -------
    bytes
        The content of the response if the request is successful.
    None
       If the request fails, logs an error message and returns None.

    Raises
    ------
        requests.exceptions.RequestException: If there is an issue with the HTTP request.

    Notes
    -----
        - Some variables in the list may not have the correct dimensions (e.g., urban/rural).
        - Some variables may not be available at the Data Zone (DZ) level.
    """

    url = f"https://build.nisra.gov.uk/en/custom/table.csv?d={var_unit}&v=LGD14&v={var_code}&p=1"
    r = requests.get(url)

    if r.status_code != 200:
        log_message = (
            f"Failed to fetch data for variable {var_name} | "
            f"Status code: {r.status_code} | "
            f"Message: {r.text}"
        )
        logger.error(log_message)
        return None
    return r.content