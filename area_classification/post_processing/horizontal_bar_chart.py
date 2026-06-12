#  This script creates horizontal bar charts

import os
import textwrap

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import gridspec

# Download the Open Sans font from https://fonts.google.com/specimen/Open+Sans
# Manually save the downloaded font to font_path:
font_path = "data/output_data/bar_charts/Open_Sans/OpenSans-VariableFont_wdth,wght.ttf"
# Add the font to matplotlib
fm.fontManager.addfont(font_path)
plt.rcParams["font.family"] = "Open Sans"


def create_bar_charts_wrapper(
    config, uk_std_cluster_means, combined_group_means, combined_subgroup_means
):
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
    # Create small multiples for supergroups, groups and subgroups against UK
    small_multiples(config, uk_std_cluster_means, level="UK", domain_col="domain")
    # Create small multiples for groups and subgroups against their parent (groups)
    small_multiples(config, combined_group_means, level="group", domain_col="domain")
    small_multiples(config, combined_subgroup_means, level="subgroup", domain_col="domain")

    # Save the data used in the bar charts into a data tabele
    bar_chart_data_table()


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
    # Replace 'your_file.csv' with your actual CSV file path
    name_lookup = pd.read_csv("./data/output_data/Name_lookup.csv")

    # Output directories
    small_multiples_parent_dir = os.path.join(
        config["bar_chart_directory"], "parent_cluster_small_multiples"
    )
    small_multiples_uk_dir = os.path.join(config["bar_chart_directory"], "uk_small_multiples")
    os.makedirs(small_multiples_parent_dir, exist_ok=True)
    os.makedirs(small_multiples_uk_dir, exist_ok=True)

    v01_index = dataframe.columns.get_loc("v01")
    categories = list(dataframe.columns[v01_index:])
    lookup = pd.read_csv(config["select_variables_lookup"])
    domain_dict = lookup.set_index("new_code")[domain_col].to_dict()
    label_dict = lookup.set_index("new_code")["radial_plot_label"].to_dict()

    desired_order = [
        "Demography and Migration",
        "Labour Market",
        "Ethnicity, Identity, Language and Religion",
        "Housing",
        "Health, Disability and Unpaid Care",
        "Education",
    ]

    # Identify grouping column
    if level == "group" or level == "subgroup":
        grouped = dataframe.groupby(level)
    elif level == "UK":
        grouped = dataframe.groupby("cluster")
    else:
        raise ValueError(f"Unknown level: {level}")

    for group_name, group_df in grouped:
        fig = plt.figure(figsize=(4, 20))  # 4 inches wide × 150 dpi = 600px
        # fig = plt.figure(figsize=(18, 10))

        # Calculate number of bars for each domain
        num_bars_per_domain = []
        for domain in desired_order:
            domain_cats = [cat for cat in categories if domain_dict.get(cat) == domain]
            num_bars_per_domain.append(len(domain_cats))

        # Set height ratios: 0.09 per bar (no minimum)
        height_ratios = [0.09 * n for n in num_bars_per_domain]

        # Create GridSpec with dynamic height ratios
        gs = gridspec.GridSpec(6, 1, height_ratios=height_ratios)
        axes = [fig.add_subplot(gs[i, 0]) for i in range(6)]

        for i, domain in enumerate(desired_order):
            domain_cats = [cat for cat in categories if domain_dict.get(cat) == domain]
            if not domain_cats:
                axes[i].set_visible(False)
                continue
            means = group_df[domain_cats].mean()
            axes[i].set_axisbelow(True)
            axes[i].grid(axis="x", color="lightgrey", linestyle="-", linewidth=1)
            # bar_colors = [config["domain_colours"].get(domain, "#206095")] * len(domain_cats)
            bar_colors = ["#206095" if val >= 0 else "#f66068" for val in means]
            y_labels = [label_dict.get(cat, cat) for cat in domain_cats]

            # Split y-axis labels at 28 characters
            def split_label(label, width=31):
                return "\n".join(textwrap.wrap(label, width=width))

            y_labels = [split_label(label, 31) for label in y_labels]

            # Horizontal gridlines
            for y in range(len(y_labels)):
                # 2px dash, 2px gap # square cap
                axes[i].axhline(
                    y,
                    color="#D9D9D9",
                    linewidth=1,
                    linestyle=(0, (2, 2)),
                    solid_capstyle="butt",
                    zorder=1,
                )

            # Make bars equal thickness
            axes[i].barh(y_labels, means, color=bar_colors, height=0.6)

            # Remove outline box
            for spine in axes[i].spines.values():
                spine.set_visible(False)

            # Subtitle formatting
            axes[i].set_title(domain, fontsize=14, color="#414042", fontweight="bold", loc="left")

            # Vertical line
            axes[i].axvline(0, color="#B3B3B3", linewidth=1.5, linestyle="", zorder=2)

            # Set label formatting
            # axes[i].set_xlabel("Value")
            axes[i].set_yticks(range(len(y_labels)))
            axes[i].set_yticklabels(y_labels, color="#414042", fontsize=8)

            # Remove x and y axis tick marks
            axes[i].tick_params(axis="y", length=0)
            axes[i].tick_params(axis="x", length=0, labelsize=8)
            axes[i].tick_params(axis="x", colors="#707071")
            # Set axis limits
            axes[i].set_xlim(-3, 3)
            # Find the row where cluster_code == 'group_name'
            row = name_lookup[name_lookup["cluster_code"] == group_name]
            # Print the value(s) in the cluster_name column for that row
            cluster_name = row["cluster_name"].iloc[0]
            if level == "group":
                # plt.suptitle(f"{group_name} {level} (supergroup mean)", fontsize=16, weight="bold")
                plot_path = os.path.join(
                    small_multiples_parent_dir,
                    f"Group {group_name} - {cluster_name} characteristics.png",
                )
            if level == "subgroup":
                # plt.suptitle(f"{group_name} {level} (group mean)", fontsize=16, weight="bold")
                plot_path = os.path.join(
                    small_multiples_parent_dir,
                    f"Subgroup {group_name} - {cluster_name} characteristics.png",
                )
            elif level == "UK":
                # plt.suptitle(f"{group_name} (UK mean)", fontsize=16, weight="bold")
                plot_path = os.path.join(
                    small_multiples_uk_dir,
                    f"Supergroup {group_name} - {cluster_name} characteristics.png",
                )
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.subplots_adjust(left=0.18, right=1, top=0.98, bottom=0.05)
        plt.savefig(plot_path, bbox_inches="tight", dpi=150)
        plt.close(fig)


def bar_chart_data_table():
    """
    Export cluster means data used in bar charts to an Excel file with multiple sheets.

    Reads three CSV files containing cluster means data, filters the UK standard cluster means
    to include only the Supergroup data and and writes combines this with the other two CSVs to
    create an Excel file with three sheets: 'Supergroups', 'Groups', and 'Subgroups'.

    Parameters
    ----------
    None

    Returns
    -------
    None
        Writes 'bar_chart_data_table.xlsx' to the current directory with three sheets:
        - 'Supergroups': Filtered UK standard cluster means (only 'Supergroup' rows)
        - 'Groups': Parent cluster group means
        - 'Subgroups': Parent cluster subgroup means
    """
    # Read the CSV files
    lookup = pd.read_csv("./data/lookups/UK_selected_codes_lookup.csv")
    uk_std = pd.read_csv("./data/output_data/std_means/uk_std_means/uk_std_cluster_means_output.csv")
    group_means = pd.read_csv(
        "./data/output_data/std_means/parent_std_means/parent_std_cluster_group_means_output.csv"
    )
    subgroup_means = pd.read_csv(
        "./data/output_data/std_means/parent_std_means/parent_std_cluster_subgroup_means_output.csv"
    )

    # Filter rows where 'hierarchy_level' contains ' supergroup'
    uk_supergroups = uk_std[uk_std["hierarchy_level"].str.contains("supergroup", na=False)]
    # Remove the 'hierarchy_level' column and rename 'cluster' to 'supergroups'
    uk_supergroups = uk_supergroups.drop(columns=["hierarchy_level"])
    uk_supergroups = uk_supergroups.rename(columns={"cluster": "supergroups"})

    rename_dict = dict(zip(lookup["new_code"], lookup["radial_plot_label"]))

    # Rename columns in all three DataFrames
    uk_supergroups = uk_supergroups.rename(columns=rename_dict)
    group_means = group_means.rename(columns=rename_dict)
    subgroup_means = subgroup_means.rename(columns=rename_dict)

    # Round all numeric columns to 3 decimal places
    uk_supergroups = uk_supergroups.round(3)
    group_means = group_means.round(3)
    subgroup_means = subgroup_means.round(3)

    # Write to Excel with three tabs
    with pd.ExcelWriter("data/output_data/bar_charts/bar_chart_data_table.xlsx") as writer:
        uk_supergroups.to_excel(writer, sheet_name="Supergroups", index=False)
        group_means.to_excel(writer, sheet_name="Groups", index=False)
        subgroup_means.to_excel(writer, sheet_name="Subgroups", index=False)
