# STILL TO DO, LOOP THROUGH ALL THE levels at the parent level.
# WORK OUT ERROR
# LOOK INTO SMALL MULTIPLES!
# 
#  # Horizontal bar chart
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import gridspec
import numpy as np
import os
import pandas as pd
from area_classification.utilities.load_config import load_config

def create_horizontal_bar_chart_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means):
    """
    Wrapper function to create horizional bar charts.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing filepaths.
    uk_std_cluster_means : DataFrame
        DataFrame containing standardised cluster means for the UK.
    combined_group_means : DataFrame
        DataFrame containing group-level means.
    combined_subgroup_means : DataFrame
        DataFrame containing subgroup-level means.
    level : str
        Either 'group' or 'subgroup' to indicate the type of data.

    Returns
    -------
    None
        Created bar charts are saved to the 'bar_charts' folder

    Notes
    -----
    The lookup CSV file must contain at least the columns 'new_code', 'radial_plot_label', and 'domain'.
    """

    # Create bar charts for supergroups, groups and subgroups against UK
    horizontal_bar_charts(config, uk_std_cluster_means, level="UK")
    
    # Create radial plots for groups against their parent (groups)
    horizontal_bar_charts(config, combined_group_means, level="group")

    # Create radial plots for subgroups against their parent (groups)
    horizontal_bar_charts(config, combined_subgroup_means, level="subgroup")



def horizontal_bar_charts(config, dataframe, level):
    """
    Helper function to create horizontal bar charts for a given dataframe.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing settings for the plotting.    
    dataframe : DataFrame
        The input DataFrame (either combined_group_means or combined_subgroup_means).
    level : str
        Either 'group' or 'subgroup' to indicate the type of data.

    """
    
    # Load lookup for variable labels and domains
    lookup = pd.read_csv(config['select_variables_lookup'])
    label_dict = lookup.set_index('new_code')['radial_plot_label'].to_dict()
    domain_dict = lookup.set_index('new_code')['domain'].to_dict()

    categories = list(dataframe.columns[2:])
    category_domains = {cat: domain_dict.get(cat, None) for cat in categories}
    # Use label_dict to get y-axis labels
    y_labels = [label_dict.get(cat, cat) for cat in categories]

    # Output directories
    bar_parent_dir = os.path.join(config["bar_chart_directory"], "parent_cluster_bar_charts")
    bar_uk_dir = os.path.join(config["bar_chart_directory"], "uk_bar_charts")
    os.makedirs(bar_parent_dir, exist_ok=True)
    os.makedirs(bar_uk_dir, exist_ok=True)
    
    for idx, row in dataframe.iterrows():
        values = row[categories].tolist()
        
        fig = plt.figure(figsize=(12, 8))
        gs = gridspec.GridSpec(1, 2, width_ratios=[0.3, 5], wspace=0.05)

        # Color strip axis
        ax2 = fig.add_subplot(gs[0])
        ax2.set_ylim(-0.5, len(categories) - 0.5)
        ax2.set_xlim(0, 1)
        ax2.axis('off')

        # Draw colored strips for each domain group
        current_domain = None
        start_idx = 0
        for i, cat in enumerate(categories + [None]):
            domain = category_domains.get(cat) if cat else None
            if domain != current_domain:
                if current_domain is not None and current_domain in config['domain_colours']:
                    ax2.add_patch(Rectangle(
                        (0.7, start_idx - 0.4),
                        0.9,
                        i - start_idx,
                        facecolor=config['domain_colours'][current_domain],
                        edgecolor='none'
                    ))
                current_domain = domain
                start_idx = i

        # Main bar chart axis
        ax = fig.add_subplot(gs[1], sharey=ax2)
        ax.barh(y_labels, values, color='#206095')
        ax.axvline(0, color='grey', linewidth=2, linestyle='--', zorder=2)
        ax.tick_params(axis='y', pad=30)  # Move y-axis labels further left
        ax.set_xlabel('Values')
        plt.tight_layout()

        # Plot the data line and set title/filename
        # colour of the plotted line is blue for groups, green for subgroups and black for UK
        if level == "group":
            ax.set_title(f"{row[level]} {level} (supergroup mean)", size=26, pad=80, weight='bold')
            plot_path = os.path.join(bar_parent_dir, f"{row[level]}_{level}.png")
        elif level == "subgroup":
            ax.set_title(f"{row[level]} {level} (group mean)", size=26, pad=80, weight='bold')
            plot_path = os.path.join(bar_parent_dir, f"{row[level]}_{level}.png")
        elif level == "UK":
            ax.set_title(f"{row['cluster']} {row['hierarchy_level']} (UK mean)", size=26, pad=80, weight='bold')
            plot_path = os.path.join(bar_uk_dir, f"{row['cluster']}_{row['hierarchy_level']}.png")

        # Save the plot
        fig.savefig(plot_path, bbox_inches='tight', dpi=150)
        plt.close(fig)


if __name__ == "__main__":

    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
       
    uk_std_cluster_means = pd.read_csv('./data/output_data/std_means/uk_std_means/uk_std_cluster_means_output.csv') 
    combined_group_means = pd.read_csv('./data/output_data/std_means/parent_std_means/parent_std_cluster_group_means_output.csv') 
    combined_subgroup_means = pd.read_csv('./data/output_data/std_means/parent_std_means/parent_std_cluster_group_means_output.csv')
    create_horizontal_bar_chart_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means)
    #return 
    print(uk_std_cluster_means)