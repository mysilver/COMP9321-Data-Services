"""
Books REST API using Flask and pandas

This API serves book details from a CSV file and allows:
1. Retrieving a book by its ID (GET).
2. Deleting a book by its ID (DELETE).

Data preprocessing:
- Drops unnecessary columns.
- Cleans and converts publication year.
- Replaces spaces in column names.
- Sets 'Identifier' as the index.

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

# Load CSV
df = pd.read_csv(csv_file)

# Drop unnecessary columns
df.drop(columns=columns_to_drop, inplace=True)

# Extract 4-digit year from 'Date of Publication', convert to int, fill missing with 0
df['Date of Publication'] = (
    df['Date of Publication']
    .str.extract(r'^(\d{4})', expand=False)
    .fillna(0)
    .astype(int)
)

# Replace spaces in column names with underscores
df.columns = df.columns.str.replace(' ', '_', regex=False)

# Set 'Identifier' as index for fast lookup
df.set_index('Identifier', inplace=True)

# -------------------------
# API Endpoints
# -------------------------
@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id: int):
        """
        GET /books/<id>
        Retrieve a book by its Identifier.
        Returns 404 if the book does not exist.
        """
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")

        return df.loc[id].to_dict()

    def delete(self, id: int):
        """
        DELETE /books/<id>
        Remove a book by its Identifier.
        Returns 404 if the book does not exist.
        """
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")

        # Drop the book row from the DataFrame
        df.drop(id, inplace=True)
        return {"message": f"Book {id} has been removed."}, 200

# -------------------------
# Run Flask application
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)