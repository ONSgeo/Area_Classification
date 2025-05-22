
# Manually download the data for Scotland tables fromhttps://www.scotlandscensus.gov.uk/search-the-census#/search-by 
# For all Scotland downloaded csvs reformatting is required to remove excess metadata at the top.
# Additionally variable names need to be turned into variables codes which are in the meta data table so that columns align
# UV101b needs ‘all people’ ‘lives in a communal establishment’ – Council Areas need to be moved into a separate column WE NEED TO WRITE CODE FOR THIS.
# UV102b Council Areas need to be moved into a separate column, then create percentages based on the use all people then in the aggregation script the ages are grouped to align with the other census’