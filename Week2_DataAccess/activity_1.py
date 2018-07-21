import pandas as pd


def read_csv(csv_file):
    return pd.read_csv(csv_file)


def write_csv(dataframe, file):
    dataframe.to_csv(file, sep=',', encoding='utf-8')


def print_dataframe(df, print_colum=True, print_rows=True):
    # print column names
    if print_colum:
        print(",".join([column for column in df]))

    # print rows one by one
    if print_rows:
        for index, row in df.iterrows():
            print(",".join([str(row[column]) for column in df]))


if __name__ == '__main__':
    csv_file = '../datasets/Demographic_Statistics_By_Zip_Code.csv'
    dataframe = read_csv(csv_file)
    print_dataframe(dataframe)
    write_csv(dataframe, "../datasets/Demographic_Statistics.csv")
