# JUST NEED A UNIT TEST FOR SCOTLAND

import pytest
import pandas as pd
import unittest
from unittest.mock import patch
import unittest
from pathlib import Path
import tempfile
import os

from area_classification.utilities.disability_age_group_conversion import convert_disability_age_group_england_wales
from area_classification.utilities.disability_age_group_conversion import convert_disability_age_group_northern_ireland
from area_classification.utilities.disability_age_group_conversion import convert_disability_age_group_scotland
class TestConvertDisabilityAgeGroupEnglandWales(unittest.TestCase):
    def setUp(self):
        self.test_data_filepath = "./tests/data/ew_test_disability_data.xlsx"
        self.config = {'input_directory': './tests/data/'}
        columns = [
            "Year", "Local Authority", "Area Code", "Category",
            "Disability status", "Age", "Count", "Population", "Sex"
        ]
        placeholders = pd.DataFrame({col: ['']*4 for col in columns})
        header = pd.DataFrame([columns], columns=columns)
        age_bands = ['under 1', '1 to 4'] + [f'{i} to {i+4}' for i in range(5, 90, 5)] + ['90+']
        population = [1000 + i*10 for i in range(len(age_bands))]
        disabled_count = [i*20 for i in range(20)]
        non_disabled_count = [population[i] - disabled_count[i] for i in range(20)]

        data = {
            "Year": [2021]*40,
            "Local Authority": ['Adur']*40,
            "Area Code": ['E07000223']*40,
            "Category": ['Two category']*40,
            "Disability status": ['Disabled']*20 + ['Non-disabled']*20,
            "Age": age_bands*2,
            "Count": disabled_count + non_disabled_count,
            "Population": population*2,
            "Sex": ['Persons']*40
        }
        data_rows = pd.DataFrame(data)
        df = pd.concat([placeholders, header, data_rows], ignore_index=True)
        os.makedirs(os.path.dirname(self.test_data_filepath), exist_ok=True)
        df.to_excel(self.test_data_filepath, sheet_name='Table 6', index=False, header=False)

        self.expected_df = pd.DataFrame({
            'area_code': ['E07000223', 'E07000223'],
            'local_authority': ['Adur', 'Adur'],
            'age_group': ['<15 and >=65', '15-64'],
            'total_disabled': [2100, 1700],
            'total_population': [11050, 10850], 
        })

    def test_convert_disability_age_group_england_wales(self):
        result_df = convert_disability_age_group_england_wales(self.test_data_filepath, self.config)
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertFalse(result_df.empty)
        pd.testing.assert_frame_equal(result_df, self.expected_df)

class TestConvertDisabilityAgeGroupNorthernIreland(unittest.TestCase):
    def setUp(self):
        self.test_data_filepath = "./tests/data/ni_test_disability_data.xlsx"
        self.config = {'input_directory': './tests/data/'}
        columns = [
            "Geography", "Geography code", "All usual residents", 
            "All usual residents:Day-to-day activities limited a lot", 
            "All usual residents:Day-to-day activities limited a little", 
            "All usual residents:Day-to-day activities not limited", 
            "Usual residents aged 0-14 years", 
            "Usual residents aged 0-14 years:Day-to-day activities limited a lot", 
            "Usual residents aged 0-14 years: Day-to-day activities limited a little", 
            "Usual residents aged 0-14 years: Day-to-day activities not limited", 
            "Usual residents aged 15-39 years",
            "Usual residents aged 15-39 years: Day-to-day activities limited a lot",
            "Usual residents aged 15-39 years: Day-to-day activities limited a little",
            "Usual residents aged 15-39 years: Day-to-day activities not limited",
            "Usual residents aged 40-64 years",
            "Usual residents aged 40-64 years: Day-to-day activities limited a lot",
            "Usual residents aged 40-64 years: Day-to-day activities limited a little",
            "Usual residents aged 40-64 years: Day-to-day activities not limited",
            "Usual residents aged 65+ years",
            "Usual residents aged 65+ years: Day-to-day activities limited a lot",
            "Usual residents aged 65+ years: Day-to-day activities limited a little",
            "Usual residents aged 65+ years: Day-to-day activities not limited"
        ]
        placeholders_before = pd.DataFrame({col: ['']*8 for col in columns})
        header = pd.DataFrame([columns], columns=columns)

        data = {
        "Geography": ["Antrim and Newtownabbey", "Belfast"],
        "Geography code": ["N09000001", "N09000003"],
        "All usual residents": [1000, 1200],
        "All usual residents:Day-to-day activities limited a lot": [100, 120],
        "All usual residents:Day-to-day activities limited a little": [150, 180],
        "All usual residents:Day-to-day activities not limited": [750, 900],
        "Usual residents aged 0-14 years": [200, 250],
        "Usual residents aged 0-14 years:Day-to-day activities limited a lot": [10, 12],
        "Usual residents aged 0-14 years: Day-to-day activities limited a little": [20, 25],
        "Usual residents aged 0-14 years: Day-to-day activities not limited": [170, 213],
        "Usual residents aged 15-39 years": [300, 350],
        "Usual residents aged 15-39 years: Day-to-day activities limited a lot": [20, 25],
        "Usual residents aged 15-39 years: Day-to-day activities limited a little": [30, 35],
        "Usual residents aged 15-39 years: Day-to-day activities not limited": [250, 290],
        "Usual residents aged 40-64 years": [300, 350],
        "Usual residents aged 40-64 years: Day-to-day activities limited a lot": [40, 45],
        "Usual residents aged 40-64 years: Day-to-day activities limited a little": [50, 60],
        "Usual residents aged 40-64 years: Day-to-day activities not limited": [210, 245],
        "Usual residents aged 65+ years": [200, 250],
        "Usual residents aged 65+ years: Day-to-day activities limited a lot": [30, 38],
        "Usual residents aged 65+ years: Day-to-day activities limited a little": [50, 60],
        "Usual residents aged 65+ years: Day-to-day activities not limited": [120, 152]
    }
        data_rows = pd.DataFrame(data)
        placeholders_after = pd.DataFrame({col: ['empty']*14 for col in columns})
        df = pd.concat([placeholders_before, header, data_rows, placeholders_after], ignore_index=True)
        os.makedirs(os.path.dirname(self.test_data_filepath), exist_ok=True)
        df.to_excel(self.test_data_filepath, sheet_name='LGD', index=False, header=False)

        self.expected_df = pd.DataFrame({
            'area_code': ['N09000001', 'N09000001', 'N09000003', 'N09000003'],
            'local_authority': ['Antrim and Newtownabbey', 'Antrim and Newtownabbey', 'Belfast', 'Belfast'],
            'age_group': ['<15 and >=65', '15-64','<15 and >=65', '15-64' ],
            'total_disabled': [110, 140, 135, 165],
            'total_population': [400, 600, 500, 700], 
        })

    def test_convert_disability_age_group_northern_ireland(self):
        result_df = convert_disability_age_group_northern_ireland(self.test_data_filepath, self.config)
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertFalse(result_df.empty)
        pd.testing.assert_frame_equal(result_df, self.expected_df)


if __name__ == '__main__':
    unittest.main()