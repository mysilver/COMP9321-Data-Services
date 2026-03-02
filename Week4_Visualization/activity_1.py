"""
Visualizing Book Publication Places with a Pie Chart using pandas and matplotlib

This script demonstrates:
1. Cleaning the 'Place of Publication' column
2. Counting the number of books per publication place
3. Visualizing the distribution using a pie chart

References:
- pandas.Series.value_counts: https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html
- matplotlib.pyplot.pie: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def clean_place_of_publication(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the 'Place of Publication' column:
    - Replace '-' with space
    - Standardize all entries containing 'London' to 'London'

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a 'Place of Publication' column

    Returns
    -------
    pd.DataFrame
        DataFrame with cleaned 'Place of Publication'
    """
    df['Place of Publication'] = (
        df['Place of Publication']
        .str.replace('-', ' ', regex=False)  # replace '-' with space
        .mask(df['Place of Publication'].str.contains('London', na=False), 'London')  # standardize London
    )
    return df


def main() -> None:
    csv_file = Path('Books.csv')

    # Step 1: Load CSV
    df = pd.read_csv(csv_file)

    # Step 2: Optional cleaning
    df = clean_place_of_publication(df)

    # Step 3: Count the number of books per publication place
    place_counts = df['Place of Publication'].value_counts()

    # Step 4: Plot as a pie chart
    plt.figure(figsize=(8, 8))
    place_counts.plot.pie(
        autopct='%1.1f%%',  # show percentages
        startangle=90,       # rotate start angle for better visual
        counterclock=False,  # clockwise order
        shadow=True          # add shadow for 3D effect
    )
    plt.title("Distribution of Books by Place of Publication")
    plt.ylabel("")  # remove default y-label
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()