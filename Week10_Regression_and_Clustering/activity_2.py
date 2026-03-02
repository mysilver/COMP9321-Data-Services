import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.utils import shuffle


def load_iris(iris_path: str):
    """
    Load the Iris dataset from CSV, shuffle it, and separate features from labels.

    :param iris_path: Path to the CSV file containing Iris dataset
    :return: df (original dataframe), df_without_label (features only)
    """
    df = pd.read_csv(iris_path)

    # Shuffle the rows for randomness
    df = shuffle(df, random_state=42)

    # Separate features (exclude 'species' column)
    df_without_label = df.drop('species', axis=1)

    return df, df_without_label


def main():
    csv_file = 'iris.csv'

    # Load dataset
    df, df_without_label = load_iris(csv_file)

    # Fit K-Means estimator
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(df_without_label)

    # Add cluster labels to the original dataframe
    df['cluster'] = kmeans.labels_

    print("Cluster labels assigned:")
    print(df['cluster'].values)

    # Colors for clusters (can expand if more clusters)
    cluster_colors = ['blue', 'red', 'green']

    # Initialize the figure
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title("K-Means Clustering of Iris Dataset", fontsize=16)
    ax.set_xlabel("Petal Length")
    ax.set_ylabel("Petal Width")

    # Plot each cluster dynamically
    for cluster_num in range(n_clusters):
        cluster_data = df[df['cluster'] == cluster_num]
        ax.scatter(
            cluster_data['petal_length'],
            cluster_data['petal_width'],
            label=f'Cluster-{cluster_num}',
            color=cluster_colors[cluster_num],
            s=50,
            alpha=0.6
        )

    # Annotate each point with first 4 letters of species
    for _, row in df.iterrows():
        ax.annotate(
            row['species'][:4],
            (row['petal_length'], row['petal_width']),
            color='gray',
            fontsize=9,
            horizontalalignment='left',
            verticalalignment='bottom'
        )

    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()