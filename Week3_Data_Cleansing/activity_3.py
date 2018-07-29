import pandas as pd


def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))


def clean(dataframe):
    dataframe['Place of Publication'] = dataframe['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))

    new_date = dataframe['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    dataframe['Date of Publication'] = new_date

    return dataframe


if __name__ == "__main__":
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)
    df = clean(df)

    # Replace the spaces with the underline character ('_')
    # Because panda's query method does not work well with column names which contains white spaces
    df.columns = [c.replace(' ', '_') for c in df.columns]

    #
    df = df.query('Date_of_Publication > 1866 and Place_of_Publication == "London"')

    print_dataframe(df)


