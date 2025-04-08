# Scotland Census 2022 Output Areas
This repository contains code to download and clean all Data Zone level data for the Scottish 2022 Census

The python code:

* Downloads the bulk data from the [Scotland Census](https://www.scotlandscensus.gov.uk/documents/2022-output-area-data/)
* Processes and cleans the tables
* Create new variable names based on the sequential ordering of the variables and the table identification code
* Create a metadata lookup table providing the link between the new names and the original names
* Export the data zone data as both CSV and Parquet files

The created CSV are available in the folder ["/output_data/csv"](/output_data/csv) and the parquet files in the folder ["/output_data/parquet"](/output_data/parquet)