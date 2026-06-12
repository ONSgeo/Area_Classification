import os
import tempfile
import unittest

import pandas as pd

from area_classification.utilities.loading_data import load_data, load_format_data


def create_dummy_csv(directory, filename, data):
    path = os.path.join(directory, filename)
    pd.DataFrame(data).to_csv(path, index=False)
    return path


class TestLoadFormatData(unittest.TestCase):
    def test_load_data_handles_missing_values(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a CSV file with missing values
            data = {"A": [1, None, 3], "B": [4, 5, None]}
            csv_path = os.path.join(tmpdir, "test.csv")
            pd.DataFrame(data).to_csv(csv_path)
            # Call load_data
            df = load_data(csv_path)
            # Check that missing values are replaced with 0
            self.assertTrue((df.isnull().sum().sum() == 0))
            self.assertEqual(df.loc[1, "A"], 0)
            self.assertEqual(df.loc[2, "B"], 0)

    def test_load_format_data_merges_multiple_files_correctly(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create two dummy CSV files with a common join column
            data1 = {"geo_code": [1, 2], "A": [10, 20]}
            data2 = {"geo_code": [1, 2], "B": [100, 200]}
            create_dummy_csv(tmpdir, "ts001.csv", data1)
            create_dummy_csv(tmpdir, "ts002.csv", data2)
            # Prepare config with input_directory
            config = {"input_directory": tmpdir}
            # Run function
            merged = load_format_data(tmpdir, "ts*.csv", "geo_code", config)
            # Check shape and columns
            self.assertEqual(merged.shape, (2, 3))
            self.assertEqual(set(merged.columns), {"geo_code", "A", "B"})
            self.assertEqual(merged.loc[0, "A"], 10)
            self.assertEqual(merged.loc[0, "B"], 100)

    def test_load_format_data_raises_if_no_files_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {"input_directory": tmpdir}
            with self.assertRaises(FileNotFoundError) as cm:
                load_format_data(tmpdir, "ts*.csv", "geo_code", config)
            self.assertIn("No files matching", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
