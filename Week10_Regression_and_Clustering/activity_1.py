import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle


def load_diet(diet_path, split_percentage):
    df = pd.read_csv(diet_path, index_col=0)

    df = shuffle(df)
    diet_x = df.drop('weight6weeks', axis=1).values
    diet_y = df['weight6weeks'].values

    # Split the dataset in train and test data
    # A random permutation, to split the data randomly

    split_point = int(len(diet_x) * split_percentage)
    diet_X_train = diet_x[:split_point]
    diet_y_train = diet_y[:split_point]
    diet_X_test = diet_x[split_point:]
    diet_y_test = diet_y[split_point:]

    return diet_X_train, diet_y_train, diet_X_test, diet_y_test


if __name__ == "__main__":
    diet_X_train, diet_y_train, diet_X_test, diet_y_test = load_diet("diet.csv", split_percentage=0.7)
    model = linear_model.LinearRegression()
    # model = linear_model.BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, compute_score=False, copy_X=True,
    #                                    fit_intercept=True, lambda_1=1e-06, lambda_2=1e-06, n_iter=300,
    #                                    normalize=False, tol=0.001, verbose=False)
    model.fit(diet_X_train, diet_y_train)

    y_pred = model.predict(diet_X_test)

    for i in range(len(diet_y_test)):
        print("Expected:", diet_y_test[i], "Predicted:", y_pred[i])

    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(diet_y_test, y_pred))
