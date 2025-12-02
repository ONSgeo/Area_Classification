
# Downloading data
## 1.0 Terminology

| Term |	Definition |	
| -------- |   ---------- |  
| API |	Application Programming Interface, an interface implemented by a software program to enable interaction with other software.|	
| nomis | an ONS-provided service that publishes statistics. These include data from current and previous censuses. |	
| NISRA | Northern Ireland Statistics and Research Agency. Where census data is downloaded from |
| metadata | Information about something, for example further descriptive text for a code, often shown either using annotations or in a dedicated Metadata XML file, or csv file in this case |
| LGD | Local Government District. A level of Geography used for census statistics. The NI equivalent of Local Authority Distrcits (EW) and Council Areas (Scot) | 
| LAD | Local Authority District. A level of Geography used for census statistics. The EW equivalent of Local Government Districts (NI) and Council Areas (Scot) |
| CA / CA19 | Council Areas 2019. A level of Geography used for census statistics. The Scot equivalent of Local Authority Distrcits (EW) and Local Government Districts (NI) |

## 2.0 Introduction
This specificaiton covers data download for the area classification pipeline. Census data is required from England, Wales, Scotland and Northern Ireland. The objective of this component is to import and make consistent data from different sources (NOMIS, NIRSA and Scot Census). For England and Wales, a bulk download is used to collect the required CSVs, for Northern Ireland an API is used to retrive the data and for Scotland the data is manually downloaded. As well as downloading data from the three sources, data formatting makes data structure consistent and merges all the tables into one table for each individual country. Meta data extraction is involved in this component. Steps 1 to 3 in the main pipeline covers this process.

## 3.0 Assumptions and requirements
### 3.1 Assumptions <br>
Data Format Consistency:<br>
The structure of the data and metadata (e.g., column names, table layout) on the NOMIS and NISRA website remains consistent and matches the parsing logic in the script.

File Naming Conventions:<br>
The script relies on specific naming conventions for downloaded files (e.g., *-ltla.csv for EW census downloads).

Manual downloads:<br>
The files requiring manual download listed in the main Readme have been downloaded before running the main pipeline.

Scotland tables structure:<br>
There are functions that reformat the Scot tables so that they are consistent with EW and NI tables. This assumes that the tables are structured the same as the time of download. For example, all contain excess metadata in the top and bottom rows and certain tables like UV103 - Age by single year are strucutred differently to the rest. 

### 3.2 Requirements <br>
Output Directory Structure:<br>
The script requires the output directory to follow a specific structure, for example:<br>
inputs/ew_downloads/ for downloaded CSV files.<br>

Disk Space:<br>
Sufficient disk space is required for downloading, extracting, and saving the data.

## 4.0 Method
### 4.1 Method inputs
Listed are the conditions for the data that is downloaded in the first instance, either via , bulk download or manual download. Data specifications are as followed:<br>
* EW and NI is from 2021, Scotland data 2022
* At LGD/LAD/CA level
* Contains LGD/LAD/CA area codes and area names
* Format is 'count', rather than 'percentage'
* Units are 'household' or 'people'
* Structured by area name/code as rows, with census responses as columns
* 'Total: All usual residents' column should be included

### 4.2 Method outputs
The downloading data component produces three dataframes - one for each Census (EW, NI and Scot). Each table follows a similar strucutre, where 'census response' refer to the response to a census question. For example, for the Census table 'TS001 - Number of usual residents in households and communal establishments':<br>
- CENSUS RESPONSE 1 = total number of residents who answered the question.
- CENSUS RESPONSE 2 = number of people living in a household.
- CENSUS RESPONSE 3 = number of people living in a communal establishment.<br />

The number of CENSUS RESPONSE columns varies by question, but CENSUS RESPONSE 1 is always the total respondents.

| LEVEL OF GEOGRAPHY | CENSUS RESPONSE 1 | CENSUS RESPONSE 2 | CENSUS RESPONSE 1 | CENSUS RESPONSE 2 | CENSUS RESPONSE 3 |
| -------- | ---------- | ---------- | ---------- | ---------- | ---------- | 
| GEOGRAPHY CODE 1 | COUNT 1 | COUNT 2 | COUNT 1 | COUNT 2 | COUNT 3 |
| GEOGRAPHY CODE 2 | COUNT 1 | COUNT 2 | COUNT 1 | COUNT 2 | COUNT 3 |

## 4.3 Process 

1. For England and Wales data, the Nomis bulk download page is scraped for relevant census table ZIP file URLs, excluding unwanted tables. Tables are downloaded and the metadata formatted and exported.
2. For NI, the data is fetched from URLs and downloaded table-by-table. Metadata is fetched and downloaded. The manually downloaded population density table is reformatted to only contain relevent columns and to convert from hectare to km2.
4. Assuming the Scotland data has been manually downloaded, the tables are reformatted to be consistent with the EW and NI tables. For example, tables are renamed based on their table ID and excess metadata within the tables is removed. Certain tables have unique formatting, which requires custom functions to format them to be consistent with the rest. 


For all Scotland downloaded tables, reformatting is required to remove excess metadata at the top.
Variable names need to be turned into variables codes which are in the metadata table so that columns align.
UV101b needs ‘all people’ ‘lives in a communal establishment’ – Council Areas need to be moved into a separate column.
UV103 needs additional formatting, then in the aggregation script, the ages need to be grouped to align with the other census’.

### 4.4 Strengths
The code fetches metadata and formats it into a structured table, which is useful for verification.<br>
The download data function for EW data dynamically fetches URLs from the Nomis website, ensuring the latest data is used.<br>

### 4.5 Limitations
Some URL's for fetching data and metadata and structure of the file names are hardcoded, making the code less flexible if the source changes.



