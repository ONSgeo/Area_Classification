# Post-processing

## 1.0 Terminology

| Term |	Definition |	
| -------- |   ---------- |   
| Radial plot | circular chart that displays multivariate data. The axes radiating from the centre point represent different variables |     
| Supergroup |	The supergroup (highest level of the hierarchy) this local authority has been clustered into. |
| Group	| The group (middle level of the hierarchy) this local authority has been clustered into. |
| Subgroup |The subgroup (lowest level of the hierarchy) this local authority has been clustered into. |
| Parent cluster | The cluster level above the current level. For example, the parent cluster of group 1a is supergroup 1. 
| Standardisation | Transforms each variable to have a mean of 0 and a standard deviation of 1, making them dimensionless and directly comparable. Without this, variables with larger magnitudes or ranges would dominate calculations of the mean. It makes it easier to identify which variables are most characteristic of each cluster. |

## 2.0 Introduction
This post-processing component restructures the clustering output for easier interpretation. Radial plots and small written summaries are generated to highlight the variables most characteristic of each cluster. 

## 3.0 Assumptions and requirements



## 4.0 Methods
### 4.1 Method inputs
The output dataframe from the clustering stage is required:

| Column name |	Data type |	Definition |	
| -------- |   ---------- |     ---------- |
| XXX |    |      |
| XXX |    |      |

The table that is outputted in the pre-processing stage, with the 60 selected variables for EW/NI/Scot in one combined dataframe. In 'main_pipeline.py' this is defined as the 'chosen_clustering_variables' dataframe:

| Column name |	Data type |	Definition |	
| -------- |   ---------- |     ---------- |
| XXX |    |      |
| XXX |    |      |

### 4.2 Method outputs


| Geography name |	Geography code |	supergroup |	group |	subgroup |	
| -------- |   ---------- |     ---------- |   ---------- |   ---------- |
| XXX |  XXX  |  1   | 1a | 1a1 |
| XXX |  XXX  |  2  | 2a | 2a1 |


Standardised means tables: 

Two groups of radial plots: One are based on the comparison of a cluster to the UK mean. The other group compare variables within a cluster to the mean of parent cluster. For example, a radial plot for cluster 5a (group level) represents a comparison to the mean of all clusters that make up supergroup 5. 



### 4.3 Process

1. standardised means of the table that has all selected variables, before its prepared for clustering. So all variables contribute equally to mean calculations further on in this component
2. restrucutre the clustering output table for easier interpretation
3. calculate standardised means for each variable at each cluster/hierarchy level. this forms the basis for comparing means to the whole UK mean.
4. calculate means for each cluster, standardised to the parent cluster. For example, the mean for variable 1 in cluster 5a (group level) has been standardised to all of the values in variable 1 that occur supergroup 5.
5. radial plots are created from the outputs of steps 3 and 4.
6. cluster summaries

### 4.4 Strengths

### 4.5 Limitations



