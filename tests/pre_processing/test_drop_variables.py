#TEST NOT WORKING YET - CHANGES TO FUNCTION ITSELF REQUIRED FIRST
import unittest
import pandas as pd
from area_classification.pre_processing.drop_variables import drop_variables_pre_clustering 

class TestDropVariables(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [50, 30, 20, 100],
            'v02': [100, 60, 40, 100],
            'v03': [25, 15, 10, 50],
            'v04': [50, 30, 20, 200]
        })
        print(self.input_df)
        self.variables_to_drop = pd.DataFrame({
            'v02',
            'v04'
        })

        # Expected output DataFrame after conversion
        self.expected_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [50, 30, 20, 100],  
            'v03': [25, 15, 10, 50]   
        })

    def test_drop_variables(self):
        from utilities.load_config import load_config
        # Call the function to test
        config = load_config('area_classification/config.yaml')
        variables_to_drop = config.get('variables_to_drop', [])   
        result_df = drop_variables_pre_clustering(config, self.input_df, variables_to_drop)
        print(result_df)
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()