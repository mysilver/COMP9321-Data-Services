"""
Data Cleaning and Transformation on 'Books.csv' using pandas

This script demonstrates:
1. Cleaning a column with string replacement and conditional logic
2. Extracting the year from a publication date column using regex
3. Handling missing values (NaN)

Pandas References:
- String methods: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html
- Extract with regex: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html
- Fill missing values: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html
"""

from pathlib import Path
import pandas as pd


def clean_place_of_publication(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Clean the 'Place of Publication' column:
    - Replace any entry containing 'London' with 'London'
    - Replace all '-' characters with a space

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame
    column : str
        Column name to clean

    Returns
    -------
    pd.DataFrame
        DataFrame with cleaned 'Place of Publication' column
    """
    # Use vectorized string methods instead of apply for better performance
    df[column] = df[column].str.replace('-', ' ', regex=False)  # replace '-' with space
    df[column] = df[column].mask(df[column].str.contains('London', na=False), 'London')  # replace rows containing 'London'
    return df


def extract_year(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Extract the 4-digit year from a 'Date of Publication' column.
    Converts to numeric and fills NaN with 0.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame
    column : str
        Column name containing date strings

    Returns
    -------
    pd.DataFrame
        DataFrame with cleaned 'Date of Publication' column
    """
    # Extract first 4 digits at the beginning of the string
    df[column] = pd.to_numeric(df[column].str.extract(r'^(\d{4})', expand=False), errors='coerce')
    # Replace NaN with 0
    df[column] = df[column].fillna(0).astype(int)
    return df


def main() -> None:
    csv_file = Path("Books.csv")

    # Step 1: Load CSV
    df = pd.read_csv(csv_file)

    # Step 2: Clean 'Place of Publication'
    print("Step 2: Cleaning 'Place of Publication' column...")
    df = clean_place_of_publication(df, 'Place of Publication')
    print(df['Place of Publication'].head(10))

    # Step 3: Extract year from 'Date of Publication'
    print("\nStep 3: Extracting year from 'Date of Publication' column...")
    df = extract_year(df, 'Date of Publication')
    print(df['Date of Publication'].head(10))

    # Step 4: Final preview
    print("\nFinal cleaned DataFrame preview:")
    print(df.head(10).to_string())


if __name__ == "__main__":
    main()