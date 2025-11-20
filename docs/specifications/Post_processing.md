# Post-processing

## 1.0 Terminology

| Term |	Definition |	
| -------- |   ---------- |   
| Radial plot | A circular chart that displays multivariate data. The axes radiating from the centre point represent different variables. |     
| Supergroup |	The supergroup (highest level of the hierarchy) this local authority has been clustered into. |
| Group	| The group (middle level of the hierarchy) this local authority has been clustered into. |
| Subgroup |The subgroup (lowest level of the hierarchy) this local authority has been clustered into. |
| Parent cluster | The cluster level above the current level. For example, the parent cluster of group 1a is supergroup 1. 
| Standardisation | Transforms each variable to have a mean of 0 and a standard deviation of 1, making them dimensionless and directly comparable. Without this, variables with larger magnitudes or ranges would dominate calculations of the mean. It makes it easier to identify which variables are most characteristic of each cluster. |

## 2.0 Introduction
This post-processing component restructures the clustering output for easier interpretation. Radial plots and short written summaries are generated to highlight the variables most characteristic of each cluster. 

## 3.0 Assumptions and requirements

For standardisation, it is assumed that the variable data are roughly normally distributed, with no major outliers. 

To create the radial plots and label the variables correctly, the [selected codes lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv) is required. This lookup is also required for creating the summaries of each cluster. 

## 4.0 Methods
### 4.1 Method inputs

#### 4.1.1 Table containing all chosen variables 
The table that is outputted in the pre-processing stage, with the selected variables and the percentage values for EW/NI/Scot in one combined dataframe. This could be the full 60 variables as listed in the [lookup](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv), or less if it has been specified in the config file to drop specific variables. In 'main_pipeline.py' this is defined as the 'chosen_clustering_variables' dataframe:
Example:

|  LAD_code |	v01 |	v02 |	v03 |	
| -------- |   ---------- |     ---------- |  ---------- |
| XXX |  0.9  |  45.8   |  8.3 |
| XXX |  5.5  |   36.7   | 7.7 |

#### 4.1.2 Clustering output:
The outputs from the clustering component are three data frames; one for each level of clustering (supergroup, group and subgroup).
- supergroup = "clustering"
- group = "subclustering"
- subgroup = "subsubclustering"

Example table for a subgroup output:
| LAD_code |	subsubcluster|		
| -------- |   ---------- |     
| XXX |  1ab  |      
| XXX |  2bc  |     


### 4.2 Method outputs

#### 4.2.1 Clustering output dataframe that has been restrucutred: 

| LAD_name |	LAD_code |	supergroup |	group |	subgroup |	
| -------- |   ---------- |     ---------- |   ---------- |   ---------- |
| XXX |  XXX  |  1   | 1a | 1a1 |
| XXX |  XXX  |  2  | 2a | 2a1 |


#### 4.2.2 Standardised means tables: 
UK table containing means of each variable within each cluster, standardised to the UK mean. 
Example using dummy data:

| cluster | hierarchy_level | v01 | v02 | v03 |
| ------ | ------ | ------ | ------ | ------ | 
| 0 | supergroup | -0.01 | -0.6 | 0.08 |
| 0a | group | -0.5 | -0.6 | 0.2 |
| 0a1 | subgroup | -0.1 | 0.8 | 0.08 |

Two tables, one containing the means of each variable in each group-level cluster, standardised to the mean of the parent cluster (supergroup). The other contains the means of each variable in each subgroup-level cluster, standardised to the mean of the parent cluster (group).
Example group output using dummy data. The subgroup output has the same structure:
| group | v01 | v02 | v03 |
| ---- | ---- | ---- | ---- |
| 0a | -0.3 | -0.01 | -0.2 |
| 0b | 0.4 | -0.5 | -0.9 |


#### 4.2.3 Two groups of radial plots:
One are based on the comparison of a cluster to the UK mean. The other group compare variables within a cluster to the mean of parent cluster. For example, a radial plot for cluster 5a (group level) represents a comparison to the mean of all clusters that make up supergroup 5. 


### 4.3 Process

1. Take the table containing all chosen variables that is outputted at the pre-processing stage. For each value and each variable, the standardised mean is calculated. This ensures that all variables contribute equally to further calculations of the mean.
2. The output table from the clustering component is restructured for easier interpretation. The column containing cluster codes are seperated out into seperate columns for supergroup, group, and subgroup. The final character in the subgroup column is then converted to a number (a=1, b=2, c=3, etc.).
3. Using the tables from steps 1 and 2, means are calculated for each variable at each cluster/hierarchy level, standardised to the UK mean.
4. Using the tables from steps 1 and 2, it sorts by supergroup/group/subgroup and calculates means of each variable in each cluster, standardised to the parent mean. 
5. Radial plots are created from the outputs of steps 3 and 4.
6. Short summaries are printed out in the terminal when running the post-processing component. These provide an overview of the characteristics of each cluster. 

### 4.4 Strengths
Comparability:
Calculating standardised means put all variables on the same scale, allowing direct comparison across variables regardless of their original units or ranges.

Interpretability: 
Producing radial plots highlight which variables drive cluster differences.

### 4.5 Limitations
Standardisation assumes that variables are normally distributed and standardised means can be affected by outliers in the data. It is therefore not always appropriate depending on the dataset. 




