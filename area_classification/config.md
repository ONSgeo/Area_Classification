# Config
| Paramater   | Description            | Data Type   | Acceptance values      |
|-------------|------------------------|-------------|------------------------|
|working_directory | The working directory location            | 	string   | Any filepath.     |
|LAD_lookup_file_path |The path to where the Local Authority District (LAD) lookup is saved |scot_input_folder |The manually downloaded Scot tables (and those for EW and NI) should be saved in inputs
|drop_columns | The          | 	string   | True or False     |
|variables_to_drop | The          | 	list   | True or False     |
|pre_clustering_data | The filepath for the table before filtering   | 	string   | Any filepath.    |
|pre_clustering_data_filtered | The filepath after it has been filtered / variables from the v60 which are not being used are dropped    | 	string   | Any filepath.     |
|pre_clustering_data_std_mean | The filepath after it has been standardised and transformed, before it goes into clustering | 	string   | Any filepath.    |
|restructured_subclustering_output | The filepath of the table which is restrucutred so Supergroup, group and subgroup are all in separate columns      | 	string   | Any filepath.    |
|number_of_clusters | The number of clusters in the Kmeans clustering            | int   | Any int |
|number_of_times_k_means_initialised | The number of times the Kmeans is ran    | int   | Any int |
|random_seed| The initial value to start the clustering algorithm | int   | Any int    |
|subclustering_mapping| The  | list of int   | Any int    |
|subsubclustering_mapping| The  | int   | Any int    |
|select_variables_lookup | The path to where the lookup for the 60 selected variables is saved            | 	string   | Any filepath.     |
|input_directory | The path where inputs required for the clustering are saved             | 	string   | Any filepath.     |
|qa_directory |  The path where outputs should be saved to for quality assurance (QA) checks            | 	string   | Any filepath.     |
|output_directory | The path where outputs should be saved to | 	string   | Any filepath.     |
|clustergram_directory | The path where outputted clustergrams should be saved to      | 	string   | Any filepath.     |
|radial_plot_directory | The path where outputted radial plots should be saved to      | 	string   | Any filepath.     |
|scot_input_folder| The file path for where the Scotland input data is saved | string   | Any filepath. |
|ni_pop_density_filepath | The path to where the population density file for Northern Ireland is stored    | 	string   | Any filepath.  |
|ew_file_pattern| The file pattern for England and Wales files to be selected           | string   | Acceptance values      |
|ew_join_column_name | The name of column in England and Wales tables containing area codes which will be used for joining  | string   | Any valid column name.      |
|ew_excluded_form_code| The name of column which is not included in the percentage conversion during pre-processing as population density is already a ratio  | string   | Any valid column name. |
|ni_file_pattern | The file pattern for England and Wales files to be selected           | string   | Acceptance values      |
|ni_join_column_name| The name of column in Northern Irish tables containing area codes which will be used for joining            | string   | Any valid column name. 
|ni_excluded_form_code| The name of column which is not inculded in the percentage conversion during pre-processing as population density is already a ratio  | string   | Any valid column name. 
|scot_join_column_name|The name of column in Scottish tables containing area codes which will be used for joining | string   | Any valid column name. 
|scot_excluded_form_code| The name of column which is not inculded in the percentage conversion during pre-processing as population density is already a ratio  | string   | Any valid column name. 
|england_wales_disability_file| The file name for the England and Wales disability data file | string   | Any valid column name. |
|ni_disability_file| The file name for the Northern Ireland disability data file | string   | Any valid column name. |
|scotland_disability_file| The file name for the Scotland disability data file | string   | Any valid column name. |
|england_wales_disability_input|The filepath for where the raw disability data is stored for England and Wales is stored | string   | Any filepath. |
|ni_disability_input|The filepath for where the raw disability data is stored for Northern Ireland is stored | string  | Any filepath. |
|scotland_disability_input| The filepath for where the raw disability data is stored for Scotland is stored | string  | Any filepath. |
|keep_column| The names of columns to keep in the table restructure | string  | Any valid column name. |
|split_column| The names of columns to split into separate character in the table restructure | string  | Any valid column name. |
|england_and_wales_table_codes_to_remove | Tables which do not have OA data for England and Wales | list[]   | Any valid table codes. |
## Guidance for use
As an end user, you will only need to change some of the config (named config.yaml) - you may just need to update the filepaths in the top section of the config.

# Aggregation_setup
The aggregation_setup.yaml file contains the variable codes which are merged together to produce the select vairables required.

## Usage 

## Updating
