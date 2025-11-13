# Area Classification
This repository contains the workflow for downloading, pre-processing, performing clustering using k-means and post processing to create an Area Classification for Local Authority District (LAD) level data for the UK 2021/22 census'. It follows a process, similar to that described in the [2021 OAC Paper](https://rgs-ibg.onlinelibrary.wiley.com/doi/full/10.1111/geoj.12550).   

# Background
Area Classification - “a hierarchical geodemographic classification across the UK which identifies areas of the country with similar characteristics.” [Geographic Data Service (GeoDS)​](https://data.geods.ac.uk/dataset/output-area-classification-2021#:~:text=The%202021%20Classification%20for%20Output,which%20provides%20a%20thorough%20evaluation.)

Current focus:
* 2021 ​
* Supergroups​, Groups and Subgroups
* Local Authority District​ (LAD)
    * England and Wales (NOMIS) ​
        * 2022 local authorities: district / unitary​ (LTLA)
    * Northern Ireland (NISRA) ​
        * Local Government District 2014​ (LGD)
    * Scotland ​(Scotland Census)
        * Local authority (CA2019)​

# Data
This section explains the data used in this pipeline. Later in this ReadMe you will find the [Data Downlaod section](https://github.com/ONSgeo/Area_Classification/blob/main/README.md#data-download) within [Set-up](https://github.com/ONSgeo/Area_Classification/blob/main/README.md#set-up ) which provides links and instructions for downloading the data mentioned in this section. 

### England and Wales
Data for England and Wales is collected from the bulk download available on their census data platforms ([NOMIS 2021 Census Bulk Data Download](https://www.nomisweb.co.uk/sources/census_2021_bulk)). Table codes generally start with "TS".

**Exceptions:**
* Manual download needed for England and Wales disability data required to calculate Standardised Illness Ratio (SIR).
### Northern Ireland
Data for Northern Ireland is collected from the bulk download available on their census data platforms ([NISRA flexible table builder](https://build.nisra.gov.uk/en/)). Table codes generally start with "ni".

**Exceptions:**
* Ethnic group for Bangladeshi - this data is not available for Northern Ireland 2021 - read more in the [assumptions_caveats.md](https://github.com/ONSgeo/Area_Classification/blob/main/docs/analytical_quality_assurance/assumptions_caveats.md).
* Manual download needed for Northern Ireland Census 2021 Population Density data at the Local Government District level. Population density for Northern Ireland at other levels of geography is available on [the UK Data Service](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density).<br>**Note:** Northern Ireland population density is in hectare's whereas the others are in square KM, so this is converted in the code.
* Manual download needed for Northern Ireland disability data required to calculate SIR.
  
### Scotland
At this time the bulk files are only available for the output area (OA) geography, so currently data for [Scotland is manually downloaded from Scotland's Census Search Census Data](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). Table codes generally start with "UV". The manual download was completed 22 April 2025.

**Exceptions:**<br>
Manual downloads needed for:
* Census 2022 table 'population density'. Population density table was downloaded 15 April 2025.
* Census 2022 table 'migrant indicator'. Migrant indicator table was downloaded 22 April 2025.
* Census 2022 disability data required to calculate SIR.

<br>**Note:** it is not advised to aggregate from a lower level of geography (such as OA), if the geography is available as an option on the Flexible Table Builder as cell key perturbation has been used to help protect the confidentiality of data within tables. This means that cells might not sum to sub totals and totals due to these Statistical Disclosure Controls (SDC). When building tables using smaller geographies this protection is applied to a lot of cells and doesn’t always cancel out. So, there are differences when you add them all up. Perturbation is consistent and repeatable so will always be applied consistently when the same records contribute to the cell total.

## Look ups
* [UK_selected_codes_lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) has been created to run the 2021 England and Wales (EW), 2021 Northern Ireland (NI) and 2022 Scotland (Scot) area classification for Local Authority Districts (LAD). This will need updating if choosing to run at another level of geography or different combination of census'.
* A Local Authority Districts Names and Codes in the UK Lookup is required from the [ONS Geography Portal](https://geoportal.statistics.gov.uk/) to convert between area names and area codes.


## Process
The flow diagram shows the stages of the area classification process:

<img width="542" height="456" alt="Methods_diagram (4)" src="https://github.com/user-attachments/assets/e827d2b6-b4a0-4375-919b-8de5a8595b83" />

[Clicking this link will open the image in a separate  window to allow you to zoom in if needed](https://github.com/user-attachments/assets/e827d2b6-b4a0-4375-919b-8de5a8595b83)

### Folder structure
[The folder and script structure can be found in the user guide folder.](https://github.com/ONSgeo/Area_Classification/blob/main/docs/user_guide/repo_structure.md)

## Set Up 
Firstly, clone the repo locally. If you need support cloning the repo, take a look at [the GitHub cloning a repository instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or if you are working with Visual Studio code take a look at [clone and use a GitHub repository in Visual Studio Code instructions](https://learn.microsoft.com/en-us/azure/developer/javascript/how-to/with-visual-studio-code/clone-github-repository?tabs=activity-bar).

### Requirements 
To start using this project, first make sure your system meets its
requirements.

It's suggested that you install this package and its requirements within
a virtual environment.

- Python 3.1-3.4 installed

Contributors have some additional requirements - please see our [contributing guidance][contributing].

#### Installing the package

Whilst in the root folder, in a terminal, you can install the package and its
Python dependencies using:

```shell
python -m pip install -U pip setuptools
pip install -e .
```

#### Install for contributors (Python only)

To install the contributing requirements, use:
```shell
python -m pip install -U pip setuptools
pip install -e .[dev]
pre-commit install
```

This installs an editable version of the package. This means that when you update the
package code you do not have to reinstall it for the changes to take effect.
This saves a lot of time when you test your code.

Remember to update the setup and requirement files inline with any changes to your
package.

#### Running the pipeline (Python only)

The entry point for the pipeline is stored within the package and called `run_pipeline.py`.
To run the pipeline, run the following code in the terminal (either in the root directory of the
project, or by specifying the path to `run_pipeline.py` from elsewhere).

```shell
python src/area_classification/run_pipeline.py
```

Alternatively, most Python IDEs allow you to run the code directly using a `run` button.

### Folders setup
When your repository is cloned, find the repository within your file explorer. 
Locate the 'data' folder. Within this, a folder called **'lookups'** should already exist. In this 'data/lookups' folder the [Selected_codes_Lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) will already exist. 

Going back to the 'data' folder, create a new folder called **'inputs'**. This is where the downloaded census tables will be stored.
Within the 'data/inputs' folder create three new folders:
* **'ew_downloads'**
* **'ni_downloads'**
* **'scot_downloads'**

Also in the 'data/inputs' folder, create a new folder called **'population_density'**. This is where data used to calculate population densities of each output cluster will be stored. 

## Data download
As mentioned above, some data requires manual downloads, so before running any of the scripts, ensure the data listed below has been downloaded and saved in the correct folders listed.<br>

For more information on the data (England/Wales and Northern Ireland census tables) that is automatically downloaded when running the pipeline via API's, see the [downloading data page in the specifications folder.](https://github.com/ONSgeo/Area_Classification/blob/main/docs/specifications/Downloading_data.md)

#### 'population_density' folder:<br>
* Download Mid-2022 and Mid-2021 [Estimates of the population for the UK, England, Wales, Scotland, and Northern Ireland](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland). Once downloaded and saved in this folder, rename the files to 'population_2021.xls' and 'population_2022.xlsx'.
* Download csv versions of [Standard Area Measurements for Administrative Areas (December 2021) in the UK (V2)](https://geoportal.statistics.gov.uk/datasets/ba0873184e6349bebb63b5da6dd050b5/about) and [Standard Area Measurements for Administrative Areas (December 2022) in the UK (V2)](https://geoportal.statistics.gov.uk/datasets/235c70d40c494361bd6b0ddaebdf0bad/about) from the Open Geography Portal. From the zip files, save the SAM_LAD_DEC_2021_UK.csv and SAM_LAD_DEC_2022_UK_V2.csv respectively to this folder.

#### 'lookups' folder:<br>
* Local Authority Districts Names and Codes in the UK Lookup from the [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/). We used [Local Authority Districts (December 2022) Names and Codes in the UK](https://geoportal.statistics.gov.uk/datasets/42af123c4663466496dafb4c8fcb0c82_0/explore). This is required to convert between are names and area codes.

#### 'ew_downloads' folder:<br>
* England and Wales disability data [disabilitycensus2021.xlsx from the ONS website](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/disability/datasets/disabilityinenglandandwales2021). The file name should be 'disabilitycensus2021.xlsx'.

#### 'ni_downloads' folder:<br>
* Northern Ireland disability data [MS-D02 Long-term health problem or disability by broad age bands [UPDATED]](https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-d02.xlsx) from [Census 2021 main statistics health, disability and unpaid care tables](https://www.nisra.gov.uk/publications/census-2021-main-statistics-health-disability-and-unpaid-care-tables). The file should be named 'census-2021-ms-d02.xlsx'.<br>
* Northern Ireland Census 2021 [MS-A14: Population density at Local Government District level for Northern Ireland](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density/resource/9a859cde-7da2-487a-86bd-dc5bfbaa4924) and ensure it is named 'census-2021-ms-a14-LGD.xlsx'.<br>

#### 'scot_downloads' folder:<br> 
* Scotland's Census 2022: Usual resident population density, Council Areas in [Table 4 in Scotland's Rounded population estimates](https://www.scotlandscensus.gov.uk/media/h5qokkij/scotland-s-census-2022-first-results-rounded-population-estimates-data.xlsx). The file should be renamed 'population_density.xlsx'.<br>

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
   - Click 'Download table'
  
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

<img width="576" height="1085" alt="area classification file structure for README (5)" src="https://github.com/user-attachments/assets/4221b59e-ad10-4862-b036-ca5a7acb5fba" />
[Clicking this link will open the image in a separate  window to allow you to zoom in if needed.](https://github.com/user-attachments/assets/4221b59e-ad10-4862-b036-ca5a7acb5fba)

## Output
Lookup tables allocating each area code for the Local Authority Districts equivalent in England, Wales, Northern Ireland and Scotland to clusters for supergroup, group and subgroup.

This repo contains a [QA script](https://github.com/ONSgeo/Area_Classification/blob/main/area_classification/utilities/qa_functions.py). This is currently not embedded in the pipeline but, can be ran on any data frame from any stage of the pipeline. The QA script checks for the expected values, zero values, duplicate values and descriptors like range. 

## Limitations
These are high level limitations of the overall pipeline. For more specific limitations for each pipeline component see [Specifications folder](https://github.com/ONSgeo/Area_Classification/tree/main/docs/specifications):
1. **Combining data from two separate years** - Census for EW, NI and Scot are usually conducted in line with each other. However due to the [impact of COVID-19, Scotland moved their census to 2022](https://www.scotlandscensus.gov.uk/news-and-events/news-release-scotland-s-census-to-be-moved-to-march-2022/). This difference in time may have affected responses to variables across the devolved administrations, particularly, it may have affected responses to questions around employment and effect the variables included in this research. Additionally, it is possible if individuals moved house between 2021 and 2022, they may have been included or excluded from both census'. This may raise considerations of the utility of this classification produced given the special circumstances at the time of COVID 19.
2. **Choice of variables** - The variables used in this pipeline have been chosen in line with the earlier work on the [2021 Output Area Classification](https://data.geods.ac.uk/dataset/output-area-classification-2021) which used Census data. If other variables were used (including those not from Census), the clustering may differ.
3. **Level of geography** - This pipeline looks at Local Authority District (LAD) levels of geography (LTLA, LGD and CA19), and so will not reflect the heterogeneity within LADs. 
More detailed limitations can be found in the [Specifications folder](https://github.com/ONSgeo/Area_Classification/tree/main/docs/specifications).

## Future scope
This pipeline could be adapted in future to work for different levels of geography. This would not be possible running this current code as due to the inconsistencies of the raw data tables from different countries' census', there has been a requirement to hard code some of the pre-processing stages to ensure consistency between datasets when feeding into the clustering algorithm.

## Licence

Unless stated otherwise, the codebase is released under the MIT License. This covers
both the codebase and any sample code in the documentation. The documentation is ©
Crown copyright and available under the terms of the Open Government 3.0 licence.

## Acknowledgements
Thanks to Jakub Wyszomierski (jakubwyszomierski), Owen Goodwin (ogoodwin505) and Alex Singleton (alexsingleton) at the Geographic Dara Service for their early code which formed the starting point of this repo.
- [Geographic Data Service](https://github.com/GeographicDataService)
- [OAC2021-2](https://github.com/GeographicDataService/OAC2021-2)
- [Census_2021_Output_Areas](https://github.com/alexsingleton/Census_2021_Output_Areas) (England and Wales)
- [Scotland_Census_2022_OA](https://github.com/GeographicDataService/Scotland_Census_2022_OA).
- [Northern_Ireland_Census_2022_Data_Zone](https://github.com/GeographicDataService/Northern_Ireland_Census_2022_Data_Zone)
- [Geodemographic Python Example](https://github.com/ogoodwin505/pygeodem)
  
This project structure is based on the [`govcookiecutter` template project][govcookiecutter].

[contributing]: https://github.com/best-practice-and-impact/govcookiecutter/blob/main/%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/contributor_guide/CONTRIBUTING.md
[govcookiecutter]: https://github.com/best-practice-and-impact/govcookiecutter
[docs-loading-environment-variables]: https://github.com/best-practice-and-impact/govcookiecutter/blob/main/%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/user_guide/loading_environment_variables.md
[docs-loading-environment-variables-secrets]: https://github.com/best-practice-and-impact/govcookiecutter/blob/main/%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/user_guide/loading_environment_variables.md#storing-secrets-and-credentials

## Contributing

If you want to help us build and improve `area_classification`, please take a look at our [contributing guidance][contributing].

## Contacts
[ONS Geography inbox](mailto:ons.geography@ons.gov.uk)


