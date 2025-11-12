
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
This specificaiton covers data download for the area classification pipeline. Census data is required from England, Wales, Scotland and Northern Ireland, the objective of this component is to import and make consistent data from different sources (NOMIS, NIRSA and Scot Census). For England and Wales, a bulk download is used to collect the required CSVs, for Northern Ireland an API is used to retrive the data and for Scotland the data is manually downloaded. As well as downloading data from the three sources, there is some data formatting which takes place, this merges all the tables into one table for each individual country. Meta data extraction is involved in this component. Steps 1 to 3 in the main pipeline covers this process.

## 3.0 Assumptions and requirements


## 4.0 Methods inputs and outputs
### 4.1 Method inputs
Input data must contain the following fields:
| Column name |	Data type |	Definition |	
| -------- |   ---------- |     ---------- |
| XXX |    |      |
| XXX |    |      |

### 4.2 Method outputs
The downloading data component produces three dataframes. One for each Census (EW, NI and Scot) The tables for each have the following structure:

| LEVEL OF GEOGRAPHY | CENSUS VARIABLE 1 | CENSUS VARIABLE 2 | CENSUS VARIABLE 3 |
| -------- |   ---------- |   ---------- |   ---------- | 
| GEOGRAPHY CODE 1 | COUNT 1 | COUNT 2 | COUNT 3 |
| GEOGRAPHY CODE 2 | COUNT 1 | COUNT 2 | COUNT 3 |

## 5.0 Method
### 5.1 Strengths

### 5.2 Limitations


