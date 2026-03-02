"""
CSV Processing Script with Two Print Options

This script demonstrates:
1. Reading a CSV file into a pandas DataFrame
2. Printing a preview in two different ways:
   - Option 1: Standard pandas display
   - Option 2: CSV-format display (like a CSV file)
3. Writing the DataFrame back to a CSV file

Pandas Documentation (recommended):
https://pandas.pydata.org/docs/user_guide/io.html
"""

from pathlib import Path
import pandas as pd
import sys


def read_csv(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.
    """
    return pd.read_csv(file_path)


def write_csv(dataframe: pd.DataFrame, file_path: Path) -> None:
    """
    Write a DataFrame to a CSV file.
    """
    dataframe.to_csv(file_path, index=False, encoding="utf-8")


def print_dataframe_option1(dataframe: pd.DataFrame, max_rows: int = 10) -> None:
    """
    Option 1: Standard pandas preview (like df.head()).

    Parameters
    ----------
    dataframe : pd.DataFrame
        The DataFrame to display.
    max_rows : int
        Maximum number of rows to display.
    """
    # Use pandas option_context to control display settings
    with pd.option_context(
        "display.max_rows", max_rows,  # limit rows
        "display.max_columns", None,   # show all columns
        "display.width", 1000          # prevent wrapping
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
    # Take only the first max_rows rows
    preview_df = dataframe.head(max_rows)

    # Use pandas to_csv to print in CSV format directly to stdout
    preview_df.to_csv(sys.stdout, index=False, line_terminator='\n')


def main() -> None:
    # File paths
    input_file = Path("Demographic_Statistics_By_Zip_Code.csv")
    output_file = Path("Demographic_Statistics_New.csv")

    # Step 1: Load CSV
    print("Step 1: Loading CSV file into a DataFrame...")
    df = read_csv(input_file)

    # Step 2: Preview with Option 1
    print("\nStep 2a: Preview (Option 1: standard pandas display)")
    print_dataframe_option1(df, max_rows=10)

    # Step 2: Preview with Option 2
    print("\nStep 2b: Preview (Option 2: CSV format display)")
    print_dataframe_option2_csv(df, max_rows=10)

    # Step 3: Write to a new CSV
    print("\nStep 3: Writing DataFrame to a new CSV file...")
    write_csv(df, output_file)

    print("Process completed successfully.")


if __name__ == "__main__":
    main()