#  This script creates horizontal bar charts

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import gridspec
import matplotlib.gridspec as gridspec
import os
import pandas as pd
from area_classification.utilities.load_config import load_config

def create_bar_charts_wrapper(config, uk_std_cluster_means, combined_group_means, combined_subgroup_means):
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

    Returns
    -------
    None
        Created bar charts are saved to the 'bar_charts' folder

    """

    # Create horizontal bar charts for supergroups, groups and subgroups against UK
    horizontal_bar_charts(config, uk_std_cluster_means, level="UK")
    
    # Create horizontal bar charts for groups and subgroups against their parent (groups)
    horizontal_bar_charts(config, combined_group_means, level="group")
    horizontal_bar_charts(config, combined_subgroup_means, level="subgroup")

    # Create small multiples for supergroups, groups and subgroups against UK
    small_multiples(config, uk_std_cluster_means, level = "UK", domain_col = "domain")
    # Create small multiples for groups and subgroups against their parent (groups)
    small_multiples(config, combined_group_means, level = "group", domain_col = "domain")
    small_multiples(config, combined_subgroup_means, level = "subgroup", domain_col = "domain")



def horizontal_bar_charts(config, dataframe, level):
    """
    Create horizontal bar charts for a given dataframe.

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

    v01_index = dataframe.columns.get_loc("v01")
    categories = list(dataframe.columns[v01_index:])
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
        ax.set_xlim(-3, 3)
        ax.barh(y_labels, values, color='#206095')
        ax.axvline(0, color='grey', linewidth=2, linestyle='--', zorder=2)
        ax.tick_params(axis='y', pad=30)  # Move y-axis labels further left
        ax.set_xlabel('Values')
        plt.tight_layout()

        # Plot the data line and set title/filename
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


def small_multiples(config, dataframe, level, domain_col):
    """
    Create a set of small multiples for every group.
    Each set contains 6 plots, one for each domain.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing settings for the plotting.    
    dataframe : DataFrame
        The input DataFrame (either combined_group_means or combined_subgroup_means).
    level : str
        Either 'group' or 'subgroup' to indicate the type of data.
    domain_colours : Dictionary
        The list of colours used for the domains. 

    """
    # Output directories
    small_multiples_parent_dir = os.path.join(config["bar_chart_directory"], "parent_cluster_small_multiples")
    small_multiples_uk_dir = os.path.join(config["bar_chart_directory"], "uk_small_multiples")
    os.makedirs(small_multiples_parent_dir, exist_ok=True)
    os.makedirs(small_multiples_uk_dir, exist_ok=True)

    v01_index = dataframe.columns.get_loc("v01")
    categories = list(dataframe.columns[v01_index:])
    lookup = pd.read_csv(config['select_variables_lookup'])
    domain_dict = lookup.set_index('new_code')[domain_col].to_dict()
    label_dict = lookup.set_index('new_code')['radial_plot_label'].to_dict()

    desired_order = [
        "Demography and Migration", 
        "Labour Market",              
        "Ethnicity, Identity, Language and Religion",                 
        "Housing",                   
        "Health, Disability and Unpaid Care",                    
        "Education"                   
    ]
    
    # Identify grouping column
    if level == "group":
        grouped = dataframe.groupby(level)
    elif level == "subgroup":
        grouped = dataframe.groupby(level)
    elif level == "UK":
        grouped = dataframe.groupby("cluster")
    else:
        raise ValueError(f"Unknown level: {level}")
    
    for group_name, group_df in grouped:
        fig = plt.figure(figsize=(18, 10))
        # Adjust the height of the small multiples (top row, middle row, bottom row)
        gs = gridspec.GridSpec( 3, 2, height_ratios=[1.5, 1, 0.25], )
        axes = [fig.add_subplot(gs[i, j]) for i in range(3) for j in range(2)]

        for i, domain in enumerate(desired_order):
            domain_cats = [cat for cat in categories if domain_dict.get(cat) == domain]
            if not domain_cats:
                axes[i].set_visible(False)
                continue
            means = group_df[domain_cats].mean()
            bar_colors = [config['domain_colours'].get(domain, '#206095')] * len(domain_cats)
            y_labels = [label_dict.get(cat, cat) for cat in domain_cats]
            axes[i].barh(y_labels, means, color=bar_colors)
            axes[i].set_title(domain)
            axes[i].axvline(0, color='grey', linewidth=2, linestyle='--', zorder=2)
            axes[i].set_xlim(-3, 3)
            axes[i].set_xlabel('Value')
            axes[i].set_yticklabels(y_labels, fontsize=8)
            if level == "group":
                plt.suptitle(f"{group_name} {level} (supergroup mean)", fontsize=16, weight='bold')
                plot_path = os.path.join(small_multiples_parent_dir, f"{group_name}_{level}.png")
            if level == "subgroup":
                plt.suptitle(f"{group_name} {level} (group mean)", fontsize=16, weight='bold')
                plot_path = os.path.join(small_multiples_parent_dir, f"{group_name}_{level}.png")
            elif level == "UK":
                plt.suptitle(f"{group_name} (UK mean)", fontsize=16, weight='bold')
                plot_path = os.path.join(small_multiples_uk_dir, f"{group_name}.png")
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(plot_path, bbox_inches='tight', dpi=150)
        plt.close(fig)