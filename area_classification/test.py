import pandas as pd

csv1 = './data/output_data/cluster_assignments/restructured_subclustering_output.csv'
csv2 = './data/output_data/cluster_assignments/restructured_subclustering_output-2025OUTPUT.csv'


df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

# Sort columns for consistent comparison
df1_sorted = df1.sort_values(list(df1.columns)).reset_index(drop=True)
df2_sorted = df2.sort_values(list(df2.columns)).reset_index(drop=True)

if df1_sorted.equals(df2_sorted):
    print("The CSV files have the same contents.")
else:
    print("The CSV files are different.")

    # Find differing rows
    diff1 = pd.concat([df1_sorted, df2_sorted]).drop_duplicates(keep=False)
    diff2 = pd.concat([df2_sorted, df1_sorted]).drop_duplicates(keep=False)

    print("\nRows unique to the first file (before removal):")
    print(diff1)
    print("\nRows unique to the second file (before removal):")
    print(diff2)

    # Remove leading 0 or 6 from specified columns
    for col in ['supergroup', 'group', 'subgroup']:
        if col in diff1.columns:
            diff1[col] = diff1[col].astype(str).str.replace(r'^[06]', '', regex=True)
        if col in diff2.columns:
            diff2[col] = diff2[col].astype(str).str.replace(r'^[06]', '', regex=True)

    # Sort and reset index again for comparison
    diff1_sorted = diff1.sort_values(list(diff1.columns)).reset_index(drop=True)
    diff2_sorted = diff2.sort_values(list(diff2.columns)).reset_index(drop=True)

    print("\nRows unique to the first file (after removal):")
    print(diff1_sorted)
    print("\nRows unique to the second file (after removal):")
    print(diff2_sorted)

    if diff1_sorted.equals(diff2_sorted):
        print("\nAfter removing leading 0 or 6, the differing rows are now the same.")
    else:
        print("\nAfter removing leading 0 or 6, the differing rows are still different.")