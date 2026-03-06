import os
import shutil
import unittest

import pandas as pd

from area_classification.post_processing.cluster_variables_mean import cluster_variable_means


class TestClusterVariableMeans(unittest.TestCase):
    def setUp(self):
        # Create a temporary output directory
        self.test_output_dir = "test_output"
        os.makedirs(self.test_output_dir, exist_ok=True)

        # Mock config
        self.config = {"output_directory": self.test_output_dir}

        # Mock restructured_cluster_table DataFrame
        self.restructured_cluster_table = pd.DataFrame(
            {
                "LAD_name": ["Hartlepool", "Middlesbrough", "Redcar and Cleveland"],
                "LAD_code": ["E06000001", "E06000002", "E06000003"],
                "supergroup": [1, 2, 1],
                "group": ["1a", "2b", "1b"],
                "subgroup": ["1a1", "2b1", "1b1"],
            }
        )

        # Mock pre_clustering_data_std_mean DataFrame
        self.pre_clustering_data_std_mean = pd.DataFrame(
            {
                "LAD_code": ["E06000001", "E06000002", "E06000003"],
                "V01": [-1, 0.5, 0.1],
                "V02": [3, 0.7, -0.2],
                "V03": [0.1, -0.2, 0.3],
            }
        )

    def tearDown(self):
        # Remove the temporary output directory after the test
        shutil.rmtree(self.test_output_dir)

    def test_cluster_variable_means(self):
        # Run the function
        result = cluster_variable_means(
            self.config, self.restructured_cluster_table, self.pre_clustering_data_std_mean
        )

        # Check the output DataFrame structure
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("cluster", result.columns)
        self.assertIn("hierarchy_level", result.columns)
        self.assertIn("V01", result.columns)
        self.assertIn("V02", result.columns)
        self.assertIn("V03", result.columns)

        # Define expected means for the '1 supergroup' row
        expected_means = {"V01": -0.45, "V02": 1.4, "V03": 0.2}

        # Filter the DataFrame for the '1 supergroup' row
        supergroup_row = result.query("cluster == 1 and hierarchy_level == 'supergroup'")

        # Ensure the row exists
        self.assertEqual(len(supergroup_row), 1, "Expected exactly one row for '1 supergroup'")

        # Compare the actual values with the expected values
        for column, expected_value in expected_means.items():
            self.assertAlmostEqual(
                supergroup_row.iloc[0][column],
                expected_value,
                places=6,
                msg=f"Mismatch in {column} for '1 supergroup'",
            )

        # Check if the output file is created
        output_file_path = os.path.join(
            self.test_output_dir, "std_means", "uk_std_means", "uk_std_cluster_means_output.csv"
        )
        self.assertTrue(os.path.exists(output_file_path))

        # Check if the output file contains the expected data
        output_data = pd.read_csv(output_file_path)
        self.assertFalse(output_data.empty)


if __name__ == "__main__":
    unittest.main()
