import unittest
import pandas as pd
import numpy as np
from area_classification.pre_processing.prepare_clustering_data import prepare_clustering_data

class TestStandardizeDataframe(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': [52.0, 25.0, 50.0, 10.0],  # Percentages of v01 / v01_total
            'v02': [30.0, 50.0, 60.0, 25.0]   # Percentages of v02 / v02_total
        })

        # Expected output DataFrame after standardization, arcsinh transformation, and min-max scaling
        # Standardization: z = (x - mean) / std
        # Inverse hyperbolic sine: arcsinh(z)
        # Min-max scaling: (z - min) / (max - min)
        standardized_v01 = (self.input_df['v01'] - self.input_df['v01'].mean()) / self.input_df['v01'].std()
        standardized_v02 = (self.input_df['v02'] - self.input_df['v02'].mean()) / self.input_df['v02'].std()

        arcsinh_v01 = np.arcsinh(standardized_v01)
        arcsinh_v02 = np.arcsinh(standardized_v02)

        minmax_v01 = (arcsinh_v01 - arcsinh_v01.min()) / (arcsinh_v01.max() - arcsinh_v01.min())
        minmax_v02 = (arcsinh_v02 - arcsinh_v02.min()) / (arcsinh_v02.max() - arcsinh_v02.min())

        self.expected_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001', 'S12000005'],
            'v01': minmax_v01,
            'v02': minmax_v02
        })

    def test_standardize_dataframe(self):
        result_df = prepare_clustering_data(self.input_df)
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()