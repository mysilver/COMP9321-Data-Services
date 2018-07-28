import json
import pandas as pd
from pymongo import MongoClient


def read_csv(csv_file):
    """
    :param csv_file: the path of csv file
    :return: A dataframe out of the csv file
    """
    return pd.read_csv(csv_file)


def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))


def write_in_mongodb(dataframe, mongo_host, mongo_port, db_name, collection):
    """
    :param dataframe: 
    :param mongo_host: Mongodb server address 
    :param mongo_port: Mongodb server port number
    :param db_name: The name of the database
    :param collection: the name of the collection inside the database
    """
    client = MongoClient(host=mongo_host, port=mongo_port)
    db = client[db_name]
    c = db[collection]
    # You can only store documents in mongodb;
    # so you need to convert rows inside the dataframe into a list of json objects
    records = json.loads(dataframe.T.to_json()).values()
    c.insert(records)


def read_from_mongodb(mongo_host, mongo_port, db_name, collection):
    """
    :param mongo_host: Mongodb server address 
    :param mongo_port: Mongodb server port number
    :param db_name: The name of the database
    :param collection: the name of the collection inside the database
    :return: A dataframe which contains all documents inside the collection
    """
    client = MongoClient(host=mongo_host, port=mongo_port)
    db = client[db_name]
    c = db[collection]
    return pd.DataFrame(list(c.find()))


if __name__ == '__main__':

    db_name = 'comp9321'
    mongo_port = 27017
    mongo_host = 'localhost'

    csv_file = 'Demographic_Statistics_By_Zip_Code.csv'  # path to the downloaded csv file
    df = read_csv(csv_file)
    collection = 'Demographic_Statistics'

    print("Writing into the mongodb")
    write_in_mongodb(df, mongo_host, mongo_port, db_name, collection)

    print("Querying the database")
    df = read_from_mongodb(mongo_host, mongo_port, db_name, collection)

    print_dataframe(df)
