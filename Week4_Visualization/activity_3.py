import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


if __name__=='__main__':
    csv_file = 'iris.csv'
    df = pd.read_csv(csv_file)

    # for type in np.unique(df['species'].values):
    #     print type

    setosa_df = df.query('species == "setosa"')
    versicolor_df = df.query('species == "versicolor"')
    virginica_df = df.query('species == "virginica"')

    ax = setosa_df.plot.scatter(x='sepal_length', y='sepal_width', label='setosa')
    ax = versicolor_df.plot.scatter(x='sepal_length', y='sepal_width', label='versicolor', color='green', ax=ax)
    ax = virginica_df.plot.scatter(x='sepal_length', y='sepal_width', label='virginica', color='red', ax=ax)

    ax = setosa_df.plot.scatter(x='petal_length', y='petal_width', label='setosa')
    ax = versicolor_df.plot.scatter(x='petal_length', y='petal_width', label='versicolor', color='green', ax=ax)
    ax = virginica_df.plot.scatter(x='petal_length', y='petal_width', label='virginica', color='red', ax=ax)

    plt.show()
