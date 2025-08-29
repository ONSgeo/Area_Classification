import pandas as pd
import os
import numpy as np
import csv
from functools import reduce
import unittest
from unittest.mock import patch, MagicMock, mock_open


from area_classification.downloading_data.scot_tables_reformatting import (
    reformat_uv101b, reformat_uv103, reformat_uv104, reformat_uv210,
    reformat_migrant_indicator, extract_pop_density_table, reformat_pop_density,
    extract_metadata_from_files, replace_ca19_names_with_codes, remove_rows
)
from area_classification.utilities.load_config import load_config

# reformat_uv101b(scot_input_folder, LAD_lookup_file_path, config)

# reformat_uv103(scot_input_folder, LAD_lookup_file_path, config)

# reformat_uv104(scot_input_folder, LAD_lookup_file_path, config)

# reformat_uv210(scot_input_folder, LAD_lookup_file_path, config)

# reformat_migrant_indicator(scot_input_folder, LAD_lookup_file_path, config)

# extract_pop_density_table(scot_input_folder)

# reformat_pop_density(scot_input_folder, config)

# extract_metadata_from_files(scot_input_folder)

# replace_ca19_names_with_codes(scot_input_folder, LAD_lookup_file_path, config)

#Remove Rows Test
class TestRemoveRows(unittest.TestCase):
    @patch("os.listdir")
    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    @patch("os.makedirs")
    def test_remove_rows(self, mock_makedirs, mock_to_csv, mock_read_csv, mock_listdir):
        # Mock the directory listing
        mock_listdir.return_value = ["reformat_test.csv", "uv101b.csv", "other_file.csv"]

        # Mock the input DataFrame
        mock_df = pd.DataFrame({
            0: ["Council Area 2019", "Value1", "Value2", "Value3", "Extra1", "Extra2", "Extra3"],
            1: ["Header1", "Data1", "Data2", "Data3", "Extra1", "Extra2", "Extra3"],
            2: ["Header2", "Data4", "Data5", "Data6", "Extra1", "Extra2", "Extra3"]
        })
        mock_read_csv.return_value = mock_df

        # Define the config and folderpath
        config = load_config('area_classification/config.yaml')
        folderpath = "/tests/data/scot_tables_refomatting"

        # Call the function
        remove_rows(config, folderpath)

        # Verify os.listdir was called with the correct folderpath
        mock_listdir.assert_called_once_with(folderpath)

        # Verify pandas.read_csv was called with the correct file path
        mock_read_csv.assert_called_once_with("/tests/data/scot_tables_refomatting/removerows.csv", on_bad_lines='warn', header=None)

        # Verify the transformations on the DataFrame
        expected_df = pd.DataFrame({
            0: ["", "Value1", "Value2", "Value3"],
            1: [np.nan, "Header1", "Data1", "Data2"],
            2: [np.nan, "Header2", "Data4", "Data5"]
        })
        pd.testing.assert_frame_equal(mock_read_csv.return_value.iloc[:-3, :], expected_df)

        # Verify pandas.DataFrame.to_csv was called with the correct file path
        mock_to_csv.assert_called_once_with("/tests/data/scot_tables_refomatting/removerows.csv", index=False, header=False)

        # Verify os.makedirs was called to ensure the save location exists
        mock_makedirs.assert_called_once_with(os.path.dirname("/tests/data/scot_tables_refomatting/removerows.csv"), exist_ok=True)

if __name__ == "__main__":
    unittest.main()

# replace_variable_names_with_codes(config)

# concat_reformatted_tables(config)
             

