from area_classification.downloading_data.ew_lad_bulk_download import ew_lad_bulk_download
from area_classification.downloading_data.ni_lgd_downloading_data import ni_download
# from area_classification.pre_processing. ADD PREPROCESSING OF SCOT
from area_classification.pre_processing.pre_processing import pre_processing    
from area_classification.utilities.load_config import load_config
# from area_classification.clustering.clustering import clustering


def main_pipeline():
    """
    Main pipeline to process area classification data.
    """
    config = load_config()

    # Step 1: Download england and wales data
    ew_df = ew_lad_bulk_download(config)

    # Step 2: Download Northen Ireland data
    ni_download()

    # Step 3: Processing of Scotland data
    # scot_process()

    # Step 4: pre-processing
    pre_processing(ew_df , ni_df, scot_df, config)

    # Step 5: Clustering

    # Step 6: Create outputs

if __name__ == "__main__":
    main_pipeline()