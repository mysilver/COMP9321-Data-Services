import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    csv_file = 'iris.csv'
    df = pd.read_csv(csv_file)

    df = df.groupby('species').mean()
    df.plot.bar()

    plt.show()
