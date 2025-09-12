
import unittest
import pandas as pd
import os
from area_classification.post_processing.cluster_summaries import calculate_cluster_variance
from area_classification.post_processing.cluster_summaries import cluster_population_percentages
from area_classification.post_processing.cluster_summaries import cluster_summary
from area_classification.post_processing.cluster_summaries import identify_cluster_drivers
from area_classification.utilities.load_config import load_config

#Tests for all functions in the culuster_summaries script:
# calculate_cluster_variance
# cluster_population_percentage
# cluster_summary
# identify_cluster_drivers

class TestCalculateClusterVariance(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['S12000001', 'S12000002', 'S12000003','S12000004', 'S12000005', 'S12000006' ],
            'supergroup': [1, 3, 2, 2, 3, 1],
            'group': ['1b', '3a', '2a', '2b', '3a', '1b'],
            'subgroup': ['1b1', '3a2', '2a1', '2b1', '3a1', '1b2'],
            'v01': [0.50, 0.30, 0.20, 0.20, 0.75, 0.7],
            'v02': [0.60, 0.90, 0.10, 0.20, 0.75, 0.9]
        })

        # Expected output DataFrame after aggregation
        self.expected_df = pd.DataFrame({
            'supergroup': [1, 2, 3],
            'v01': [0.02, 0, 0.10125],
            'v02': [0.045,  0.005, 0.01125],
            'cluster_average_variance': [0.0325, 0.0025, 0.05625 ]
        }).set_index('supergroup')  # Set 'supergroup' as the index

    def test_calculate_cluster_variance(self):

        result_df =  calculate_cluster_variance(self.input_df, cluster_column = 'supergroup')
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)


class TestClusterPopulationPercentages(unittest.TestCase):
    def setUp(self):
        
        # Create folder for the data if it doesn't exist
        if not os.path.exists("tests/data"):
            os.makedirs("tests/data")

        csv_file_path = 'tests/data/test_cluster_population_percentages.csv'  # Specify the file name or path
        # Create a mock lad population dataset
        self.test_mock_populations_input = pd.DataFrame({
            'col1': ['Pop estimates', 'date', 'analysis', 'sex:', 'age', '', 'local authority','', 'Hartlepool', 'Middlesbrough', 'Redcar and Cleveland','Stockton-on-Tees', 'Darlington', 'County Durham', 'Column Total' ],
            'col2': ['', '', '', 'total', 'total', '', 'mnemonic','', 'E06000001' , 'E06000002', 'E06000003', 'E06000004', 'E06000005', 'E06000047', 'Column Total' ],
            'col3': ['', '', '', '', '', '', '2021', '', '52' , '86', '21', '73', '50', '50', '332'],
            'col4': ['', '', '', '',  '','', '2022', '','58' , '80', '40', '73', '55', '45', '351' ]
        })
        # Save the mock lad population dataset
        self.test_mock_populations_input.to_csv(csv_file_path, index=False) 
       
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001' , 'E06000002', 'E06000003', 'E06000004', 'E06000005', 'E06000047' ],
            'supergroup': [1, 3, 2, 2, 3, 1],
            'group': ['1b', '3a', '2a', '2b', '3a', '1b'],
            'subgroup': ['1b1', '3a2', '2a1', '2b1', '3a1', '1b2'],
            'v01': [0.50, 0.30, 0.20, 0.20, 0.75, 0.7],
            'v02': [0.60, 0.90, 0.10, 0.20, 0.75, 0.9]
        })

        # Expected output DataFrame after aggregation
        self.expected_df = pd.DataFrame({
            'supergroup': [1, 2, 3],
            '2021_supergroup_population': [102.0, 94.0, 136.0],
            '2022_supergroup_population': [103.0, 113.0, 135.0],
            '2021_percentage': [30.72, 28.31, 40.96],
            '2022_percentage': [29.34, 32.19, 38.46]
        })

    def test_cluster_population_percentages(self):
        population_estimates_filepath = ('tests/data/test_cluster_population_percentages.csv')
        result_df =  cluster_population_percentages (self.input_df, population_estimates_filepath, 'supergroup')
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)


class TestClusterSummary(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001' , 'E06000002', 'E06000003', 'E06000004', 'E06000005', 'E06000047' ],
            'LAD_name': ['Hartlepool', 'Middlesbrough', 'Redcar and Cleveland','Stockton-on-Tees', 'Darlington', 'County Durham'],
            'supergroup': [1, 3, 2, 2, 3, 1],
            'group': ['1b', '3a', '2a', '2b', '3a', '1b'],
            'subgroup': ['1b1', '3a2', '2a1', '2b1', '3a1', '1b2'],
            'v01': [0.50, 0.30, 0.20, 0.20, 0.75, 0.7],
            'v02': [0.60, 0.90, 0.10, 0.20, 0.75, 0.9],
            'v12': [0.12, 0.34, 0.06, 0.11, 0.06, 0.20]
        })

        # Mock uk_std_cluster_means DataFrame
        self.uk_std_cluster_means_df = pd.DataFrame({
            'cluster': [1, 2, 3],
            'hierarchy_level': ['supergroup', 'supergroup', 'supergroup'],
            'v01': [0.35, 0.2, 0.525],
            'v02': [0.75,  0.15, 0.825],
            'v12': [0.16, 0.08, 0.20],
        })

        # Mock variance DataFrame
        self.variance_df = pd.DataFrame({
            'supergroup': [1, 2, 3],
            'v01': [0.02, 0, 0.10125],
            'v02': [0.045,  0.005, 0.01125],
            'cluster_average_variance': [0.0325, 0.0025, 0.05625 ]
        }).set_index('supergroup')  # Set 'supergroup' as the index

        # Mock population sums DataFrame
        self.pop_sums_df = pd.DataFrame({
            'supergroup': [1, 2, 3],
            '2021_supergroup_population': [102.0, 94.0, 136.0],
            '2022_supergroup_population': [103.0, 113.0, 135.0],
            '2021_percentage': [30.72, 28.31, 40.96],
            '2022_percentage': [29.34, 32.19, 38.46]
        })

        # Expected output strings
        self.expected_output = [
            'Cluster 1 contains 2 local authorities which is 33.33% of UK local authorities, in 2021 this was 30.72% of the UK population and in 2022 it was 29.34%. It has a population density of 0.16.\nThe average variance for cluster 1 is 0.03. Example areas: County Durham, Hartlepool', 
            'Cluster 2 contains 2 local authorities which is 33.33% of UK local authorities, in 2021 this was 28.31% of the UK population and in 2022 it was 32.19%. It has a population density of 0.08.\nThe average variance for cluster 2 is 0.00. Example areas: Stockton-on-Tees, Redcar and Cleveland', 
            'Cluster 3 contains 2 local authorities which is 33.33% of UK local authorities, in 2021 this was 40.96% of the UK population and in 2022 it was 38.46%. It has a population density of 0.20.\nThe average variance for cluster 3 is 0.06. Example areas: Darlington, Middlesbrough'
        ]

    def test_cluster_summary(self):
        self.maxDiff = None  # Show full diff for debugging
        result_df = cluster_summary(self.input_df, self.uk_std_cluster_means_df, self.variance_df, self.pop_sums_df, cluster_column='supergroup')

        # Compare the lists
        self.assertListEqual(result_df, self.expected_output)


# # Step 4: 
# identify_cluster_drivers(uk_std_cluster_means, lookup_file, cluster_info, variance_df, cluster_column, top_n=3)

if __name__ == "__main__":
    unittest.main()


    