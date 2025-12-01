#pip install xlwt
import xlwt
import unittest
import pandas as pd
import os
import shutil
from unittest.mock import patch
import io
from area_classification.post_processing.cluster_summaries import cluster_summaries_wrapper

class TestClusterSummariesWrapperIntegration(unittest.TestCase):
    def setUp(self):
        # Create a mock configuration
        self.config = {
            'input_directory': './tests/data/pop_density/',
            'output_directory': './tests/data/pop_density/',
            'population_estimates_filepath_2021': './tests/data/pop_density/population_density/population_2021.xls',
            'population_estimates_filepath_2022': './tests/data/pop_density/population_density/population_2022.xlsx',
            'sam_2021_filepath': './tests/data/pop_density/population_density/SAM_LAD_DEC_2021_UK.csv',
            'sam_2022_filepath': './tests/data/pop_density/population_density/SAM_LAD_DEC_2022_UK_V2.csv'
        }

        # Create mock data for restructured_cluster_table_long
        self.restructured_cluster_table_long = pd.DataFrame({
            'LAD_name': ['Hartlepool', 'Middlesbrough', 'City of Edinburgh', 'Glasgow City'],            
            'LAD_code': ['E06000001' , 'E06000002', 'S12000036', 'S12000049'],
            'supergroup': ['1', '1', '2', '2'],
            'group': ['1a', '1a', '2b', '2b'],
            'subgroup': ['1a1', '1a2', '2b1', '2b2'],
            'v01': [0.5, 0.6, 0.7, 0.8],
            'v02': [0.1, 0.7, 0.2, 0.3],
            'v12': [0.5, 0.3, 0.9, 0.8]
        })
        self.restructured_cluster_table_long.to_csv('test_restructured_cluster_table_long.csv', index=False)

        # Create mock uk_std_cluster_means DataFrame
        self.uk_std_cluster_means = pd.DataFrame({
            'cluster': [1, '1a', '1a1', '1a1', '1a2', '2', '2b', '2b1', '2b2'],
            'hierarchy_level': ['supergroup', 'group', 'subgroup', 'subgroup', 'subgroup', 'supergroup', 'group', 'subgroup', 'subgroup'],
            'v01': [0.35, 0.2, 0.525, 0.45, 0.60, 0.55, 0.40, 0.625, 0.70],
            'v02': [0.75,  0.15, -0.825, 0.90, 0.10, 0.95, -0.20, 1.025, 1.10],
            'v12': [0.16, 0.08, 0.20, -0.24, 0.32, 0.40, -0.12, 0.48, 0.56],
        })

        # Create a mock lookup file
        os.makedirs('./tests/data/pop_density/population_density/', exist_ok=True)
        self.lookup_file = './tests/data/pop_density/lookup_file.csv'

        pd.DataFrame({
            'variable_name': ['Lives in a communal establishment', 'Never married and never registered a civil partnership', 'Usual residents per square kilometre'],
            'variable_code': ['ts0010003', 'ts0020002', 'ts0060001'],
            'table_ID': ['TS001', 'TS002', 'TS006'],
            'table_name': ['Residency type', 'Legal partnership status', 'Population density' ],
            'country': ['ew', 'ew', 'ew'],
            'new_code': ['v01', 'v02', 'v12'],
            'domain': ['Demography and Migration', 'Demography and Migration', 'Demography and Migration']
        }).to_csv(self.lookup_file, index=False)

        # Make mock popultion density and SAM data files
        pd.DataFrame({
            'LAD21CD': ['E06000001' , 'E06000002', 'S12000036', 'S12000049'],
            'LAD21NM': ['Hartlepool', 'Middlesbrough', 'City of Edinburgh', 'Glasgow City'],
            'AREAEHECT': [116637.77, 77554.08, 116637.77, 77554.08],
            'AREACHECT': [116637.77, 73763.24, 116637.77, 73763.24],
            'AREAIHECT': [0, 587.16, 0, 587.16],
            'AREALHECT': [116637.77, 73176.08, 116637.77, 73176.08]
        }).to_csv(self.config['sam_2021_filepath'], index=False)

        pd.DataFrame({
            'LAD22CD': ['E06000001' , 'E06000002', 'S12000036', 'S12000049'],
            'LAD22NM': ['Hartlepool', 'Middlesbrough', 'City of Edinburgh', 'Glasgow City'],
            'LAD22NMW': ['', '', '', ''],
            'AREAEHECT': [116637.78, 77554.07, 116637.78, 77554.07],
            'AREACHECT': [116637.78, 73763.23, 116637.78, 73763.23],
            'AREAIHECT': [0, 587.16, 0, 587.16],
            'AREALHECT': [116637.78, 73176.07, 116637.78, 73176.07]
        }).to_csv(self.config['sam_2022_filepath'], index=False)       

        os.makedirs(os.path.dirname(self.config['population_estimates_filepath_2021']), exist_ok=True)
        # This version of pandas doesn't support xls to to create a mock xls, need to creat a CSV then convert
        pop_2021_df = pd.DataFrame({
            'Code': ['empty', 'empty','empty','empty','empty','empty','empty','Code','E06000001', 'E06000002','S12000036', 'S12000049'],
            'Name': ['empty', 'empty','empty','empty','empty','empty','empty','Name','Hartlepool', 'Middlesbrough','City of Edinburgh', 'Glasgow City'],
            'Geography': ['empty', 'empty','empty','empty','empty','empty','empty','Geography','Unitary Authority', 'Unitary Authority', 'Council Area', 'Council Area'],
            'All ages': ['empty', 'empty','empty','empty','empty','empty','empty','All ages', 110000, 150000, 630050, 520010]
            })
        
        pop_estimates_CSV_2021 = os.path.join(self.config['input_directory'], 'pop_estimates_CSV_2021.xls')
        pop_2021_df.to_csv(pop_estimates_CSV_2021, index=False)

        # Read in the CSV to convert
        df = pd.read_csv(pop_estimates_CSV_2021)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('MYE2 - Persons')

        # Write header
        for col_idx, col_name in enumerate(df.columns):
            ws.write(0, col_idx, col_name)

        # Write data
        for row_idx, row in enumerate(df.values, start=1):
            for col_idx, value in enumerate(row):
                ws.write(row_idx, col_idx, value)

        wb.save(os.path.join(self.config['population_estimates_filepath_2021']))

        os.makedirs(os.path.dirname(self.config['population_estimates_filepath_2022']), exist_ok=True)
        pop_2022_df = pd.DataFrame({
            'Code': ['empty', 'empty','empty','empty','empty','empty','empty','Code','E06000001', 'E06000002','S12000036', 'S12000049'],
            'Name': ['empty', 'empty','empty','empty','empty','empty','empty','Name','Hartlepool', 'Middlesbrough', 'City of Edinburgh', 'Glasgow City'],
            'Geography': ['empty', 'empty','empty','empty','empty','empty','empty','Geography','Unitary Authority', 'Unitary Authority', 'Council Area', 'Council Area'],
            'All ages': ['empty', 'empty','empty','empty','empty','empty','empty','All ages', 110050, 150005, 630000, 520000]
        })
        with pd.ExcelWriter(self.config['population_estimates_filepath_2022'], engine='openpyxl') as writer:
            pop_2022_df.to_excel(writer, sheet_name='MYE2 - Persons', index=False)

        
    def test_cluster_summaries_wrapper(self):
        # Expected output strings
        # When checking variance, remember sample var used.
        expected_output = (
            "Cluster 1\n"
            "Cluster 1 contains 2 local authorities which is 50.00% of UK local authorities, this included 18.44% of the UK population (values are taken for 2021 for EW and NI, but 2022 for Scot, due to times of the census). This cluster has a population density of 1.37 people per hectare.\n"
            "The average variance for cluster 1 is 0.07. Example areas: Middlesbrough, Hartlepool\n"
            "Values in the brackets below are the difference between the mean of the variable for this cluster\n"
            "        compared with the mean of the other clusters combined. The population of cluster 1 has a:\n"
            "• lower (-0.45) Usual residents per square kilometre. Variance:0.02 (Demography and Migration domain)\n"
            "• lower (-0.20) proportion of people who live in a communal establishment. Variance:0.005 (Demography and Migration domain)\n"
            "• higher (0.15) proportion of people who are Never married and never registered a civil partnership. Variance:0.18 (Demography and Migration domain)\n" 
            "----------------------------------------\n"
            "Cluster 2\n"
            "Cluster 2 contains 2 local authorities which is 50.00% of UK local authorities, this included 81.56% of the UK population (values are taken for 2021 for EW and NI, but 2022 for Scot, due to times of the census). This cluster has a population density of 6.06 people per hectare.\n"
            "The average variance for cluster 2 is 0.005. Example areas: Glasgow City, City of Edinburgh\n"
            "Values in the brackets below are the difference between the mean of the variable for this cluster\n"
            "        compared with the mean of the other clusters combined. The population of cluster 2 has a:\n"
            "• higher (0.45) Usual residents per square kilometre. Variance:0.005 (Demography and Migration domain)\n"
            "• higher (0.20) proportion of people who live in a communal establishment. Variance:0.005 (Demography and Migration domain)\n"
            "• lower (-0.15) proportion of people who are Never married and never registered a civil partnership. Variance:0.005 (Demography and Migration domain)\n"
            
            "----------------------------------------\n"
        )    

        for col, dtype in self.restructured_cluster_table_long.dtypes.items():
            print(f"{col}: {dtype}") 

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
    #         print("Running cluster_summaries_wrapper...")
            cluster_summaries_wrapper(
                config=self.config, 
                restructured_cluster_table_long=self.restructured_cluster_table_long,
                uk_std_cluster_means=self.uk_std_cluster_means,
                lookup_file=self.lookup_file,
                cluster_column='supergroup'
            )
        #         print("Checking outputs...")
        print("expected output:", expected_output)
        print("actual output:", fake_out.getvalue())
        self.assertIn(expected_output, fake_out.getvalue())



        # print("Cleaning up test files...")
        # # Clean up - remove created files and folders
        # for filename in os.listdir(self.config['input_directory']):
        #     file_path = os.path.join(self.config['input_directory'], filename)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        #     elif os.path.isdir(file_path):
        #         shutil.rmtree(file_path)
        #         shutil.rmtree(self.config['input_directory'])

        # print("Integration test completed.")

if __name__ == '__main__':
    unittest.main()