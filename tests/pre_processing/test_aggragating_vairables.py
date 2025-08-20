import unittest
import pandas as pd
from area_classification.pre_processing.aggregating_variables import aggregating_variables 

class TestAggregatingVariables(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame({
            'LAD_code': ['S12000001', 'S12000002', 'S12000003','S12000004'],
            'UV1040003': [50, 30, 20, 100],
            'UV1040004': [100, 60, 40, 100],
            'UV1040005': [25, 15, 10, 50],
            'UV1040006': [50, 30, 20, 200]
        })

        # Expected output DataFrame after aggregation
        self.expected_df = pd.DataFrame({
            'LAD_code': ['S12000001', 'S12000002', 'S12000003', 'S12000004'],
            'UV1040003': [50, 30, 20, 100],
            'UV1040004': [100, 60, 40, 100],
            'UV1040005': [25, 15, 10, 50],
            'UV1040006': [50, 30, 20, 200],
            'separated_divorced': [125, 75, 50, 150]  # Added UV1040004 + UV1040005
        })

    def test_aggregating_variables(self):
        from utilities.load_config import load_config
        config = load_config('area_classification/config.yaml')
        aggregation_config = load_config('area_classification/aggregation_setup.yaml')
        aggregation_configs = aggregation_config['scot_file_configs']
        result_df = aggregating_variables(self.input_df, aggregation_configs, config )
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)

if __name__ == '__main__':
    unittest.main()