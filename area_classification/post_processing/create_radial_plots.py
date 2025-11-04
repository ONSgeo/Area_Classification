# Creation of radial plots
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means):  
    """
    Wrapper function to create radial plots for UK clusters and parent clusters.

    Radial plots for parent clusters represent difference from parent cluster standardized means.
    Radial plots for the area classification clusters to represent difference from UK standardized means.

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

    # Create radial plots for supergroups, groups and subgroups against UK
    create_radial_plots(config, uk_std_cluster_means, level="UK")
    
    # Create radial plots for groups against their parent (groups)
    create_radial_plots(config, combined_group_means, level="group")

    # Create radial plots for subgroups against their parent (groups)
    create_radial_plots(config, combined_subgroup_means, level="subgroup")


def create_radial_plots(config, dataframe, level):
    """
    Helper function to create radial plots for a given dataframe.

    Parameters
    ----------
    dataframe : DataFrame
        The input DataFrame (either combined_group_means or combined_subgroup_means).
    level : str
        Either 'group' or 'subgroup' to indicate the type of data.
    """
    # Create a dictionary from the lookup DataFrame
    lookup_dict = pd.read_csv(config['select_variables_lookup']).set_index("new_code")["variable_name"].to_dict()

    # Create the 'radial_plots' directory
    radial_plots_dir_parent = os.path.join(config["radial_plot_directory"], "parent_cluster_radial_plots")
    os.makedirs(radial_plots_dir_parent, exist_ok=True)
    # Create the 'radial_plots' directory
    radial_plots_dir_UK = os.path.join(config["radial_plot_directory"], "uk_radial_plots")
    os.makedirs(radial_plots_dir_UK, exist_ok=True)

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
        fig, ax = plt.subplots(figsize=(10, 18), subplot_kw=dict(polar=True))

        # Adjust the margins of the plot to create extra space
        fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

        # Remove default polar axis labels (e.g., 90°, 270°)
        ax.set_xticks([])  # Remove angular ticks
        ax.set_yticks([])  # Remove radial ticks

        # Set the radial limits to ensure the same scale for all plots
        ax.set_ylim(-3, 3.2)

        # Replace feature_columns with their corresponding variable_name and domain
        replaced_labels = [lookup_dict.get(col, col) for col in feature_columns]
        domains = pd.read_csv(config['select_variables_lookup']).set_index("new_code")["domain"].to_dict()

        # Assign colors to each domain
        domain_colors = {
            "Demography and Migration": "blue",
            "Ethnicity, Identity, Language and Religion": "green",
            "Health, Disability and Unpaid Care": "orange",
            "Housing": "purple",
            "Labour Market": "red",
            "Education": "cyan"
        }

        # Add grey lines from the center to each axis label
        for angle in angles[:-1]:  # Exclude the repeated angle
            ax.plot([angle, angle], [-3, 3], color='grey', linewidth=0.8, linestyle='dotted')

        # Add tick marks going through the outer line
        ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])  # Define tick positions
        ax.yaxis.set_tick_params(width=0.8, color='grey', size=5)  # Customize tick marks

        # Adjust the transparency of the rings (gridlines)
        ax.grid(color='grey', linestyle='solid', linewidth=0.8, alpha=0.4)

        # Color the segments closest to the outer line based on the domain
        for i, col in enumerate(feature_columns):
            domain = domains.get(col, "other")
            color = domain_colors.get(domain, "gray")
            angle_start = angles[i]
            angle_end = angles[i + 1]

            # Define the polygon for the segment
            segment_angles = [angle_start, angle_end, angle_end, angle_start]
            segment_radii = [3, 3, 2.8, 2.8]  # Outer and inner radii of the segment

            # Fill the segment with the corresponding color
            ax.fill(segment_angles, segment_radii, color=color, alpha=0.4)

        # Add labels for each feature
        for i, col in enumerate(feature_columns):
            angle = angles[i]
            label = replaced_labels[i]

            # Set the radius for the labels to be outside the radial limit (e.g., 3.8)
            label_radius = 3.5  # Adjust this value as needed to position labels outside the limit

            # Adjust alignment based on the angle
            if 0 <= angle < np.pi / 2 or 3 * np.pi / 2 <= angle < 2 * np.pi:
                ha = 'left'
            else:
                ha = 'right'

            ax.text(
                angle, label_radius,  # Place labels outside the radial limit
                label,  # Label text
                fontsize=11,
                color="black",  # Keep labels black
                ha=ha,
                va='center'
            )

        # Append the first angle to the end to close the circle
        #angles = angles + angles[:1]

        # Draw a solid red ring at the radius of 0
        #ax.plot(angles, [0] * len(angles), color='red', linewidth=1.0, linestyle='solid', label='Zero Line')

        ax.plot(angles[:-1], [0] * len(angles[:-1]), color='red', linewidth=1.0, linestyle='solid', label='Zero Line')

        # Save the plot with the filename as '<group/subgroup>_group/subgroup.png'
        if level in ["group", "subgroup"]:
            ax.plot(angles, values, linewidth=1.5, linestyle='solid', label=f'{row[level]}_{level}')
            # Add a title
            ax.set_title(f"Radial plot (parent): {row[level]}_{level}", size=14, pad=40, weight='bold')
            plot_filename = f"{row[level]}_{level}.png"
            plot_path = os.path.join(radial_plots_dir_parent, plot_filename)
        elif level == "UK":
            # Draw the outline of the radar chart
            ax.plot(angles, values, linewidth=1.5, linestyle='solid', label=f'{row["cluster"]}_{row["hierarchy_level"]}')
            # Add a title
            ax.set_title(f"Radial plot (UK): {row['cluster']}_{row['hierarchy_level']}", size=14, pad=40, weight='bold')
            plot_filename = f"{row['cluster']}_{row['hierarchy_level']}.png"
            plot_path = os.path.join(radial_plots_dir_UK, plot_filename)
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close(fig)

    if level == "UK":
        print(f"UK radial plots saved in: {radial_plots_dir_UK}")
    elif level in ["group", "subgroup"]:
        print(f"Parent cluster radial plots saved in: {radial_plots_dir_parent}")

if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    uk_std_cluster_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "uk_std_means", "uk_std_cluster_means_output.csv"))
    combined_group_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "parent_std_means","parent_std_cluster_group_means_output.csv"))
    combined_subgroup_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "parent_std_means","parent_std_cluster_subgroup_means_output.csv"))
    create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means)