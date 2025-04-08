import requests
import pandas as pd
import os
import zipfile
from io import BytesIO
import re
import shutil



if __name__ == "__main__":

    DATA_DIR = "output_data"
    CSV_DIR = f"{DATA_DIR}/csv"
    PARQUET_DIR = f"{DATA_DIR}/parquet"
    #create dirs
    import os
    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(PARQUET_DIR, exist_ok=True)


    #data dirs
    url = "https://nrscensusprodumb.blob.core.windows.net/media/zz85kfinmf97whklasd98gfjk_20241003_1200_Topic2G__9575hj6t9375h/Census-2022-Output-Area-v1.zip"
    # Download the zip file
    r = requests.get(url)
    z = zipfile.ZipFile(BytesIO(r.content))
    z.extractall("./tmp")


    # create metadata table
    meta_data_table = pd.DataFrame(
        columns=[
            "Table_Name",
            "Table_ID",
            "Variable_Name",
            "Type",
        ]
    )


    oa_files = os.listdir("./tmp")
    units = []
    for file in oa_files:
        t_tab_loc = file
        t_id = t_tab_loc.split(" - ")[0]
        if t_id == "Uv211b":
            t_id = "UV211b"  # eurgh
        t_name = t_tab_loc.split(" - ",1)[1].split(".")[0] #remove the code, but keep the full name (inc household when applicable)
        # load the csv file raw (not df) and print the first 5 lines
        with open(f"./tmp/{t_tab_loc}", "r") as f:
            # remove any complete empty lines
            lines = [line for line in f if line.strip() != ""]
            # remove any lines that are all commas
            lines = [line for line in lines if not re.match(r"^,+$", line)]
            # third is who the table includes
            table_includes = lines[2].strip()

            #fimnd the unit of measure
            # if table includes had  'people' in it, Unit of measure is Person
            # if table includes had  'households' in it, Unit of measure is Household
            # if table has both, Unit of measure is Person
            unit = "-"
            if "Household Reference Persons " in table_includes:
                unit = "Household Reference Person"
            elif "people" in table_includes or "Persons" in table_includes:
                unit = "Person"
            elif "household" in table_includes and "people" not in table_includes:
                unit = "Household"
            else:
                print(f"Unit of measure not found for {t_id}, table includes: {table_includes}")


            # remove the first 3 lines
            lines = lines[3:]

            # find the header indices, they are any remaining lines that have a blank space before the first comma
            header_indices = [
                i for i, line in enumerate(lines) if line.strip().startswith(",")
            ]

            # load to df
            df = pd.read_csv(
                BytesIO("".join(lines).encode()),
                index_col=0,
                # low_memory=False,
                header=header_indices,
                skipfooter=5,
                engine="python",
                na_values=["-"],
            )

            # remove any rows that don't have an OA of the form S12345678
            # gets rid of the (varying rows of) rubbish at the end of the files
            df = df[df.index.str.match(r"S\d{8}")]

            # append multiidiex columns to single column if necessary
            if df.columns.nlevels > 1:
                df.columns = [": ".join(col).strip() for col in df.columns.values]

            # if any column contains Mar-15 replace it with 3 - 15
            df.columns = df.columns.str.replace("Mar-15", "3 - 15")
            df.index.name = "OA"

            # fill na with 0
            df.fillna(0, inplace=True)

            if len(df) != 46363:
                # skip the table if it doesn't have 46363 rows, this removes tmp/UV608 - National Statistics Socio-economic Classification (NS-SeC) of Household Reference Person (HRP).csv
                # which only has 1 row for some reason
                print(f"Table {t_id} has {len(df)} rows, not 46363")
                continue

                # # validate data and types
            # check if all columns are numeric
            non_numeric = df.map(lambda x: not isinstance(x, (int, float)))
            if non_numeric.any().any():
                print("Non-numeric data found in the following cells:")
                print(df[non_numeric])


            # Create new column names with zero padding
            variable_names = df.columns
            var_ids = [f"{t_id}{str(i).zfill(4)}" for i in range(1, len(variable_names) + 1)]
            df.columns = var_ids
            # save to new csv and parquet
            df.to_csv(f"{CSV_DIR}/{t_id}.csv")
            df.to_parquet(f"{PARQUET_DIR}/{t_id}.parquet")
            # add to metadata table
            meta_data_table = pd.concat(
                [
                    meta_data_table,
                    pd.DataFrame(
                        {
                            "Variable_Name": variable_names,
                            "Variable_ID": var_ids,
                            "Table_ID": [t_id] * len(variable_names),
                            "Table_Name": [t_name] * len(variable_names),
                            "Unit": [unit] * len(variable_names),
                        }
                    ),
                ]
            )

    # Remove the temporary files and directory
    shutil.rmtree("./tmp")
    # save metadata table
    # create full name column
    meta_data_table["Full_Name"] = (
        meta_data_table["Table_Name"] + " - " + meta_data_table["Variable_Name"]
    )
    meta_data_table = meta_data_table[["Variable_Name", "Variable_ID", "Table_ID", "Table_Name", "Type", "Unit", "Full_Name"]]

    #manually set Type to 'Count' for all tables
    meta_data_table['Type'] = 'Count'
    meta_data_table.to_csv(f"{DATA_DIR}/Table_Metadata.csv", index=False)
