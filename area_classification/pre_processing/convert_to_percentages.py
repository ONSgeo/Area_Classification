def convert_to_percentages(raw_totals_df):
    """
    Converts raw totals DataFrame to percentages by dividing variable columns
    by their corresponding '_total' columns and multiplying by 100.

    Parameters
    ----------
    raw_totals_df : pd.DataFrame
        Input DataFrame with area codes as the first column followed by columns like
        'v01', 'v01_total'. Values are raw counts.

    Returns
    -------
    pd.DataFrame
        DataFrame with area codes in the first column followed by percentage values for
        each variable from v1 to v60 (excluding '_total' columns).
    """

    # Create a copy of the DataFrame to store percentages
    percentages_df = raw_totals_df.copy()

    # Iterate over columns to calculate percentages
    for col in raw_totals_df.columns:
        if col.endswith("_total"):
            # Get the base column name (e.g., 'v01' from 'v01_total')
            base_col = col.replace("_total", "")

            if base_col in raw_totals_df.columns:
                # Calculate percentage and update the base column
                percentages_df[base_col] = (raw_totals_df[base_col] / raw_totals_df[col]) * 100

    # Drop all '_total' columns
    percentages_df = percentages_df[
        [col for col in percentages_df.columns if not col.endswith("_total")]
    ]

    return percentages_df
