# Background / introduction / about
Work in development

Area Classification
“The 2021 Classification for Output Areas (2021 OAC) is a hierarchical geodemographic classification across the UK which identifies areas of the country with similar characteristics.” Consumer data research centre (CDRC)​
Current focus
* 2021 ​
* Supergroups​
* Local Authority District​
    * England and Wales (NOMIS) ​
        * 2022 local authorities: district / unitary​
    * Northern Ireland (NISRA) ​
        * Local Government District 2014​
    * Scotland ​
        * Local authority (CA2019)​

## Description of files
A table that describes each of the files in the repo (like we did for the automated mapping repo)

## Data
Description of the input datasets

## Methodology / process description
## Output
## Limitations
## Future scope
## Contacts / authors / acknowledgements
ogoodwin505 Owen Goodwin
ONS Data Science Office


# Previous README:
# Geodemographic Python Example  

This repository contains the workflow for producing a geodemographic classification in Python using k-means clustering. It follows a simplified process, similar to that described in the [2021 OAC Paper](https://rgs-ibg.onlinelibrary.wiley.com/doi/full/10.1111/geoj.12550).  

## Files  
- **Main notebook:** `1_geodemographic_example.ipynb`  
- **Requirements:** Dependencies are listed in `requirements.txt`  
- **Example data:** `example_oacdata.csv`  

## Setup (dependencies)
The dependencies can be installed from inside the notebook.

Alternatively;
### Using `pip` and a virtual environment  
Create and activate a virtual environment:  
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
pip install -r requirements.txt
```

