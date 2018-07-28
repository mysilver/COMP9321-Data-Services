import pandas as pd


def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))


if __name__ == "__main__":
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)

    print("The percentage of nan in the data per column:")
    num_of_rows = df.shape[0]
    for column in df:
        percent = 100 * df[column].isnull().sum() / num_of_rows
        print(column, str(percent) + '%')

    print("****************************************")
    print("Dataframe before dropping the columns")
    print_dataframe(df)

    print("****************************************")
    print("Dataframe after dropping the columns")
    df.drop(columns_to_drop, inplace=True, axis=1)
    print_dataframe(df)
    print("****************************************")
