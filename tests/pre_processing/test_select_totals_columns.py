import unittest
from unittest.mock import patch

import pandas as pd

from area_classification.pre_processing.select_totals_columns import select_totals_columns

MODULE = "area_classification.pre_processing.select_totals_columns"


class TestTotalColumnsSelectUk(unittest.TestCase):
    def setUp(self):
        # Scotland data
        self.aggregate_input_s = pd.DataFrame(
            {
                "area_code": ["S12000001", "S12000002", "S12000003", "S12000004"],
                "UV101b0001": [50, 100, 110, 145],
                "UV101b0002": [20, 10, 77, 56],
                "UV101b0003": [30, 90, 33, 143],
                "hours_part": [30, 25, 33, 10],
                "hours_full": [30, 25, 32, 40],
                "UV6040001": [60, 50, 65, 50],
            }
        )
        self.select_input_s = pd.DataFrame(
            {
                "area_code": ["S12000001", "S12000002", "S12000003", "S12000004"],
                "v01": [30, 90, 33, 143],
                "v45": [30, 25, 33, 10],
                "v46": [30, 25, 32, 40],
            }
        )
        # England/Wales data
        self.aggregate_input_e = pd.DataFrame(
            {
                "area_code": ["E12000001", "E12000002", "E12000003", "E12000004"],
                "ts0010001": [50, 100, 110, 145],
                "ts0010002": [20, 10, 77, 56],
                "ts0010003": [30, 90, 33, 143],
                "ts0590002": [30, 25, 33, 10],
                "ts0590005": [30, 25, 32, 40],
                "ts0590001": [60, 50, 65, 50],
            }
        )
        self.select_input_e = pd.DataFrame(
            {
                "area_code": ["E12000001", "E12000002", "E12000003", "E12000004"],
                "v01": [30, 90, 33, 143],
                "v45": [30, 25, 33, 10],
                "v46": [30, 25, 32, 40],
            }
        )
        # Expected concatenated output
        self.expected_df = pd.DataFrame(
            {
                "area_code": [
                    "E12000001",
                    "E12000002",
                    "E12000003",
                    "E12000004",
                    "S12000001",
                    "S12000002",
                    "S12000003",
                    "S12000004",
                ],
                "v01": [30, 90, 33, 143, 30, 90, 33, 143],
                "v01_total": [50, 100, 110, 145, 50, 100, 110, 145],
                "v45": [30, 25, 33, 10, 30, 25, 33, 10],
                "v45_total": [60, 50, 65, 50, 60, 50, 65, 50],
                "v46": [30, 25, 32, 40, 30, 25, 32, 40],
                "v46_total": [60, 50, 65, 50, 60, 50, 65, 50],
            }
        )

    @patch(f"{MODULE}.os.listdir")
    @patch(f"{MODULE}.pd.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_total_columns_select_uk_concat(self, mock_to_csv, mock_read_csv, mock_listdir):
        mock_to_csv.return_value = None
        # Patch os.listdir to return the expected select files
        mock_listdir.return_value = [
            "preprocessing_ew_selected_variables.csv",
            "preprocessing_scot_selected_variables.csv",
        ]

        # In setUp, add:
        self.lookup_df = pd.DataFrame(
            {
                "new_code": ["v01", "v45", "v46", "v01", "v45", "v46"],
                "table_ID": ["ts001", "ts059", "ts059", "UV101b", "UV604", "UV604"],
                "country": ["ew", "ew", "ew", "scot", "scot", "scot"],
            }
        )

        # set up a mock config:
        config = {
            "qa_directory": "./data/QA/",
            "select_variables_lookup": "tests/data/total_columns_select_uk_test_data/lookup.csv",
        }

        # Map file paths to DataFrames
        def side_effect(path, *args, **kwargs):
            if "preprocessing_aggregated_all_variables_CA19.csv" in path:
                return self.aggregate_input_s
            if "preprocessing_scot_selected_variables.csv" in path:
                return self.select_input_s
            if "preprocessing_aggregated_all_variables_LTLA.csv" in path:
                return self.aggregate_input_e
            if "preprocessing_ew_selected_variables.csv" in path:
                return self.select_input_e
            if "lookup.csv" in path:
                return self.lookup_df
            raise ValueError(f"Unexpected file path: {path}")

        mock_read_csv.side_effect = side_effect

        result_df = select_totals_columns(config, "tests/data/total_columns_select_uk_test_data")

        for col in self.expected_df.columns:
            if col.endswith("_total"):
                self.expected_df[col] = self.expected_df[col].astype(int)

        pd.testing.assert_frame_equal(
            result_df.reset_index(drop=True), self.expected_df.reset_index(drop=True)
        )


if __name__ == "__main__":
    unittest.main()
