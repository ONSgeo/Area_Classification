import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
import os
from tempfile import TemporaryDirectory
from area_classification.pre_processing.select_variables import select_variables

class TestSelectVariables():
    def test_select_variables(self):
        with TemporaryDirectory() as temp_dir:
            # Create dummy base file
            base_file = os.path.join(temp_dir, "base_file.csv")
            base_data = {"LTLA": [1, 2, 3], "Base_Column": ["A", "B", "C"]}
            pd.DataFrame(base_data).to_csv(base_file, index=False)

            # Create dummy input file
            input_file = os.path.join(temp_dir, "input_file.csv")
            input_data = {"LTLA": [1, 2, 3], "Var1": [10, 20, 30]}
            pd.DataFrame(input_data).to_csv(input_file, index=False)

            # Create dummy config
            selected_variables = ["Var1"]
            new_names = {"Var1": "New_Var1"}

            # Call the function with the new_names parameter
            select_variables(temp_dir, base_file, selected_variables, new_names, "LTLA", "left")

            # Load the updated base file
            updated_base_df = pd.read_csv(base_file)

            # Expected output
            expected_data = {
                "LTLA": [1, 2, 3],
                "Base_Column": ["A", "B", "C"],
                "New_Var1": [10, 20, 30]
            }
            expected_df = pd.DataFrame(expected_data)

            # Assert the result
            assert_frame_equal(updated_base_df, expected_df)