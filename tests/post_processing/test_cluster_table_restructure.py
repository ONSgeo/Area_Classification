#THIS DOES NOT CURRENTLY RUN AS THE FUNCTION ONLY USES A CONFIG!

import unittest
import pandas as pd
#from post_processing.cluster_table_restructure.py import cluster_table_restructure
from area_classification.post_processing.cluster_table_restructure import cluster_table_restructure

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
            'subgroup': ['1ab', '2bc', '3cb', '6ab'] 
        })

    def test_restructure_table(self):
        # Call the function to test
        result_df = cluster_table_restructure(self.input_df)

        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()