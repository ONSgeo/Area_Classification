# Pre-processing

## 1.0 Introduction
The clustering algorithm requires input data to be in a consistent format, consquently since the data comes form multiple different data sources (NOMIS, NISRA and Scotland's Census websites) some pre-processing is required to achieve this consistency. 


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
| Standardisation |    |     
| Hyperbolic sine |    |  

## 3.0 Assumptions and requirements
hyperbolic sine?

## 4.0 Methods inputs and outputs
### 4.1 Method inputs

Scotland pre-processing:
For all Scotland downloaded csvs reformatting is required to remove excess metadata at the top.
Additionally variable names need to be turned into variables codes which are in the metadata table so that columns align.
UV101b needs ‘all people’ ‘lives in a communal establishment’ – Council Areas need to be moved into a separate column.
UV103 needs additional formatting, then in the aggregation script, the ages need to be grouped to align with the other census’.



Input data must contain the following fields:
| Column name |	Data type |	Definition |	
| -------- |   ---------- |     ---------- |
| Area identifier |   string |     this could be the area name or area code for a LAD |
| Variable value |   Numeric |      |

### 4.2 Method outputs
The output includes the following fields:
| Column name |	Data type |	Definition |	
| -------- |   ---------- |     ---------- |
| LAD code |   string |     this is the area code for the LTLA (England and Wales), LGD (Northern Ireland) and CA (Scotland). |
| 60 variable fields |   int |     these are the values for each variable in that LAD. |



## 5.0 Method
Stardisation and transformation methods - hyperbolic sine
### 5.1 Strengths

### 5.2 Limitations
