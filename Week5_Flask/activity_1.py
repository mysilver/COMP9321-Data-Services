"""
Books REST API using Flask and pandas

This API serves book details from a CSV file. It performs the following:
1. Reads the CSV using pandas.
2. Cleans unnecessary columns.
3. Extracts and cleans the publication year.
4. Exposes a GET endpoint to fetch book details by ID.

References:
- pandas documentation: https://pandas.pydata.org/docs/
- Flask RESTx documentation: https://flask-restx.readthedocs.io/en/latest/
"""

import pandas as pd
from flask import Flask
from flask_restx import Resource, Api

# -------------------------
# Flask & API Setup
# -------------------------
app = Flask(__name__)
api = Api(app)

# -------------------------
# Load and preprocess data
# -------------------------
csv_file = "Books.csv"

# Columns to drop from the dataset
columns_to_drop = [
    'Edition Statement',
    'Corporate Author',
    'Corporate Contributors',
    'Former owner',
    'Engraver',
    'Contributors',
    'Issuance type',
    'Shelfmarks'
]

# Load CSV using pandas
df = pd.read_csv(csv_file)

# Drop unnecessary columns
df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

# Replace spaces in column names with underscores
df.columns = df.columns.str.replace(' ', '_', regex=False)

# Extract 4-digit year from 'Date of Publication' and convert to numeric
# Any missing or invalid years will be replaced with 0
df['Date_of_Publication'] = (
    df['Date_of_Publication']
    .str.extract(r'^(\d{4})', expand=False)  # Extract 4-digit year
    .astype(float)                           # Convert to numeric
    .fillna(0)                               # Fill missing values with 0
    .astype(int)                             # Optional: make integer
)


# Set the 'Identifier' column as the DataFrame index for fast lookup
df.set_index('Identifier', inplace=True)

# -------------------------
# API Endpoint
# -------------------------
@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id: int):
        """
        GET /books/<id>
        Retrieve a book by its Identifier.
        Returns a 404 error if the book does not exist.
        """
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")

        # Convert the row to dictionary and return
        return df.loc[id].to_dict()

# -------------------------
# Run Flask application
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)