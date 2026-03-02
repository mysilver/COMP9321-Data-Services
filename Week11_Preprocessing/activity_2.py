import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score


def load_exposure(exposure_path: str,
                  test_size: float = 0.3,
                  strategy: str = "mean",
                  random_state: int = 42):
    """
    Load and preprocess the exposure dataset.

    Steps:
    - Read CSV
    - Select relevant columns
    - Clean numeric columns
    - Encode categorical features
    - Impute missing values
    - Split into train/test sets

    :param exposure_path: Path to CSV file
    :param test_size: Fraction of dataset used for testing
    :param strategy: Imputation strategy ('mean', 'median', 'most_frequent', 'constant')
    :param random_state: Seed for reproducibility
    :return: X_train, X_test, y_train, y_test
    """

    # Load dataset (limit to first 2000 rows for performance)
    df = pd.read_csv(
        exposure_path,
        delimiter=";",
        encoding="ISO-8859-1"
    ).head(2000)

    # Select relevant columns
    df = df[[
        'GHRP',
        'Aid dependence',
        'Remittances',
        'food import dependence ',
        'primary commodity export dependence',
        'tourism as percentage of GDP',
        'tourism dependence',
        'Foreign currency reserves',
        'Foreign direct investment, net inflows percent of GDP',
        'Foreign direct investment',
        'Covid_19_Economic_exposure_index',
        'Income classification according to WB'
    ]]

    # Remove rows where target is missing
    df = df[df['Income classification according to WB'].notna()]

    # Numeric columns
    numeric_columns = [
        "Remittances",
        "Aid dependence",
        "Foreign direct investment",
        "Foreign currency reserves",
        "Foreign direct investment, net inflows percent of GDP",
        "tourism dependence",
        "tourism as percentage of GDP",
        "food import dependence ",
        "primary commodity export dependence",
        "Covid_19_Economic_exposure_index",
    ]

    # Clean numeric columns
    for col in numeric_columns:
        df[col] = (
            df[col]
            .replace("x", np.nan)
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Encode categorical column 'GHRP'
    df['GHRP'] = df['GHRP'].fillna("Unknown")
    encoder = OrdinalEncoder()
    df['GHRP'] = encoder.fit_transform(df[['GHRP']])

    # Impute missing numeric values (single imputer for all columns)
    imputer = SimpleImputer(strategy=strategy)
    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])

    # Separate features and target
    X = df.drop('Income classification according to WB', axis=1).values
    y = df['Income classification according to WB'].values

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )

    return X_train, X_test, y_train, y_test


def main():
    csv_file = 'exposure.csv'

    strategies = ["mean", "median", "most_frequent", "constant"]

    for strategy in strategies:
        print("\n" + "*" * 25, strategy.upper(), "*" * 25)

        # Load data using chosen imputation strategy
        X_train, X_test, y_train, y_test = load_exposure(
            csv_file,
            test_size=0.3,
            strategy=strategy
        )

        # Initialize classifier (reproducible)
        model = DecisionTreeClassifier(random_state=42)

        # Train model
        model.fit(X_train, y_train)

        # Predict
        predictions = model.predict(X_test)

        # Evaluate
        print("Accuracy:\t", accuracy_score(y_test, predictions))
        print("Precision:\t", precision_score(y_test, predictions, average=None))
        print("Recall:\t\t", recall_score(y_test, predictions, average=None))


if __name__ == "__main__":
    main()