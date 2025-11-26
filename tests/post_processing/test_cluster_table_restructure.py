import unittest
import pandas as pd
import os
from area_classification.post_processing.cluster_table_restructure import cluster_table_restructure

config = {
        "LAD_lookup_file_path": "./tests/data/LAD_lookup.csv",
        "output_directory": "./tests/data/"
        }

import unittest
from unittest.mock import patch
import pandas as pd
import os

class TestClusterTableRestructure(unittest.TestCase):
    @patch("os.makedirs")
    @patch("pandas.DataFrame.to_csv")
    def setUp(self, mock_to_csv, mock_makedirs):
        # No actual directories or files will be created
        if not os.path.exists(config["output_directory"]+"cluster_assignments/"):
            os.makedirs(config["output_directory"]+ "cluster_assignments/")

        lookup_df = pd.DataFrame({
            'LAD22NM': ['Hartlepool', 'Isle of Anglesey', 'Antrim and Newtownabbey','Clackmannanshire'],
            'LAD22CD': ['E06000001', 'W06000001', 'N09000001','S12000005'],
        })
        lookup_df.to_csv(config["LAD_lookup_file_path"], index=True, header=True)

        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'subsubcluster': ['1ab', '2bc', '3cb', '6ab'],
        })

        self.standardised_data = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [0.35, 0.2, 0.525, 0.45],
            'v02': [0.75,  0.15, 0.825, 0.60],
            'v12': [0.16, 0.08, 0.20, 0.12],
        })

        self.expected_df = pd.DataFrame({
            'LAD_name': ['Hartlepool', 'Isle of Anglesey', 'Antrim and Newtownabbey','Clackmannanshire'],
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'supergroup': ['1', '2', '3', '6'],
            'group': ['1a', '2b', '3c', '6a'],
            'subgroup': ['1a2', '2b3', '3c2', '6a2'], 
        })

        self.expected_df_long = pd.DataFrame({
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
        result_df, result_df_long = cluster_table_restructure(
            config, self.input_df, split_column='subsubcluster',
            keep_column='LAD_code', standardised_data=self.standardised_data
        )
        pd.testing.assert_frame_equal(result_df, self.expected_df)
        pd.testing.assert_frame_equal(result_df_long, self.expected_df_long)

if __name__ == '__main__':
    unittest.main()