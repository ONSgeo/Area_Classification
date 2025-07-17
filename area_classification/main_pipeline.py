import os
from area_classification.utilities.load_config import load_config
from area_classification.utilities.loading_data import load_format_data
from area_classification.downloading_data.ew_lad_bulk_download import ew_lad_bulk_download
from area_classification.downloading_data.ni_lgd_downloading_data import ni_lgd_download_data
from area_classification.downloading_data.scot_tables_reformatting import scot_reformatting_wrapper
from area_classification.pre_processing.pre_processing import pre_processing
from area_classification.analysis.clustering import clustering_wrapper      
from area_classification.post_processing.post_processing import post_process_cluster_table      


def main_pipeline():
    """
    Main pipeline to process area classification data.

    This function runs the entire pipeline for creation of the Local Authority District area classification 
    clusters, including downloading, formatting, pre-processing, and clustering.

    Steps
    -----
    1. Download and process England and Wales data.
    2. Download and process Northern Ireland data.
    3. Process manually downloaded Scotland data.
    4. Perform pre-processing on combined data.
    5. Perform clustering on the pre-processed data.

    Parameters
    ----------
    None

    Notes
    -----
    - The configuration file `area_classification/config.yaml` is loaded to provide all necessary settings.
    - The clustering step assumes pre-processed data is saved locally and loads it during clustering. 

    """
    config = load_config('area_classification/config.yaml')

    # Step 1: Download england and wales data
    ew_lad_bulk_download(config)
    ew_input_csv_path = os.path.join(config["input_data_directory"], "./ew_downloads/")
    ew_df = load_format_data(ew_input_csv_path, config["ew_file_pattern"],config["ew_join_column_name"], config)


    # Step 2: Download Northen Ireland data
    ni_lgd_download_data(config)
    # Loading and getting into format to be used to process and combine
    ni_input_csv_path = os.path.join(config["input_data_directory"], "./ni_downloads/")
    ni_df = load_format_data(ni_input_csv_path, config["ni_file_pattern"],config["ni_join_column_name"], config)
  
    # Step 3: Processing of Scotland data which was manually downloaded
    scot_df = scot_reformatting_wrapper(config["scot_input_folder"], config["LAD_lookup_file_path"], config)

    # Step 4: pre-processing
    pre_processing(ew_df , ni_df, scot_df, config)
                           
    # Step 5: Clustering
    # This assumes the data is saved locally and then loads during clustering. 
    # Will need to refactor to allow this to take df input.
    clustering_output = clustering_wrapper(
        input_dataframe_or_filepath= config["preprocessed_input_table"],
        num_clusters=config["number_of_clusters"],
        n_init=config["number_of_times_k_means_initialised"],
        output_directory=config["output_directory"],
        plot_directory=config["plot_directory"],
        random_seed=config["random_seed"])
    
    # Step 6: Post processing
    #post_processing = post_process_cluster_table(output_folder, file_name, keep_column, split_column)


if __name__ == "__main__":
    main_pipeline()
