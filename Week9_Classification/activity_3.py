import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


def load_iris(iris_path: str):
    """
    Load the Iris dataset from CSV and return features and labels.

    :param iris_path: Path to the CSV file containing the Iris dataset
    :return: X (features), y (labels)
    """
    df = pd.read_csv(iris_path)

    # Features are all columns except 'species'; labels are in 'species'
    X = df.drop('species', axis=1).values
    y = df['species'].values

    return X, y


def main():
    csv_file = 'iris.csv'

    # Load dataset
    X, y = load_iris(csv_file)

    # List of classifiers to evaluate
    classifiers = [
        KNeighborsClassifier(n_neighbors=5),
        DecisionTreeClassifier(),
        LinearDiscriminantAnalysis(),
        LogisticRegression(max_iter=200),
        GaussianNB(),
        SVC()
    ]

    # Metrics to evaluate
    scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']

    results = []

    # Evaluate each classifier using 5-fold cross-validation
    for clf in classifiers:
        # cross_validate returns a dict with keys like 'test_accuracy', 'test_precision_macro', etc.
        cv_results = cross_validate(clf, X, y, cv=5, scoring=scoring_metrics)

        # Compute mean for each metric across folds
        mean_accuracy = cv_results['test_accuracy'].mean()
        mean_precision = cv_results['test_precision_macro'].mean()
        mean_recall = cv_results['test_recall_macro'].mean()
        mean_f1 = cv_results['test_f1_macro'].mean()

        # Save results with classifier name
        results.append({
            'Classifier': type(clf).__name__,
            'Accuracy': mean_accuracy,
            'Precision': mean_precision,
            'Recall': mean_recall,
            'F1-Score': mean_f1
        })

    # Sort classifiers by accuracy
    results = sorted(results, key=lambda x: x['Accuracy'], reverse=True)

    # Display results
    print("Classifier performance (5-fold cross-validation):")
    for r in results:
        print(f"{r['Classifier']:25s} | "
              f"Accuracy: {r['Accuracy']:.4f} | "
              f"Precision: {r['Precision']:.4f} | "
              f"Recall: {r['Recall']:.4f} | "
              f"F1-Score: {r['F1-Score']:.4f}")


if __name__ == "__main__":
    main()