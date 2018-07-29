import matplotlib.pyplot as plt
import pandas as pd


def clean(df):
    # Let's Clean the data to get rid of exceptions
    df['Place of Publication'] = df['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))
    return df


if __name__ == '__main__':
    csv_file = 'Books.csv'
    df = pd.read_csv(csv_file)

    # Cleaning is Optional; but it will increase the accuracy of the results
    df = clean(df)

    # value_counts: returns a Series containing counts of each category.
    unival = df['Place of Publication'].value_counts()
    unival.plot.pie(subplots=True)

    plt.show()
