"""
Fetch JSON from a URL and convert to pandas DataFrame.

This script demonstrates:
1. Fetching JSON data from a remote URL
2. Inspecting and converting JSON data to a DataFrame
3. Displaying the DataFrame

Useful References:
- Requests library: https://docs.python-requests.org/en/latest/
- Pandas DataFrame from JSON: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_records.html
"""

from typing import Any, Dict
import requests
import pandas as pd


def get_json(url: str) -> Any:
    """
    Fetch JSON data from a URL.

    Parameters
    ----------
    url : str
        The URL of the JSON resource.

    Returns
    -------
    dict | list
        JSON data parsed into Python objects.

    Raises
    ------
    requests.exceptions.RequestException
        If the HTTP request failed.
    ValueError
        If the response content is not valid JSON.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch URL {url}: {e}")
    except ValueError:
        raise ValueError("Response content is not valid JSON")


def json_to_dataframe(json_obj: Any, data_key: str = None) -> pd.DataFrame:
    """
    Convert JSON data to a pandas DataFrame.

    Parameters
    ----------
    json_obj : dict | list
        JSON object to convert.
    data_key : str, optional
        If the JSON root contains multiple keys, specify the key containing the data.
        Default is None (uses the root if it's a list of records).

    Returns
    -------
    pd.DataFrame
        DataFrame representing the JSON data.

    Notes
    -----
    - If JSON contains nested structures, you might need to flatten it.
    - You can inspect the JSON using `json.dumps(json_obj, indent=2)` to understand its structure.
    """
    # If a specific key is provided, extract that sublist
    if data_key is not None:
        if data_key in json_obj:
            records = json_obj[data_key]
        else:
            raise KeyError(f"Key '{data_key}' not found in JSON object")
    else:
        records = json_obj

    # Use pandas built-in from_records to convert list of dicts to DataFrame
    return pd.DataFrame.from_records(records)


def main() -> None:
    url = "https://raw.githubusercontent.com/joseluisq/json-datasets/master/json/operating-systems/macosx_releases.json"

    # Step 1: Fetch JSON data
    print("Step 1: Fetching JSON data...")
    json_obj = get_json(url)

    # Optional: Inspect the structure (uncomment if needed)
    # import json
    # print(json.dumps(json_obj, indent=2))

    # Step 2: Convert JSON to DataFrame
    # Note: For this dataset, root is a list of dicts, so no key is required
    print("Step 2: Converting JSON to DataFrame...")
    df = json_to_dataframe(json_obj)

    # Step 3: Display the DataFrame
    pd.set_option("display.max_rows", 20)
    pd.set_option("display.max_columns", None)
    print(df.to_string())


if __name__ == "__main__":
    main()