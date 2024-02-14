import pandas as pd


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

    print("The percentage of NaN in the data per column:")
    num_of_rows = df.shape[0]
    for column in df:
        # df[column].isnull() : returns an array of True/False showing the cell is null or not
        percent = 100 * df[column].isnull().sum() / num_of_rows
        print(column, str(percent) + '%')

    print("****************************************")
    print("Dataframe before dropping the columns")
    print(df.to_string())

    print("****************************************")
    print("Dataframe after dropping the columns")
    df.drop(columns_to_drop, inplace=True, axis=1)
    # Pandas' drop method is used to remove columns of a dataframe
    # Inplace=True indicates that the changes should be applied to the given dataframe instead of creating a new one
    # axis=1 : Whether to drop labels from the index (0 / 'index') or columns (1 / 'columns').

    print(df.to_string())
    print("****************************************")
