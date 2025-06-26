
import pandas as pd
import os
import numpy as np
import csv

from area_classification.pre_processing.scot_tables_reformatting import scot_reformatting_wrapper
from area_classification.utilities.load_config import load_config
config = load_config('area_classification/config.yaml')

scot_reformatting_wrapper(input_directory="D:/Repos/Area_Classification_data/Percentages/TEST",
    CA_lookup_file_path="D:/Repos/Area_Classification/area_classification/pre_processing/Local_Authority_Districts_(December_2022)_Names_and_Codes_UK.csv",
    config =config)
