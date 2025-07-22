# Post clustering wrapper
#INITAL PLACE HOLDER SCRIPT - NOTE DOES NOT RUN!

def post_processing(post_process_args, extract_columns_args, cluster_means_args):
    """
    Wrapper function to run post_process_cluster_table, 
    extract_matching_and_partial_columns, and get_cluster_means in sequence.

    Args:
        post_process_args (tuple): Arguments for post_process_cluster_table.
        extract_columns_args (tuple): Arguments for extract_matching_and_partial_columns.
        cluster_means_args (tuple): Arguments for get_cluster_means.

    Returns:
        The result of get_cluster_means.
    """
    # Step 1: Run post_process_cluster_table
    post_process_cluster_table(output_folder, file_name, keep_column, split_column)

    # Step 2: Run extract_matching_and_partial_columns
    extract_matching_and_partial_columns(inputs_folder, lookup_file, output_file)

    # Step 3: Run get_cluster_means
    cluster_means_result = get_cluster_means(config)

    # Return the result of get_cluster_means
    return cluster_means_result