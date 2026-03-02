"""
Analyze NaN values and drop selected columns in a CSV using pandas.

This script demonstrates:
1. Calculating the percentage of missing values per column
2. Dropping unnecessary columns
3. Displaying the DataFrame before and after dropping columns

Pandas References:
- isna(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html
- drop(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
"""

from pathlib import Path
import pandas as pd
from typing import List


def calculate_nan_percentage(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the percentage of NaN values per column.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    pd.Series
        A Series containing the percentage of NaN values per column.
    """
    # df.isna() returns True/False for missing values
    # .mean() computes the fraction of True per column
    return df.isna().mean() * 100


def drop_columns(df: pd.DataFrame, columns_to_drop: List[str]) -> pd.DataFrame:
    """
    Drop the specified columns from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The original DataFrame.
    columns_to_drop : list of str
        List of column names to drop.

    Returns
    -------
    pd.DataFrame
        DataFrame after dropping the columns.
    """
    return df.drop(columns=columns_to_drop, axis=1, inplace=False)


def main() -> None:
    csv_file = Path("Books.csv")

    # Columns to remove
    columns_to_drop = [
        "Edition Statement",
        "Corporate Author",
        "Corporate Contributors",
        "Former owner",
        "Engraver",
        "Contributors",
        "Issuance type",
        "Shelfmarks"
    ]

    # Step 1: Load CSV
    df = pd.read_csv(csv_file)

    # Step 2: Calculate and print NaN percentages
    print("Step 1: Percentage of missing values per column:")
    nan_percentages = calculate_nan_percentage(df)
    for column, percent in nan_percentages.items():
        print(f"{column}: {percent:.2f}%")

    print("\n" + "*" * 50)
    print("DataFrame before dropping columns:")
    print(df.to_string())

    print("\n" + "*" * 50)
    print("DataFrame after dropping columns:")
    df_cleaned = drop_columns(df, columns_to_drop)
    print(df_cleaned.to_string())
    print("*" * 50)


if __name__ == "__main__":
    main()