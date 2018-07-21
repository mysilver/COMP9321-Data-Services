import json




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
