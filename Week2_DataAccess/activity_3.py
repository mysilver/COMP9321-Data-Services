"""
CSV to MongoDB Processing Script using pandas

This script demonstrates how to:
1. Read a CSV file into a pandas DataFrame
2. Print the DataFrame (two options)
3. Write the DataFrame into a MongoDB collection
4. Read documents back from MongoDB into a DataFrame

Useful References:
- PyMongo documentation: https://pymongo.readthedocs.io/en/stable/
- Pandas read_csv: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
- Pandas to_json: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html
"""

import json
from pathlib import Path
import pandas as pd
from pymongo import MongoClient
from typing import Union


def read_csv(csv_file: Union[str, Path]) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.

    Parameters
    ----------
    csv_file : str | Path
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the CSV data.
    """
    return pd.read_csv(csv_file)


def print_dataframe_option1(dataframe: pd.DataFrame, max_rows: int = 10) -> None:
    """
    Option 1: Standard pandas preview.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The DataFrame to display.
    max_rows : int
        Maximum number of rows to display.
    """
    with pd.option_context(
        "display.max_rows", max_rows,
        "display.max_columns", None,
        "display.width", 1000
    ):
        print(dataframe)


def print_dataframe_option2_csv(dataframe: pd.DataFrame, max_rows: int = 10) -> None:
    """
    Option 2: Print DataFrame in CSV format.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The DataFrame to display.
    max_rows : int
        Maximum number of rows to display.
    """
    preview_df = dataframe.head(max_rows)
    preview_df.to_csv(index=False, line_terminator='\n')


def write_to_mongodb(
    dataframe: pd.DataFrame,
    mongo_host: str,
    mongo_port: int,
    db_name: str,
    collection_name: str
) -> None:
    """
    Write a pandas DataFrame into a MongoDB collection.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The DataFrame to insert into MongoDB.
    mongo_host : str
        MongoDB server hostname or IP address.
    mongo_port : int
        MongoDB server port (default MongoDB port: 27017).
    db_name : str
        Name of the database to use.
    collection_name : str
        Name of the collection inside the database.

    Notes
    -----
    - Converts each row of the DataFrame into a JSON document.
    - Uses insert_many to store all documents efficiently.
    - Make sure MongoDB server is running before executing this function.
    """
    with MongoClient(host=mongo_host, port=mongo_port) as client:
        db = client[db_name]
        collection = db[collection_name]

        # Convert DataFrame rows to list of dicts
        records = json.loads(dataframe.T.to_json()).values()
        collection.insert_many(records)


def read_from_mongodb(
    mongo_host: str,
    mongo_port: int,
    db_name: str,
    collection_name: str
) -> pd.DataFrame:
    """
    Read all documents from a MongoDB collection into a pandas DataFrame.

    Parameters
    ----------
    mongo_host : str
        MongoDB server hostname or IP address.
    mongo_port : int
        MongoDB server port.
    db_name : str
        Name of the database.
    collection_name : str
        Name of the collection.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all documents from the collection.

    Notes
    -----
    - Uses list(c.find()) to convert MongoDB cursor to a Python list.
    - Can include filters in c.find({}) if needed.
    """
    with MongoClient(host=mongo_host, port=mongo_port) as client:
        db = client[db_name]
        collection = db[collection_name]
        return pd.DataFrame(list(collection.find()))


def main() -> None:
    """
    Main function: read CSV, write to MongoDB, query back, and display.
    """
    # MongoDB connection parameters
    db_name = "comp9321"
    mongo_host = "localhost"
    mongo_port = 27017
    collection_name = "Demographic_Statistics"

    # CSV file path
    csv_file = Path("Demographic_Statistics_By_Zip_Code.csv")

    # Step 1: Load CSV
    print("Step 1: Loading CSV into DataFrame...")
    df = read_csv(csv_file)

    # Step 2: Write to MongoDB
    print("Step 2: Writing DataFrame into MongoDB...")
    write_to_mongodb(df, mongo_host, mongo_port, db_name, collection_name)

    # Step 3: Read from MongoDB
    print("Step 3: Querying MongoDB...")
    queried_df = read_from_mongodb(mongo_host, mongo_port, db_name, collection_name)

    # Step 4: Preview the data
    print("\nOption 1: Standard pandas preview (first 10 rows)")
    print_dataframe_option1(queried_df, max_rows=10)

    print("\nOption 2: CSV format preview (first 10 rows)")
    print_dataframe_option2_csv(queried_df, max_rows=10)


if __name__ == "__main__":
    main()