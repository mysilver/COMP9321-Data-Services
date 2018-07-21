import pandas as pd


def print_dataframe(df, type="columns"):
    if type == "columns":
        # print column names
        for column in df:
            print(column)
    elif type == "rows":
        # print rows one by one
        for index, row in df.iterrows():
            print(row['sepal_length'], row['sepal_width'], row['petal_length'], row['petal_width'], str(row['species']))
    else:
        # print the whole dataset once
        print(df)


def read_csv():
    df = pd.read_csv('../data/iris.csv')
    print_dataframe(df)


def read_sql_database():
    import sqlite3
    conn = sqlite3.connect("../data/iris.db")
    df = pd.read_sql_query("select * from iris limit 10;", conn)
    print_dataframe(df, "rows")


def read_nosql_database():
    import pandas as pd
    from pymongo import MongoClient
    client = MongoClient('mongodb://user:comp9321@ds147461.mlab.com:47461/comp9321', )
    db = client.comp9321
    collection = db.iris
    data = pd.DataFrame(list(collection.find()))
    print_dataframe(data, "rows")


if __name__ == "__main__":
    # read_nosql_database()
    # read_csv()
    # read_sql_database()
