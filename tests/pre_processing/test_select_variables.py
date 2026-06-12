import unittest

import pandas as pd

from area_classification.pre_processing.select_variables import select_variables


class TestSelectVariables(unittest.TestCase):
    def setUp(self):
        # Sample input DataFrame
        self.input_df = pd.DataFrame(
            {
                "LAD_code": ["S12000001", "S12000002", "S12000003", "S12000004"],
                "UV1040001": [50, 30, 20, 100],
                "UV1040002": [100, 60, 40, 100],
                "UV1040003": [25, 15, 10, 50],
                "UV1040004": [50, 30, 20, 200],
            }
        )

        # Expected output DataFrame after conversion
        self.expected_df = pd.DataFrame(
            {
                "LAD_code": ["S12000001", "S12000002", "S12000003", "S12000004"],
                "v02": [100, 60, 40, 100],
                "v03": [25, 15, 10, 50],
            }
        )

        self.lookup_df = pd.DataFrame(
            {
                "variable_name": ["Never married", "Married"],
                "variable_code": ["UV1040002", "UV1040003"],
                "table_id": ["UV104", "UV104"],
                "table_name": ["Marital status", "Marital status"],
                "country": ["scot", "scot"],
                "new_code": ["v02", "v03"],
                "domain": ["Demography and Migration", "Demography and Migration"],
            }
        )

    def test_select_variables(self):
        result_df = select_variables(self.input_df, self.lookup_df)
        # Assert that the result matches the expected output
        pd.testing.assert_frame_equal(result_df, self.expected_df)


if __name__ == "__main__":
    unittest.main()
