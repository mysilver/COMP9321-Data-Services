"""
Books REST API using Flask and pandas

Features:
- GET /books/<id>      : Retrieve a book by its Identifier.
- DELETE /books/<id>   : Remove a book by its Identifier.
- PUT /books/<id>      : Update a book by its Identifier.
- GET /books           : get all books

Data preprocessing:
- Drops unnecessary columns
- Cleans and converts publication year
- Replaces spaces in column names
- Sets 'Identifier' as the index

References:
- pandas documentation: https://pandas.pydata.org/docs/
- Flask RESTx documentation: https://flask-restx.readthedocs.io/en/latest/
"""

import pandas as pd
from flask import Flask, request
from flask_restx import Resource, Api, fields

# -------------------------
# Flask & API Setup
# -------------------------
app = Flask(__name__)
api = Api(app)

# -------------------------
# Book Model Schema
# -------------------------
book_model = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})

# -------------------------
# Load & preprocess CSV
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
# API Endpoints
# -------------------------
@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id: int):
        """Retrieve a book by its Identifier."""
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")
        return df.loc[id].to_dict()

    def delete(self, id: int):
        """Delete a book by its Identifier."""
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")
        df.drop(id, inplace=True)
        return {"message": f"Book {id} has been removed."}, 200

    @api.expect(book_model)
    def put(self, id: int):
        """Update a book by its Identifier."""
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")

        book_data = request.json

        # Ensure Identifier cannot be changed
        if 'Identifier' in book_data and book_data['Identifier'] != id:
            return {"message": "Identifier cannot be changed"}, 400

        # Validate keys
        invalid_keys = [k for k in book_data if k not in book_model.keys()]
        if invalid_keys:
            return {"message": f"Invalid properties: {', '.join(invalid_keys)}"}, 400

        # Update book row efficiently using pandas
        df.loc[id] = pd.Series(book_data)
        return {"message": f"Book {id} has been successfully updated"}, 200

import json
from flask_restx import reqparse, inputs

# -------------------------
# Request parser for /books
# -------------------------
parser = reqparse.RequestParser()
parser.add_argument(
    'order',
    choices=list(book_model.keys()),
    help="Column to sort the books by"
)
parser.add_argument(
    'ascending',
    type=inputs.boolean,
    default=True,
    help="Sort order: true=ascending, false=descending"
)

# -------------------------
# /books endpoint for listing all books
# -------------------------
@api.route('/books')
class BooksList(Resource):
    @api.expect(parser)
    def get(self):
        """
        GET /books
        Retrieve all books as a list.
        Optional query parameters:
          - order: column name to sort by
          - ascending: true/false sort order
        """
        args = parser.parse_args()

        order_by = args.get('order')
        ascending = args.get('ascending', True)

        # Sort the dataframe if a valid column is provided
        df_sorted = df.copy()
        if order_by:
            df_sorted = df_sorted.sort_values(by=order_by, ascending=ascending)

        # Convert to JSON and prepare the list of dictionaries
        # Using 'records' orientation avoids the manual index conversion
        books_list = df_sorted.reset_index().to_dict(orient='records')

        return books_list
# -------------------------
# Run Flask application
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)