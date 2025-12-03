# Creation of radial plots

# WORK OUT HOW TO INCREASE THE SIZE OF THE TICK MARKS FOR THE LABELS AT THE TOP AND BOTTOM
# NEED TO ADD A FUNCTION THAT CREATES A KEY FOR THE DOMAINS AND THEIR COLOURS
# NEED TO ADJUST THE RADIAL PLOT TO HAVE DIFFERENT SCALES FOR VALUES GREATER THAN 3 OR LESS THAN -3
# NEED TO ADD A FUNCTION THAT CREATES A KEY FOR THE LINE COLOURS FOR SUPERGROUPS/GROUPS/SUBGROUPS/UK

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
    config : dict
        Configuration dictionary containing settings for the plotting.    
    """
    # Load lookup for variable labels and domains
    lookup = pd.read_csv(config['select_variables_lookup'])
    label_dict = lookup.set_index('new_code')['radial_plot_label'].to_dict()
    domain_dict = lookup.set_index('new_code')['domain'].to_dict()

    # Output directories
    parent_dir = os.path.join(config["radial_plot_directory"], "parent_cluster_radial_plots_v2")
    uk_dir = os.path.join(config["radial_plot_directory"], "uk_radial_plots_v2")
    os.makedirs(parent_dir, exist_ok=True)
    os.makedirs(uk_dir, exist_ok=True)

    # Feature columns (e.g., v01, v02, ...)
    feature_cols = [col for col in dataframe if col.startswith("v")]

    # Domain color mapping
    domain_colors = {
        "Demography and Migration": "#004272", # blue
        "Ethnicity, Identity, Language and Religion": "#006400", # dark green
        "Health, Disability and Unpaid Care": "#584001", # brown
        "Housing": "#4b0082", # indigo
        "Labour Market": "#9e0d0d", # dark red
        "Education": "#525151" # grey
    }

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
        ax.set_ylim(-3, 4.0)
        # Make the outer polar axis border (spine) transparent 
        ax.spines['polar'].set_visible(False)

        # Draw colored domain segments
        for i, col in enumerate(feature_cols):
            domain = domain_dict.get(col, "Other")
            color = domain_colors.get(domain, "black")
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
        top_tick_ends = [5.0, 5.0, 4.5, 4.5, 4.0, 4.0] # WORK OUT WHY THESE ARE ALL THE SAME LENGTH IN THE OUTPUT
        bottom_label_radii = [4.6, 4.6, 4.4, 4.4, 4.2, 4.2]  # Closest to bottom (angle=pi), then next, etc.
        bottom_tick_ends = [5.0, 5.0, 4.5, 4.5, 4.0, 4.0] # WORK OUT WHY THESE ARE ALL THE SAME LENGTH IN THE OUTPUT
        default_label_radius = 4.0
        default_tick_end = 3.8

        angle_label_indices = list(enumerate(angles[:-1]))  # Exclude the closing angle
        # Top 6: closest to π/2 (90°)
        top_indices_sorted = sorted(angle_label_indices, key=lambda x: abs(x[1] - (np.pi / 2)))[:6]
        top_indices = set(idx for idx, _ in top_indices_sorted)
        # Bottom 6: closest to 3π/2 (270°), but exclude any already in top_indices
        bottom_candidates = [item for item in angle_label_indices if item[0] not in top_indices]
        bottom_indices_sorted = sorted(bottom_candidates, key=lambda x: abs(x[1] - (3 * np.pi / 2)))[:6]

        # Debug printout for verification
        print("Top 6 label indices and angles (closest to 90°):")
        for idx, ang in top_indices_sorted:
            print(f"  idx={idx}, angle={ang:.3f}, label={label_dict.get(feature_cols[idx], feature_cols[idx])}")
        print("Bottom 6 label indices and angles (closest to 270°):")
        for idx, ang in bottom_indices_sorted:
            print(f"  idx={idx}, angle={ang:.3f}, label={label_dict.get(feature_cols[idx], feature_cols[idx])}")

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
        ax.plot(angles, [0] * len(angles), color='red', linewidth=1.0, linestyle='solid', label='Zero Line')

        # Plot the data line and set title/filename
        # colour of the plotted line is blue for groups, green for subgroups and black for UK
        if level == "group":
            ax.plot(angles, values, color='blue', linewidth=1.5, linestyle='solid') 
            ax.set_title(f"{row[level]} {level} (supergroup mean)", size=18, pad=80, weight='bold')
            plot_path = os.path.join(parent_dir, f"{row[level]}_{level}.png")
        elif level == "subgroup":
            ax.plot(angles, values, color='green', linewidth=1.5, linestyle='solid')
            ax.set_title(f"{row[level]} {level} (group mean)", size=18, pad=80, weight='bold')
            plot_path = os.path.join(parent_dir, f"{row[level]}_{level}.png")
        elif level == "UK":
            ax.plot(angles, values, color='black', linewidth=1.5, linestyle='solid')
            ax.set_title(f"{row['cluster']} {row['hierarchy_level']} (UK mean)", size=18, pad=80, weight='bold')
            plot_path = os.path.join(uk_dir, f"{row['cluster']}_{row['hierarchy_level']}.png")

        plt.savefig(plot_path)
        plt.close(fig)

    if level == "UK":
        print(f"UK radial plots saved in: {uk_dir}")
    elif level in ["group", "subgroup"]:
        print(f"Parent cluster radial plots saved in: {parent_dir}")

if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    uk_std_cluster_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "uk_std_means", "uk_std_cluster_means_output.csv"))
    combined_group_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "parent_std_means","parent_std_cluster_group_means_output.csv"))
    combined_subgroup_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "parent_std_means","parent_std_cluster_subgroup_means_output.csv"))
    create_radial_plots_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means)