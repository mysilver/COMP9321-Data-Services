import sqlite3
from pandas.io import sql
from Week2_DataAccess.activity_1 import read_csv


def write_in_sqlite(dataframe, database_file: str, table_name: str) -> None:
    """
    :param dataframe: The dataframe which must be written into the database
    :param database_file: where the database is stored
    :param table_name: the name of the table
    """

    cnx = sqlite3.connect(database_file)
    sql.to_sql(dataframe, name=table_name, con=cnx)


def read_from_sqlite(database_file: str, table_name: str):
    """
    :param database_file: where the database is stored
    :param table_name: the name of the table
    :return: A Dataframe
    """
    cnx = sqlite3.connect(database_file)
    return sql.read_sql('select * from ' + table_name, cnx)


if __name__ == '__main__':
    table_name = "Demographic_Statistics"
    database_file = '../datasets/Demographic_Statistics.db'
    csv_file = '../datasets/Demographic_Statistics_By_Zip_Code.csv'
    df = read_csv(csv_file)

    print("Creating database")
    write_in_sqlite(csv_file, database_file, table_name)

    print("Querying the database")
    df = read_from_sqlite(database_file, table_name)
