"""
Books Data Processing and Analysis Pipeline using pandas

This script demonstrates:
1. Cleaning book publication data
2. Merging with city data
3. Grouping and aggregating publications by country

Pandas References:
- String operations: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html
- Regex extract: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html
- Merge: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
- GroupBy: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
"""

from pathlib import Path
import pandas as pd


def clean_books(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean book DataFrame columns:
    - Standardize 'Place of Publication': replace '-' with space, map entries containing 'London' to 'London'
    - Extract 4-digit year from 'Date of Publication' and convert to integer

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing book data

    Returns
    -------
    pd.DataFrame
        Cleaned book DataFrame
    """
    # Vectorized string replacement and conditional mapping
    df['Place of Publication'] = (
        df['Place of Publication']
        .str.replace('-', ' ', regex=False)
        .mask(df['Place of Publication'].str.contains('London', na=False), 'London')
    )

    # Extract year and convert to numeric
    df['Date of Publication'] = pd.to_numeric(
        df['Date of Publication'].str.extract(r'^(\d{4})', expand=False),
        errors='coerce'
    ).fillna(0).astype(int)

    return df


def main() -> None:
    # File paths
    books_file = Path("Books.csv")
    city_file = Path("City.csv")

    # Step 1: Load CSVs
    books_df = pd.read_csv(books_file)
    city_df = pd.read_csv(city_file)

    # Step 2: Clean book data
    books_df = clean_books(books_df)

    # Step 3: Rename columns for query/merge safety
    books_df.columns = [col.replace(' ', '_') for col in books_df.columns]
    city_df.columns = [col.replace(' ', '_') for col in city_df.columns]

    # Step 4: Merge book data with city data
    # Left join keeps all books; adds country info from city_df
    merged_df = pd.merge(
        books_df,
        city_df,
        how='left',
        left_on='Place_of_Publication',
        right_on='City'
    )

    # Step 5: Group by 'Country' and count number of publications
    publications_by_country = merged_df.groupby('Country', as_index=False)['Identifier'].count()
    publications_by_country.rename(columns={'Identifier': 'Publication_Count'}, inplace=True)

    # Step 6: Display results
    print("Number of publications by country:")
    print(publications_by_country.to_string(index=False))


if __name__ == "__main__":
    main()