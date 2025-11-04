# WORK IN DEVELOPMENT
This repository contains the workflow for downlaoding, pre-processing, and performing analysis using k-means clustering to createa Area Classification for Local Authority District level data for the UK 2021/22 census'. It follows a process, similar to that described in the [2021 OAC Paper](https://rgs-ibg.onlinelibrary.wiley.com/doi/full/10.1111/geoj.12550).   

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

# Data
### England and Wales
Data for E&W is collected from the bulk download available on their census data platforms ([NOMIS 2021 Census Bulk Data Download](https://www.nomisweb.co.uk/sources/census_2021_bulk)). Table codes generally start with "TS".

**Exceptions:**
* Manual download needed for England and Wales disability data required to calculate Standardised Illness Ratio (SIR)
### Northern Ireland
Data for Northern Ireland (NI) is collected from the bulk download available on their census data platforms ([NISRA flexible table builder](https://build.nisra.gov.uk/en/)). Table codes generally start with "ni".

**Exceptions:**
* Ethnic group for Bangladeshi - this data is not available for Northern Ireland 2021 - read more in the [assumptions_caveats.md](https://github.com/ONSgeo/Area_Classification/blob/main/docs/analytical_quality_assurance/assumptions_caveats.md)
* Manual download needed for Northern Ireland Census 2021 Population Density data at the Local Government District level. Population density for Northern Ireland at other levels of geography is available on [the UK Data Service](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density).<br>**Note:** Northern Ireland population density is in hectare's whereas the others are in square KM, so this is converted in the code.
* Manual download needed for Northern Ireland disability data required to calculate SIR.
  
### Scotland
At this time the bulk files are only available for the output area (OA) geography, so currently data for [Scotland is manually downloaded from Scotland's Census Search Census Data](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). Table codes generally start with "UV". The manual download was completed 22 April 2025 (three exceptions listed below).<br>**Note:** it is not advised to aggregate from a lower level of geography (such as OA), if the geography is available as an option on the Flexible Table Builder as cell key perturbation has been used to help protect the confidentiality of data within tables. This means that cells might not sum to sub totals and totals due to these Statistical Disclosure Controls (SDC). When building tables using smaller geographies this protection is applied to a lot of cells and doesn’t always cancel out. So, there are differences when you add them all up. Perturbation is consistent and repeatable so will always be applied consistently when the same records contribute to the cell total.

**Exceptions:**<br>
Manual downloads needed for:
* Census 2022 table 'population density'. Population density table was downloaded 15 April 2025.
* Census 2022 table 'migrant indicator'. Migrant indicator table was downloaded 22 April 2025.
* Census 2022 disability data required to calculate SIR.


## Look ups
* [UK_selected_codes_lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) has been created to run the England and Wales (EW), Northern Ireland (NI) and Scotland (Scot) area classification for Local Authority Districts (LAD). This will need updating if choosing to run at another level of geography or different combination of census'.
* A Local Authority Districts Names and Codes in the UK Lookup is required to convert between area names and area codes.
* 

# Methodology / process description

## Set Up 

Firstly, clone the repo locally. If you need support cloning the repo, take a look at [The GitHub Cloning a repository instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or if you are working with Visual Studio code take a look at [Clone and use a GitHub repository in Visual Studio Code instructions](https://learn.microsoft.com/en-us/azure/developer/javascript/how-to/with-visual-studio-code/clone-github-repository?tabs=activity-bar).

### Folders setup
When your repository is cloned, find the repository within your file explorer. 
Locate the 'data' folder. Within this, a folder called **'lookups'** should already exist. In this 'data/lookups' folder the [Selected_codes_Lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) will already exist. 

Going back to the 'data' folder, create a new folder called **'inputs'**.
Within the 'data/inputs' folder create three new folders:
* **'ew_downloads'**
* **'ni_downloads'**
* **'scot_downloads'**

## Data download
As mentioned above, some data requires manual downloads, so before running any of the scripts, ensure the data listed below has been downloaded and saved in the correct folders listed.

### **'lookups'**:<br>
* Local Authority Districts Names and Codes in the UK Lookup from the [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/). We used [Local Authority Districts (December 2022) Names and Codes in the UK](https://geoportal.statistics.gov.uk/datasets/42af123c4663466496dafb4c8fcb0c82_0/explore). This is required to convert between are names and area codes.
* 

### **'ew_downloads'**:<br>
* England and Wales disability data [disabilitycensus2021.xlsx from the ONS website](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/disability/datasets/disabilityinenglandandwales2021). The file name should be 'disabilitycensus2021.xlsx'.

### **'ni_downloads'**:<br>
* Northern Ireland disability data [MS-D02 Long-term health problem or disability by broad age bands [UPDATED]](https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-d02.xlsx) from [Census 2021 main statistics health, disability and unpaid care tables](https://www.nisra.gov.uk/publications/census-2021-main-statistics-health-disability-and-unpaid-care-tables). The file should be named 'census-2021-ms-d02.xlsx'.<br>
* Northern Ireland Census 2021 [MS-A14: Population density at Local Government District level for Northern Ireland](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density/resource/9a859cde-7da2-487a-86bd-dc5bfbaa4924) and ensure it is named 'census-2021-ms-a14-LGD.xlsx'.<br>

### **'scot_downloads'**:<br> 
* Scotland's Census 2022: Usual resident population density, Council Areas in [Table 4 in Scotlands Rounded population estimates](https://www.scotlandscensus.gov.uk/media/h5qokkij/scotland-s-census-2022-first-results-rounded-population-estimates-data.xlsx). The file should be renamed 'population_density.xlsx'.<br>

* Scotland's 'migrant indicator' data [from the Flexible Table Builder](https://www.scotlandscensus.gov.uk/webapi/jsf/dataCatalogueExplorer.xhtml):
   - Select 'New table' in the bottom left
   - Scroll through the 'Fields' section to find 'Migration'
   - Click on 'Migrant indicator' in the 'Migration' folder
   - Select all 5 options in the drop down
   - Drag to the table area and select 'column'
	- Then scroll the 'Fields' section to find 'Geography'
	- Select all in 'Council Area 2019' and drag into the table area and select 'row'
   - Now click the 'retrieve data' button to build the table
   - Download table as a csv
   - The file should be renamed 'migrant_indicator.csv'

* Scotland tables from the [Scotland Census table builder search](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). For each table:
   - Select data from 2022
   - Select data by location - Local authority (CA2019) - 'Select all'
   - Use the Search function to find the table IDs listed below
   - Then use the dropdown to the left of the 'Download table' button to select 'Comma Separated Value (.csv)'
   - Click 'Download table':
  
| table_ID |	table_name |	country |
| -------- |   ---------- |   ------- |
| UV101b |	Usual resident population by sex by age (6) |	scot|
| UV103 |	Age |	scot|
| UV104 |	Marital and civil partnership status |	scot|
| UV113 |	Household composition - Households |	scot|
| UV201 |	Ethnic group (21) | 	scot|
| UV203 |	Multiple ethnic groups |	scot|
| UV204 |	Country of birth | 	scot|
| UV205 |	Religion |	scot|
| UV210 |	English language skills |	scot|
| UV301 |	Provision of unpaid care |	scot|
| UV303a | Long-term health problem or disability by sex by age (20 groups) | soct|
| UV402 |	Accommodation type - Households |	scot|
| UV404 |	Household tenure - Households | scot|
| UV405 |	Car or van availability |	scot|
| UV415 |	Occupancy rating for bedrooms |	scot|
| UV501 |	Highest level of qualification |	scot|
| UV601 |	Economic activity |	scot|
| UV604 |	Hours worked |	scot|
| UV606 |	Occupation |	scot|
| UV607 |	National Statistics Socio-economic Classification (NS-SeC) |	scot|


#### Set Up - folders and download data diagram
Your file structure should look like the following. Text in red are the folders and CSV file which already exist in the repo. The text in black are the folders you need to manually create, and files which you need to download and save as mentioned in instructions above.

<img width="646" height="1080" alt="area classification file structure for README (1)" src="https://github.com/user-attachments/assets/7dc6dc56-4192-4d84-ad9d-56a8a9e18529" />



## Process
The flow diagram shows the stages of the area classification proccess
<img width="475" height="349" alt="Methods_diagram" src="https://github.com/user-attachments/assets/224dcb2f-2544-47bc-aac9-234907619bbf" />
<span style="color: red;">THIS NEEDS REVISITING AND UPDATING - LINK ON SHAREPOINT</span> .

The python code:
* Download the bulk census data from [Nomis](https://www.nomisweb.co.uk/sources/census_2021_bulk)
* Import the LTLA Area level data into python
* Create new variable names based on the sequential ordering of the variables and the table identification code
* Merges all of the variables for Northern Ireland into one table
* Create a metadata lookup table providing the link between the new names and the original names

* Finds the available variables from the [NISRA Table Builder](https://build.nisra.gov.uk/)
* Scrapes the tables for each variable using beautiful soup
* Create new variable names based on the sequential ordering of the variables and the table identification code
* Merges all of the variables for Northern Ireland into one table
* Create a metadata lookup table providing the link between the new names and the original names


The created CSV are available in the folder ["/output_data/csv"](/output_data/csv) and the parquet files in the folder ["/output_data/parquet"](/output_data/parquet)
## Output
Lookup tables allocating each area code for the Local Authority Districts equivlents in England, Wales, Northern Ireland and Scotland to clusters for supergroup, group and subgroup.

## Limitations
## Future scope
This pipeline could be adapted in future to work for different levels of geography. This would not be possible running this current code as due to the inconsistancies of raw data tables deivlered from different conutries' census', there has been a rewuirement to hard code some of the pre-processing stages to ensure consistancy between datasets when feeding into the clustering algorithm.
## Contacts / authors / 
[ONS Geography inbox](https://github.com/ONSgeo/Access_To_Amenities/blob/main/ONS.Geography@ons.gov.uk)

## Acknowledgements
Thanks to Jakub Wyszomierski (jakubwyszomierski), Owen Goodwin (ogoodwin505) and Alex Singleton (alexsingleton) at the Geographic Dara Service for their early code which formed the starting point of this repo.
[Geographic Data Service](https://github.com/Geographic-Data-Service)
[Census_2021_Output_Areas](https://github.com/Geographic-Data-Service/Census_2021_Output_Areas) (England and Wales)
[Scotland_Census_2022_OA](https://github.com/Geographic-Data-Service/Scotland_Census_2022_OA)
[Northern_Ireland_Census_2022_Data_Zone](https://github.com/Geographic-Data-Service/Northern_Ireland_Census_2022_Data_Zone)
[Geodemographic Python Example](https://github.com/ogoodwin505/pygeodem)
