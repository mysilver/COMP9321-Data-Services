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
# Flask & API Setup with Swagger metadata
# -------------------------
app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Books Management API",
    description="A CRUD API to manage books using pandas and Flask-RESTx",
    default="Books",  # Default namespace name
    default_label="Book operations"  # Label for default namespace
)

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
# Book Model Schema
# -------------------------
book_model = api.model('Book', {
    'Flickr_URL': fields.String(description="URL of book image on Flickr"),
    'Publisher': fields.String(description="Name of the publisher"),
    'Author': fields.String(description="Author of the book"),
    'Title': fields.String(description="Title of the book"),
    'Date_of_Publication': fields.Integer(description="Year the book was published"),
    'Identifier': fields.Integer(description="Unique Identifier of the book"),
    'Place_of_Publication': fields.String(description="Place where the book was published")
})

# -------------------------
# Request parser for GET /books
# -------------------------
parser = reqparse.RequestParser()
parser.add_argument(
    'order',
    choices=list(book_model.keys()),
    help="Column name to sort the books by"
)
parser.add_argument(
    'ascending',
    type=inputs.boolean,
    default=True,
    help="Sort order: true for ascending, false for descending"
)

# -------------------------
# CRUD Endpoints for individual books
# -------------------------
@api.route('/books/<int:id>')
class Books(Resource):
    @api.doc(description="Retrieve a book by its unique Identifier")
    @api.param("id", "Unique identifier of the book", _in="path")
    @api.response(200, "Book retrieved successfully")
    @api.response(404, "Book not found")
    def get(self, id: int):
        """Retrieve a book by its Identifier."""
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")
        return df.loc[id].to_dict()

    @api.doc(description="Delete a book by its unique Identifier")
    @api.param("id", "Unique identifier of the book", _in="path")
    @api.response(200, "Book deleted successfully")
    @api.response(404, "Book not found")
    def delete(self, id: int):
        """Delete a book by its Identifier."""
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")
        df.drop(id, inplace=True)
        df.to_csv(csv_file, index=True)
        return {"message": f"Book {id} has been removed."}, 200

    @api.expect(book_model)
    @api.doc(description="Update a book by its unique Identifier. Identifier cannot be changed.")
    @api.param("id", "Unique identifier of the book", _in="path")
    @api.response(200, "Book updated successfully")
    @api.response(400, "Invalid payload or Identifier change attempted")
    @api.response(404, "Book not found")
    def put(self, id: int):
        """Update a book by its Identifier."""
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")

        book_data = request.json

        if 'Identifier' in book_data and book_data['Identifier'] != id:
            return {"message": "Identifier cannot be changed"}, 400

        invalid_keys = [k for k in book_data if k not in book_model.keys()]
        if invalid_keys:
            return {"message": f"Invalid properties: {', '.join(invalid_keys)}"}, 400

        df.loc[id] = pd.Series(book_data)
        df.to_csv(csv_file, index=True)
        return {"message": f"Book {id} has been successfully updated"}, 200

# -------------------------
# CRUD Endpoints for books list
# -------------------------
@api.route('/books')
class BooksList(Resource):
    @api.doc(description="Retrieve all books as a list, optionally sorted by a column")
    @api.expect(parser)
    @api.response(200, "Books retrieved successfully")
    def get(self):
        """Retrieve all books, optionally sorted by a column."""
        args = parser.parse_args()
        order_by = args.get('order')
        ascending = args.get('ascending', True)

        df_sorted = df.copy()
        if order_by:
            df_sorted = df_sorted.sort_values(by=order_by, ascending=ascending)

        return df_sorted.reset_index().to_dict(orient='records')

    @api.expect(book_model)
    @api.doc(description="Add a new book to the collection")
    @api.response(201, "Book added successfully")
    @api.response(400, "Invalid payload or Identifier already exists")
    def post(self):
        """Add a new book."""
        book_data = request.json

        invalid_keys = [k for k in book_data if k not in book_model.keys()]
        if invalid_keys:
            return {"message": f"Invalid properties: {', '.join(invalid_keys)}"}, 400

        book_id = book_data.get('Identifier')
        if book_id is None:
            return {"message": "Identifier is required"}, 400
        if book_id in df.index:
            return {"message": f"Book {book_id} already exists"}, 400

        df.loc[book_id] = pd.Series(book_data)
        df.to_csv(csv_file, index=True)
        return {"message": f"Book {book_id} has been successfully added"}, 201

# -------------------------
# Run Flask application
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)