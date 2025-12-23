# Creation of radial plots

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means):  
    """
    Wrapper function to create radial plots for UK clusters and parent clusters.

    Radial plots for parent clusters represent difference from parent cluster standardised means.
    Radial plots for the area classification clusters to represent difference from UK standardised means.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing settings for the plotting.
    uk_std_cluster_means : DataFrame
        DataFrame containing standardised cluster means for the UK.
    combined_group_means : DataFrame
        DataFrame containing group-level means.
    combined_subgroup_means : DataFrame
        DataFrame containing subgroup-level means.
    """

    # Create radial plots for supergroups, groups and subgroups against UK
    create_radial_plots(config, uk_std_cluster_means, level="UK", domain_colours = config['domain_colours'])
    
    # Create radial plots for groups against their parent (groups)
    create_radial_plots(config, combined_group_means, level="group", domain_colours = config['domain_colours'])

    # Create radial plots for subgroups against their parent (groups)
    create_radial_plots(config, combined_subgroup_means, level="subgroup", domain_colours = config['domain_colours'])

    # Create legends
    legend_creation (config['domain_colours'])


def create_radial_plots(config, dataframe, level, domain_colours):
    """
    Helper function to create radial plots for a given dataframe.

    Parameters
    ----------
    dataframe : DataFrame
        The input DataFrame (either combined_group_means or combined_subgroup_means).
    level : str
        Either 'group' or 'subgroup' to indicate the type of data.
    config : dict
        Configuration dictionary containing settings for the plotting.    
    """
    # Load lookup for variable labels and domains
    lookup = pd.read_csv(config['select_variables_lookup'])
    label_dict = lookup.set_index('new_code')['radial_plot_label'].to_dict()
    domain_dict = lookup.set_index('new_code')['domain'].to_dict()

    # Output directories
    parent_dir = os.path.join(config["radial_plot_directory"], "parent_cluster_radial_plots")
    uk_dir = os.path.join(config["radial_plot_directory"], "uk_radial_plots")
    os.makedirs(parent_dir, exist_ok=True)
    os.makedirs(uk_dir, exist_ok=True)

    # Feature columns (e.g., v01, v02, ...)
    feature_cols = [col for col in dataframe if col.startswith("v")]

    for _, row in dataframe.iterrows():
        # Data for this cluster
        values = row[feature_cols].tolist() + [row[feature_cols[0]]]
        num_vars = len(feature_cols)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist() + [0]
        # Set up the polar plot
        fig, ax = plt.subplots(figsize=(26, 16), subplot_kw=dict(polar=True))
        fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylim(-3, 4.3)
        # Make the outer polar axis border (spine) transparent 
        ax.spines['polar'].set_visible(False)

        # Draw colored domain segments
        for i, col in enumerate(feature_cols):
            domain = domain_dict.get(col, "Other")
            color = domain_colours.get(domain, "black")
            ax.fill([
                angles[i], angles[i+1], angles[i+1], angles[i]
            # Set where the colored segments start (3.25) and end (3.5) on the y-axis
            ], [3.35, 3.35, 3.6, 3.6], color=color) 

        # Draw grid and radial lines
        for angle in angles[:-1]:
            ax.plot([angle, angle], [-3, 3], color='grey', linewidth=0.8, linestyle='solid')
        # set the scale for y axis
        ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
        ax.yaxis.set_tick_params(width=1.0, color='grey', size=5, labelsize=16)
        ax.grid(color='grey', linestyle='solid', linewidth=1.0, alpha=0.4)

        # User-defined radii for top 6 and bottom 6 labels (edit these as needed)
        top_label_radii = [4.6, 4.6, 4.4, 4.4, 4.2, 4.2]  # Closest to top (angle=0), then next, etc.
        top_tick_ends =  [r - 0.25 for r in top_label_radii] # [5.0, 5.0, 4.5, 4.5, 4.0, 4.0]
        bottom_label_radii = [4.6, 4.6, 4.4, 4.4, 4.2, 4.2]  # Closest to bottom (angle=pi), then next, etc.
        bottom_tick_ends = [r - 0.25 for r in bottom_label_radii] # [5.0, 5.0, 4.5, 4.5, 4.0, 4.0]
        default_label_radius = 4.0
        default_tick_end = 3.8

        angle_label_indices = list(enumerate(angles[:-1]))  # Exclude the closing angle
        # Top 6: closest to π/2 (90°)
        top_indices_sorted = sorted(angle_label_indices, key=lambda x: abs(x[1] - (np.pi / 2)))[:6]
        top_indices = set(idx for idx, _ in top_indices_sorted)
        # Bottom 6: closest to 3π/2 (270°), but exclude any already in top_indices
        bottom_candidates = [item for item in angle_label_indices if item[0] not in top_indices]
        bottom_indices_sorted = sorted(bottom_candidates, key=lambda x: abs(x[1] - (3 * np.pi / 2)))[:6]

        # Build maps for radii/tick_end
        top_map = {idx: (r, t) for (idx, _), r, t in zip(top_indices_sorted, top_label_radii, top_tick_ends)}
        bottom_map = {idx: (r, t) for (idx, _), r, t in zip(bottom_indices_sorted, bottom_label_radii, bottom_tick_ends)}

        for i, col in enumerate(feature_cols):
            angle = angles[i]
            label = label_dict.get(col, col)
            if i in top_map:
                label_radius, tick_end = top_map[i]
            elif i in bottom_map:
                label_radius, tick_end = bottom_map[i]
            else:
                label_radius = default_label_radius
                tick_end = default_tick_end
            tick_start = 3.35

            ax.plot([angle, angle], [tick_start, tick_end], color='black', linewidth=2.0, zorder=10)
            ha = 'left' if 0 <= angle < np.pi / 2 or 3 * np.pi / 2 <= angle < 2 * np.pi else 'right'
            ax.text(angle, label_radius, label, fontsize=18, color="black", ha=ha, va='center', zorder=11)

        # Draw line at y=0
        #ax.plot(angles, [0] * len(angles), color='red', linewidth=1.0, linestyle='solid', label='Zero Line')

        # Plot the data line and set title/filename
        # colour of the plotted line is blue for groups, green for subgroups and black for UK
        if level == "group":
            ax.plot(angles, [0] * len(angles), color='black', linewidth=1.0, linestyle='solid', label='Zero Line')
            ax.plot(angles, values, color='blue', linewidth=1.5, linestyle='solid') 
            ax.set_title(f"{row[level]} {level} (supergroup mean)", size=26, pad=80, weight='bold')
            plot_path = os.path.join(parent_dir, f"{row[level]}_{level}.png")
        elif level == "subgroup":
            ax.plot(angles, [0] * len(angles), color='blue', linewidth=1.0, linestyle='solid', label='Zero Line')           
            ax.plot(angles, values, color='green', linewidth=1.5, linestyle='solid')
            ax.set_title(f"{row[level]} {level} (group mean)", size=26, pad=80, weight='bold')
            plot_path = os.path.join(parent_dir, f"{row[level]}_{level}.png")
        elif level == "UK":
            ax.plot(angles, [0] * len(angles), color='red', linewidth=1.0, linestyle='solid', label='Zero Line')            
            ax.plot(angles, values, color='black', linewidth=1.5, linestyle='solid')
            ax.set_title(f"{row['cluster']} {row['hierarchy_level']} (UK mean)", size=26, pad=80, weight='bold')
            plot_path = os.path.join(uk_dir, f"{row['cluster']}_{row['hierarchy_level']}.png")

        plt.savefig(plot_path)
        plt.close(fig)

    if level == "UK":
        print(f"UK radial plots saved in: {uk_dir}")
    elif level in ["group", "subgroup"]:
        print(f"Parent cluster radial plots saved in: {parent_dir}")

def legend_creation (domain_colours):
    """
    Function to great pngs of the legend for both the radial plot domains and the lines on the
    radial plots.

    Parameters
    ----------
    domain_colours : Dictionary
        The list of colours used for the domains.    
    """
    # Create the domain legend
    fig, ax = plt.subplots(figsize=(1, 3))
    ax.axis('off')
    y = 0.1
    for domain, color in domain_colours.items():
        ax.scatter(0.013, y, s=300, color=color, marker='s')
        ax.text(0.0134, y, domain, va='center', fontsize=14)
        y -= 0.13
    domain_colour_filepath = os.path.join(config["radial_plot_directory"], "Domain key.png")
    plt.savefig(domain_colour_filepath, bbox_inches='tight', dpi=150)
    plt.close(fig)

    #Create the line legend
    # Define the line types and their colours
    line_info = [
        ("UK mean", "#FA0000"),
        ("Group mean", "blue"),
        ("Subgroup mean", "green"),
        ("Supergroup mean", "black")
    ]

    fig, ax = plt.subplots(figsize=(2, 2))
    ax.axis('off')

    y_positions = [0.8, 0.6, 0.4, 0.2]
    for (label, color), y in zip(line_info, y_positions):
        ax.plot([0.1, 0.11], [y, y], color=color, linewidth=6)
        ax.text(0.111, y, label, va='center', fontsize=14)

    line_colour_filepath = os.path.join(config["radial_plot_directory"], "Line colour.png")
    plt.savefig(line_colour_filepath, bbox_inches='tight', dpi=200)
    plt.close(fig)

if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    uk_std_cluster_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "uk_std_means", "uk_std_cluster_means_output.csv"))
    combined_group_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "parent_std_means","parent_std_cluster_group_means_output.csv"))
    combined_subgroup_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "parent_std_means","parent_std_cluster_subgroup_means_output.csv"))
    create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means)