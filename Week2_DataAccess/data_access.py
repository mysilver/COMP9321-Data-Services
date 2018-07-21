import pandas as pd







def read_sql_database():
    import sqlite3
    conn = sqlite3.connect("../datasets/Demographic_Statistics_By_Zip_Code.db")
    df = pd.read_sql_query("select * from iris limit 10;", conn)
    print_dataframe(df)


def read_nosql_database():
    import pandas as pd
    from pymongo import MongoClient
    client = MongoClient('mongodb://user:comp9321@ds147461.mlab.com:47461/comp9321', )
    db = client.comp9321
    collection = db.iris
    data = pd.DataFrame(list(collection.find()))
    print_dataframe(data)


if __name__ == "__main__":
    read_csv()
    read_nosql_database()
    read_sql_database()
