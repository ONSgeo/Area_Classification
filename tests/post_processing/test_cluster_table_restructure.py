import unittest
import pandas as pd
from area_classification.post_processing.cluster_table_restructure import cluster_table_restructure
from area_classification.utilities.load_config import load_config

class TestClusterTableRestructure(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'subsubcluster': ['1ab', '2bc', '3cb', '6ab'],
        })

        # Sample input DataFrame
        self.standardised_data = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [0.35, 0.2, 0.525, 0.45],
            'v02': [0.75,  0.15, 0.825, 0.60],
            'v12': [0.16, 0.08, 0.20, 0.12],
        })

        # Expected output DataFrame after restructuring
        self.expected_df = pd.DataFrame({
            'LAD_name': ['Hartlepool', 'Isle of Anglesey', 'Antrim and Newtownabbey','Clackmannanshire'],
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'supergroup': ['1', '2', '3', '6'],
            'group': ['1a', '2b', '3c', '6a'],
            'subgroup': ['1a2', '2b3', '3c2', '6a2'], 
            'v01': [0.35, 0.2, 0.525, 0.45],
            'v02': [0.75,  0.15, 0.825, 0.60],
            'v12': [0.16, 0.08, 0.20, 0.12],
        })

    def test_restructure_table(self):
        print(self.expected_df)
        config = load_config('area_classification/config.yaml')
        result_df = cluster_table_restructure(config, self.input_df, split_column = 'subsubcluster', keep_column = 'LAD_code' , standardised_data = self.standardised_data)
        print(result_df)
        #THIS DOESN'T WORK AS THERE ARE TWO TABLES OUTPUTTED BY CLUSTER TABLE FUNCTION SO NEED TO WORK OUT HOW TO TEST
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()