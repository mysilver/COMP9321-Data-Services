import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, accuracy_score, recall_score


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

    # Split the data into test and train parts
    iris_X_train, iris_y_train, iris_X_test, iris_y_test = load_iris(csv_file, split_percentage=0.7)

    # train a classifier
    knn = KNeighborsClassifier()
    knn.fit(iris_X_train, iris_y_train)

    # predict the test set
    predictions = knn.predict(iris_X_test)

    print("confusion_matrix:\n", confusion_matrix(iris_y_test, predictions))
    print("precision:\t", precision_score(iris_y_test, predictions, average=None))
    print("recall:\t\t", recall_score(iris_y_test, predictions, average=None))
    print("accuracy:\t", accuracy_score(iris_y_test, predictions))
