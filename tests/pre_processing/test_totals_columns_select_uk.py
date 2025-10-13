import unittest
import pandas as pd
import os
from area_classification.pre_processing.totals_columns_select_uk import select_totals_columns 
from area_classification.utilities.load_config import load_config
class TestTotalColumnsSelectUk(unittest.TestCase):
    def setUp(self):
        # Create folder for the data if it doesn't exist
        if not os.path.exists("tests/data/total_columns_select_uk_test_data"):
            os.makedirs("tests/data/total_columns_select_uk_test_data")

        csv_file_path = 'tests/data/total_columns_select_uk_test_data/test_select.csv'  # Specify the file name or path
        # Sample aggregate output test data
        self.aggregate_input_s = pd.DataFrame({
                'area_code': ['S12000001', 'S12000002', 'S12000003', 'S12000004'],
                'UV101b0001': [50, 100, 110, 145],
                'UV101b0002': [20, 10, 77, 56],
                'UV101b0003': [30, 90, 33, 143],
                'hours_part': [30, 25, 33, 10],
                'hours_full': [30, 25, 32, 40],
                'UV6040001': [60, 50, 65, 50]
        })
        # Save the aggregate output test data
        csv_file_path = 'tests/data/total_columns_select_uk_test_data/preprocessing_aggregated_all_variables_CA19.csv'
        self.aggregate_input_s.to_csv(csv_file_path, index=False) 

         # Sample select variables test data
        self.select_input_s = pd.DataFrame({
            'area_code': ['S12000001', 'S12000002', 'S12000003', 'S12000004'],
            'v01': [30, 90, 33, 143],
            'v45': [30, 25, 33, 10],
            'v46': [30, 25, 32, 40]
         })
        # Save the select variables test data
        csv_file_path = 'tests/data/total_columns_select_uk_test_data/test_scot_select.csv'
        self.select_input_s.to_csv(csv_file_path, index=False) 
        
        # Sample aggregate output test data
        self.aggregate_input_e = pd.DataFrame({
                'area_code': ['E12000001', 'E12000002', 'E12000003', 'E12000004'],
                'ts0010001': [50, 100, 110, 145],
                'ts0010002': [20, 10, 77, 56],
                'ts0010003': [30, 90, 33, 143],
                'ts0590002': [30, 25, 33, 10],
                'ts0590005': [30, 25, 32, 40],
                'ts0590001': [60, 50, 65, 50]
        })
        # Save the aggregate output test data
        csv_file_path = 'tests/data/total_columns_select_uk_test_data/preprocessing_aggregated_all_variables_LTLA.csv'
        self.aggregate_input_e.to_csv(csv_file_path, index=False) 

        # Sample select variables test data
        self.select_input_e = pd.DataFrame({
            'area_code': ['E12000001', 'E12000002', 'E12000003', 'E12000004'],
            'v01': [30, 90, 33, 143],
            'v45': [30, 25, 33, 10],
            'v46': [30, 25, 32, 40]
         })
        # Save the select variables test data
        csv_file_path = 'tests/data/total_columns_select_uk_test_data/test_ew_select.csv'  # Specify the file name or path
        self.select_input_e.to_csv(csv_file_path, index=False) 

        # Expected output DataFrame after conversion
        self.expected_df = pd.DataFrame({
                'area_code': ['E12000001', 'E12000002', 'E12000003', 'E12000004','S12000001', 'S12000002', 'S12000003', 'S12000004'],
                    'v01': [30, 90, 33, 143, 30, 90, 33, 143],
                    'v01_total': [50, 100, 110, 145, 50, 100, 110, 145],
                    'v45': [30, 25, 33, 10, 30, 25, 33, 10],
                    'v45_total': [60, 50, 65, 50, 60, 50, 65, 50],
                    'v46': [30, 25, 32, 40, 30, 25, 32, 40],
                    'v46_total': [60, 50, 65, 50, 60, 50, 65, 50]
         })
        
    def test_total_columns_select_uk(self):

        config = load_config('area_classification/config.yaml')
        result_df = select_totals_columns(config, 'tests/data/total_columns_select_uk_test_data' )
        print(result_df)
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()