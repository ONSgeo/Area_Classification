import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
from io import BytesIO

def ni_download(): 
    print("Placeholder to download Northen Ireland data.")  

# Set up logging enabled flag
LOGGING_ENABLED = False  # Set this to False to silence logs

# Set up basic logging (logs to console by default)
if LOGGING_ENABLED:
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.CRITICAL)  # Disable logging when set to False


#Data dirs

DATA_DIR = "output_data"
CSV_DIR = f"{DATA_DIR}/csv"
PARQUET_DIR = f"{DATA_DIR}/parquet"

#create dirs
import os
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(PARQUET_DIR, exist_ok=True)


def get_available_vars():
    """
    Fetches available variables from the NISRA dataset metadata page.

    This function sends a GET request to the NISRA metadata page for the PEOPLE dataset,
    parses the HTML content to extract table data, and returns the data as a list of lists.
    Each inner list represents a row in the table, containing the text content of each cell.

    Returns:
        list of list of str: A list where each element is a list representing a row of table data.
    """
            
    table_data = []

    url = "https://build.nisra.gov.uk/en/metadata/dataset?d=PEOPLE"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for row in soup.select("tr"):
        cells = row.find_all(["td", "th"])
        table_data.append([cell.text.strip() for cell in cells] + ['PEOPLE'])

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

    This function constructs a URL based on the provided variable code, variable name, 
    and variable unit, then sends a GET request to fetch the corresponding data in CSV format.

    Args:
        var_code (str): The code of the variable to fetch.
        var_name (str): The name of the variable to fetch.
        var_unit (str): The unit of the variable to fetch.

    Returns:
        bytes: The content of the response if the request is successful.
        None: If the request fails, logs an error message and returns None.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.

    Notes:
        - Some variables in the list may not have the correct dimensions (e.g., urban/rural).
        - Some variables may not be available at the Data Zone (DZ) level.
    """

    url = f"https://build.nisra.gov.uk/en/custom/table.csv?d={var_unit}&v=LGD14&v={var_code}&p=1"
    r = requests.get(url)

    # some vars in the list don't have the correct dimensions (like urban/rural)
    # some aren't available for DZ level, ie
    if r.status_code != 200:
        log_message = (
            f"Failed to fetch data for variable {var_name} | "
            f"Status code: {r.status_code} | "
            f"Message: {r.text}"
        )
        logging.error(log_message)
        return None
    return r.content





if __name__ == "__main__":


    vars = get_available_vars()

    # create metadata table
    meta_data_table = pd.DataFrame(
        columns=[
            "Table_Name",
            "Table_ID",
            "Variable_Name",
            "Type",
        ]
    )

    for var in vars:
        t_name = var[0]
        t_dcode = var[1]
        t_unit = var[2]
        # create a unique ID code for the tab ni001 -> ni002

        t_id = "ni" + str(vars.index(var)).zfill(3)

        # get data
        data = fetch_data(t_dcode, t_name, t_unit)
        if data is None:
            continue

        # get metadata, there is more stuff here we could grab if needed
        meta_url = f"https://build.nisra.gov.uk/en/custom/table.csv-metadata.json?d={t_unit}&v=LGD14&v={t_dcode}&p=1"
        r = requests.get(meta_url)
        if r.status_code != 200:
            log_message = (
                f"Failed to fetch metadata for variable {t_name} | "
                f"Status code: {r.status_code} | "
                f"Message: {r.text}"
            )
            logging.error(log_message)
            continue
        type = r.json()["tableSchema"]["columns"][4]["titles"]
        df = pd.read_csv(BytesIO(data), skiprows=1)
        
        df.rename(columns={"Local Government District 2014 Code": "LGD"}, inplace=True)
        df.set_index("LGD", inplace=True)
        # drop the label column
        df.drop(columns=["Local Government District 2014 Label"], inplace=True)
        # drop the "No code required" column if it exists
        if "No code required" in df.columns:
            df.drop(columns=["No code required"], inplace=True)
    
        # create a total column, that includes everything except "No code required"
        df["All " + t_unit] = df.sum(axis=1)
        # put the total column first
        df = df[["All " + t_unit] + [col for col in df.columns if col != "All " + t_unit]]
        # Create new column names with zero padding
        variable_names = df.columns
        var_ids = [f"{t_id}{str(i).zfill(4)}" for i in range(1, len(variable_names) + 1)]
        df.columns = var_ids

        # save to csv and parquet
        df.to_csv(CSV_DIR + f"/{t_id}.csv")
        df.to_parquet(PARQUET_DIR + f"/{t_id}.parquet")

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

    # rename units to match other scripts
    meta_data_table["Unit"] = meta_data_table["Unit"].replace(
        {
            "PEOPLE": "Person",
            "HOUSEHOLD": "Household",
        }
    )
    # full name column
    meta_data_table["Full_Name"] = (
        meta_data_table["Table_Name"] + ": " + meta_data_table["Variable_Name"]
    )
    # save metadata table
    meta_data_table = meta_data_table[
        ["Variable_Name", "Variable_ID", "Table_ID", "Table_Name", "Type", "Unit", "Full_Name"]
    ]

    # manually set Type to 'Count' for all tables
    meta_data_table["Type"] = "Count"
    meta_data_table.to_csv("ni_lgd_table_metadata.csv", index=False)

