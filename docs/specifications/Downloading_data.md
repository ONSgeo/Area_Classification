
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
This specificaiton covers data download for the area classification pipeline. Census data is required from England, Wales, Scotland and Northern Ireland. The objective of this component is to import and make consistent data from different sources (NOMIS, NIRSA and Scot Census). For England and Wales, a bulk download is used to collect the required CSVs, for Northern Ireland an API is used to retrive the data and for Scotland the data is manually downloaded. As well as downloading data from the three sources, data formatting steps merge all the tables into one table for each individual country. Meta data extraction is involved in this component. Steps 1 to 3 in the main pipeline covers this process.

## 3.0 Assumptions and requirements
### 3.1 Assumptions <br>
Data Format Consistency:<br>
The structure of the data and metadata (e.g., column names, table layout) on the NOMIS and NISRA website remains consistent and matches the parsing logic in the script.

File Naming Conventions:<br>
The script relies on specific naming conventions for downloaded files (e.g., *-ltla.csv for EW census downloads).

Manual downloads:<br>
The files requiring manual download listed in the main Readme have been downloaded before running the main pipeline.

### 3.2 Requirements <br>
Output Directory Structure:<br>
The script requires the output directory to follow a specific structure, for example:<br>
inputs/ew_downloads/ for downloaded CSV files.<br>

Disk Space:<br>
Sufficient disk space is required for downloading, extracting, and saving the data.

## 4.0 Methods inputs and outputs
### 4.1 Method inputs
Listed are the conditions for the data that is downloaded in the first instance, either via API, bulk download or manual download. Data specifications are as followed:<br>
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

## 5.0 Method
### 5.1 Strengths
The code fetches metadata and formats it into a structured table, which is useful for verification.<br>
The download data function for EW data dynamically fetches URLs from the Nomis website, ensuring the latest data is used.<br>

### 5.2 Limitations
Some URL's for fetching data and metadata and structure of the file names are hardcoded, making the code less flexible if the source changes.



