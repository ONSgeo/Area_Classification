import os
import pandas as pd

from area_classification.utilities.load_config import load_config
from area_classification.utilities.loading_data import load_format_data
from area_classification.downloading_data.ew_lad_bulk_download import ew_lad_bulk_download
from area_classification.downloading_data.ni_lgd_downloading_data import ni_lgd_download_data
from area_classification.downloading_data.scot_tables_reformatting import scot_reformatting_wrapper
from area_classification.pre_processing.pre_processing import pre_processing
from area_classification.pre_processing.drop_variables import check_drop_columns_true
from area_classification.clustering.clustering import clustering_wrapper      
from area_classification.post_processing.post_processing import post_processing
from area_classification.pre_processing.prepare_clustering_data import prepare_clustering_data  
from area_classification.data_visualisation.horizontal_bar_chart import create_horizontal_bar_chart_wrapper   

def main_pipeline():
    """
    Main pipeline to process area classification data.

    This function runs the entire pipeline for creation of the Local Authority District area classification 
    clusters, including downloading, formatting, pre-processing, and clustering.

    Steps
    -----
    1. Download and process England and Wales data tables.
    2. Download and process Northern Ireland data tables.
    3. Process the manually downloaded Scotland data tables.
    4. Perform pre-processing on the combined data for all countries.
    5. Establish the variables which will be used for clustering (some may be dropped).
    6. standardise the pre-processed data for clustering.
    7. Perform clustering on the pre-processed data, using variables chosen.
    8. Reformat the cluster tables, calculate the means of the clustered data and generate radial plots.
    9. Generate data visualisations from the outputs.

    Parameters
    ----------
    None

    Notes
    -----
    - The configuration file `area_classification/config.yaml` is loaded to provide all necessary settings.
    - The clustering step assumes pre-processed data is saved locally and loads it during clustering. 

    """
    config = load_config('area_classification/config.yaml')

    # Step 1: Download england and wales data and reformat to be processed and combined
    #ew_lad_bulk_download(config)
    ew_input_csv_path = os.path.join(config["input_directory"], "./ew_downloads/")
    ew_df = load_format_data(ew_input_csv_path, config["ew_file_pattern"],config["ew_join_column_name"], config)

    # Step 2: Download Northen Ireland data and reformat to be processed and combined
    #ni_lgd_download_data(config)
    ni_input_csv_path = os.path.join(config["input_directory"], "./ni_downloads/")
    ni_df = load_format_data(ni_input_csv_path, config["ni_file_pattern"],config["ni_join_column_name"], config)
  
    # Step 3: Processing of Scotland data which was manually downloaded
    scot_df = scot_reformatting_wrapper(config["scot_input_folder"], config["LAD_lookup_file_path"], config)

    # Step 4: Pre-processing
    preprocessed_df = pre_processing(ew_df , ni_df, scot_df, config)

    # Step 5: Choose to drop/not drop
    # If not running the full 60 variables, update the 'drop_columns' in the config to 
    # True and change the 'variables_to_drop' in the config
    chosen_clustering_variables = check_drop_columns_true(config, preprocessed_df)

    # Step 6: Standardise pre_clustering data (used in the clustering)
    pre_clustering_data_std_mean = prepare_clustering_data(chosen_clustering_variables)
    # Save the standardised pre clusting data to a new file 
    pre_clustering_data_std_mean.to_csv(config["pre_clustering_data_std_mean"], index=False)
         
    # Step 7: Clustering
    clustering_output = clustering_wrapper(
        config,
        input_dataframe=pre_clustering_data_std_mean,
        number_of_clusters=config["number_of_clusters"],
        n_init=config["number_of_times_k_means_initialised"],
        output_directory=config["output_directory"],
        clustergram_directory=config["clustergram_directory"],
        random_seed=config["random_seed"]
    )
    
    # Add a break
    input("Press Enter to continue to post processing...")
 
    # Step 8: Post processing
    combined_group_means, combined_subgroup_means, uk_std_cluster_means = post_processing(config, clustering_output, chosen_clustering_variables)

    # Step 9: Data visualisation
    create_horizontal_bar_chart_wrapper(uk_std_cluster_means)

if __name__ == "__main__":
    main_pipeline()