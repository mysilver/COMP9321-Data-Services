import pandas as pd


def read_csv(csv_file: str):
    """
    :param csv_file: the path of csv file
    :return: A dataframe out of the csv file
    """
    return pd.read_csv(csv_file)


def write_in_csv(dataframe, file) -> None:
    """
    :param dataframe: The dataframe which must be written into a csv file
    :param file: where the csv must be stored
    """
    dataframe.to_csv(file, sep=',', encoding='utf-8')


def print_dataframe(df, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in df]))

    # print rows one by one
    if print_rows:
        for index, row in df.iterrows():
            print(",".join([str(row[column]) for column in df]))


if __name__ == '__main__':
    csv_file = '../datasets/Demographic_Statistics_By_Zip_Code.csv'
    dataframe = read_csv(csv_file)

    print("Loading the csv file")
    print_dataframe(dataframe)

    print("Write the dataframe as a csv file")
    write_in_csv(dataframe, "../datasets/Demographic_Statistics.csv")
