import os
import tempfile
import pandas as pd
from area_classification.utilities.loading_data import load_format_data



def create_dummy_csv(directory, filename, data):
    path = os.path.join(directory, filename)
    pd.DataFrame(data).to_csv(path, index=False)
    return path

def test_load_format_data_merges_multiple_files_correctly():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two dummy CSV files with a common join column
        data1 = {'geo_code': [1, 2], 'A': [10, 20]}
        data2 = {'geo_code': [1, 2], 'B': [100, 200]}
        create_dummy_csv(tmpdir, 'ts001.csv', data1)
        create_dummy_csv(tmpdir, 'ts002.csv', data2)
        # Run function
        merged = load_format_data(tmpdir, 'ts*.csv', 'geo_code')
        # Check shape and columns
        assert merged.shape == (2, 3)
        assert set(merged.columns) == {'geo_code', 'A', 'B'}
        assert merged.loc[0, 'A'] == 10
        assert merged.loc[0, 'B'] == 100

def test_load_format_data_raises_if_no_files_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        # No files created
        try:
            load_format_data(tmpdir, 'ts*.csv', 'geo_code')
        except FileNotFoundError as e:
            assert "No files matching" in str(e)
        else:
            assert False, "FileNotFoundError not raised"

    # Dummy data files for manual inspection (not used in tests, but as requested)
    # File 1: ts001.csv
    # geo_code,A
    # 1,10
    # 2,20

    # File 2: ts002.csv
    # geo_code,B
    # 1,100
    # 2,200