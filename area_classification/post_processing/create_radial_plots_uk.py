# THIS CURRENTLY WORKS FOR SUPERGROUPS ONLY

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def create_radial_plots_uk(config, uk_std_cluster_means):
    """
    Create radial plots for the area classification clusters.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing settings for the plotting.
    uk_std_cluster_means : DataFrame
        DataFrame containing standardized cluster means for the UK.
    """

    # Create the 'radial_plots' directory
    radial_plots_dir = os.path.join(config["output_directory"], "radial_plots")
    os.makedirs(radial_plots_dir, exist_ok=True)

    # Filter rows where hierarchy_level is 'supergroup'
    supergroup_data = uk_std_cluster_means[uk_std_cluster_means["hierarchy_level"] == "supergroup"]

    # Get the feature columns (assuming they start from 'v01' to 'v59')
    feature_columns = [col for col in uk_std_cluster_means.columns if col.startswith("v")]

        # Create a radial plot for each supergroup row
    for idx, row in supergroup_data.iterrows():
        # Extract the feature values for the current row
        values = row[feature_columns].tolist()
        values += values[:1]  # Repeat the first value to close the circle

        # Angles for the radar chart
        num_vars = len(feature_columns)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Repeat the first angle to close the circle

        # Initialize the radar chart
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Draw the outline of the radar chart
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=f'Supergroup {row["cluster"]}')
        ax.fill(angles, values, alpha=0.25)

        # Add labels for each feature
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(feature_columns)

        # Add a title
        ax.set_title(f"Radial Plot for Supergroup {row['cluster']}", size=14, pad=20)

        # Draw a solid red ring at the radius of 0
        ax.plot(angles[:-1], [0] * len(angles[:-1]), color='red', linewidth=2, linestyle='solid', label='Zero Line')

        # Save the plot with the filename as '<cluster>_supergroup.png'
        plot_filename = f"{row['cluster']}_supergroup.png"
        plot_path = os.path.join(radial_plots_dir, plot_filename)
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close(fig)

    print(f"Radial plots saved in: {radial_plots_dir}")

if __name__ == "__main__":
    from area_classification.utilities.load_config import load_config
    config = load_config('area_classification/config.yaml')
    uk_std_cluster_means = pd.read_csv(os.path.join(config["output_directory"], "std_means", "uk_std_means", "uk_std_cluster_means_output.csv"))

    create_radial_plots_uk(config, uk_std_cluster_means)






    




