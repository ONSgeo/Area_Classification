# Pre-processing

## 1.0 Introduction
This specification covers the pre-processing component in the area classification pipeline, this is step 4, step 5 and step 6 in the main_pipeline.py.

The clustering algorithm requires input data to be in a consistent format and since the data comes form multiple different data sources (NOMIS, NISRA and Scotland's Census websites) some pre-processing is required to achieve this consistency. 


## 2.0 Terminology
| Term |	Definition |	
| -------- |   ---------- |  
| ONS |	The Office for National Statistics is responsible for running the census in England and Wales - https://www.ons.gov.uk/census	|	
| NOMIS | 	A service provided by the Office for National Statistics (ONS), which hosts statistics including data from censuses - https://www.nomisweb.co.uk/ |	
| NISRA | Northern Ireland Statistics and Research Agency (NISRA) is responsible for running the census in Northern Ireland - https://www.nisra.gov.uk/ |
| NRS | National Records of Scotland (NRS) is responsible for the census in Scotland - https://www.scotlandscensus.gov.uk/|
| LAD code | Local authority district (LAD) codes are GSS (Government Statistical Service) 9 character codes which identify a LAD. LADs are a level of geography used for census statistics. They include Unitary Authorities (W), Council Areas (S), Local Government Districts (NI) and in England include London Borough, Metropolitan Districts, Non-metropolitan Districts, Unitary Authorities. |
| LTLA | 	Lower Tier Local Authority. A level of geography used for census statistics. The EW equivalent of Local Government Districts (NI) and Council Areas (Scot) | 
| LGD | Local Government District Lower Tier Local Authority. A level of geography used for census statistics. The NI equivalent of Lower Tier Local Authority (EW) and Council Areas (Scot) |
| CA | Council Areas (CA19 = 2019. A level of Geography used for census statistics. The Scot equivalent of Local Authority Distrcits (EW) and Local Districts (NI) |
| Standardisation | A process that transforms each variable to have a mean of 0 and a standard deviation of 1, making them dimensionless and directly comparable. Without this, variables with larger magnitudes or ranges would dominate clustering. |     
| Inverse hyperbolic sine (arcsinh) transformation | A mathematical function used to transform data to make data more "normal" or less skewed, a useful step for clustering. |  
| Min-max scaling | A technique that transforms data so that all values are mapped to a fixed range, useful for distance-based algorithms like k-means. |

## 3.0 Assumptions and requirements
The [selected codes lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) is required to only select certain variables. 


## 4.0 Methods 
### 4.1 Method inputs

From the downloading data component, the pre-processing component requires three dataframes; EW, NI and Scot tables containing all of the downloaded census variables. 
These dataframes must contain the following fields:
| Column name |	Data type |	Definition |	
| -------- |   ---------- |     ---------- |
| Area identifier |   string |     this could be the area name or area code for a LAD |
| Variable value |   Numeric | counts  |

### 4.2 Method outputs
The output includes the following fields:
| Column name |	Data type |	Definition |	
| -------- |   ---------- |     ---------- |
| LAD code |   string |     this is the area code for the LTLA (England and Wales), LGD (Northern Ireland) and CA (Scotland). |
| 60 variable fields |   int |     these are the values for each variable in that LAD. |




## 4.3 Process




Stardisation and transformation methods - hyperbolic sine

### 4.4 Strengths
arcsinh can handle zero and negative values, unlike the logarithm. 

### 4.5 Limitations
