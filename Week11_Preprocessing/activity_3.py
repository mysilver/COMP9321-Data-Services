import numpy
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import precision_score, accuracy_score, recall_score
from sklearn.preprocessing import OrdinalEncoder, PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier


def load_exposure(exposure_path, split_percentage, strategy):
    df = pd.read_csv(exposure_path, delimiter=";", encoding="ISO-8859-1").head(2000)

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
    columns = ["Remittances", "Aid dependence", "Foreign direct investment", 'Foreign currency reserves',
               'Foreign direct investment, net inflows percent of GDP', 'tourism dependence',
               'tourism as percentage of GDP', 'food import dependence ',
               'primary commodity export dependence',
               'Covid_19_Economic_exposure_index', ]

    df = df[df['Income classification according to WB'].notna()]

    for column in columns:
        df[column] = df[column].apply(lambda a: numpy.nan if a == "x" else float(str(a).replace(",", ".")))

    # Ordinal Encoders
    encGhrp = OrdinalEncoder()
    df['GHRP'] = df['GHRP'].fillna("Unknown")
    df['GHRP'] = encGhrp.fit_transform(df[['GHRP']])

    for column in columns:
        imputer = SimpleImputer(missing_values=numpy.nan, strategy=strategy)
        df[column] = imputer.fit_transform(df[[column]])

    exposure_x = df.drop('Income classification according to WB', axis=1).values
    exposure_y = df['Income classification according to WB'].values

    # Split exposure data in train and test data
    split_point = int(len(exposure_x) * split_percentage)
    exposure_X_train = exposure_x[:split_point]
    exposure_y_train = exposure_y[:split_point]
    exposure_X_test = exposure_x[split_point:]
    exposure_y_test = exposure_y[split_point:]

    return exposure_X_train, exposure_y_train, exposure_X_test, exposure_y_test


if __name__ == '__main__':
    csv_file = 'exposure.csv'

    # Split the data into test and train parts
    exposure_X_train, exposure_y_train, exposure_X_test, exposure_y_test \
        = load_exposure(csv_file, split_percentage=0.7, strategy="most_frequent")

    # train a classifier
    dt = DecisionTreeClassifier()
    dt.fit(exposure_X_train, exposure_y_train)

    # predict the test set
    predictions = dt.predict(exposure_X_test)

    print("*************************** without PolynomialFeatures ***********************************")
    print("precision:\t", precision_score(exposure_y_test, predictions, average=None))
    print("recall:\t\t", recall_score(exposure_y_test, predictions, average=None))
    print("accuracy:\t", accuracy_score(exposure_y_test, predictions))

    poly = PolynomialFeatures(1)
    exposure_X_train_scaled = poly.fit_transform(exposure_X_train)
    exposure_X_test_scaled = poly.fit_transform(exposure_X_test)
    dt = DecisionTreeClassifier()
    dt.fit(exposure_X_train_scaled, exposure_y_train)
    predictions = dt.predict(exposure_X_test_scaled)

    print("*************************** with PolynomialFeatures ***********************************")
    print("precision:\t", precision_score(exposure_y_test, predictions, average=None))
    print("recall:\t\t", recall_score(exposure_y_test, predictions, average=None))
    print("accuracy:\t", accuracy_score(exposure_y_test, predictions))