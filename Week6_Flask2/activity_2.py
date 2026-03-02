"""
Books REST API using Flask and pandas

Features:
- GET /books/<id>      : Retrieve a book by its Identifier.
- DELETE /books/<id>   : Remove a book by its Identifier.
- PUT /books/<id>      : Update a book by its Identifier.
- GET /books           : Get all books with optional sorting.
- POST /books          : Add a new book.

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
from flask_restx import Resource, Api, fields, reqparse, inputs

# -------------------------
# Flask & API Setup
# -------------------------
app = Flask(__name__)
api = Api(app, title="Books API", description="CRUD API for managing books using pandas")

# -------------------------
# CSV File Configuration
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

# -------------------------
# Load & preprocess CSV
# -------------------------
df = pd.read_csv(csv_file)
df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# Clean 'Date of Publication' and convert to integer
df['Date_of_Publication'] = (
    df['Date of Publication']
    .str.extract(r'^(\d{4})', expand=False)
    .fillna(0)
    .astype(int)
)

# Replace spaces in column names
df.columns = df.columns.str.replace(' ', '_', regex=False)

# Set 'Identifier' as the index
df.set_index('Identifier', inplace=True)

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
# Request parser for GET /books
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
# CRUD Endpoints for individual books
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
        df.to_csv(csv_file, index=True)  # Persist changes
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

        # Replace entire row
        df.loc[id] = pd.Series(book_data)
        df.to_csv(csv_file, index=True)  # Persist changes
        return {"message": f"Book {id} has been successfully updated"}, 200

# -------------------------
# CRUD Endpoints for books list
# -------------------------
@api.route('/books')
class BooksList(Resource):
    @api.expect(parser)
    def get(self):
        """Retrieve all books, optionally sorted by a column."""
        args = parser.parse_args()
        order_by = args.get('order')
        ascending = args.get('ascending', True)

        df_sorted = df.copy()
        if order_by:
            df_sorted = df_sorted.sort_values(by=order_by, ascending=ascending)

        # Convert to list of dictionaries
        return df_sorted.reset_index().to_dict(orient='records')

    @api.expect(book_model)
    def post(self):
        """Add a new book."""
        book_data = request.json

        # Validate keys
        invalid_keys = [k for k in book_data if k not in book_model.keys()]
        if invalid_keys:
            return {"message": f"Invalid properties: {', '.join(invalid_keys)}"}, 400

        # Ensure Identifier exists and is unique
        book_id = book_data.get('Identifier')
        if book_id is None:
            return {"message": "Identifier is required"}, 400
        if book_id in df.index:
            return {"message": f"Book {book_id} already exists"}, 400

        # Add new row
        df.loc[book_id] = pd.Series(book_data)
        df.to_csv(csv_file, index=True)  # Persist changes
        return {"message": f"Book {book_id} has been successfully added"}, 201

# -------------------------
# Run Flask application
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)