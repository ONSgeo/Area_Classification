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
|CA| Council Areas, the Scottish equivalent to LAD (CA19 is the abbreviation for Council Areas defined in 2019)|
|ONS| The Office for National Statistics is responsible for running the census in England and Wales - https://www.ons.gov.uk/census |
|NOMIS| A service provided by the Office for National Statistics (ONS), which hosts statistics including data from censuses - https://www.nomisweb.co.uk/|
|NISRA| Northern Ireland Statistics and Research Agency (NISRA) is responsible for running the census in Northern Ireland - https://www.nisra.gov.uk/ |
|NRS| In Scotland, the National Records of Scotland is responsible for the census - https://www.scotlandscensus.gov.uk/|
|ew| England and Wales, referring to the census data for 2021|
|ni| Northern Ireland, referring to the census data for 2021|
|scot| Scotland, referring to the census data for 2022|
|v| 'v' when used alongside a number e.g. v1 or v2 represents a vairable within the dataset, variables can be interpreted using the [UK_selected_codes_lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv)|
|SAM| Standard Area Measurements are produced by ONS, they provide a definitive list of measurements for administrative, health, Census, electoral and other geographic areas in the UK|
|AREALHECT| Area to Mean High Water Excluding Area of Inland Water, this is the land area of a geography|


## Code
Variable_codes, Table_IDs and table_name for tables downloaded as well as the variable number (v1 to v60) can be looked up in the [UK_selected_codes_lookup.csv](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv)


## Outputs
This pipeline produces a range of outputs which can be found in the 'output' folder. These contain subfolders for:
- Cluster_assignments - spreadsheets contain the supergroups, groups and subgroups which local authorities have been allocated to (more below).
- Clustergrams - diagrams for each cluster used to visualise the cluster analysis and how the data is grouped.
- Radial plots - circular diagram which representing the variable distribution. The red line in the supergroup radial plots is for the UK average, in group and subgroup it is the supergroup average and group average respectively.
- std_mean - tables of standardised means for each variable. 

The most notable output is within the cluster_assignments folder -  restructured_subclustering_output:

| Output column   | Description            |
|--------|------------------------|
|LAD_name | Local authority district name, for England and Wales these are local authorities: district / unitary (LTLA), Local Government Districts for Northern Ireland and Council Areas for Scotland |
|LAD_code | Local authority district code are GSS (Government Statistical Service) 9 character codes which identify the local authority. |
|supergroup | The supergroup (highest level of the hierarchy) this local authority has been clustered into.|
|group | The group (middle level of the hierarchy) this local authority has been clustered into.|
|subgroup | The subgroup (lowest level of the hierarchy) this local authority has been clustered into.|
