import unittest
import pandas as pd
from area_classification.pre_processing.standardised_illness_ratio import SIR_calculation
from pathlib import Path
from unittest.mock import patch

class TestSIRCalculation(unittest.TestCase):
    def setUp(self):
        patcher_to_csv = patch("pandas.DataFrame.to_csv")
        patcher_makedirs = patch("os.makedirs")
        self.mock_to_csv = patcher_to_csv.start()
        self.mock_makedirs = patcher_makedirs.start()
        self.addCleanup(patcher_to_csv.stop)
        self.addCleanup(patcher_makedirs.stop)

    def test_SIR_calculation(self):
        mock_data = pd.DataFrame({
            "area_code": ['S1', 'S1', 'S2', 'S2', 'S3', 'S3'],
            'Local_Authority': ['LA1', 'LA1', 'LA2', 'LA2', 'LA3', 'LA3'],
            'age_group': ['0_14_65_over', '15_64', '0_14_65_over', '15_64', '0_14_65_over', '15_64'],
            'total_population': [100, 200, 150, 250, 120, 180],
            'total_disabled': [10, 20, 12, 24, 12, 22]
        })
        config = {"qa_directory": ''}
        df_output = SIR_calculation(mock_data, config)
        output = df_output[["area_code", "SIR"]]
        expected_output = pd.read_csv(Path("./tests/data/sir_test_expected_output.csv")).rename(columns={"SIR_expected": "SIR"})
        pd.testing.assert_frame_equal(output, expected_output, check_dtype=False)

if __name__ == "__main__":
    unittest.main()