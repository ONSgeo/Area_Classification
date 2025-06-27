# WORK IN DEVELOPMENT

# Background
Area Classification
“The 2021 Classification for Output Areas (2021 OAC) is a hierarchical geodemographic classification across the UK which identifies areas of the country with similar characteristics.” Consumer data research centre (CDRC)​
Current focus:
* 2021 ​
* Supergroups​, Groups and Subgroups
* Local Authority District​
    * England and Wales (NOMIS) ​
        * 2022 local authorities: district / unitary​ (LTLA)
    * Northern Ireland (NISRA) ​
        * Local Government District 2014​
    * Scotland ​(Scotland Cenusus)
        * Local authority (CA2019)​

## Description of files
A table that describes each of the files in the repo (like we did for the automated mapping repo)

## Data
### England and Wales
Data for E&W is collected from the bulk download availble on their census data platforms ([NOMIS 2021 Census Bulk Data Download](https://www.nomisweb.co.uk/sources/census_2021_bulk). Table codes generally start with "TS".

**Exceptions**
* England and Wales disability data required to calculate SIR -[disabilitycensus2021.xlsx on our SharePoint](https://officenationalstatistics.sharepoint.com/:x:/s/Geospat/ESTsbP6yeyJEqlAWqFI8E0MBKjSyzvNrxTzrfJozjRzYvA?e=LfgQr2&isSPOFile=1&xsdata=MDV8MDJ8fGQ0MTI1MTE5M2IzOTQ1MzU3NDM1MDhkZGFhNzQ2OTc5fDA3ODgwN2JmY2U4MjQ2ODhiY2UwMGQ4MTE2ODRkYzQ2fDB8MHw2Mzg4NTQxMzkxMTg5NzQwMDV8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxMMk5vWVhSekx6RTVPakJrWkRkaU5ERTNNVFV4WkRRM1pUTTRZelF3TXpRME9UZ3paamRsWWpjeFFIUm9jbVZoWkM1Mk1pOXRaWE56WVdkbGN5OHhOelE1T0RFM01URXhOakE0fGRjY2Y5OGM4MTJkZDQ4YjA3NDM1MDhkZGFhNzQ2OTc5fDZjYzBhZjc0ZGE4ZjQ4NmJiNmU2ZWVhOWM2YzIwZjhm&sdata=b2RXMXY5azRTUjhYWlg1V2RVTjNIanJoVTJKbXAxUmVMN3pQcCs3REJFbz0%3D&ovuser=078807bf-ce82-4688-bce0-0d811684dc46%2CElla.Goodman%40ons.gov.uk)
  
### Northern Ireland
Data for NI is collected from the bulk download availble on their census data platforms ([NISRA flexible table builder](https://build.nisra.gov.uk/en/)). Table codes generally start with "ni".

**Exceptions:**
* Northern Ireland Census 2021 - [MS-A14: Population density at Local Government District level for Northern Ireland](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density/resource/9a859cde-7da2-487a-86bd-dc5bfbaa4924). Popultion density for NI at other levels of geography is availble on [the UK Data Service](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density) **Note:** NI population density is in hectare's where as the others are in square KM, so this is converted in the code.
* Ethnic group for Bangladeshi - this data is not available for Northern Ireland 2021 - read more in the [assumptions_caveats.md](https://github.com/ONSgeo/Area_Classification/blob/main/docs/aqa/assumptions_caveats.md)
* Northern Ireland disability data required to calculate SIR - [MS-D02 Long-term health problem or disability by broad age bands [UPDATED]](https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-d02.xlsx) from [Census 2021 main statistics health, disability and unpaid care tables](https://www.nisra.gov.uk/publications/census-2021-main-statistics-health-disability-and-unpaid-care-tables)
  
### Scotland
At this time the bulk files are only available for the output area (OA) geography, so currently data for [Scotland is manually downloaded from Scotland's Census Search Census Data](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). The manual download was completed 22 April 2025 (two exceptions listed below). Note: it is not advised to aggregate from a lower level of geography (such as OA), if the geography is available as an option on the Flexible Table Builder as cell key perturbation has been used to help protect the confidentiality of data within tables. This means that cells might not sum to sub totals and totals due to these Statistical Disclosure Controls (SDC). When building tables using smaller geographies this protection is applied to a lot of cells, and doesn’t always cancel out. So there are differences when you add them all up. Perturbation is consistent and repeatable so will always be applied consistently when the same records contribute to the cell total.
Table codes generally start with "UV".

**Exceptions:**
* Scotlands's Census 2022: Ususal resident population density, Council Areas in [Table 4 in Scotlands Rounded population estimates](https://www.scotlandscensus.gov.uk/media/h5qokkij/scotland-s-census-2022-first-results-rounded-population-estimates-data.xlsx) Population density was downloaded 15 April 2025.
* Migrant indicator is available on the [Flexible Table Builder](https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml). Manually downloaded 22 April 2025.
* Scotland disability data required to calculate SIR - Table[UV303a](https://officenationalstatistics.sharepoint.com/:x:/s/Geospat/ERDnFH1wu_dMkMZ-uArn5pUBRv9ilznhCWD9tzZSNhLYdA?e=3g9mzZ) from [Flexible TableBuilder](https://www.scotlandscensus.gov.uk/search-the-census#/search-by)


## Look ups
* [Selected_codes_Lookup](https://github.com/ONSgeo/Area_Classification/blob/main/area_classification/pre_processing/Selected_codes_lookup.csv) has been created to run the EW, NI and Scot area classification for LAD. This will need updating if choosing to run at another level of geography or different combination of census'.
* Local_Authority_Districts_(December_2022)_Names_and_Codes_UK was downloaded from [Open Geography Portal](https://geoportal.statistics.gov.uk/search?q=NAC_LAD&sort=Date%20Created%7Ccreated%7Cdesc)


## Methodology / process description

### Data download

Do the manual data downloads first before running any of the scripts. Ensure they are in the same directory where the downloads will be stored. 

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

### Scotland Census 


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

