# Manually download the data for Scotland tables from https://www.scotlandscensus.gov.uk/search-the-census#/search-by 
# For all Scotland downloaded csvs reformatting is required to remove excess metadata at the top.
# Additionally variable names need to be turned into variables codes which are in the metadata table so that columns align
# UV101b needs ‘all people’ ‘lives in a communal establishment’ – Council Areas need to be moved into a separate column.
# UV103 needs additional formatting, then in the aggregation script, the ages need to be grouped to align with the other census’.
