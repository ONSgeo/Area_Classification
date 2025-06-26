import pandas as pd
from area_classification.pre_processing.standard_illness_ratio import SIR_calculation
from pathlib import Path


def test_SIR_calculation():
    mock_data = pd.DataFrame({
        "Area_Code": ['S1', 'S1', 'S2', 'S2', 'S3', 'S3'],
        'Local_Authority': ['LA1', 'LA1', 'LA2', 'LA2', 'LA3', 'LA3'],
        'age_group': ['0_14_65_over', '15_64', '0_14_65_over', '15_64', '0_14_65_over', '15_64'],
        'total_population': [100, 200, 150, 250, 120, 180],
        'total_disabled': [10, 20, 12, 24, 12, 22]
    })


    df_output = SIR_calculation(mock_data)
    output = df_output[["Area_Code","Local_Authority", "SIR"]]
    expected_output = pd.read_csv(Path("tests/data/sir_test_expected_output.csv")).rename(columns = {"SIR_expected": "SIR"})
    pd.testing.assert_frame_equal(output, expected_output, check_dtype=False)