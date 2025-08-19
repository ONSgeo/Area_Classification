import unittest
import pandas as pd
from area_classification.pre_processing.convert_to_percentages import convert_to_percentages 

class TestConvertToPercentages(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [50, 30, 20, 100],
            'v01_total': [100, 60, 40, 1000],
            'v02': [25, 15, 10, 50],
            'v02_total': [50, 30, 20, 200]
        })

        # Expected output DataFrame after conversion
        self.expected_df = pd.DataFrame({
            'LAD_code': ['E06000001', 'W06000001', 'N09000001','S12000005'],
            'v01': [50.0, 50.0, 50.0, 10.0],  # Percentages of v01 / v01_total
            'v02': [50.0, 50.0, 50.0, 25.0]   # Percentages of v02 / v02_total
        })

    def test_convert_to_percentages(self):
        # Call the function to test
        result_df = convert_to_percentages(self.input_df)
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()