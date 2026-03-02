import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def load_diet(diet_path: str, test_size: float = 0.3, random_state: int = 42):
    """
    Load the diet dataset from CSV and split into training and test sets.

    :param diet_path: Path to the CSV file
    :param test_size: Fraction of data to use as test set
    :param random_state: Seed for reproducibility
    :return: X_train, X_test, y_train, y_test
    """
    # Load CSV file; index_col=0 assumes first column is an index
    df = pd.read_csv(diet_path, index_col=0)

    # Separate features (all columns except 'weight6weeks') and target
    X = df.drop('weight6weeks', axis=1).values
    y = df['weight6weeks'].values

    # Split dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True
    )

    return X_train, X_test, y_train, y_test


def main():
    csv_file = "diet.csv"

    # Load dataset and split
    X_train, X_test, y_train, y_test = load_diet(csv_file, test_size=0.3)

    # Initialize the linear regression model
    model = LinearRegression()
    # Alternative: BayesianRidge can be used by uncommenting the lines below
    # from sklearn.linear_model import BayesianRidge
    # model = BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, lambda_1=1e-06, lambda_2=1e-06, n_iter=300)

    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Print expected vs predicted values
    print("Expected vs Predicted values:")
    for actual, predicted in zip(y_test, y_pred):
        print(f"Expected: {actual:.2f}, Predicted: {predicted:.2f}")

    # Calculate and print mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print(f"\nMean Squared Error: {mse:.2f}")


if __name__ == "__main__":
    main()