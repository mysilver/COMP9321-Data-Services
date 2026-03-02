"""
Books Data Cleaning and Filtering Pipeline using pandas

This script demonstrates:
1. Cleaning the 'Place of Publication' and 'Date of Publication' columns
2. Converting column names to a query-friendly format
3. Filtering the DataFrame using pandas query

Pandas References:
- String operations: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html
- Regex extract: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html
- Query method: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html
"""

from pathlib import Path
import pandas as pd


def clean(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the 'Place of Publication' and 'Date of Publication' columns.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Input DataFrame containing book data.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with:
        - 'Place of Publication' standardized
        - 'Date of Publication' extracted as numeric year
    """

    # Replace '-' with space and set all 'London' entries to 'London'
    # Using vectorized string methods for performance
    dataframe['Place of Publication'] = (
        dataframe['Place of Publication']
        .str.replace('-', ' ', regex=False)
        .mask(dataframe['Place of Publication'].str.contains('London', na=False), 'London')
    )

    # Extract 4-digit year from 'Date of Publication' using regex
    dataframe['Date of Publication'] = pd.to_numeric(
        dataframe['Date of Publication'].str.extract(r'^(\d{4})', expand=False),
        errors='coerce'
    ).fillna(0).astype(int)  # replace NaN with 0 and convert to integer

    return dataframe


def main() -> None:
    csv_file = Path("Books.csv")

    # Step 1: Load CSV
    df = pd.read_csv(csv_file)

    # Step 2: Clean data
    df = clean(df)

    # Step 3: Rename columns for query-friendly format
    # Replace spaces with underscores to avoid issues with pandas query
    df.columns = [col.replace(' ', '_') for col in df.columns]

    # Step 4: Filter DataFrame
    df_filtered = df.query('Date_of_Publication > 1866 and Place_of_Publication == "London"')

    # Step 5: Display result
    print("Filtered DataFrame:")
    print(df_filtered.to_string())


if __name__ == "__main__":
    main()