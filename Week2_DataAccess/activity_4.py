import requests
import pandas as pd


def get_json(url):
    """
    :param url: RUL of the resouce
    :return: JSON
    """
    resp = requests.get(url=url)
    data = resp.json()
    return data


def json_to_dataframe(json_obj):
    """
    Please Open the JSON using the given URL to be familiar with the 
    structure of the expected JSON object
    
    The root element contains two main elements : data and meta; 
    the former contains the statistics for a given zip code, and 
    the latter contains the information about the columns
    :param json_obj: JSON object for the dataset
    :return: A dataframe
    """
    # let's get the list of statistics for all zip codes
    json_data = json_obj

    return pd.DataFrame.from_records(json_data)

if __name__ == '__main__':
    url = "https://raw.githubusercontent.com/joseluisq/json-datasets/master/json/operating-systems/macosx_releases.json"

    print("Fetch the json")
    json_obj = get_json(url)

    print("Convert the json object to a dataframe")
    df = json_to_dataframe(json_obj)
    print(df.to_string())
