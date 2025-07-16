# Pre-processing

## 1.0 Meta


## 2.0 Terminology
ONS
NOMIS
NISRA
LAD code
LTLA (England and Wales),
LGD (Northern Ireland) 
CA (Scotland).

## 3.0 Introduction
The clustering algorithm requires input data to be in a consistent format, consquently since the data comes form multiple different data sources (NOMIS, NISRA and Scotland's Census websites) some pre-processing is required to achieve this consistency. 

### Strengths

### Limitations

## 4.0 Assumptions and requirements

## 5.0 Methods inputs and outputs
### 5.1 Method inputs
Input data must contain the following fields:
Area identifier - string - this could be the area name or area code for a LAD
Variable value - Numeric - 

### 5.2 Method outputs
The output includes the following fields:
LAD code - string - this is the area code for the LTLA (England and Wales), LGD (Northern Ireland) and CA (Scotland).
60 variable feilds - int - these are the values for each variable in that LAD.

## 6.0 Method