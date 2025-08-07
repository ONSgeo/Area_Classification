def combine_table(table1, table2, table3):
    """
    Combines three tables into one by stacking them under each other.
    
    Parameters
    ----------
        table1 : list of lists
            The first table.
        table2 : list of lists
            The second table.
        table3 : list of lists
            The third table.
 
    Returns
    -------
    list of lists
        A single table with all rows from the three tables combined.
    """
    combined_table = table1 + table2 + table3
    return combined_table
 
# # Example usage
# table1 = [
#     [1, 2, 3],
#     [4, 5, 6]
# ]
 
# table2 = [
#     [7, 8, 9],
#     [10, 11, 12]
# ]
 
# table3 = [
#     [13, 14, 15],
#     [16, 17, 18]
# ]
 
# result = combine_table(table1, table2, table3)
# for row in result:
#     print(row)
 
if __name__ == "__main__":
    # Example usage
    table1 = [
    table2 = [
    table3 = []
    
    combine_table(table1, table2, table3)