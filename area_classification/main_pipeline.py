
from area_classification.downloading_data.ew_lad_bulk_download import ew_lad_bulk_download
from area_classification.downloading_data.ni_lgd_downloading_data import ni_lgd_download_data
# from area_classification.pre_processing. ADD PREPROCESSING OF SCOT
from area_classification.pre_processing.pre_processing import pre_processing, convert_to_percentages  
from area_classification.analysis.clustering import clustering_wrapper  
from area_classification.utilities.load_config import load_config
from area_classification.pre_processing.pre_processing import pre_processing    
from area_classification.utilities.loading_data import load_format_data


def main_pipeline():
    """
    Main pipeline to process area classification data.
    """
    config = load_config()

    # Step 1: Download england and wales data
    ew_lad_bulk_download(config)
    ew_df =load_format_data(config["input_data_filepath"], config["england_wales_file_pattern"],config["england_wales_join_column_name"])


    # Step 2: Download Northen Ireland data
    ni_lgd_download_data()
    # Loading and getting into format to be used to process and combine
    ni_df = load_format_data(config["input_data_filepath"], config["ni_file_pattern"],config["ni_join_column_name"])

    # Step 3: Processing of Scotland data
    # scot_df = scot_process()

    # Step 4: pre-processing
    pre_processing(ew_df , ni_df, scot_df, config)

    #Step 5: convert to percentages for each ew, ni and scot (if necessary for scot as issues with extraction)
    # Assumption built in to function is that the total column names will be located as the first entry per table_id in metadata
    # Needs to be adapted to actual use case (with config etc) but will look something like as shown

    # populate as required for each of ew, ni, scot (needs adapting to use case)
    for info in info_from_config:
        convert_to_percentages(metadata_filepath = info["metadata_path"],
                               metadata_table_id = info["metadata_table_id"],
                               metadata_variable_id = info["metadata_variable_id"],
                               csv_folder_path = info["csv_folder_path"],
                               ignore_scaling_vars = info["ignore_scaling_cols"])
                           
    # Step 6: Clustering
    # This assumes the data is saved locally and then loads during clustering. 
    # Will need to refactor to allow this to take df input.
    clustering_output = clustering_wrapper(
        input_dataframe_or_filepath= config["input_data__filepath"],
        num_clusters=config["number_of_clusters"],
        n_init=config["number_of_times_k_means_initialised"],
        output_directory=config["output_directory"],
        plot_directory=config["plot_directory"],
        random_seed=config["random_seed"],)


if __name__ == "__main__":
    main_pipeline()
