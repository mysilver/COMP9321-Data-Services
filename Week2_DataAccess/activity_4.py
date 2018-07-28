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
    json_data = json_obj['data']

    # to create a dataframe we also need the name of the columns:
    columns = []
    for c in json_obj['meta']['view']['columns']:
        columns.append(c['name'])

    return pd.DataFrame(data=json_data, columns=columns)


def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))
            
            
if __name__ == '__main__':

    url = "https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json"

    print("Fetch the json")
    json_obj = get_json(url)

    print("Convert the json object to a dataframe")
    df = json_to_dataframe(json_obj)
    print_dataframe(df)
