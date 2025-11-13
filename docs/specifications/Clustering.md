# Clustering

## 1.0 Introduction
This specification covers the clustering component in the area classification pipeline, this is step 7 in the `main_pipeline.py`. 

This component applies the K-means clustering technique to group together local authorities with similar characteristics in an iterative process. This approach is consistent with the clustering technique used for the previous 2001 and 2011 Area Classification for Local Authorities.

## 2.0 Terminology
| Term |	Definition |	
| ---- |  ---------- |
| K-means | An algorithm which clusters data by trying to separate samples (local authorities) in n groups of equal variances, minimising a criterion known as the inertia or within-cluster sum-of-squares. This algorithm requires the number of clusters (that is, supergroups, groups and subgroups) to be specified and is an iterative process. |
| Clustering | Clustering is a technique for finding similarity groups in data, called clusters. For this classification, the clustering technique attempts to group Local Authority Districts together by similarity alone.    |
| Supergroup | The supergroup (highest level of the hierarchy) this local authority has been clustered into.     |
| Group | The group (middle level of the hierarchy) this local authority has been clustered into.  |
| Subgroup | The subgroup (lowest level of the hierarchy) this local authority has been clustered into.  |
	
## 3.0 Assumptions and requirements
This analysis assumes that the 50 census variables used in this clustering provide a broad enough picture of a range of demographic factors of these local authority districts so that the areas are grouped with most similar areas of the UK.

The k-means algorithm requires the number of clusters initially for supergroups to be specified and is an iterative process, and then the number of groups within these supergroups to be specified. We therefore assume we have made an informed judgement when making the final decision cluster numbers based on qualitative and quantitative assessments, and subjective judgement.

In order to run the analysis effectively all variables selected are required to have a value for all areas of the UK so there is a full dataset and no nulls. Therefore, if there is inconsistency in outputs from census' between devolved governments, then these variables are not able to be included in the clustering.

## 4.0 Methods inputs and outputs
### Method inputs
The input data for the cluster component comes from the pre-clustering phase. The input data must include the first column as 'LAD_code' this will be the local authority district code in line with the official GSS codes. The LAD codes for are LTLAs for England and Wales, LGD for Northern Ireland and CA for Scotland. This column will be followed by multiple columns (could be up to 60 columns) of the variables used. 

Each column will be named 'v' followed by a number for example 'v01’, 'v02'. The explanations of what these 'v' codes stand for can be identified in the [UK_selected_codes_lookup.csv](https://github.com/ONSgeo/Area_Classification/blob/main/data/lookups/UK_selected_codes_lookup.csv). The 'v' codes may not be continuous if certain variables have been dropped in pre-processing, for example "v20", # Bangladeshi is dropped in the pre-processing as this variable not available for NI at this level of geography. 

The values for each 'v' code are standardize values, ensuring all variables contribute equally in the clustering. They are also normalized to a fixed range ensuring all values are comparable. This is performed in the earlier pre-clustering phases by performing:
- inverse hyperbolic sine 
- min-max scaling 
 
Example table: 
| LAD_code |	v01 |	v02 |	
| -------- |   ---------- |     ---------- |
| string |  int |   int  |

### Method outputs
The clustering produces three data frames. One for each level of clustering (supergroup, group and subgroup). Each table contains two columns, the LAD code and the cluster assignment. The cluster assignment column will vary in name depending on the level of clustering. For example:
- supergroup = "clustering"
- group = "subclustering"
- subgroup = "subsubclustering"

At this stage the subgroup allocation is written in the format number, letter, letter for example 1aa, this is corrected in the post-processing stage to turn it into the standard format of number, letter, number e.g. 1a1.
Example table for a subgroup output using mock data:
| LAD_code |	subsubcluster|		
| -------- |   ---------- |     
| E06000001 |  1ab  |      
| W06000001 |  2bc  |      


## 5.0 Method
When provided with a data table, the K-means clustering separates the samples of Local Authority Districts in n groups of equal variance, where n is defined in the config as `number_of_clusters`, these split datasets representing the highest level of the hierarchy – supergroups. Each of the resulting datasets then has the K-means algorithm run on them separately based on the `subclustering_mapping` in the config to create the second level of the hierarchy – groups. This was then repeated on the group level to produce the lowest level of subgroups based on the subsubclustering_mapping. 

During testing different number of cluster permutations were trailed using K-means, based on a preferred range for the supergroup level, reflecting a similar hierarchical structure to the 2011 Area Classification for Local Authorities. A final decision made on cluster numbers used to create the 2021/22 Area Classification for Local Authority Districts was based on qualitative and quantitative assessments, and subjective judgement.

### Strengths
We have utilised the config to allow different parameters to be set for the clustering. For example you are able to specify the number of clusters in the K-means clustering at the supergroup level (`number_of_clusters`) and the number of times to run the Kmeans (`number_of_times_k_means_initialised`). When running multiple levels of the clustering to produce groups and subgroup, you are also able to map the number of clusters you want to break each cluster in specifically. For example:
- `subclustering_mapping` - lists the clusters which result in the first level of clustering (supergroups), and the number of subclusters (groups) to create from these
- `subsubclustering_mapping` - lists the clusters which result in the second level of clustering (groups) e.g. '1a', '1b' etc, and the number of subsubclusters (subgroups) to create from these	

### Limitations
We use a `random_seed` which is the initial value to start the clustering algorithm. We have specficied this to be 42 for this pipeline, could be seen as both a limitation and strength as it does enable reproducibility, but it does mean the k-means clustering is not truly random every time. We opted to do this so that when run at different times by different people, the same clusters would be achieved.
