"""
CSV to SQLite Processing Script using pandas

This script demonstrates how to:
1. Read a CSV file into a pandas DataFrame
2. Write the DataFrame to a SQLite database
3. Query the database back into a DataFrame
4. Display results with pandas display options

Useful References:
- Pandas to_sql documentation: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
- Pandas read_sql documentation: https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html
- SQLite Python documentation: https://docs.python.org/3/library/sqlite3.html
"""

import sqlite3
from pathlib import Path
import pandas as pd


def read_csv(csv_file: Path) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.

    Parameters
    ----------
    csv_file : Path
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the CSV data.

    Notes
    -----
    - Uses pandas read_csv to automatically infer column types.
    - Supports additional parameters like sep, encoding, parse_dates.
    """
    return pd.read_csv(csv_file)


def write_to_sqlite(dataframe: pd.DataFrame, database_file: Path, table_name: str) -> None:
    """
    Write a DataFrame into a SQLite database table.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The DataFrame to write.
    database_file : Path
        SQLite database file path. Will create it if it doesn't exist.
    table_name : str
        Name of the table to store the DataFrame.

    Notes
    -----
    - Uses pandas built-in to_sql function.
    - If the table already exists, use if_exists='replace' to overwrite.
    - Connection is automatically closed using 'with' context manager.
    """
    # Open a connection to the SQLite database (auto-closes with 'with')
    with sqlite3.connect(database_file) as cnx:
        dataframe.to_sql(
            name=table_name,
            con=cnx,
            if_exists='replace',  # replace table if it already exists
            index=False           # do not write DataFrame index as a column
        )


def read_from_sqlite(database_file: Path, table_name: str) -> pd.DataFrame:
    """
    Read a table from a SQLite database into a DataFrame.

    Parameters
    ----------
    database_file : Path
        SQLite database file path.
    table_name : str
        Table name to query.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the queried table.

    Notes
    -----
    - Uses pandas read_sql function for convenience.
    - Connection is safely managed using 'with' context.
    """
    query = f"SELECT * FROM {table_name}"  # Use f-string for clarity
    with sqlite3.connect(database_file) as cnx:
        return pd.read_sql(query, cnx)


def main() -> None:
    """
    Main function: read CSV, write to SQLite, read back, and display results.
    """
    # File paths and table name
    csv_file = Path("Demographic_Statistics_By_Zip_Code.csv")
    database_file = Path("Demographic_Statistics.db")
    table_name = "Demographic_Statistics"

    # Step 1: Load CSV into DataFrame
    print("Step 1: Loading CSV into DataFrame...")
    df = read_csv(csv_file)

    # Step 2: Write DataFrame to SQLite database
    print("Step 2: Writing DataFrame to SQLite database...")
    write_to_sqlite(df, database_file, table_name)

    # Step 3: Query database back into DataFrame
    print("Step 3: Querying the database...")
    queried_df = read_from_sqlite(database_file, table_name)

    # Step 4: Display preview
    # Adjust pandas display options for clarity
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', None)  # show all columns
    pd.set_option('display.max_colwidth', 50)  # column width for readability

    print("\nPreview of queried data (first 10 rows):")
    print(queried_df.head(10))


if __name__ == "__main__":
    main()