from area_classification.downloading_data.ew_lad_bulk_download import ew_download
from area_classification.downloading_data.ni_lgd_downloading_data import ni_download
# from area_classification.pre_processing. ADD PREPROCESSING OF SCOT
from area_classification.pre_processing.pre_processing import pre_processing  
from area_classification.analysis.clustering import clustering_wrapper  
from area_classification.utilities.load_config import load_config


def main_pipeline():
    """
    Main pipeline to process area classification data.
    """
    config = load_config()

    # Step 1: Download england and wales data
    ew_download()

    # Step 2: Download Northen Ireland data
    ni_download()

    # Step 3: Processing of Scotland data
    # scot_process()

    # Step 4: pre-processing
    pre_processing(ew_df , ni_df, scot_df, config)

    # Step 5: Clustering
    # This assumes the data is saved locally and then loads during clustering. 
    # Will need to refactor to allow this to take df input.
    clustering_output = clustering_wrapper(
        input_dataframe_or_filepath= config["input_data__filepath"],
        num_clusters=config["number_of_clusters"],
        n_init=config["number_of_times_k_means_initialised"],
        output_directory=config["output_directory"],
        plot_directory=config["plot_directory"],
        random_seed=config["random_seed"],)

    # Step 6: Create outputs

if __name__ == "__main__":
    main_pipeline()