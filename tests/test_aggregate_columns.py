import pandas as pd
import numpy as np
import pytest
from pandas.testing import assert_frame_equal
from area_classification.pre_processing.aggregating_variables import batch_ag_columns as ag_columns

df_dummy = pd.DataFrame({'col_1': [1, 1, 2, 2, 5],
                'col_2': [6, 7, 8, 9, 10],
                'col_3': [20, 30, 40, 50, 60]})

df_expected_multiple = pd.DataFrame({'col_1': [1, 1, 2, 2, 5],
                'col_2': [6, 7, 8, 9, 10],
                'col_3': [20, 30, 40, 50, 60],
                'col_4': [27, 38, 50, 61, 75]})

df_expected_1_column = pd.DataFrame({'col_1': [1, 1, 2, 2, 5],
                'col_2': [6, 7, 8, 9, 10],
                'col_3': [20, 30, 40, 50, 60],
                'col_4': [1, 1, 2, 2, 5]})

df_dummy_nan = pd.DataFrame({'col_1': [1, None, 2, 2, 5],
                'col_2': [6, 7, np.nan, 9, 10],
                'col_3': [20, 30, 40, 50, 60]})

df_expected_nan = pd.DataFrame({'col_1': [1, None, 2, 2, 5],
                'col_2': [6, 7, np.nan, 9, 10],
                'col_3': [20, 30, 40, 50, 60],
                'col_4': [27, 37, 42, 61, 75]})

df_dummy_inf = pd.DataFrame({'col_1': [1, 1, np.inf, 2, 5],
                'col_2': [6, 7, 8, 9, 10],
                'col_3': [20, 30, 40, 50, 60]})

#df_expected_inf = pd.DataFrame({'col_1': [1, 1, np.inf, 2, 5],
#                'col_2': [6, 7, 8, 9, 10],
#                'col_3': [20, 30, 40, 50, 60],
#                'col_4': [27, 38, , 61, 75]})

def test_ag_columns():
    df_actual = ag_columns(df_dummy, ['col_1', 'col_2', 'col_3'], 'col_4')
    assert_frame_equal(df_actual, df_expected_multiple, check_dtype=False)

def test_ag_1_column():
    df_actual = ag_columns(df_dummy, ['col_1'], 'col_4')
    assert_frame_equal(df_actual, df_expected_1_column, check_dtype=False)

def test_ag_nan():
    df_actual = ag_columns(df_dummy_nan, ['col_1', 'col_2', 'col_3'], 'col_4')
    assert_frame_equal(df_actual, df_expected_nan, check_dtype=False)

@pytest.mark.xfail(reason="Function has not been updated to raise value errors")
def test_ag_inf():
    with pytest.raises(ValueError):
        ag_columns(df_dummy_inf, ['col_1', 'col_2', 'col_3'], 'col_4')
    