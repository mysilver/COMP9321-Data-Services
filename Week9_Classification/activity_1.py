import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def load_iris(iris_path: str, test_size: float = 0.3, random_state: int = 42):
    """
    Load the Iris dataset from a CSV file and split it into training and test sets.

    :param iris_path: Path to the CSV file containing the Iris dataset
    :param test_size: Fraction of data to be used as test set (default 0.3)
    :param random_state: Random seed for reproducibility (default 42)
    :return: X_train, X_test, y_train, y_test
    """
    # Load CSV into a DataFrame
    df = pd.read_csv(iris_path)

    # Separate features (X) and target labels (y)
    X = df.drop('species', axis=1).values  # Features: all columns except 'species'
    y = df['species'].values               # Labels: the 'species' column

    # Split data into training and test sets with random shuffling
    # Returns X_train, X_test, y_train, y_test
    return train_test_split(X, y, test_size=test_size, random_state=random_state, shuffle=True)


def main():
    csv_file = 'iris.csv'

    # Load data and split into training and test sets
    X_train, X_test, y_train, y_test = load_iris(csv_file, test_size=0.3)

    # Initialize the K-Nearest Neighbors classifier
    knn = KNeighborsClassifier(n_neighbors=5)

    # Train the classifier on the training data
    knn.fit(X_train, y_train)

    # Predict the labels for the test set
    predictions = knn.predict(X_test)

    # Print the actual labels
    print("Actual labels:")
    print(y_test)

    # Print the predicted labels
    print("\nPredictions:")
    print(predictions)

    # Evaluate the classifier by calculating accuracy
    acc = accuracy_score(y_test, predictions)
    print(f"\nAccuracy: {acc:.2f}")


if __name__ == "__main__":
    main()