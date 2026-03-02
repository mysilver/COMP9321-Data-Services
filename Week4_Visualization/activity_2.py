"""
Visualizing Average Measurements per Species in the Iris Dataset using pandas and matplotlib

This script demonstrates:
1. Loading the Iris dataset
2. Computing average measurements per species
3. Visualizing the results with a bar chart

References:
- pandas groupby: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
- pandas mean: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.mean.html
- matplotlib bar plot: https://matplotlib.org/stable/api/pyplot_api.html#matplotlib.pyplot.bar
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_species_averages(csv_file: Path) -> None:
    """
    Load the Iris dataset, compute average measurements per species,
    and plot a bar chart.

    Parameters
    ----------
    csv_file : Path
        Path to the CSV file containing the Iris dataset.
    """
    # Step 1: Load CSV
    df = pd.read_csv(csv_file)

    # Step 2: Group by species and calculate mean
    species_avg = df.groupby('species', as_index=True).mean()

    # Optional: sort species alphabetically
    species_avg = species_avg.sort_index()

    # Step 3: Plot bar chart
    ax = species_avg.plot.bar(
        figsize=(10, 6),
        rot=0  # horizontal x-axis labels
    )
    ax.set_xlabel("Species")
    ax.set_ylabel("Average Measurement")
    ax.set_title("Average Measurements of Iris Species")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    csv_file = Path('iris.csv')
    plot_species_averages(csv_file)