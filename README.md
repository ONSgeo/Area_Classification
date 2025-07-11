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
    * Scotland ​(Scotland Census)
        * Local authority (CA2019)​

## Description of files
A table that describes each of the files in the repo (like we did for the automated mapping repo)

## Data
### England and Wales
Data for E&W is collected from the bulk download available on their census data platforms ([NOMIS 2021 Census Bulk Data Download](https://www.nomisweb.co.uk/sources/census_2021_bulk). Table codes generally start with "TS".

**Exceptions**
* England and Wales disability data required to calculate SIR -[disabilitycensus2021.xlsx from the Office for National Statistics (ONS) website](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/disability/datasets/disabilityinenglandandwales2021)
  
### Northern Ireland
Data for Northern Ireland (NI) is collected from the bulk download available on their census data platforms ([NISRA flexible table builder](https://build.nisra.gov.uk/en/)). Table codes generally start with "ni".

**Exceptions:**
* Ethnic group for Bangladeshi - this data is not available for Northern Ireland 2021 - read more in the [assumptions_caveats.md](https://github.com/ONSgeo/Area_Classification/blob/main/docs/aqa/assumptions_caveats.md)
* Northern Ireland Census 2021 - [MS-A14: Population density at Local Government District level for Northern Ireland](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density/resource/9a859cde-7da2-487a-86bd-dc5bfbaa4924). Population density for Northern Ireland at other levels of geography is available on [the UK Data Service](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density) **Note:** Northern Ireland population density is in hectare's whereas the others are in square KM, so this is converted in the code.
* Northern Ireland disability data required to calculate SIR - [MS-D02 Long-term health problem or disability by broad age bands [UPDATED]](https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-d02.xlsx) from [Census 2021 main statistics health, disability and unpaid care tables](https://www.nisra.gov.uk/publications/census-2021-main-statistics-health-disability-and-unpaid-care-tables)
  
### Scotland
At this time the bulk files are only available for the output area (OA) geography, so currently data for [Scotland is manually downloaded from Scotland's Census Search Census Data](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). The manual download was completed 22 April 2025 (two exceptions listed below). Note: it is not advised to aggregate from a lower level of geography (such as OA), if the geography is available as an option on the Flexible Table Builder as cell key perturbation has been used to help protect the confidentiality of data within tables. This means that cells might not sum to sub totals and totals due to these Statistical Disclosure Controls (SDC). When building tables using smaller geographies this protection is applied to a lot of cells and doesn’t always cancel out. So, there are differences when you add them all up. Perturbation is consistent and repeatable so will always be applied consistently when the same records contribute to the cell total.
Table codes generally start with "UV".

**Exceptions:**
* Scotland's Census 2022: Usual  resident population density, Council Areas in [Table 4 in Scotland's Rounded population estimates](https://www.scotlandscensus.gov.uk/media/h5qokkij/scotland-s-census-2022-first-results-rounded-population-estimates-data.xlsx) Population density was downloaded 15 April 2025.
* Migrant indicator is available on the [Flexible Table Builder](https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml). Manually downloaded 22 April 2025.
* Scotland disability data required to calculate SIR - Table[UV303a](https://officenationalstatistics.sharepoint.com/:x:/s/Geospat/ERDnFH1wu_dMkMZ-uArn5pUBRv9ilznhCWD9tzZSNhLYdA?e=3g9mzZ) from [Flexible TableBuilder](https://www.scotlandscensus.gov.uk/search-the-census#/search-by)


## Look ups
* [Selected_codes_Lookup](https://github.com/ONSgeo/Area_Classification/blob/main/area_classification/pre_processing/Selected_codes_lookup.csv) has been created to run the England and Wales (EW), Northern Ireland (NI) and Scotland (Scot) area classification for Local Authority Districts (LAD). This will need updating if choosing to run at another level of geography or different combination of census'.
* A Local Authority Districts Names and Codes in the UK Lookup is required to convert between are names and area codes. Download a the look up from the [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/). We used [Local Authority Districts (December 2022) Names and Codes in the UK](https://geoportal.statistics.gov.uk/datasets/42af123c4663466496dafb4c8fcb0c82_0/explore). This CSV should be saved into the repo in 'data/lookups' folder, if saved elsewhere update the file path in the config.yaml.

## Methodology / process description

### Set Up - folders and download data

As mentioned above, some data requires manual downloads, so before running any of the scripts, ensure the data listed below has been downloaded and saved in the correct locations listed.

Firstly, clone the repo locally. If you need support cloning the repo, take a look at [The GitHub Cloning a repository instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or if you are working with Visual Studio code take a look at [Clone and use a GitHub repository in Visual Studio Code instructions](https://learn.microsoft.com/en-us/azure/developer/javascript/how-to/with-visual-studio-code/clone-github-repository?tabs=activity-bar)

When your repository is cloned, find the repository within your file explorer.
Locate the 'data' folder, a folder called 'lookups' should already exist. In this 'data/lookups' folder download save the Local_Authority_Districts_(December_2022)_Names_and_Codes_UK which you have downloaded from [Open Geography Portal](https://geoportal.statistics.gov.uk/search?q=NAC_LAD&sort=Date%20Created%7Ccreated%7Cdesc)

Going back to the 'data' folder, create a new folder called 'inputs'.

Within the 'data/inputs' folder create three new folders:
* 'ew_downloads'. In this folder manually download and save England and Wales disability data [disabilitycensus2021.xlsx from the ONS website](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/disability/datasets/disabilityinenglandandwales2021). The file name should be 'disabilitycensus2021.xlsx'.
* 'ni_downloads'. In this folder manually download and save Northern Ireland disability data [MS-D02 Long-term health problem or disability by broad age bands [UPDATED]](https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-d02.xlsx). The file should be named 'census-2021-ms-d02.xlsx'.
     - Within the 'data/inputs/ni_downlaods' also save Northern Ireland Census 2021 [MS-A14: Population density at Local Government District level for Northern Ireland](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density/resource/9a859cde-7da2-487a-86bd-dc5bfbaa4924). and ensure it is named 'census-2021-ms-a14-LGD.xlsx'.
* 'scot_downloads'. In this folder download and save the following Scotland tables:
  
| table_ID |	table_name |	country |
| -------- |   ---------- |   ------- |
| UV101b |	Usual resident population by sex by age (6) |	scot|
| UV103 |	Age |	scot|
| UV104 |	Marital and civil partnership status |	scot|
| UV112 |	Household composition - People |	scot|
| UV201 |	Ethnic group (21) | 	scot|
| UV203 |	Multiple ethnic groups |	scot|
| UV204 |	Country of birth | 	scot|
| UV205 |	Religion |	scot|
| UV210 |	English language skills |	scot|
| UV301 |	Provision of unpaid care |	scot|
| UV401 |	Accommodation type - People |	scot|
| UV403 |	Household tenure - People |	scot|
| UV405 |	Car or van availability |	scot|
| UV415 |	Occupancy rating for bedrooms |	scot|
| UV501 |	Highest level of qualification |	scot|
| UV601 |	Economic activity |	scot|
| UV606 |	Occupation |	scot|
| UV607 |	National Statistics Socio-economic Classification (NS-SeC) |	scot|

   - Additionally, in the 'data/inputs/scot_downloads' folder download and save: 
      - The Scottish disability data Table[UV303a](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). The file should be named 'UV303a.csv'.
      - Scotland's Census 2022: Usual resident population density, Council Areas in [Table 4 in Scotlands Rounded population estimates](https://www.scotlandscensus.gov.uk/media/h5qokkij/scotland-s-census-2022-first-results-rounded-population-estimates-data.xlsx). The file should be renamed 'population_density.csv'.
      - Scotland's migrant indicator data [from the Flexible Table Builder](https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml). The file should be renamed 'migrant_indicator_percentage'.
#### Set Up - folders and download data diagram
Your file structure should look like the following. Text in red are the folders and CSV file which already exist in the repo. The text in black are the folders you need to manually create, and files which you need to download and save as mentioned in instructions above.
<img width="646" height="1080" alt="area classification file structure for README (5)" src="https://github.com/user-attachments/assets/d3b389f3-d1bb-4c38-bb20-7ca665703dd9" />

## Output
## Limitations
## Future scope
## Contacts / authors / 
[ONS Geography inbox](https://github.com/ONSgeo/Access_To_Amenities/blob/main/ONS.Geography@ons.gov.uk)

## Acknowledgements
Thanks to Owen Goodwin (ogoodwin505) and Alex Singleton (alexsingleton) at the ONS Data Science Office for their early code which formed the basis of this repo.
[ONS Data Science Office](https://github.com/Geographic-Data-Service)
[Census_2021_Output_Areas](https://github.com/Geographic-Data-Service/Census_2021_Output_Areas) (England and Wales)
[Scotland_Census_2022_OA](https://github.com/Geographic-Data-Service/Scotland_Census_2022_OA)
[Northern_Ireland_Census_2022_Data_Zone](https://github.com/Geographic-Data-Service/Northern_Ireland_Census_2022_Data_Zone)
[Geodemographic Python Example](https://github.com/ogoodwin505/pygeodem)

# Previous README:
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

