import json


def create_sql_database():
    import sqlite3
    from pandas.io import sql
    import pandas as pd
    df = pd.read_csv('../data/iris.csv')
    cnx = sqlite3.connect('sqlite://../iris.db')
    sql.to_sql(df, name='iris', con=cnx)
    p2 = sql.read_sql('select * from iris', cnx)
    print p2


def create_nosql_database():
    import pandas as pd
    df = pd.read_csv('../data/iris.csv')
    from pymongo import MongoClient
    client = MongoClient('mongodb://user:comp9321@ds147461.mlab.com:47461/comp9321', )
    db = client.comp9321
    collection = db.iris
    records = json.loads(df.T.to_json()).values()
    collection.insert(records)

create_nosql_database()