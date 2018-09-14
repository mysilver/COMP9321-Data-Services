import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import shuffle


def load_iris(iris_path, split_percentage):
    df = pd.read_csv(iris_path)

    df = shuffle(df)
    iris_x = df.drop('species', axis=1).values
    iris_y = df['species'].values

    # Split iris data in train and test data
    # A random permutation, to split the data randomly

    split_point = int(len(iris_x) * split_percentage)
    iris_X_train = iris_x[:split_point]
    iris_y_train = iris_y[:split_point]
    iris_X_test = iris_x[split_point:]
    iris_y_test = iris_y[split_point:]

    return iris_X_train, iris_y_train, iris_X_test, iris_y_test


if __name__ == '__main__':

    csv_file = 'iris.csv'
    iris_X, iris_y, _, _ = load_iris(csv_file, split_percentage=1)

    classifiers = [KNeighborsClassifier(),
                   DecisionTreeClassifier(),
                   LinearDiscriminantAnalysis(),
                   LogisticRegression(),
                   GaussianNB(),
                   SVC()]

    classifier_accuracy_list = []
    for i, classifier in enumerate(classifiers):
        # split the dataset into 5 folds; then test the classifier against each fold one by one
        accuracies = cross_val_score(classifier, iris_X, iris_y, cv=5)
        classifier_accuracy_list.append((accuracies.mean(), type(classifier).__name__))

    # sort the classifiers
    classifier_accuracy_list = sorted(classifier_accuracy_list, reverse=True)
    for item in classifier_accuracy_list:
        print(item[1], ':', item[0])
