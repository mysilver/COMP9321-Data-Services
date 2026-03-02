import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.utils import shuffle


def load_dataset(dataset_path: str):
    """
    Load the dataset from CSV, shuffle it, and separate features from labels.

    :param dataset_path: Path to the CSV file
    :return: df (original dataframe), df_without_label (features only)
    """
    # Load CSV into DataFrame
    df = pd.read_csv(dataset_path)

    # Shuffle rows for randomness (reproducible)
    df = shuffle(df, random_state=42)

    # Separate clustering features (exclude 'Diet' label column)
    df_without_label = df.drop('Diet', axis=1)

    return df, df_without_label


def main():
    csv_file = 'diet.csv'

    # Load dataset
    df, df_without_label = load_dataset(csv_file)

    # Initialize clustering algorithm
    n_clusters = 3
    model = AgglomerativeClustering(n_clusters=n_clusters)

    # Fit model and get cluster labels
    labels = model.fit_predict(df_without_label)

    # Add cluster labels to original dataframe
    df['cluster'] = labels

    print("Cluster labels assigned:")
    print(labels)

    # Define cluster colors (expandable if needed)
    cluster_colors = ['blue', 'red', 'green']

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title("Agglomerative Clustering on Diet Dataset", fontsize=16)
    ax.set_xlabel("Pre Weight")
    ax.set_ylabel("Weight After 6 Weeks")

    # Plot clusters dynamically
    for cluster_id in range(n_clusters):
        cluster_data = df[df['cluster'] == cluster_id]

        ax.scatter(
            cluster_data['pre.weight'],
            cluster_data['weight6weeks'],
            label=f'Cluster-{cluster_id}',
            color=cluster_colors[cluster_id],
            s=60,
            alpha=0.7
        )

    # Annotate each point with its Diet label
    for _, row in df.iterrows():
        ax.annotate(
            f"Diet_{row['Diet']}",
            (row['pre.weight'], row['weight6weeks']),
            color='gray',
            fontsize=8,
            horizontalalignment='left',
            verticalalignment='bottom'
        )

    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()