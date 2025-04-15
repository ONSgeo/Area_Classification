# WORK IN DEVELOPMENT

# Background
Area Classification
“The 2021 Classification for Output Areas (2021 OAC) is a hierarchical geodemographic classification across the UK which identifies areas of the country with similar characteristics.” Consumer data research centre (CDRC)​
Current focus:
* 2021 ​
* Supergroups​
* Local Authority District​
    * England and Wales (NOMIS) ​
        * 2022 local authorities: district / unitary​ (LTLA)
    * Northern Ireland (NISRA) ​
        * Local Government District 2014​
    * Scotland ​
        * Local authority (CA2019)​

## Description of files
A table that describes each of the files in the repo (like we did for the automated mapping repo)

## Data
Description of the input datasets

## Methodology / process description
Notes: NO BULK DOWNLOAD FOR LAD SCOTLAND SO MANUALLY DOWNLOADED FROM https://www.scotlandscensus.gov.uk/search-the-census#/search-by. Additionally migration indicator variable not available for Scotland.

### Census 2021 Output Areas (legacy ReadME)
This repository contains code to download and clean all Output Area level data for the England and Wales 2021 Census.

The R code:

* Download the bulk census data from [Nomis](https://www.nomisweb.co.uk/sources/census_2021_bulk)
* Import the Output Area level data into R
* Create new variable names based on the sequential ordering of the variables and the table identification code
* Create a metadata lookup table providing the link between the new names and the original names
* Export the OA data as both CSV and Parquet files

The created CSV are available in the folder ["/output_data/csv"](/output_data/csv) and the parquet files in the folder ["/output_data/parquet"](/output_data/parquet)

### Northern Ireland Census 2021 Data Zones (legacy ReadMe)
This repository contains code to download and clean all Data Zone level data for the Northen Irish 2021 Census

The python code:

* Finds the available variables from the [NISRA Table Builder](https://build.nisra.gov.uk/)
* Scrapes the tables for each variable using beautiful soup
* Create new variable names based on the sequential ordering of the variables and the table identification code
* Create a metadata lookup table providing the link between the new names and the original names
* Export the data zone data as both CSV and Parquet files

The created CSV are available in the folder ["/output_data/csv"](/output_data/csv) and the parquet files in the folder ["/output_data/parquet"](/output_data/parquet)

### Scotland Census 2022 Output Areas (legacy ReadMe)
This repository contains code to download and clean all Data Zone level data for the Scottish 2022 Census

The python code:

* Downloads the bulk data from the [Scotland Census](https://www.scotlandscensus.gov.uk/documents/2022-output-area-data/)
* Processes and cleans the tables
* Create new variable names based on the sequential ordering of the variables and the table identification code
* Create a metadata lookup table providing the link between the new names and the original names
* Export the data zone data as both CSV and Parquet files

The created CSV are available in the folder ["/output_data/csv"](/output_data/csv) and the parquet files in the folder ["/output_data/parquet"](/output_data/parquet)
## Output
## Limitations
## Future scope
## Contacts / authors / 

## Acknowledgements
Thanks to Owen Goodwin (ogoodwin505) and Alex Singleton (alexsingleton) at the ONS Data Science Office for their early code which formed the basis of this repo.
[ONS Data Science Office](https://github.com/Geographic-Data-Service)
[Census_2021_Output_Areas](https://github.com/Geographic-Data-Service/Census_2021_Output_Areas) (England and Wales)
[Scotland_Census_2022_OA](https://github.com/Geographic-Data-Service/Scotland_Census_2022_OA)
[Northern_Ireland_Census_2022_Data_Zone](https://github.com/Geographic-Data-Service/Northern_Ireland_Census_2022_Data_Zone)
[Geodemographic Python Example](https://github.com/ogoodwin505/pygeodem)

# Previous README:
## Geodemographic Python Example  

This repository contains the workflow for producing a geodemographic classification in Python using k-means clustering. It follows a simplified process, similar to that described in the [2021 OAC Paper](https://rgs-ibg.onlinelibrary.wiley.com/doi/full/10.1111/geoj.12550).  

### Files  
- **Main notebook:** `1_geodemographic_example.ipynb`  
- **Requirements:** Dependencies are listed in `requirements.txt`  
- **Example data:** `example_oacdata.csv`  

### Setup (dependencies)
The dependencies can be installed from inside the notebook.

Alternatively;
#### Using `pip` and a virtual environment  
Create and activate a virtual environment:  
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
pip install -r requirements.txt
```

