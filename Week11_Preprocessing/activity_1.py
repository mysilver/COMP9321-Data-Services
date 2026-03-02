import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score


def load_exposure(exposure_path: str,
                  test_size: float = 0.3,
                  random_state: int = 42):
    """
    Load and preprocess the exposure dataset.

    Steps:
    - Read CSV
    - Select relevant columns
    - Clean numeric columns
    - Encode categorical features
    - Split into train/test sets

    :param exposure_path: Path to CSV file
    :param test_size: Fraction used for test set
    :param random_state: Seed for reproducibility
    :return: X_train, X_test, y_train, y_test
    """

    # Load dataset (limit to first 2000 rows for performance)
    df = pd.read_csv(
        exposure_path,
        delimiter=";",
        encoding="ISO-8859-1"
    ).head(2000)

    # Keep only relevant columns
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

    # Remove rows where target label is missing
    df = df[df['Income classification according to WB'].notna()]

    # Columns that must be numeric
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
            .replace("x", np.nan)          # Replace 'x' with NaN
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Encode categorical column 'GHRP'
    df['GHRP'] = df['GHRP'].fillna("Unknown")
    encoder = OrdinalEncoder()
    df['GHRP'] = encoder.fit_transform(df[['GHRP']])

    # Replace remaining NaN values with 0
    df = df.fillna(0)

    # Separate features and target
    X = df.drop('Income classification according to WB', axis=1).values
    y = df['Income classification according to WB'].values

    # Train/test split (shuffled & reproducible)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )

    return X_train, X_test, y_train, y_test


def main():
    csv_file = 'exposure.csv'

    # Load and split dataset
    X_train, X_test, y_train, y_test = load_exposure(csv_file)

    # Initialize Decision Tree classifier
    model = DecisionTreeClassifier(random_state=42)

    # Train model
    model.fit(X_train, y_train)

    # Predict on test set
    predictions = model.predict(X_test)

    # Evaluate performance
    print("Model Performance:")
    print("Accuracy:\t", accuracy_score(y_test, predictions))
    print("Precision:\t", precision_score(y_test, predictions, average=None))
    print("Recall:\t\t", recall_score(y_test, predictions, average=None))


if __name__ == "__main__":
    main()