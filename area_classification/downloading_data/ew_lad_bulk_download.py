# Import necessary libraries
import os
from bs4 import BeautifulSoup  # Equivalent to rvest for web scraping
import re  # For string manipulation (similar to stringr)
import pandas as pd  # For data manipulation (similar to tidyverse and vroom)
import requests  # For making HTTP requests
from zipfile import ZipFile
from glob import glob
from shutil import rmtree
# import pyarrow as pa  # Equivalent to arrow (commented out as in the R script)

def ew_download(): 
    print("Placeholder to download England and Wales data.")  
# Read the HTML page
html_page = BeautifulSoup(requests.get("https://www.nomisweb.co.uk/sources/census_2021_bulk").content, "html.parser")

# Get census table zip file names
zip_urls = [
    link['href'] for link in html_page.find_all('a', href=True) 
    if link['href'].endswith('.zip') and 'extra.zip' not in link['href']
]

# Make zip file names into a full URL
zip_urls = ["https://www.nomisweb.co.uk" + url for url in zip_urls]

# Create an empty DataFrame with the specified column names
meta_data_table = pd.DataFrame({
    "Table_Name": [],
    "Variable_Name": [],
    "Type": [],
    "new_names": [],
    "Table_ID": []
})

# These tables dont have OA data
no_oa_tables = [
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts007.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts009.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts010.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts012.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts013.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts071.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts072.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts073.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts074.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts022.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts024.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts028.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts031.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts076.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts060.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts064.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts047.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts048.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts079.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts070.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts077.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts078.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts037asp.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts038asp.zip",
"https://www.nomisweb.co.uk/output/census/2021/census2021-ts039asp.zip"
]


# Create output directories for the census tables
os.makedirs("./output_data/csv", exist_ok=True)
# os.makedirs("./output_data/parquet", exist_ok=True)  # Commented out as in the R code

# Remove the tables without OA
zip_urls = list(set(zip_urls) - set(no_oa_tables))

# Initialize an empty metadata table
meta_data_table = pd.DataFrame()


for url in zip_urls:
    # Create a temporary directory for unzipping
    tmp_dir = "./tmp"
    os.makedirs(tmp_dir, exist_ok=True)

    # Download the specified zip file
    response = requests.get(url)
    zip_path = os.path.join(tmp_dir, "temp.zip")
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # Unzip the file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)

    # Extract the table name from the URL
    t_name_match = re.search(r"ts\d{3}[a-z]?", url)
    t_name = t_name_match.group(0) if t_name_match else None

    # Extract the LTLA CSV location
    t_tab_loc = glob(os.path.join(tmp_dir, f"*{t_name}-ltla.csv"))
    if not t_tab_loc:
        # Handle typo case
        t_tab_loc = glob(os.path.join(tmp_dir, f"*{t_name}-llta.csv"))

    if not t_tab_loc:
        print(f"No matching file found for {t_name}")
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
    N_list = pd.DataFrame({
        "old_names": old_names,
        "new_names": new_names,
        "Table_ID": t_name
    })

    # Append to the metadata table
    meta_data_table = pd.concat([meta_data_table, N_list], ignore_index=True)

    # Rename the columns in the DataFrame
    df.columns = new_names
    df.reset_index(inplace=True)  # Move row names back to a column
    df.rename(columns={"geography code": "LTLA"}, inplace=True)

    # Write the DataFrame to a CSV file
    output_csv_path = os.path.join("./output_data/csv", f"{t_name}.csv")
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)

    # Clean up temporary objects
    del N_list, old_names, new_names, t_name, t_tab_loc, df

    # Remove all downloaded files for this table
    rmtree(tmp_dir)


# Format the lookup table
meta_data_table2 = (
    meta_data_table
    .assign(Table_Name=meta_data_table['old_names'].str.split(':', n=1).str[0])  # Extract Table_Name
    .assign(Type=meta_data_table['old_names'].str.extract(r'; measures: (\w+)')[0])  # Extract Type
    .assign(Variable_Name=meta_data_table['old_names'].str.replace(r';.*', '', regex=True))  # Remove everything after ";"
    .assign(Variable_Name=lambda df: df['Variable_Name'].str.replace(
        df['Table_Name'] + ': ', '', regex=False))  # Remove "Table_Name: " prefix
)

# Write the resulting DataFrame to a CSV file
# Should be updated to output to specific path. 
meta_data_table2.to_csv("ew_lad_table_metadata.csv", index=False)