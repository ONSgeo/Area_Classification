import unittest

import pandas as pd

from area_classification.pre_processing.prepare_clustering_data import prepare_clustering_data


class TestPrepareClusteringDataIntegration(unittest.TestCase):
    def test_prepare_clustering_data_pipeline(self):
        # Arrange: Create a sample DataFrame
        data = {
            "LAD_code": ["E06000001", "W06000001", "N09000001", "S12000005"],
            "v01": [10, 20, 30, 15],
            "v02": [5, 15, 25, 12],
        }
        dataframe = pd.DataFrame(data)

        # Act: Apply the prepare_clustering_data function
        result = prepare_clustering_data(dataframe)

        # Assert: Check the transformations
        # 1. Ensure the first column (Area) remains unchanged
        pd.testing.assert_series_equal(result["LAD_code"], dataframe["LAD_code"])

        # 2. Ensure numeric columns are scaled to [0, 1]
        numeric_columns = result.iloc[:, 1:]
        self.assertTrue((numeric_columns.min().min() >= 0) and (numeric_columns.max().max() <= 1))

        # 3. Ensure the output DataFrame has the same shape as the input
        self.assertEqual(result.shape, dataframe.shape)

        # 4. Ensure no NaN values exist in the result
        self.assertFalse(result.isnull().values.any())


if __name__ == "__main__":
    unittest.main()
