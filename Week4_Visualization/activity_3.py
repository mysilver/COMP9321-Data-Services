from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def plot_iris_scatter_corrected(df: pd.DataFrame) -> None:
    """
    Plot two separate scatter charts for the Iris dataset (corrected version):
    - 1st plot: Sepal Length vs Sepal Width
    - 2nd plot: Petal Length vs Petal Width
    - Only two figures pop up, one per plot
    """
    species_colors = {
        'setosa': 'blue',
        'versicolor': 'green',
        'virginica': 'red'
    }

    # ----------------- Sepal Scatter Plot -----------------
    ax = None
    for species, color in species_colors.items():
        subset = df.query('species == @species')
        ax = subset.plot.scatter(
            x='sepal_length',
            y='sepal_width',
            label=species,
            color=color,
            ax=ax  # plot on the same axes
        )
    plt.title("Sepal Length vs Sepal Width")
    plt.xlabel("Sepal Length (cm)")
    plt.ylabel("Sepal Width (cm)")
    plt.legend()
    plt.show()  # Only 1 figure

    # ----------------- Petal Scatter Plot -----------------
    ax = None
    for species, color in species_colors.items():
        subset = df.query('species == @species')
        ax = subset.plot.scatter(
            x='petal_length',
            y='petal_width',
            label=species,
            color=color,
            ax=ax  # plot on the same axes
        )
    plt.title("Petal Length vs Petal Width")
    plt.xlabel("Petal Length (cm)")
    plt.ylabel("Petal Width (cm)")
    plt.legend()
    plt.show()  # Only 1 figure


if __name__ == "__main__":
    csv_file = Path("iris.csv")
    df = pd.read_csv(csv_file)
    plot_iris_scatter_corrected(df)