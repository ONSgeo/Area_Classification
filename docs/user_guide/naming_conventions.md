# Naming conventions

## Methods
| Name   | Description            |
|--------|------------------------|
|Standard illness ratio (SIR)	| The SIR is a metric calculated by comparing the disability count of an area by the expected illness. More detail on the methodology can be find in the [Standard Illness Ratio Specification](https://github.com/ONSgeo/Area_Classification/blob/main/docs/specifications/Standard_Illness_Ratio.md).|
|Clustering	| K-means cluster methodology ran at three levels of clustering to group into Supergroups, Groups and Subgroups. [More detail can be found in the speficiations doc for clustering](https://github.com/ONSgeo/Area_Classification/blob/main/docs/specifications/Clustering.md)|

### Abbreviation 
| Abbreviation    | Explaination            |
|--------|------------------------|
|LAD| Local Authority District, in Wales this is Unitary Authorities, in England these include London Borough, Metropolitan Districts, Non-metropolitan Districts, Unitary Authorities |
|LTLA| Lower Tier Local Authority |
|LGD| Local Government District, the Northern Irish equivalent to LAD |
|CA| Council Areas, the Scottish equivalent to LAD|
|ew| England and Wales, referring to the census data for 2021|
|ni| Northern Ireland, referring to the census data for 2021|
|scot| Scotland, referring to the census data for 2022|
|v| 'v' when used alongside a number e.g. v1 or v2 represents a vairable within the dataset. These 'v' codes can be interpreted using the [UK_selected_codes_lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) to look up the 'new_code' column|


## Code
Variable_codes, Table_IDs and table_name for tables downloaded as well as the variable number (v1 to v60) can be looked up in the [UK_selected_codes_lookup.csv](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv)
