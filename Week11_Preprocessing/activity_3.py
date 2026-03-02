import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score


def load_exposure(exposure_path: str,
                  test_size: float = 0.3,
                  strategy: str = "most_frequent",
                  random_state: int = 42):
    """
    Load and preprocess exposure dataset.

    Steps:
    - Read CSV
    - Select relevant columns
    - Clean numeric columns
    - Encode categorical features
    - Impute missing values
    - Split into train/test sets
    """

    df = pd.read_csv(
        exposure_path,
        delimiter=";",
        encoding="ISO-8859-1"
    ).head(2000)

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

    # Remove rows with missing target
    df = df[df['Income classification according to WB'].notna()]

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

    # Clean numeric columns safely
    for col in numeric_columns:
        df[col] = (
            df[col]
            .replace("x", np.nan)
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Encode categorical column
    df['GHRP'] = df['GHRP'].fillna("Unknown")
    encoder = OrdinalEncoder()
    df['GHRP'] = encoder.fit_transform(df[['GHRP']])

    # Impute missing numeric values (single imputer)
    imputer = SimpleImputer(strategy=strategy)
    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])

    # Split features and target
    X = df.drop('Income classification according to WB', axis=1).values
    y = df['Income classification according to WB'].values

    # Proper shuffled split
    return train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )


def evaluate_model(X_train, X_test, y_train, y_test, use_polynomial=False):
    """
    Train and evaluate Decision Tree model.
    Optionally applies polynomial feature expansion.
    """

    if use_polynomial:
        # IMPORTANT: fit only on training data (avoid data leakage)
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_train = poly.fit_transform(X_train)
        X_test = poly.transform(X_test)

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("\nWith PolynomialFeatures:" if use_polynomial else "\nWithout PolynomialFeatures:")
    print("Accuracy:\t", accuracy_score(y_test, predictions))
    print("Precision:\t", precision_score(y_test, predictions, average=None))
    print("Recall:\t\t", recall_score(y_test, predictions, average=None))


def main():
    csv_file = "exposure.csv"

    X_train, X_test, y_train, y_test = load_exposure(
        csv_file,
        test_size=0.3,
        strategy="most_frequent"
    )

    # Evaluate without polynomial features
    evaluate_model(X_train, X_test, y_train, y_test, use_polynomial=False)

    # Evaluate with polynomial features
    evaluate_model(X_train, X_test, y_train, y_test, use_polynomial=True)


if __name__ == "__main__":
    main()