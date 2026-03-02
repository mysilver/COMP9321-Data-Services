import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score


def load_iris(iris_path: str, test_size: float = 0.3, random_state: int = 42):
    """
    Load the Iris dataset from CSV and split into training and test sets.

    :param iris_path: Path to the CSV file containing Iris dataset
    :param test_size: Fraction of the dataset to be used as test set
    :param random_state: Seed for reproducibility
    :return: X_train, X_test, y_train, y_test
    """
    # Load CSV data into a DataFrame
    df = pd.read_csv(iris_path)

    # Separate features and target labels
    X = df.drop('species', axis=1).values  # Features
    y = df['species'].values               # Labels

    # Split into training and test sets with random shuffling
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True
    )
    return X_train, X_test, y_train, y_test


def main():
    csv_file = 'iris.csv'

    # Load data and split into training and test sets
    X_train, X_test, y_train, y_test = load_iris(csv_file, test_size=0.3)

    # Initialize K-Nearest Neighbors classifier
    knn = KNeighborsClassifier(n_neighbors=5)  # You can adjust n_neighbors

    # Train the classifier on the training set
    knn.fit(X_train, y_train)

    # Predict labels for the test set
    predictions = knn.predict(X_test)

    # Evaluate classifier performance
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    print("Precision (per class):\t", precision_score(y_test, predictions, average=None))
    print("Recall (per class):\t", recall_score(y_test, predictions, average=None))
    print("Overall Accuracy:\t", accuracy_score(y_test, predictions))


if __name__ == "__main__":
    main()