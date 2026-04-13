# pip install xlwt
import io
import os
import shutil
import unittest
from unittest.mock import patch

import pandas as pd

from area_classification.post_processing.cluster_summaries import cluster_summaries_wrapper


class TestClusterSummariesWrapperIntegration(unittest.TestCase):
    def setUp(self):
        # Create a mock configuration
        self.config = {
            "input_directory": "./tests/data/summaries/",
            "output_directory": "./tests/data/summaries/",
            "qa_directory": "./tests/data/summaries/",
        }

        # Create mock data for restructured_cluster_table_long
        self.restructured_cluster_table_long = pd.DataFrame(
            {
                "LAD_name": ["Hartlepool", "Middlesbrough", "City of Edinburgh", "Glasgow City"],
                "LAD_code": ["E06000001", "E06000002", "S12000036", "S12000049"],
                "supergroup": ["1", "1", "2", "2"],
                "group": ["1a", "1a", "2b", "2b"],
                "subgroup": ["1a1", "1a2", "2b1", "2b2"],
                "v01": [0.5, 0.6, 0.7, 0.8],
                "v02": [0.1, 0.7, 0.2, 0.3],
                "v12": [0.5, 0.3, 0.9, 0.8],
            }
        )
        self.restructured_cluster_table_long.to_csv(
            "test_restructured_cluster_table_long.csv", index=False
        )

        # Create mock uk_std_cluster_means DataFrame
        # This is used for average variance as looking at vairance of the clustering
        self.uk_std_cluster_means = pd.DataFrame(
            {
                "cluster": [1, "1a", "1a1", "1a1", "1a2", "2", "2b", "2b1", "2b2"],
                "hierarchy_level": [
                    "supergroup",
                    "group",
                    "subgroup",
                    "subgroup",
                    "subgroup",
                    "supergroup",
                    "group",
                    "subgroup",
                    "subgroup",
                ],
                "v01": [0.35, 0.2, 0.525, 0.45, 0.60, 0.55, 0.40, 0.625, 0.70],
                "v02": [0.75, 0.15, -0.825, 0.90, 0.10, 0.95, -0.20, 1.025, 1.10],
                "v12": [0.16, 0.08, 0.20, -0.24, 0.32, 0.40, -0.12, 0.48, 0.56],
            }
        )
        self.uk_std_cluster_means.to_csv("uk_std_cluster_means.csv", index=False)

        # Create a mock lookup file
        os.makedirs("./tests/data/summaries/", exist_ok=True)
        self.lookup_file = "./tests/data/summaries/lookup_file.csv"

        pd.DataFrame(
            {
                "variable_name": [
                    "Lives in a communal establishment",
                    "Never married and never registered a civil partnership",
                    "Usual residents per square kilometre",
                ],
                "variable_code": ["ts0010003", "ts0020002", "ts0060001"],
                "table_ID": ["TS001", "TS002", "TS006"],
                "table_name": ["Residency type", "Legal partnership status", "Population density"],
                "country": ["ew", "ew", "ew"],
                "new_code": ["v01", "v02", "v12"],
                "domain": [
                    "Demography and Migration",
                    "Demography and Migration",
                    "Demography and Migration",
                ],
            }
        ).to_csv(self.lookup_file, index=False)

    def test_cluster_summaries_wrapper(self):
        # Expected output strings
        # When checking variance, remember sample var used and the value after higher / lower is related to the UK_means table
        expected_output = (
            "Cluster 1\n"
            "Cluster 1 contains 2 local authorities which is 50.00% of UK local authorities. The average variance for cluster 1 is 0.068. Example areas: Middlesbrough, Hartlepool\n"
            "Values in the brackets below are the difference between the mean of the \n"
            "              variable for this cluster compared with the mean of the other clusters combined. \n"
            "              The population of cluster 1 has a:\n"
            "• lower (-0.240) Usual residents per square kilometre. Variance:0.020 (Demography and Migration domain)\n"
            "• lower (-0.200) proportion of people who live in a communal establishment. Variance:0.005 (Demography and Migration domain)\n"
            "• lower (-0.200) proportion of people who are Never married and never registered a civil partnership. Variance:0.180 (Demography and Migration domain)\n"
            "----------------------------------------\n"
            "Cluster 2\n"
            "Cluster 2 contains 2 local authorities which is 50.00% of UK local authorities. The average variance for cluster 2 is 0.005. Example areas: Glasgow City, City of Edinburgh\n"
            "Values in the brackets below are the difference between the mean of the \n" 
            "              variable for this cluster compared with the mean of the other clusters combined. \n"
            "              The population of cluster 2 has a:\n"
            "• higher (0.240) Usual residents per square kilometre. Variance:0.005 (Demography and Migration domain)\n"
            "• higher (0.200) proportion of people who live in a communal establishment. Variance:0.005 (Demography and Migration domain)\n"
            "• higher (0.200) proportion of people who are Never married and never registered a civil partnership. Variance:0.005 (Demography and Migration domain)\n"
            "----------------------------------------\n"
        )

        for col, dtype in self.restructured_cluster_table_long.dtypes.items():
            print(f"{col}: {dtype}")

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            #         print("Running cluster_summaries_wrapper...")
            cluster_summaries_wrapper(
                config=self.config,
                restructured_cluster_table_long=self.restructured_cluster_table_long,
                uk_std_cluster_means=self.uk_std_cluster_means,
                lookup_file=self.lookup_file,
                cluster_column="supergroup",
            )
        #         print("Checking outputs...")
        print("expected output:", expected_output)
        print("actual output:", fake_out.getvalue())
        self.assertIn(expected_output, fake_out.getvalue())

        print("Cleaning up test files...")
        # Clean up - remove created files and folders
        for filename in os.listdir(self.config["input_directory"]):
            file_path = os.path.join(self.config["input_directory"], filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                shutil.rmtree(self.config["input_directory"])

        print("Integration test completed.")


if __name__ == "__main__":
    unittest.main()
