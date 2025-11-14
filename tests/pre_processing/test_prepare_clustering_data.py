import unittest
import pandas as pd
from area_classification.pre_processing.prepare_clustering_data import standardise_data
from area_classification.pre_processing.prepare_clustering_data import apply_arcsinh_transformation
from area_classification.pre_processing.prepare_clustering_data import apply_min_max_scaling

class TestPrepareClusteringData(unittest.TestCase):
    def test_standardise_dataframe(self):
        # Define input DataFrame
        input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': [52.0, 25.0, 50.0, 10.0],  # Percentages of v01 / v01_total
            'v02': [30.0, 50.0, 60.0, 25.0]   # Percentages of v02 / v02_total
        })

        # Define expected output DataFrame
        expected_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': [1.009456, -0.526055, 0.895714, -1.379116],  
            'v02': [-0.786334, 0.611593, 1.310556, -1.135815]  
        })

        # Run the function and assert the result
        std_result_df = standardise_data(input_df)
        pd.testing.assert_frame_equal(std_result_df, expected_df)

    def test_apply_arcsinh_transformation(self):
        # Define input DataFrame
        input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': [1.009456, -0.526055, 0.895714, -1.379116],  
            'v02': [-0.786334, 0.611593, 1.310556, -1.135815] 
        })

        # Define expected output DataFrame after arcsinh transformation
        expected_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': [0.888044207, -0.504393876, 0.80567778, -1.125783223],
            'v02': [-0.7219613, 0.57874036, 1.084870788, -0.974225475]
        })

        # Run the function and assert the result
        arcsinh_result_df = apply_arcsinh_transformation(input_df)
        pd.testing.assert_frame_equal(arcsinh_result_df, expected_df)

    def test_apply_min_max_scaling(self):
        # Define input DataFrame
        input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': [0.888044207, -0.504393876, 0.80567778, -1.125783223],
            'v02': [-0.7219613, 0.57874036, 1.084870788, -0.974225475]
        })

        # Define expected output DataFrame after min-max scaling
        expected_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': [1.0, 0.308561561,0.959099737, 0.0],  
            'v02': [0.122512292, 0.754197718, 1.0, 0.0]
        })

        # Run the function and assert the result
        mm_result_df = apply_min_max_scaling(input_df)
        pd.testing.assert_frame_equal(mm_result_df, expected_df)

if __name__ == '__main__':
    unittest.main()



