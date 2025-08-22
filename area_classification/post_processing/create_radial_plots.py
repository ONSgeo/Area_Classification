# THIS CURRENTLY WORKS FOR SUPERGROUPS ONLY

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means):  
    """
    Wrapper function to create radial plots for UK clusters and parent clusters.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing settings for the plotting.
    uk_std_cluster_means : DataFrame
        DataFrame containing standardized cluster means for the UK.
    combined_group_means : DataFrame
        DataFrame containing group-level means.
    combined_subgroup_means : DataFrame
        DataFrame containing subgroup-level means.
    """
    #lookup = pd.read_csv(config['select_variables_lookup'])
    create_radial_plots_uk(config, uk_std_cluster_means)
    create_radial_plots_parent_clusters(config, combined_group_means, combined_subgroup_means)
    


def create_radial_plots_parent_clusters(config, combined_group_means, combined_subgroup_means):
    """
    Create radial plots for the area classification clusters to represent difference from parent cluster standardized means.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing settings for the plotting.
    combined_group_means : DataFrame
        DataFrame containing group-level means.
    combined_subgroup_means : DataFrame
        DataFrame containing subgroup-level means.
    """

    # Create the 'radial_plots' directory
    radial_plots_dir = os.path.join(config["output_directory"], "radial_plots", "parent_cluster_radial_plots")
    os.makedirs(radial_plots_dir, exist_ok=True)


    def create_radial_plots(dataframe, level):
        """
        Helper function to create radial plots for a given dataframe.

        Parameters
        ----------
        dataframe : DataFrame
            The input DataFrame (either combined_group_means or combined_subgroup_means).
        level : str
            Either 'group' or 'subgroup' to indicate the type of data.
        """
        # Get the feature columns (assuming they start from 'v01' to 'v59')
        feature_columns = [col for col in dataframe if col.startswith("v")]
        #feature_columns = feature_columns.map(lookup.set_index('variable')['variable_name'])

        # Create a radial plot for each row in the input dataframe
        for idx, row in dataframe.iterrows():
            # Extract the feature values for the current row
            values = row[feature_columns].tolist()
            values += values[:1]  # Repeat the first value to close the circle

            # Angles for the radar chart
            num_vars = len(feature_columns)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1]  # Repeat the first angle to close the circle

            # Initialize the radar chart
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

            # # Set the starting angle to the top
            # ax.set_theta_zero_location("N")  # "N" stands for North (top)
            # ax.set_theta_direction(-1)  # Clockwise direction

            # Draw the outline of the radar chart
            ax.plot(angles, values, linewidth=1.5, linestyle='solid', label=f'{row[level]}_{level}')

            # Add labels for each feature
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(feature_columns)

            # Add a title
            ax.set_title(f"Radial Plot for {row[level]}_{level}", size=14, pad=20)

            # Draw a solid red ring at the radius of 0
            ax.plot(angles[:-1], [0] * len(angles[:-1]), color='red', linewidth=1.5, linestyle='solid', label='Zero Line')

            # Save the plot with the filename as '<group/subgroup>_group/subgroup.png'
            plot_filename = f"{row[level]}_{level}.png"
            plot_path = os.path.join(radial_plots_dir, plot_filename)
            plt.savefig(plot_path, bbox_inches='tight')
            plt.close(fig)

    # Create radial plots for groups
    create_radial_plots(combined_group_means, level="group")

    # Create radial plots for subgroups
    create_radial_plots(combined_subgroup_means, level="subgroup")

    print(f"Parent cluster radial plots saved in: {radial_plots_dir}")




def create_radial_plots_uk(config, uk_std_cluster_means):
    """
    Create radial plots for the area classification clusters to represent difference from UK standardized means

    Parameters
    ----------
    config : dict
        Configuration dictionary containing settings for the plotting.
    uk_std_cluster_means : DataFrame
        DataFrame containing standardized cluster means for the UK.
    """

    # Create the 'radial_plots' directory
    radial_plots_dir = os.path.join(config["output_directory"], "radial_plots", "uk_radial_plots")
    os.makedirs(radial_plots_dir, exist_ok=True)

    # Get the feature columns (assuming they start from 'v01' - 'v59')
    feature_columns = [col for col in uk_std_cluster_means.columns if col.startswith("v")]
    #feature_columns = feature_columns.map(lookup.set_index('variable')['variable_name'])

    # Create a radial plot for each row (area_code) in the input dataframe
    for idx, row in uk_std_cluster_means.iterrows():
        # Extract the feature values for the current row
        values = row[feature_columns].tolist()
        values += values[:1]  # Repeat the first value to close the circle

        # Angles for the radar chart
        num_vars = len(feature_columns)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Repeat the first angle to close the circle

        # Initialize the radar chart
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Set the starting angle to the top
        # ax.set_theta_zero_location("N")  # "N" stands for North (top)
        # ax.set_theta_direction(-1)  # Clockwise direction
        
        # Draw the outline of the radar chart
        ax.plot(angles, values, linewidth=1.5, linestyle='solid', label=f'{row["cluster"]}_{row["hierarchy_level"]}')

        # Add labels for each feature
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(feature_columns)

        # Add a title
        ax.set_title(f"Radial Plot for {row['cluster']}_{row['hierarchy_level']}", size=14, pad=20)

        # Draw a solid red ring at the radius of 0
        ax.plot(angles[:-1], [0] * len(angles[:-1]), color='red', linewidth=1.5, linestyle='solid', label='Zero Line')

        # Save the plot with the filename as '<cluster>_<hierarchy_level>.png'
        plot_filename = f"{row['cluster']}_{row['hierarchy_level']}.png"
        plot_path = os.path.join(radial_plots_dir, plot_filename)
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close(fig)

    print(f"UK radial plots saved in: {radial_plots_dir}")


if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    uk_std_cluster_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "uk_std_means", "uk_std_cluster_means_output.csv"))
    combined_group_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "group_means.csv"))
    combined_subgroup_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "subgroup_means.csv"))
    create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_group_means)