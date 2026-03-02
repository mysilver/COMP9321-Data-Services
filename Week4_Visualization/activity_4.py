"""
Visualizing Iris Dataset with Scatter Plots using pandas and matplotlib

This script demonstrates:
1. Splitting the Iris dataset by species
2. Plotting multiple scatter plots with different colors
3. Comparing sepal and petal measurements

References:
- pandas.DataFrame.plot.scatter: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.scatter.html
- matplotlib.pyplot: https://matplotlib.org/stable/api/pyplot_api.html
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_iris_scatter(df: pd.DataFrame) -> None:
    """
    Plot scatter charts for Iris dataset: sepal and petal measurements.

    Parameters
    ----------
    df : pd.DataFrame
        Iris dataset with columns 'species', 'sepal_length', 'sepal_width',
        'petal_length', 'petal_width'.
    """

    # Define colors for each species
    species_colors = {
        'setosa': 'blue',
        'versicolor': 'green',
        'virginica': 'red'
    }

    # Create subplots: one for sepal, one for petal
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Scatter plot for sepal length vs width
    for species, color in species_colors.items():
        subset = df.query('species == @species')
        subset.plot.scatter(
            x='sepal_length',
            y='sepal_width',
            label=species,
            color=color,
            ax=axes[0]
        )
    axes[0].set_title("Sepal Length vs Sepal Width")
    axes[0].set_xlabel("Sepal Length (cm)")
    axes[0].set_ylabel("Sepal Width (cm)")

    # Scatter plot for petal length vs width
    for species, color in species_colors.items():
        subset = df.query('species == @species')
        subset.plot.scatter(
            x='petal_length',
            y='petal_width',
            label=species,
            color=color,
            ax=axes[1]
        )
    axes[1].set_title("Petal Length vs Petal Width")
    axes[1].set_xlabel("Petal Length (cm)")
    axes[1].set_ylabel("Petal Width (cm)")

    # Adjust layout and show
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    csv_file = Path('iris.csv')
    df = pd.read_csv(csv_file)
    plot_iris_scatter(df)