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
    books_df = pd.read_csv(csv_file)
    books_df = clean(books_df)
    # Replace the spaces with the underline character ('_')
    # Because panda's query method does not work well with column names which contains white spaces
    books_df.columns = [c.replace(' ', '_') for c in books_df.columns]

    city_df = pd.read_csv('City.csv')

    # merge the two dataframes
    df = pd.merge(books_df, city_df, how='left', left_on=['Place_of_Publication'], right_on=['City'])

    # Group by Country and keep the country as a column
    gb_df = df.groupby(['Country'], as_index=False)

    # Select a column (as far as it has values for all rows, you can select any column)
    df = gb_df['Identifier'].count()

    # print the dataframe which shows publication number by country
    print_dataframe(df)
