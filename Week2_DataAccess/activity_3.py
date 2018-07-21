import json
import pandas as pd
from pymongo import MongoClient
from Week2_DataAccess.activity_1 import read_csv, print_dataframe


def write_in_mongodb(dataframe, connection_url: str, db_name: str, collection: str) -> None:
    """
    :param dataframe: 
    :param connection_url: A connection string for the database 
    :param db_name: The name of the database
    :param collection: the name of the collection inside the database
    """
    client = MongoClient(connection_url)
    db = client[db_name]
    c = db[collection]
    # You can only store documents in mongodb;
    # so you need to convert rows inside the dataframe into a list of json objects
    records = json.loads(dataframe.T.to_json()).values()
    c.insert(records)


def read_from_mongodb(connection_url: str, db_name: str, collection: str):
    """
    :param connection_url: A connection string for the database 
    :param db_name: The name of the database
    :param collection: the name of the collection inside the database
    :return: A dataframe which contains all documents inside the collection
    """
    client = MongoClient(connection_url)
    db = client[db_name]
    c = db[collection]
    return pd.DataFrame(list(c.find()))


if __name__ == '__main__':
    """
    # the following information is needed when you use mLab.com instead of a local mongodb instance
    # We highly encourage you to use mLab to be familiar with the concept of Database as a Service
    # Moreover, in this case, you do not need to install mongodb on your own machine!
    # However, connecting to a local mongodb is a bit more straightforward than the following code!
    """

    user = 'user'
    password = 'comp9321'
    db_name = 'comp9321'
    connection_url = 'mongodb://' + user + ':' + password + '@ds147461.mlab.com:47461/' + db_name

    csv_file = '../datasets/Demographic_Statistics_By_Zip_Code.csv'
    df = read_csv(csv_file)
    collection = 'Demographic_Statistics'

    print("Writing into the mongodb")
    write_in_mongodb(df, connection_url, db_name, collection)

    print("Querying the database")
    df = read_from_mongodb(connection_url, db_name, collection)

    print_dataframe(df)
