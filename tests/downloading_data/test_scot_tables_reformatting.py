import os
import unittest
from unittest.mock import patch, mock_open, call, MagicMock
import pandas as pd
import pandas.testing as pdt
import numpy as np

# DO WE NEED UNIT TESTS FOR THE INDIVIDUAL TABLES REFORMAT FUNCTIONS?
from area_classification.downloading_data.scot_tables_reformatting import (
    rename_csv_files_by_table_id, extract_pop_density_table,
    extract_metadata_from_files, replace_ca19_names_with_codes,
    remove_rows, reformat_uv101b, reformat_uv103, 
    reformat_migrant_indicator, reformat_pop_density,
    replace_variable_names_with_codes
)

class TestRenameCsvFilesByTableId(unittest.TestCase):
    @patch("os.listdir")
    @patch("builtins.open", new_callable=mock_open, read_data="Some text UV101b more text")
    @patch("os.rename")
    @patch("area_classification.downloading_data.scot_tables_reformatting.logger")
    def test_rename_csv_files_by_table_id(
        self, mock_logger, mock_rename, mock_open_fn, mock_listdir
    ):
        # Setup mock for os.listdir
        mock_listdir.return_value = ["file1.csv", "file2.csv", "not_a_csv.txt"]

        # Call the function
        test_folder = "test_folder"
        rename_csv_files_by_table_id(test_folder)

        # Check that os.rename was called for each CSV file with a Table ID
        expected_calls = [
            call(
                os.path.join(test_folder, "file1.csv"),
                os.path.join(test_folder, "UV101b.csv")
            ),
            call(
                os.path.join(test_folder, "file2.csv"),
                os.path.join(test_folder, "UV101b.csv")
            )
        ]   
        self.assertEqual(mock_rename.call_count, 2)
        self.assertEqual(mock_rename.call_args_list, expected_calls)

        # Check that logger.info was called
        self.assertTrue(mock_logger.info.called)


class ExtractPopDensityTable(unittest.TestCase):
    @patch("area_classification.downloading_data.scot_tables_reformatting.logger")
    @patch("os.remove")
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_excel")
    @patch("os.path.exists")
    def test_extract_pop_density_table(
        self, mock_exists, mock_read_excel, mock_to_csv, mock_remove, mock_logger
    ):
        mock_exists.return_value = True
        mock_read_excel.return_value = pd.DataFrame({"A": [1]})

        folder = "test_folder"
        extract_pop_density_table(folder)

        mock_exists.assert_called_once()
        xlsx_path = os.path.join(folder, "population_density.xlsx")
        mock_read_excel.assert_called_once_with(xlsx_path, sheet_name="Table 4")
        mock_to_csv.assert_called_once()
        mock_remove.assert_called_once()
        mock_logger.info.assert_called()
  


class TestExtractMetadataFromFiles(unittest.TestCase):
    @patch("area_classification.downloading_data.scot_tables_reformatting.logger")
    @patch("os.listdir")
    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.reader")
    def test_extract_metadata_from_files(
        self, mock_csv_reader, mock_open_file, mock_listdir, mock_logger
    ):
        # Setup mock files
        mock_listdir.return_value = [
            "UV303a.csv",  # Should be skipped
            "reformat_UV123.csv",  # Should be skipped
            "migrant_indicator.csv",  # Special case
            "population_density.csv",  # Special case
            "UV607.csv",  # Special case for table_name
            "UV123.csv"   # Normal file
        ]

        # Create a mapping of filenames to mock file objects
        def open_side_effect(file, *args, **kwargs):
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.name = file
            return mock_file

        mock_open_file.side_effect = open_side_effect

        # Setup CSV content for UV607.csv and UV123.csv
        def csv_reader_side_effect(file_obj):
            if "UV607.csv" in file_obj.name:
                # 9 rows, row 4 has special format, row 9 has "Individuals"
                return [
                    [], [], [], ["Some-Text-TableName-All"], [], [], [], [], ["Individuals"]
                ]
            elif "UV123.csv" in file_obj.name:
                # 9 rows, row 4 has normal format, row 9 has "Households"
                return [
                    [], [], [], ["Some-Text-AnotherTable"], [], [], [], [], ["Households"]
                ]
            else:
                return [[]] * 9

        mock_csv_reader.side_effect = csv_reader_side_effect

        # Patch file_obj.name for mock_open
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.name = "UV607.csv"
        mock_open_file.return_value = mock_file

        # Call function
        metadata = extract_metadata_from_files("test_folder")

        # Check special cases
        self.assertIn(
            {"table_id": "migrant_indicator", "table_name": "Migrant Indicator", "unit": "Person"},
            metadata
        )
        self.assertIn(
            {"table_id": "population_density", "table_name": "Population Density", "unit": "Persons per square kilometer"},
            metadata
        )

        # Check normal file
        self.assertTrue(any(entry["table_id"] == "UV123" and entry["unit"] == "Household" for entry in metadata))

        # Check UV607 special parsing
        self.assertTrue(any(entry["table_id"] == "UV607" and "TableName" in entry["table_name"] for entry in metadata))

# CANNOT GET THIS TO WORK - RETURN TO WORK ON THIS

class TestReplaceCA19NamesWithCodes(unittest.TestCase):
    @patch.object(pd.DataFrame, "to_csv")
    @patch("pandas.read_csv")
    @patch("os.listdir", return_value=["test.csv"])
    @patch("os.path.exists", return_value=True)
    @patch("os.makedirs")
    def test_code_swapping(self, mock_makedirs, mock_exists, mock_listdir, mock_read_csv, mock_to_csv):
        lookup_df = pd.DataFrame({
            "LAD22NM": ["Edinburgh", "Glasgow"],
            "LAD22CD": ["S12000036", "S12000049"]
        })
        input_df = pd.DataFrame({
            0: ["Council Area 2019", "Edinburgh", "Glasgow"],
            1: ["variable1", 1, 2]
        })

        def read_csv_side_effect(path, *args, **kwargs):
            if "lookup" in path:
                return lookup_df
            else:
                return input_df
        mock_read_csv.side_effect = read_csv_side_effect

        captured = {}
        def to_csv_side_effect(self, *args, **kwargs):
            captured['df'] = self.copy()
        mock_to_csv.side_effect = to_csv_side_effect

        config = {"reformat_scot_input_folder": "dummy_output_folder"}
        replace_ca19_names_with_codes("dummy_input_folder", "lookup.csv", config)

        result_df = captured['df']

        expected_df = pd.DataFrame({
            0: ["Council Area 2019", "S12000036", "S12000049"],
            1: ["variable1", 1, 2]
        })

        pdt.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


class TestRemoveRows(unittest.TestCase):
    @patch("os.makedirs")
    @patch("os.path.dirname", return_value="dummy_dir")
    @patch("os.listdir", return_value=["reformat_test.csv"])
    @patch("pandas.read_csv")
    def test_remove_rows(self, mock_read_csv, mock_listdir, mock_dirname, mock_makedirs):
        # Mock input DataFrame: 5 rows, "Council Area 2019" in first cell, last 3 rows are extra
        input_df = pd.DataFrame({
            0: ["Table name", "Council Area 2019", "A", "B", "extra1", "extra2", "extra3"],
            1: ["all people", '', 3, 4, "extra4", "extra5", "extra6"]
        })
        mock_read_csv.return_value = input_df.copy()

        captured = {}
        def to_csv_side_effect(self, file_path, index, header):
            captured['df'] = self.copy()
        with patch.object(pd.DataFrame, "to_csv", new=to_csv_side_effect):
            config = {"reformat_scot_input_folder": "dummy_folder"}
            remove_rows(config, "dummy_folder")

        # Expected output after processing
        expected_df = pd.DataFrame({
            0: ["CA19", "A", "B"],
            1: ["all people", 3, 4]
        })

        # Compare output DataFrame to expected DataFrame
        pd.testing.assert_frame_equal(captured['df'].reset_index(drop=True), expected_df)



class TestReformatMigrantIndicator(unittest.TestCase):
    @patch("os.makedirs")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("pandas.read_csv")
    def test_reformat_migrant_indicator(self, mock_read_csv, mock_join, mock_exists, mock_makedirs):
        # Mock input DataFrame (after skiprows=9, header=None)
        migrant_data = pd.DataFrame([
            ["Table name", "Header1", "Header2", "Total"],
            ["Council Area 2019", "Value1", "Value2", "Sum"],
            ["Glasgow City", 10, 20, 30],
            ["Edinburgh, City of", 5, 15, 20],
            ["Total", "", "", ""]
        ])
        # Mock lookup DataFrame
        lookup_data = pd.DataFrame({
            "LAD22NM": ["Glasgow City", "Edinburgh, City of"],
            "LAD22CD": ["S12000046", "S12000036"]
        })

        # pandas.read_csv returns migrant_data first, then lookup_data
        mock_read_csv.side_effect = [migrant_data, lookup_data]

        # Capture output DataFrame
        captured = {}
        def to_csv_side_effect(self, file_path, index):
            captured['df'] = self.copy()
            captured['file_path'] = file_path

        with patch.object(pd.DataFrame, "to_csv", new=to_csv_side_effect):
            config = {"reformat_scot_input_folder": "output_folder"}
            reformat_migrant_indicator("input_folder", "lookup.csv", config)

        # Check output DataFrame
        df = captured['df']
        expected_columns = ["CA19", "Total", "Header1", "Header2"]
        self.assertListEqual(list(df.columns), expected_columns)
        self.assertIn("S12000046", df["CA19"].values)
        self.assertIn("S12000036", df["CA19"].values)
        self.assertEqual(captured['file_path'], "output_folder/reformat_migrant_indicator.csv")



class TestReformatMigrantIndicator(unittest.TestCase):
    @patch("os.makedirs")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("pandas.read_csv")
    def test_reformat_migrant_indicator(self, mock_read_csv, mock_join, mock_exists, mock_makedirs):
        # Mock input DataFrame (after skiprows=9, header=None)
        migrant_data = pd.DataFrame([
            ["Table name", "Header1", "Header2", "Total"],
            ["Council Area 2019", "", "", ""],
            ["Glasgow City", 10, 20, 30],
            ["Edinburgh", 5, 15, 20],
            ["Total", "", "", ""]
        ])
        # Mock lookup DataFrame
        lookup_data = pd.DataFrame({
            "LAD22NM": ["Glasgow City", "Edinburgh"],
            "LAD22CD": ["S12000046", "S12000036"]
        })

        # pandas.read_csv returns migrant_data first, then lookup_data
        mock_read_csv.side_effect = [migrant_data, lookup_data]

        # Capture output DataFrame
        captured = {}
        def to_csv_side_effect(self, file_path, index):
            captured['df'] = self.copy()
            captured['file_path'] = file_path

        with patch.object(pd.DataFrame, "to_csv", new=to_csv_side_effect):
            config = {"reformat_scot_input_folder": "output_folder"}
            reformat_migrant_indicator("input_folder", "lookup.csv", config)

        # Check output DataFrame
        df = captured['df']
        expected_columns = ["CA19", "Total", "Header1", "Header2"]
        self.assertListEqual(list(df.columns), expected_columns)
        self.assertIn("S12000046", df["CA19"].values)
        self.assertIn("S12000036", df["CA19"].values)
        self.assertEqual(captured['file_path'], "output_folder/reformat_migrant_indicator.csv")




class TestReformatPopDensity(unittest.TestCase):
    @patch("os.makedirs")
    @patch("os.path.dirname", return_value="dummy_dir")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("pandas.read_csv")
    def test_reformat_pop_density(self, mock_read_csv, mock_join, mock_exists, mock_dirname, mock_makedirs):
        
        
        # Mock input DataFrame
        df_input = pd.DataFrame({
            "Area Name": ["Area name1", "Area name1"],
            "Area code": ["S92000003", "S12000046"], # expect S92000003 row to be removed
            "Area type": ["Country", "Council Area"],
            "Population density": [100, 200]
        })
        mock_read_csv.return_value = df_input.copy()

        # Capture output DataFrame
        captured = {}
        def to_csv_side_effect(self, file_path, index):
            captured['df'] = self.copy()
            captured['file_path'] = file_path

        with patch.object(pd.DataFrame, "to_csv", new=to_csv_side_effect):
            config = {"reformat_scot_input_folder": "output_folder"}
            reformat_pop_density("input_folder", config)

        # Check output DataFrame columns
        expected_columns = [
            "CA19",
            "Population density (number of usual residents per square kilometre)"
        ]
        self.assertListEqual(list(captured['df'].columns), expected_columns)
        # Check 'S92000003' row is removed
        self.assertNotIn("S92000003", captured['df']["CA19"].values)
        # Check output file path
        self.assertEqual(
            captured['file_path'],
            "output_folder/reformat_population_density.csv"
        )




class TestReplaceVariableNamesWithCodes(unittest.TestCase):
    @patch("os.makedirs")
    @patch("os.path.dirname", return_value="dummy_dir")
    @patch("os.listdir", return_value=["reformat_uv123.csv"])
    @patch("pandas.read_csv")
    def test_replace_variable_names_with_codes_uv123(self, mock_read_csv, mock_listdir, mock_dirname, mock_makedirs):
        # Step 1: Mock input DataFrame
        input_df = pd.DataFrame({
            "CA19": ["A", "B"],
            "var1": [1, 2],
            "var2": [3, 4],
            "var3": [5, 6] # expecting this to be dropped from output
        })
        mock_read_csv.return_value = input_df.copy()

        # Step 2: Patch to_csv to capture output DataFrame
        captured = {}
        def to_csv_side_effect(self, file_path, index, header):
   
            captured['df'] = self.copy()
        with patch.object(pd.DataFrame, "to_csv", new=to_csv_side_effect):
            config = {"reformat_scot_input_folder": "dummy_folder"}
            result = replace_variable_names_with_codes(config)
        
        # Step 3: Assert output DataFrame columns
        # last column has been dropped from output
        expected_columns = ["CA19", "uv1230001", "uv1230002"]
        self.assertListEqual(list(captured['df'].columns), expected_columns)

        # Step 4: Assert returned variable names and ids
        # varialble_names and variable_ids get created before the last column is dropped
        expected_variable_names = ["CA19", "var1", "var2", "var3"]
        expected_variable_ids = ["uv1230001", "uv1230002", "uv1230003"]
        self.assertListEqual(list(result[0][0]), expected_variable_names)
        self.assertListEqual(list(result[0][1]), expected_variable_ids)


if __name__ == "__main__":
    unittest.main()


