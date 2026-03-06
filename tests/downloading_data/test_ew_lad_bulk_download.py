# Unit test not running yet!
import unittest
from unittest.mock import Mock, mock_open, patch

import pandas as pd

from area_classification.downloading_data.ew_lad_bulk_download import (
    download_and_unzip_data,
    format_and_export_metadata_table,
    get_census_table_urls,
)

MODULE = "area_classification.downloading_data.ew_lad_bulk_download"


class TestGetCensusTableUrls(unittest.TestCase):
    @patch(f"{MODULE}.requests.get")
    def test_get_census_table_urls(self, mock_get):
        # Mock HTML with three .zip links
        html = """
        <html>
            <body>
                <a href="/output/census/2021/census2021-abc123.zip">Table 1</a>
                <a href="/output/census/2021/census2021-def456.zip">Table 2</a>
                <a href="/output/census/2021/census2021-ghi789.zip">Table 3</a>
                <a href="/output/census/2021/census2021-extra.zip">Extra Table</a>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.content = html.encode("utf-8")
        mock_get.return_value = mock_response

        config = {"england_and_wales_table_codes_to_remove": ["def456"]}

        urls = get_census_table_urls(config)
        expected_urls = [
            "https://www.nomisweb.co.uk/output/census/2021/census2021-abc123.zip",
            "https://www.nomisweb.co.uk/output/census/2021/census2021-ghi789.zip",
        ]
        self.assertCountEqual(urls, expected_urls)


class TestDownloadAndUnzipData(unittest.TestCase):
    @patch(f"{MODULE}.rmtree")
    @patch(f"{MODULE}.os.makedirs")
    @patch(f"{MODULE}.pd.DataFrame.to_csv")
    @patch(f"{MODULE}.pd.read_csv")
    @patch(f"{MODULE}.glob")
    @patch(f"{MODULE}.ZipFile")
    @patch(f"{MODULE}.open", create=True)
    @patch(f"{MODULE}.requests.get")
    @patch(f"{MODULE}.tempfile.mkdtemp")
    def test_download_and_unzip_data(
        self,
        mock_mkdtemp,
        mock_requests_get,
        mock_open_func,
        mock_zipfile,
        mock_glob,
        mock_read_csv,
        mock_to_csv,
        mock_makedirs,
        mock_rmtree,
    ):
        # --- Test case 1: ts001, unit from metadata ---
        mock_mkdtemp.return_value = "/tmp/mockdir"
        mock_requests_get.return_value.content = b"fakezip"
        mock_zipfile.return_value.__enter__.return_value.extractall = Mock()
        # CSV and metadata txt file
        mock_glob.side_effect = [
            ["/tmp/mockdir/census2021-ts001-ltla.csv"],  # CSV
            ["/tmp/mockdir/metadata/meta.txt"],  # Metadata txt
        ]
        # Mock open for metadata file
        metadata_content = "Some header\nUnit of measure: Household\nOther info\n"
        m_open = mock_open(read_data=metadata_content)
        m_open.return_value.__iter__ = lambda self: iter(metadata_content.splitlines(True))
        mock_open_func.side_effect = m_open

        df = pd.DataFrame(
            {
                "date": [20210101],
                "geography": ["Area1"],
                "geography code": ["E123"],
                "col1": [1],
                "col2": [2],
            }
        )
        mock_read_csv.return_value = df
        zip_urls = ["https://www.nomisweb.co.uk/output/census/2021/census2021-ts001.zip"]
        config = {"input_directory": "/mock/input"}
        meta = download_and_unzip_data(zip_urls, config)
        self.assertIn("Unit", meta.columns)
        self.assertEqual(meta["Unit"].iloc[0], "Household")

        # --- Test case 2: ts007a, special case unit ---
        mock_glob.side_effect = [
            ["/tmp/mockdir/census2021-ts007a-ltla.csv"],  # CSV
            [],  # No metadata txt
        ]
        zip_urls = ["https://www.nomisweb.co.uk/output/census/2021/census2021-ts007a.zip"]
        meta = download_and_unzip_data(zip_urls, config)
        self.assertIn("Unit", meta.columns)
        self.assertEqual(meta["Unit"].iloc[0], "Person")

        # Check other metadata columns
        self.assertIn("Full_Name", meta.columns)
        self.assertIn("Variable_ID", meta.columns)
        self.assertIn("Table_ID", meta.columns)
        self.assertTrue(mock_to_csv.called)


class TestFormatAndExportMetadataTable(unittest.TestCase):
    @patch(f"{MODULE}.os.makedirs")
    @patch(f"{MODULE}.pd.DataFrame.to_csv")
    def test_format_and_export_metadata_table(self, mock_to_csv, mock_makedirs):
        # Sample input DataFrame
        meta_data_table = pd.DataFrame(
            {
                "Full_Name": [
                    "Tenure of household: Total: All households",
                    "Year of arrival in the UK: Total: All usual residents; measures: Value",
                ],
                "Variable_ID": ["ts0010001", "ts0020001"],
                "Table_ID": ["TS001", "TS002"],
            }
        )
        config = {"input_directory": "mock_dir/input"}

        # Call the function
        result = format_and_export_metadata_table(meta_data_table, config)

        # Check directory creation
        mock_makedirs.assert_called_once_with("mock_dir", exist_ok=True)

        # Check CSV export
        mock_to_csv.assert_called_once()
        args, kwargs = mock_to_csv.call_args
        self.assertIn("ew_lad_table_metadata.csv", args[0])
        self.assertFalse(kwargs.get("index", True))

        # Check returned DataFrame columns
        self.assertIn("Table_Name", result.columns)
        self.assertIn("Variable_Name", result.columns)
        # Check values
        self.assertEqual(result.loc[0, "Table_Name"], "Tenure of household")
        self.assertEqual(result.loc[0, "Variable_Name"], "All households")
        self.assertEqual(result.loc[1, "Table_Name"], "Year of arrival in the UK")
        self.assertEqual(result.loc[1, "Variable_Name"], "All usual residents")


if __name__ == "__main__":
    unittest.main()
