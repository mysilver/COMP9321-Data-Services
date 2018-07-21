import json


def create_sql_database():
    import sqlite3
    from pandas.io import sql
    import pandas as pd
    df = pd.read_csv('../datasets/Demographic_Statistics_By_Zip_Code.csv')
    cnx = sqlite3.connect('../datasets/Demographic_Statistics.db')
    sql.to_sql(df, name='Demographic_Statistics', con=cnx)
    p2 = sql.read_sql('select * from Demographic_Statistics', cnx)
    from Week2_DataAccess import data_access
    data_access.print_dataframe(p2)


def create_nosql_database():
    import pandas as pd
    df = pd.read_csv('../datasets/Demographic_Statistics_By_Zip_Code.csv')
    from pymongo import MongoClient
    client = MongoClient('mongodb://user:comp9321@ds147461.mlab.com:47461/comp9321', )
    db = client.comp9321
    collection = db.Demographic_Statistics
    records = json.loads(df.T.to_json()).values()
    collection.insert(records)


if __name__ == "__main__":
    # create_sql_database()
    create_nosql_database()
