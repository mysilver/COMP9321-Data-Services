import sqlite3
from pandas.io import sql
from Week2_DataAccess.activity_1 import read_csv


def create_sql_database(dataframe, database_file, db_name):
    cnx = sqlite3.connect(database_file)
    sql.to_sql(dataframe, name=db_name, con=cnx)


def read_from_sqlite(database_file, db_name):
    cnx = sqlite3.connect(database_file)
    return sql.read_sql('select * from ' + db_name, cnx)


if __name__ == '__main__':
    db_name = "Demographic_Statistics"
    database_file = '../datasets/Demographic_Statistics.db'
    csv_file = '../datasets/Demographic_Statistics_By_Zip_Code.csv'
    df = read_csv(csv_file)
    print("Creating database")
    create_sql_database(csv_file, database_file, db_name)

    print("Querying the database")
    df = read_from_sqlite(database_file, db_name)
