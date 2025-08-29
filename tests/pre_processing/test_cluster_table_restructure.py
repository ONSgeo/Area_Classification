import unittest
import pandas as pd
from area_classification.cluster_table_restructure import cluster_table_restructure
from area_classification.utilities.load_config import load_config

class TestClusterTableRestructure(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'subsubcluster': ['1ab', '2bc', '3cb', '6ab'],
        })

        # Expected output DataFrame after restructuring
        self.expected_df = pd.DataFrame({
            'LAD_name': ['Hartlepool', 'Isle of Anglesey', 'Antrim and Newtownabbey','Clackmannanshire'],
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'supergroup': ['1', '2', '3', '6'],
            'group': ['1a', '2b', '3c', '6a'],
            'subgroup': ['1a2', '2b3', '3c2', '6a2'] 
        })

    def test_restructure_table(self):
        config = load_config('area_classification/config.yaml')
        result_df = cluster_table_restructure(config, self.input_df)
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()