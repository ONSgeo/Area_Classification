import yaml
import gptables as gpt
from area_classification.utilities.load_config import load_config
from create_cluster_tables import (cluster_table_wrapper)
from area_classification.Statistical_Release.output_table_formatting import (
    build_dataset_sheets, build_notes, build_cover, build_contents, build_filepath)

config = load_config('area_classification/config.yaml')
cluster_table_wrapper(config, config['restructured_subclustering_output'], 'D:/Repos/Area_Classification/data/output_data/test_name_lookup.csv')
####
#CAN I USE CONFIG TWICE IN TWO DIFFERENT WAYS !?
####

# load config file
with open("area_classification/statistical_release/gptables_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# build GPTables data sheets 
sheets = build_dataset_sheets(config.get('datasets', []))

# get notes variables 
notes = build_notes(config.get('notes'))

# build cover sheet
cover = build_cover(config.get('cover'))

# get contentsheet_label variable
contents = build_contents(config.get('contents'))

# build filepath
filepath = build_filepath(config.get('save_info'))

# write workbook
gpt.write_workbook( 
     filename=filepath,
    cover=cover,
    contentsheet_label=contents, 
    notesheet_label=notes[0], 
    notes_table=notes[1],
    sheets=sheets
)

print("File successfully saved!")