
# Downloading data
## 1.0 Terminology

| Term |	Definition |	
| -------- |   ---------- |  
| API |	Application Programming Interface, an interface implemented by a software program to enable interaction with other software.|	
| nomis | an ONS-provided service that publishes statistics. These include data from current and previous censuses. |	
| NISRA | Northern Ireland Statistics and Research Agency. Where census data is downloaded from |
| metadata | Information about something, for example further descriptive text for a code, often shown either using annotations or in a dedicated Metadata XML file, or csv file in this case |
| LGD | Local Government District. A level of Geography used for census statistics. The NI equivalent of Local Authority Distrcits (EW) and Council Areas (Scot) | 
| LAD | Local Authority District. A level of Geography used for census statistics. The EW equivalent of Local Government DistrictS (NI) and Council Areas (Scot) |
| CA19 | Council Areas 2019. A level of Geography used for census statistics. The Scot equivalent of Local Authority Distrcits (EW) and ocal Government Districts (NI) |

## 2.0 Introduction
This specificaiton covers data download for the area classification pipeline. Census data is required from England, Wales, Scotland and Northern Ireland. The objective of this component is to import and make consistent data from different sources (NOMIS, NIRSA and Scot Census). For England and Wales, a bulk download is used to collect the required CSVs, for Northern Ireland an API is used to retrive the data and for Scotland the data is manually downloaded. As well as downloading data from the three sources, data formatting steps merge all the tables into one table for each individual country. Meta data extraction is involved in this component. Steps 1 to 3 in the main pipeline covers this process.

## 3.0 Assumptions and requirements


## 4.0 Methods inputs and outputs
### 4.1 Method inputs

Data that is retrieved from via NISRA API follows the following format:


Data that is retrieved from via the bulk download for EW is in the following format:


The format for most Scot tables that are manually downloaded:




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
API: are extracted based on the variable name, variable code and variable unit 'household' or 'people'.
bulk download:
manual download: census table builders

### 5.1 Strengths

### 5.2 Limitations


