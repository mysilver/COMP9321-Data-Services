import json
import pandas as pd
from pymongo import MongoClient
from Week2_DataAccess.activity_1 import read_csv, print_dataframe


def write_in_mongodb(dataframe, connection_url, db_name, collection):
    client = MongoClient(connection_url)
    db = client[db_name]
    c = db[collection]
    records = json.loads(dataframe.T.to_json()).values()
    c.insert(records)


def read_from_mongodb(connection_url, db_name, collection):
    client = MongoClient(connection_url)
    db = client[db_name]
    c = db[collection]
    return pd.DataFrame(list(c.find()))


if __name__ == '__main__':
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
