# Definition of Output Variables

# Outputs
This pipeline produces a range of outputs which can be found in the 'output' folder. These contain subfolders for:
Cluster_assignments - spreadsheets contain the supergroups, groups and subgroups which local authorities have been allocated to (more below).
clustergrams - diagrams for each cluster used to visualise the cluster analysis and how the data is grouped.
radial plots - circular diagram which representing the variable distribution. The red line in the supergroup radial plots is for the UK average, in group and subgroup it is the supergroup average and group average respectively.
std_mean - tables of standardised means for each variable. 

## The most notable output is within the cluster_assignments folder -  restructured_subclustering_output
| Output column   | Description            |
|--------|------------------------|
|LAD_name | Local authority district name, for England and Wales these are local authorities: district / unitary (LTLA), Local Government Districts for Northern Ireland and Council Areas for Scotland |
|LAD_code | Local authority district code are GSS (Government Statistical Service) 9 character codes which identify the local authority. |
|supergroup | The supergroup (highest level of the hierarchy) this local authority has been clustered into.|
|group | The group (middle level of the hierarchy) this local authority has been clustered into.|
|subgroup | The subgroup (lowest level of the hierarchy) this local authority has been clustered into.|
