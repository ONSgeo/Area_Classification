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
Look up V60 variables
Old	New 	Country
	v1	
	v2	
![image](https://github.com/user-attachments/assets/f48baab0-5be5-40cf-a7fd-f21e7568f3f5)

### England and Wales and Northern Ireland
Data for E&W and NI is collected from the bulk downloads availble on their respective census data platforms ([NOMIS 2021 Census Bulk Data Download](https://www.nomisweb.co.uk/sources/census_2021_bulk) , [NISRA flexible table builder](https://build.nisra.gov.uk/en/))
* Ususal residents per square kilometer doesnt exist for NI, there is population desinsty per LGD in the 2022 Mid-year population estimates.

### Scotland
At this time the bulk files are only available for the output area (OA) geography, so currently data for [Scotland is manually downloaded from Scotland's Census Search Census Data](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). The manual download was completed 22 April 2025 (two exceptions listed below). Note: it is not advised to aggregate from a lower level of geography (such as OA), if the geography is available as an option on the Flexible Table Builder as cell key perturbation has been used to help protect the confidentiality of data within tables. This means that cells might not sum to sub totals and totals due to these Statistical Disclosure Controls (SDC). When building tables using smaller geographies this protection is applied to a lot of cells, and doesn’t always cancel out. So there are differences when you add them all up. Perturbation is consistent and repeatable so will always be applied consistently when the same records contribute to the cell total.

**Exceptions:**
* Migrant indicator is available on the [Flexible Table Builder](https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml). Manually downloaded 22 April 2025.
* Scotlands's Census 2022: Ususal resident population density, Council Areas in [Table 4 in Scotlands Rounded population estimates](https://www.scotlandscensus.gov.uk/media/h5qokkij/scotland-s-census-2022-first-results-rounded-population-estimates-data.xlsx) Population density was downloaded 15 April 2025.
* **Disability data**
	* England and Wales - [disabilitycensus2021.xlsx](https://officenationalstatistics.sharepoint.com/:x:/s/Geospat/ESTsbP6yeyJEqlAWqFI8E0MBKjSyzvNrxTzrfJozjRzYvA?e=LfgQr2&isSPOFile=1&xsdata=MDV8MDJ8fGQ0MTI1MTE5M2IzOTQ1MzU3NDM1MDhkZGFhNzQ2OTc5fDA3ODgwN2JmY2U4MjQ2ODhiY2UwMGQ4MTE2ODRkYzQ2fDB8MHw2Mzg4NTQxMzkxMTg5NzQwMDV8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxMMk5vWVhSekx6RTVPakJrWkRkaU5ERTNNVFV4WkRRM1pUTTRZelF3TXpRME9UZ3paamRsWWpjeFFIUm9jbVZoWkM1Mk1pOXRaWE56WVdkbGN5OHhOelE1T0RFM01URXhOakE0fGRjY2Y5OGM4MTJkZDQ4YjA3NDM1MDhkZGFhNzQ2OTc5fDZjYzBhZjc0ZGE4ZjQ4NmJiNmU2ZWVhOWM2YzIwZjhm&sdata=b2RXMXY5azRTUjhYWlg1V2RVTjNIanJoVTJKbXAxUmVMN3pQcCs3REJFbz0%3D&ovuser=078807bf-ce82-4688-bce0-0d811684dc46%2CElla.Goodman%40ons.gov.uk)
	* Northern Ireland - [MS-D02 Long-term health problem or disability by broad age bands [UPDATED]](https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-d02.xlsx) from [Census 2021 main statistics health, disability and unpaid care tables](https://www.nisra.gov.uk/publications/census-2021-main-statistics-health-disability-and-unpaid-care-tables)
  	* Scotland - Table[UV303](https://officenationalstatistics.sharepoint.com/:x:/s/Geospat/ES29JjTPXwtOljbsv--2hyoBKPRG9DJfqIVUYKJbWrAeWA?e=wYiyEp) from [Flexible TableBuilder](https://www.scotlandscensus.gov.uk/search-the-census#/search-by)
## Methodology / process description


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

