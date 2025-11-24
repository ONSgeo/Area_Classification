
import unittest
import pandas as pd
import os
from area_classification.post_processing.cluster_summaries import calculate_cluster_variance
from area_classification.post_processing.cluster_summaries import cluster_population_percentages
from area_classification.post_processing.cluster_summaries import cluster_summary
from area_classification.post_processing.cluster_summaries import identify_cluster_drivers
from area_classification.utilities.load_config import load_config

#Tests for all functions in the cluster_summaries script:
# calculate_cluster_variance
# cluster_population_percentage
# cluster_summary


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
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001' , 'E06000002', 'E06000003', 'E06000004', 'E06000005', 'E06000047' ],
            'supergroup': [1, 3, 2, 2, 3, 1],
            'group': ['1b', '3a', '2a', '2b', '3a', '1b'],
            'subgroup': ['1b1', '3a2', '2a1', '2b1', '3a1', '1b2'],
            'population': [102.0, 94.0, 136.0, 105.0, 82.0, 130.0],
            'AREALHECT': [356, 315, 931, 192, 109, 405]
        })

        # Expected output DataFrame after aggregation
        self.expected_df = pd.DataFrame({
            'supergroup': [1, 2, 3],
            'supergroup_population': [232.0, 241.0, 176.0],
            'supergroup_percentage': [35.75, 37.13, 27.12],
        })

    def test_cluster_population_percentages(self):
        result_df =  cluster_population_percentages (self.input_df, cluster_column = 'supergroup')
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
            'supergroup': ['1', '2', '3'],
            'v01': [0.02, 0, 0.10125],
            'v02': [0.045,  0.005, 0.01125],
            'cluster_average_variance': [0.0325, 0.0025, 0.05625 ]
        }).set_index('supergroup')  # Set 'supergroup' as the index

        # Mock population sums DataFrame
        self.pop_sums_df = pd.DataFrame({
            'supergroup': [1, 2, 3],
            'supergroup_population': [232.0, 241.0, 176.0],
            'supergroup_percentage': [35.75, 37.13, 27.12],
        })

        # Mock population densities DataFrame
        self.pop_densities = pd.DataFrame({
            'cluster_allocation': [1, 2, 3],
            'population': [232.0, 241.0, 176.0],
            'AREALHECT': [761, 1123, 424],
            'population_density': [0.30486, 0.2146, 0.411509],
        })

        # Expected output strings
        self.expected_output = [
            'Cluster 1 contains 2 local authorities which is 33.33% of UK local authorities, this included 35.75% of the UK population (values are taken for 2021 for EW and NI, but 2022 for Scot, due to times of the census). This cluster has a population density of 0.30 people per hectare.\nThe average variance for cluster 1 is 0.03. Example areas: County Durham, Hartlepool', 
            'Cluster 2 contains 2 local authorities which is 33.33% of UK local authorities, this included 37.13% of the UK population (values are taken for 2021 for EW and NI, but 2022 for Scot, due to times of the census). This cluster has a population density of 0.21 people per hectare.\nThe average variance for cluster 2 is 0.00. Example areas: Stockton-on-Tees, Redcar and Cleveland', 
            'Cluster 3 contains 2 local authorities which is 33.33% of UK local authorities, this included 27.12% of the UK population (values are taken for 2021 for EW and NI, but 2022 for Scot, due to times of the census). This cluster has a population density of 0.41 people per hectare.\nThe average variance for cluster 3 is 0.06. Example areas: Darlington, Middlesbrough'
        ]

    def test_cluster_summary(self):
        self.maxDiff = None  # Show full diff for debugging
        result_df = cluster_summary(self.input_df, self.uk_std_cluster_means_df, self.variance_df, self.pop_sums_df, self.pop_densities, cluster_column='supergroup')
        # Compare the lists
        self.assertListEqual(result_df, self.expected_output)


if __name__ == "__main__":
    unittest.main()


    