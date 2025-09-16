# Unit test not running yet!

import pandas as pd  # For data manipulation (similar to tidyverse and vroom)
from zipfile import ZipFile
from glob import glob
from shutil import rmtree
# import pyarrow as pa  # Equivalent to arrow (commented out as in the R script)
from area_classification.utilities.load_config import load_config
import tempfile
import unittest
import pandas as pd
from area_classification.downloading_data.ew_lad_bulk_download import format_and_export_metadata_table
from area_classification.downloading_data.ew_lad_bulk_download import get_census_table_urls
from area_classification.downloading_data.ew_lad_bulk_download import download_and_unzip_data
from area_classification.utilities.load_config import load_config

# get_census_table_urls(config: dict)
# download_and_unzip_data(zip_urls: list, config: dict)

class TestFormatAndExportMetadataTable(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'old_names': ['Number of cars or vans: Total: All households', 'Number of cars or vans: No cars or vans in household', 'Number of cars or vans: 1 car or van in household','Number of cars or vans: 2 cars or vans in household', 'Number of cars or vans: 3 or more cars or vans in household', 'Residence type: Total; measures: Value', 'Residence type: Lives in a household; measures: Value', 'Residence type: Lives in a communal establishment; measures: Value' ],
            'new_names': ['ts0450001', 'ts0450002', 'ts0450003', 'ts0450004', 'ts0450005', 'ts0010001', 'ts0010002', 'ts0010003'],
            'Table_ID': ['ts045', 'ts045', 'ts045', 'ts045', 'ts045', 'ts001', 'ts001', 'ts001'],
        })
        
        # Expected output DataFrame after restructuring
        self.expected_df = pd.DataFrame({
            'old_names': ['Number of cars or vans: Total: All households', 'Number of cars or vans: No cars or vans in household', 'Number of cars or vans: 1 car or van in household','Number of cars or vans: 2 cars or vans in household', 'Number of cars or vans: 3 or more cars or vans in household', 'Residence type: Total; measures: Value', 'Residence type: Lives in a household; measures: Value', 'Residence type: Lives in a communal establishment; measures: Value' ],
            'new_names': ['ts0450001', 'ts0450002', 'ts0450003', 'ts0450004', 'ts0450005', 'ts0010001', 'ts0010002', 'ts0010003'],
            'Table_ID': ['ts045', 'ts045', 'ts045', 'ts045', 'ts045', 'ts001', 'ts001', 'ts001'],
            'Table_Name': ['Number of cars or vans', 'Number of cars or vans', 'Number of cars or vans', 'Number of cars or vans', 'Number of cars or vans', 'Residence type', 'Residence type', 'Residence type'],
            # 'Type': ['nan', 'nan', 'nan', 'nan', 'nan', 'Value', 'Value', 'Value'],         
            # 'Variable_Name': ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']
            # 'Type': ['', '', '', '', '', 'Value', 'Value', 'Value'],         
            # 'Variable_Name': ['', '', '', '', '', '', '', '']  
            'Type': ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'Value', 'Value', 'Value'],         
            'Variable_Name': ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']   
        })
        

    def test_format_and_export_metadata_table(self):
        config = load_config('area_classification/config.yaml')
        result_df = format_and_export_metadata_table(self.input_df, config)
        result_df = result_df.fillna('placeholder')
        # Assert that the result matches the expected output
        print(result_df)
        print(self.expected_df)
        self.expected_df = self.expected_df.fillna('placeholder')
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()
