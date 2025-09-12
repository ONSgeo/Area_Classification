## NOT YET RUNNING, NEED TO UPDATE POPULATION TABELFILE PATH
import unittest
import pandas as pd
import os
from area_classification.post_processing.cluster_summaries import cluster_summaries_wrapper

class TestClusterSummariesWrapperIntegration(unittest.TestCase):
    def setUp(self):
        # Create a mock configuration
        self.config = {
            'input_data_directory': './tests/data/'
        }

        # Create mock data for restructured_cluster_table_long
        self.restructured_cluster_table_long = pd.DataFrame({
            'cluster': [1, 1, 2, 2, 3, 3],
            'variable_1': [0.5, 0.6, -0.1, -0.2, 1.2, 1.3],
            'variable_2': [1.0, 1.1, -0.5, -0.6, 2.0, 2.1]
        })

        # Create mock uk_std_cluster_means DataFrame
        self.uk_std_cluster_means = pd.DataFrame({
            'cluster': [1, 2, 3],
            'hierarchy_level': ['supergroup', 'supergroup', 'supergroup'],
            'v01': [0.35, 0.2, 0.525],
            'v02': [0.75,  0.15, 0.825],
            'v12': [0.16, 0.08, 0.20],
        })

        # Create a mock lookup file
        self.lookup_file = './test_data/lookup_file.csv'
        os.makedirs('./test_data/', exist_ok=True)
        pd.DataFrame({
            'variable': ['variable_1', 'variable_2'],
            'description': ['Description 1', 'Description 2']
        }).to_csv(self.lookup_file, index=False)

        # Define the cluster column
        self.cluster_column = 'cluster'

    def test_cluster_summaries_wrapper(self):
        # Call the wrapper function
        cluster_summaries_wrapper(
            config=self.config,
            restructured_cluster_table_long=self.restructured_cluster_table_long,
            uk_std_cluster_means=self.uk_std_cluster_means,
            lookup_file=self.lookup_file,
            cluster_column=self.cluster_column
        )
    
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()