#cluster_populations_ reforamtting - built on Lucy's work

#These may need using if we use population data from seperate tables

def format_ew_populations(config):
    """
    Reads the 'england_wales_2021_populations.csv' file from the specified folder.
    Formats the csv to include only the relevant columns and renames them.

    Parameters
    ----------
    folder_path : str
        Path to the folder containing the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the CSV data.
    """
    file_path = os.path.join(config["input_data_directory"], 'england_wales_2021_populations.csv')
    df_ew = pd.read_csv(file_path, skiprows=6)

    # Format the table to include column headers
    df_ew.columns = ['LAD_name', 'LAD_code', 'Population']
    
    # Remove unnecessary rows from the bottom of the file
    df_ew = df_ew.iloc[:374]

    #print(df_ew)

    return df_ew

def format_scot_populations(config):
    """
    Reads only the 'Table 1' sheet in the 'scotland_census_2022_populations.xlsx' file from the specified folder.
    Formats the table to include only the relevant columns and renames them.

    Parameters
    ----------
    folder_path : str
        Path to the folder containing the excel file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the excel data from the 'Table 1' sheet. 
    """
    file_path = os.path.join(config["input_data_directory"], 'scotland_census_2022_populations.xlsx')
    df_scot = pd.read_excel(file_path, sheet_name='Table 1', skiprows=5, header = None)

    #Remove unnecessary columns C, E & F
    df_scot = df_scot.drop(df_scot.columns[[2, 4, 5]], axis=1)

    # Format the table to include column headers
    df_scot.columns = ['LAD_name', 'LAD_code', 'Population']
    
    #print(df_scot)

    return df_scot

def format_ni_populations(config):
    """
    Reads only the 'Usual residents' sheet in the 'ni_census_2021_data.xlsx' file from the specified folder.
    Formats the table to include only the relevant columns and renames them.

    Parameters
    ----------
    folder_path : str
        Path to the folder containing the excel file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the excel data from the 'Usual residents' sheet. 
    """
    
    file_path = os.path.join(config["input_data_directory"], 'ni_census_2021_data.xlsx')
    df_ni = pd.read_excel(file_path, sheet_name='Usual residents', skiprows=5, header = None)

    #Remove unnecessary columns C, D, E & F
    df_ni = df_ni.drop(df_ni.columns[[2, 3, 4, 5]], axis=1)

    #Rearrange order of columns (to be consistent with Scotland and England/Wales)
    df_ni = df_ni[[1, 0, 6]]

    # Format the table to include column headers
    df_ni.columns = ['LAD_name', 'LAD_code', 'Population']

    # Remove unnecessary rows 
    df_ni = df_ni.iloc[:11]

    #print(df_ni)

    return df_ni

def concat_populations(df_ew, df_scot, df_ni, config):

    # Concatenate the three DataFrames into one table
    df_populations = pd.concat([df_ew, df_scot, df_ni], ignore_index=True)
    print(df_populations)

    # Save the concatenated DataFrame to a new CSV file (optional)
    #df_populations.to_csv(os.path.join(folder_path, 'all_populations.csv'), index=False)

    return df_populations

if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config()
    # folder_path = "./data/Population_estimates"
    # df_ew = format_ew_populations(config)
    # df_scot = format_scot_populations(config)
    # df_ni = format_ni_populations(config)
    # concat_populations(df_ew, df_scot, df_ni, config)

    