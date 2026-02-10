# Local Authority Districts Area Classification
This repository contains the pipeline for creation of the Area Classification at Local Authority District (LAD) level using data from the censuses of the UK in 2021 & 2022. It includes downloading, pre-processing, performing clustering using k-means and post processing scripts, and follows a process, similar to that described in the [2021 OAC Paper](https://rgs-ibg.onlinelibrary.wiley.com/doi/full/10.1111/geoj.12550).   

The output of this pipeline includes a table allocating each LAD to a Supergroup, Group and Subgroup, based on input census data, as well as supporting materials in the form of radial plots and clustergrams.

This is a packaged pipeline, you can install the package (instructions **4.1.1 Installing the package**) or clone the repository to run it.

# 1.0 Background
Area Classification: a hierarchical geodemographic classification across the UK which identifies areas of the country with similar characteristics. [Geographic Data Service (GeoDS)​](https://data.geods.ac.uk/dataset/output-area-classification-2021#:~:text=The%202021%20Classification%20for%20Output,which%20provides%20a%20thorough%20evaluation.)

Repo focus:
* 2021 and 2022 UK censuses
* Supergroups​, Groups and Subgroups
* Local Authority District​ (LAD) equivalents
    * England and Wales (EW)​
        * [NOMIS](https://www.nomisweb.co.uk/): <i>2022 local authorities: district / unitary​ (LTLA)</i>
    * Northern Ireland (NI)​
        * [NISRA](https://www.nisra.gov.uk/): <i>Local Government District 2014​ (LGD)</i>
    * Scotland (Scot)
        * [Scotland Census](https://www.scotlandscensus.gov.uk/): <i>Local authority (CA2019)</i>​


# 2.0 Process
The flow diagram shows the stages of the area classification process:

<img width="533" height="456" alt="Methods-diagram" src="https://github.com/user-attachments/assets/37abc2e5-ea72-427a-984f-9c3a1fc74f78" />

[Clicking this link will open the image in a separate  window to allow you to zoom in if needed.](https://github.com/user-attachments/assets/37abc2e5-ea72-427a-984f-9c3a1fc74f78)


This repo contains a [QA script](https://github.com/ONSgeo/Area_Classification/blob/main/area_classification/utilities/qa_functions.py). This is currently not embedded in the pipeline but can be run on any data frame from any stage of the pipeline. The QA script checks for expected, zero and duplicate values, and produces descriptive statistics (e.g. range). 

### 2.1 Folder structure
[The folder and script structure can be found in the user guide folder.](https://github.com/ONSgeo/Area_Classification/blob/main/docs/user_guide/repo_structure.md)


# 3.0 Data
This section explains the data used in this pipeline. Later in this ReadMe you will find the [Data Download section](https://github.com/ONSgeo/Area_Classification/blob/main/README.md#data-download) within [Set-up](https://github.com/ONSgeo/Area_Classification/blob/main/README.md#set-up ) which provides links and instructions for downloading the data listed here. 

### 3.1.1 England and Wales
Data for England and Wales is collected from the bulk download available on the ONS census data platform, [NOMIS 2021 Census Bulk Data Download](https://www.nomisweb.co.uk/sources/census_2021_bulk). Table codes generally start with 'TS'.

**Exceptions:**
* Manual download needed for England and Wales disability data required to calculate Standardised Illness Ratio (SIR).
### 3.1.2 Northern Ireland
Data for Northern Ireland is collected from the bulk download available on the NISRA census data platform, [NISRA flexible table builder](https://build.nisra.gov.uk/en/). Table codes generally start with 'ni'.

**Exceptions:**
* Bangladeshi ethnic group category data is not available for Northern Ireland 2021. Read more in the [assumptions_caveats.md](https://github.com/ONSgeo/Area_Classification/blob/main/docs/analytical_quality_assurance/assumptions_caveats.md).
* Manual download needed for Northern Ireland Census 2021 Population Density data at the Local Government District level. <br>**Note:** Unlike the rest of the UK, raw population density data for NI is by hectare. Conversion present in code to transform to km2. 
* Manual download needed for Northern Ireland disability data required to calculate SIR.
  
### 3.1.3 Scotland
At this time the bulk files are only available for the output area (OA) geography, so currently data for [Scotland is manually downloaded from Scotland's Census Search Census Data](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). Table codes generally start with 'UV'. The manual download was completed 22 April 2025.

**Exceptions:**<br>
Additional manual downloads needed for:
* Census 2022 table 'population density'. Population density table was downloaded 15 April 2025.
* Census 2022 table 'migrant indicator'. Migrant indicator table was downloaded 22 April 2025.
* Census 2022 disability data required to calculate SIR.

<br>**Note:** it is not advised to aggregate from a lower level of geography (such as OA), if the target geography is not available on the Flexible Table Builder. Statistical Disclosure Controls - such as cell key perturbation - are implemented to protect the confidentiality of data within tables. This means that cells will not necessarily sum to sub-totals and totals.

## 3.2 Look ups
* [UK_selected_codes_lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) has been created to run the 2021 England and Wales (EW), 2021 Northern Ireland (NI) and 2022 Scotland (Scot) Area Classification for Local Authority Districts (LAD). This will need updating if choosing to run at another level of geography or different combination of censuses.
* A Local Authority Districts Names and Codes in the UK Lookup is required to convert between area names and area codes. This is available from the [ONS Geography Portal](https://geoportal.statistics.gov.uk/) .


# 4.0 Set Up 
Firstly, clone the repo locally. If you need support cloning the repo, take a look at [the GitHub cloning a repository instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or if you are working with Visual Studio code take a look at [clone and use a GitHub repository in Visual Studio Code instructions](https://learn.microsoft.com/en-us/azure/developer/javascript/how-to/with-visual-studio-code/clone-github-repository?tabs=activity-bar).

## 4.1 Requirements 
To start using this project, first make sure your system meets its
requirements.

It's suggested that you install this package and its requirements within
a virtual environment.

- Python 3.10 or higher installed
 
This may also work on earlier versions of python, but it has not been developed with versions 3.9 or lower in mind.

Contributors have additional `requirements` (e.g. the pytest package), please see our [contributing guidance][contributing] on how to install these.

### 4.1.1 Installing the package
Whilst in the root folder, in a terminal, you can install the package and its
Python dependencies using:

```shell
python -m pip install -U pip setuptools
pip install -e .
```

### 4.1.2 Install for contributors
To install the contributing requirements, use:
```shell
python -m pip install -U pip setuptools
pip install -e .[dev]
pre-commit install
```

This installs an editable version of the package. This means that when you update the
package code you do not have to reinstall it for the changes to take effect.
This saves a lot of time when you test your code.

Remember to update the setup and requirement files in line with any changes to your
package.

## 4.2 Folders setup
When your repository is cloned, find the repository within your file explorer. 
Locate the **'data'** folder. Within this, a folder called **'lookups'** should already exist. In `data/lookups` the [Selected_codes_Lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) will already exist. 

Going back to the **'data'** folder, create a new folder called **'inputs'**. This is where the downloaded census tables will be stored.
Within the `data/inputs` folder create four new folders:
* **'ew_downloads'**
* **'ni_downloads'**
* **'scot_downloads'**

## 4.3 Data download
As per **3.0 Data**, there are some manual data downloads required. Therefore, before running any of the scripts, ensure the data listed below has been downloaded and saved in the correct folders listed.

For more information on the data that is automatically downloaded when running the pipeline via API's, see the [downloading data page in the specifications folder.](https://github.com/ONSgeo/Area_Classification/blob/main/docs/specifications/1.0_Downloading_Data.md)

### 4.3.1 'lookups' folder:
* Local Authority Districts Names and Codes in the UK Lookup from the [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/). We used [Local Authority Districts (December 2022) Names and Codes in the UK](https://geoportal.statistics.gov.uk/datasets/42af123c4663466496dafb4c8fcb0c82_0/explore). This is required to convert between area names and area codes.

### 4.3.2 'ew_downloads' folder:
* England and Wales disability data [disabilitycensus2021.xlsx from the ONS website](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/disability/datasets/disabilityinenglandandwales2021). The file name should be 'disabilitycensus2021.xlsx'.

### 4.3.3 'ni_downloads' folder:
* Northern Ireland disability data [MS-D02 Long-term health problem or disability by broad age bands [UPDATED]](https://www.nisra.gov.uk/system/files/statistics/census-2021-ms-d02.xlsx) from [Census 2021 main statistics health, disability and unpaid care tables](https://www.nisra.gov.uk/publications/census-2021-main-statistics-health-disability-and-unpaid-care-tables). The file should be named 'census-2021-ms-d02.xlsx'.
* Northern Ireland Census 2021 [MS-A14: Population density at Local Government District level for Northern Ireland](https://statistics.ukdataservice.ac.uk/dataset/northern-ireland-census-2021-ms-a14-population-density/resource/9a859cde-7da2-487a-86bd-dc5bfbaa4924) and ensure it is named 'census-2021-ms-a14-LGD.xlsx'.

### 4.3.4 'scot_downloads' folder:
* Scotland's Census 2022: Usual resident population density, Council Areas in [Table 4 in Scotland's Rounded population estimates](https://www.scotlandscensus.gov.uk/media/h5qokkij/scotland-s-census-2022-first-results-rounded-population-estimates-data.xlsx). The file should be renamed 'population_density.xlsx'.
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
* Scotland tables from the [Scotland Census table builder search](https://www.scotlandscensus.gov.uk/search-the-census#/search-by). For each table in the list below:
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
  
### 4.3.5 Set Up - folders and download data diagram
Your file structure should look like the following. Text in red are the folders and csv file which already exist in the repo (`data/lookups/UK_selected_codes_lookup.csv`). The text in black are the folders you need to manually create, and files which you need to download and save as described in **4.3. Data Download**.

<img width="646" height="1080" alt="area classification file structure for README (8)" src="https://github.com/user-attachments/assets/196538ad-8df7-4011-a696-8d7744501260" />

[Clicking this link will open the image in a separate  window to allow you to zoom in if needed.](https://github.com/user-attachments/assets/196538ad-8df7-4011-a696-8d7744501260)

### 4.3.6 Running the pipeline
The entry point for the pipeline is stored within the package and called `main_pipeline.py`.
To run the pipeline, run the following code in the terminal (either in the root directory of the
project, or by specifying the path to `main_pipeline.py` from elsewhere).

```shell
python src/area_classification/main_pipeline.py
```

Alternatively, most Python IDEs allow you to run the code directly using a `run` button.

# 5.0 Output
This pipeline produces a range of outputs which can be found in the **'output'** folder. These include radial plots, clustergrams and lookup tables allocating each area code for the Local Authority Districts in England, Wales, Scotland and Northern Ireland to clusters at the supergroup, group and subgroup levels. More information on the outputs can be found in the [naming_conventions.md](https://github.com/ONSgeo/Area_Classification/blob/main/docs/user_guide/naming_conventions.md#outputs)

# 6.0 Limitations
These are high level limitations of the overall pipeline. For more specific limitations for each pipeline component see [Specifications folder](https://github.com/ONSgeo/Area_Classification/tree/main/docs/specifications):
1. **Combining data from two separate years** - Censuses for EW, Scot and NI are usually conducted on the same date. However due to the [impact of COVID-19, Scotland moved their census to 2022](https://www.scotlandscensus.gov.uk/news-and-events/news-release-scotland-s-census-to-be-moved-to-march-2022/). This collection date difference may have affected responses to variables across the countries of the UK. It may have had a particular effect on responses to questions on employment, reflecting the very different nature of work between the two years, and potentially making these variables less comparable than previously. Additionally, it is possible if individuals migrated internally between 2021 and 2022, they may have been included or excluded in more than one census. 
2. **Choice of variables** - The variables used in this pipeline have been chosen in line with the earlier work and the [2021 Output Area Classification](https://data.geods.ac.uk/dataset/output-area-classification-2021). Use of other variables (including non-Census data), will likely lead to different solutions.
3. **Level of geography** - This pipeline produces clusters at Local Authority District (LAD) levels of geography (LTLA, LGD and CA19). As such, it does not necessarily capture the heterogeneity inherent within such large populations. 
More detailed limitations can be found in the [Specifications folder](https://github.com/ONSgeo/Area_Classification/tree/main/docs/specifications).

# 7.0 Future scope
This pipeline has the potential to be developed and adapted to work for different levels of geography. This would not be possible in its current form due to inconsistencies in the raw data tables from different countries' censuses; there has been a requirement to hard code some of the pre-processing stages to ensure consistency between datasets when feeding into the clustering algorithm.

# 8.0 Licence
Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation. The documentation is ©Crown copyright and available under the terms of the Open Government 3.0 licence.

# 9.0 Acknowledgements
Thanks to Jakub Wyszomierski (jakubwyszomierski), Owen Goodwin (ogoodwin505) and Alex Singleton (alexsingleton) at the Geographic Data Service for their early code which formed the starting point for this repo.
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

# 10.0 Contributing
If you want to help us build and improve `area_classification`, please take a look at our [contributing guidance][contributing].

# 11.0 Contacts
[ONS Geography inbox](mailto:ons.geography@ons.gov.uk)


