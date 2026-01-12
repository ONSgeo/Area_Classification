from pathlib import Path
import pandas as pd
import gptables as gpt

def load_table_file(file_path: Path, sheet_name=None) -> pd.DataFrame:
    '''
    Convert a table from CSV or Excel to pandas dataframe based on file 
    extension. 
    Assumes that all preprocessing of input tables (table_source_file) is 
    completed prior to calling, and that the table data starts in cell A1.
    Parameters
    ----------
    file_path
        The location of the file that the table is located, as a pathlib Path.
    sheet_name
        Optional paremeter: the name of the sheet in the Excel workbook where 
        the table is located. If left blank, any Excel workbook provided will
        revert to default GPTables settings and first worksheet will be selected. 
    Returns
    -------
    Pandas dataframe
    
    Raises
    ------
    ValueError
        If file_path suffix is not .csv, .xlsx, or .xls. 
    '''

    suffix = file_path.suffix.lower()
    if suffix == '.csv':
        return pd.read_csv(file_path)
    elif suffix in {'.xlsx', '.xls'}:
        if sheet_name is not None:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix} for {file_path.name}")


def build_dataset_sheets(datasets) -> dict:
    '''
    Build GPTables 'tables' sheets from config.yaml file. 
    Assumes that all preprocessing of input tables (table_source_file) is 
    completed prior to calling, and that the table data starts in cell A1.
    Parameters
    ----------
    datasets
        The parent variable 'datasets' from config.yaml parsed with .get() Method.
    Returns
    -------
    sheets
        Python dictionary where key is sheet_name (sheet label) and value is the 
        sheet (GPTable), as a variable, ready for inclusion in 
        contentsheet_label argument in GPTables method write_workbook().
        
    Raises
    ------
    ValueError
        If there is no 'datasets' element in config.yaml
        If any table_id is missing in config.yaml
        If any sheet_label is missing in config.yaml
        If any table_title is missing in config.yaml
        If any table_source_file is missing in config.yaml
        If there are duplicate sheet_label values across datasets
        If there are duplicate table_id values across datasets
    
    FileNotFoundError
        If an invalid file path has been entered in config.yaml
    '''

    # check to see if datasets exist in config file 
    if not datasets:
        raise ValueError("No datasets defined in config.")

    # build sheets variables
    sheets = {}
    used_table_names = set()
    used_sheet_labels = set()

    for i, t in enumerate(datasets, start=1):
        # create individual variables 
        table_id = t.get('table_id')
        sheet_label = t.get('sheet_label')
        table_title = t.get('table_title')
        table_instructions = t.get('instructions')
        table_subtitles = t.get('table_subtitle')
        table_source_file = t.get('table_source_file')
        sheet_name = t.get('sheet_name')

        # raise ValueErrors if mandatory info is missing from datasets 
        if not table_id:
            raise ValueError(f"Table {table_title} is missing required field: table_id.")
        elif not sheet_label: 
            raise ValueError(f"Table {table_id} ({table_title}) is missing required field: sheet_label")
        elif not table_title: 
            raise ValueError(f"Table {table_id} is missing required table_title: table_title")
        elif not table_source_file: 
            raise ValueError(f"Table {table_id} ({table_title}) is missing required field: table_source_file")

        # check for duplicates 
        if sheet_label in used_sheet_labels:
            raise ValueError(f"Duplicate sheet_label '{sheet_label}'. Each sheet needs a unique label.")
        if table_id in used_table_names:
            raise ValueError(f"Duplicate table_id '{table_id}'. Each table_id must be unique.")

        # check file path is valid 
        file_path = Path(table_source_file).resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"Table file not found: {file_path}")

        # load table file and convert to pandas dataframe 

        df = load_table_file(file_path, sheet_name)

        # convert df into gptable 
        new_table = gpt.GPTable(
            table = df, # table is the dataframe 
            table_name = table_id, # table_name is the machine readable table name
            title = table_title, # title is the title at the top of the worksheet
            instructions = table_instructions,
            subtitles = table_subtitles # these are the subtitles underneath the title 
        )

        # save iterated info
        sheets[sheet_label] = new_table
        used_sheet_labels
        used_table_names

    return sheets


def build_notes(notes): 
    '''
    Build notes variables from config.yaml file
    Parameters
    ----------
    notes
        The parent variable 'notes' from config.yaml parsed with .get() Method.
    Returns
    -------
    notes_list
        A python list ready to pass to notes variables in GPTables method write_workbook().
    Raises
    ------
    ValueError
        If include_notes is not set to a Boolean value
    
    '''
    # if include_notes is set as False, return None
    if notes.get('include_notes') == False:
        notes = [None, None] 

    # if include_notes is set as True, get notes variables from config.yaml
    elif notes.get('include_notes') == True:
        notes_list = []

        notes_sheet_label = notes.get('sheet_label') 
        notes_list.append(notes_sheet_label)

        notes_table = pd.DataFrame.from_dict(notes.get('notes_table'))
        notes_list.append(notes_table)

    else: 
        raise ValueError("include_notes not set to True or False.")

    return notes_list


def build_cover(cover_info) -> gpt.Cover:
    '''
    Create GPTables cover from config file info. 
    Parameters
    ----------
    cover_info
        The parent variable 'cover' from config.yaml parsed with .get().
    Returns
    -------
    GPTables Cover as a variable ready for inclusion in contentsheet_label 
    argument in GPTables method write_workbook().
    Raises
    ------
    ValueError
        If include_cover is not set to Boolean value
    ''' 

    if cover_info.get('include_cover') == False:
        cover = None

    elif cover_info.get('include_cover') == True: 
        cover = gpt.Cover(
            cover_label = cover_info.get('sheet_label'),
            title = cover_info.get('cover_title'),
            intro=cover_info.get('introductory_information'),
            about=cover_info.get('about_these_data'),
            contact=cover_info.get('contact')
        )

    else:
        raise ValueError("include_cover not set to True or False.")

    return cover


def build_contents(contents):
    ''' 
    Builds contentsheet_label from config.yaml info ready for GPTables method write_workbook(). 
    Parameters
    ----------
    cover_info
        The parent variable 'contents' from config.yaml parsed with .get().
    Returns
    -------
    contentsheet_label as a variable ready for inclusion in contentsheet_label 
    argument in GPTables method write_workbook().
    Raises
    ------
    ValueError
        If include_cover is not set to Boolean value
    ''' 

    # get variables 
    include_contents = contents.get('include_contents') 
    content_sheet_label_name = contents.get('sheet_label') 

    # check if include_contents is True, False not not valid
    contentsheet_label = None
    if include_contents == True:
        contentsheet_label = content_sheet_label_name
    elif include_contents == False: 
        contentsheet_label = None
    else:
        raise ValueError("include_contents not set to True or False.")

    return contentsheet_label


def build_filepath(save_info):
    '''
    Builds a filepath from config.yaml file, ready to be handed to GPTables 
    method write_workbook(). 
    Parameters
    ----------
    save_info
        The parent variable 'save_info' from config.yaml parsed with .get().
    Returns
    -------
    cleaned filepath as a string
    
    '''
    # clean save_location strings
    save_location = save_info.get('save_location')
    save_location = save_location.replace('\\', '/')

    # clean file_save_name strings
    file_save_name = save_info.get('file_save_name') 
    file_save_name = file_save_name.split('.')
    file_save_name = file_save_name[0]

    # form filepath from save_location and file_save_name
    filepath = save_location + '/' + file_save_name + '.xlsx'
    filepath = filepath.replace('//', '/')

    return filepath