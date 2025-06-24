import pandas as pd
import pytest
from area_classification.pre_processing.convert_to_percentages import convert_to_percentages

@pytest.fixture
def sample_dataframe():
    # Create a DataFrame with two groups (ts001, ts002), each with a total column (ending 0001) and other columns
    data = {
        "LTLA": ["A", "B"],
        "ts0010001": [100, 200],  # total for ts001
        "ts0010002": [30, 50],
        "ts0010003": [70, 150],
        "ts0020001": [400, 800],  # total for ts002
        "ts0020002": [100, 200],
        "ts0020003": [200, 400],
        "ts0020004": [100, 200],
    }
    return pd.DataFrame(data)

def test_convert_to_percentages_basic(sample_dataframe):
    df = sample_dataframe.copy()
    result = convert_to_percentages(df, area_code_column_name="LTLA")

    # Check that the area code column is unchanged
    assert (result["LTLA"] == sample_dataframe["LTLA"]).all()

    # Check ts001 group
    assert pytest.approx(result.loc[0, "ts0010001"]) == 100.0
    assert pytest.approx(result.loc[0, "ts0010002"]) == 30.0
    assert pytest.approx(result.loc[0, "ts0010003"]) == 70.0
    assert pytest.approx(result.loc[1, "ts0010001"]) == 100.0
    assert pytest.approx(result.loc[1, "ts0010002"]) == 25.0
    assert pytest.approx(result.loc[1, "ts0010003"]) == 75.0

    # Check ts002 group
    assert pytest.approx(result.loc[0, "ts0020001"]) == 100.0
    assert pytest.approx(result.loc[0, "ts0020002"]) == 25.0
    assert pytest.approx(result.loc[0, "ts0020003"]) == 50.0
    assert pytest.approx(result.loc[0, "ts0020004"]) == 25.0
    assert pytest.approx(result.loc[1, "ts0020001"]) == 100.0
    assert pytest.approx(result.loc[1, "ts0020002"]) == 25.0
    assert pytest.approx(result.loc[1, "ts0020003"]) == 50.0
    assert pytest.approx(result.loc[1, "ts0020004"]) == 25.0

def test_convert_to_percentages_nan_and_zero_division():
    # Test with zero in total column and NaN in data
    data = {
        "LTLA": ["A", "B"],
        "ts0010001": [0, 100],  # total for ts001, first row is zero
        "ts0010002": [10, None],
        "ts0010003": [0, 100],
    }
    df = pd.DataFrame(data)
    result = convert_to_percentages(df, area_code_column_name="LTLA")

    # For row 0, division by zero should result in 0 after fillna
    assert result.loc[0, "ts0010001"] == 0
    assert result.loc[0, "ts0010002"] == 0
    assert result.loc[0, "ts0010003"] == 0

    # For row 1, normal calculation, NaN replaced by 0
    assert result.loc[1, "ts0010001"] == 100
    assert result.loc[1, "ts0010002"] == 0
    assert result.loc[1, "ts0010003"] == 100

def test_convert_to_percentages_missing_total_column():
    # Should raise ValueError if total column is missing
    data = {
        "LTLA": ["A"],
        "ts0010002": [10],
        "ts0010003": [20],
    }
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Total column 'ts0010001' not found in DataFrame."):
        convert_to_percentages(df, area_code_column_name="LTLA")

def test_convert_to_percentages_out_of_range():
    # Should raise ValueError if result is out of [0, 100]
    data = {
        "LTLA": ["A"],
        "ts0010001": [10],
        "ts0010002": [20],  # 200%
    }
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Column ts0010002 contains values outside the range"):
        convert_to_percentages(df, area_code_column_name="LTLA")