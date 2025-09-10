import unittest
import pandas as pd
from area_classification.pre_processing.prepare_clustering_data import prepare_clustering_data

class TestStandardizeDataframe(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [52.0, 25.0, 50.0, 10.0],  # Percentages of v01 / v01_total
            'v02': [30.0, 50.0, 60.0, 25.0]   # Percentages of v02 / v02_total
        })

        # Expected output DataFrame after conversion
        # calculated in excel =STANDARDIZE(value,mean,sd) 
        self.expected_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [0.87421454, -0.455576591, 0.775711493, -1.194349441],
            'v02': [-0.680984918, 0.529654936, 1.134974863, -0.983644881]
        })

    def test_standardize_dataframe(self):
        result_df = standardize_dataframe(self.input_df)
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()