"""
Books REST API using Flask, pandas, Flask-RESTx
With HTTP Basic Authentication documented in Swagger UI
"""
from functools import wraps

import pandas as pd
from flask import Flask, request
from flask_restx import Resource, Api, fields, reqparse, inputs, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------
# Flask & API Setup
# -------------------------
app = Flask(__name__)

# 🔐 Swagger Security Definition
authorizations = {
    'basicAuth': {
        'type': 'basic'
    }
}

api = Api(
    app,
    version="1.0",
    title="Books Management API",
    description="A CRUD API to manage books using pandas and Flask-RESTx",
    default="Books",
    default_label="Book operations",
    authorizations=authorizations,
    security='basicAuth'  # Apply globally in Swagger
)

# -------------------------
# Basic Authentication Setup
# -------------------------

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            abort(401)

        if not (auth.username == 'admin' and 'admin' == auth.password):
            abort(401)

        return f(*args, **kwargs)

    return decorated


# -------------------------
# Load & preprocess CSV
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

df = pd.read_csv(csv_file)
df.drop(columns=columns_to_drop, inplace=True, errors="ignore")
df.columns = df.columns.str.replace(' ', '_', regex=False)

df['Date_of_Publication'] = (
    df['Date_of_Publication']
    .astype(str)
    .str.extract(r'^(\d{4})', expand=False)
    .astype(float)
    .fillna(0)
    .astype(int)
)

df.set_index('Identifier', inplace=True)

# -------------------------
# Book Model
# -------------------------
book_model = api.model('Book', {
    'Flickr_URL': fields.String(description="URL of book image on Flickr"),
    'Publisher': fields.String(description="Name of the publisher"),
    'Author': fields.String(description="Author of the book"),
    'Title': fields.String(description="Title of the book"),
    'Date_of_Publication': fields.Integer(description="Year published"),
    'Identifier': fields.Integer(description="Unique Identifier"),
    'Place_of_Publication': fields.String(description="Publication place")
})

# -------------------------
# Request Parser
# -------------------------
parser = reqparse.RequestParser()
parser.add_argument(
    'order',
    choices=list(book_model.keys()),
    help="Column name to sort by"
)
parser.add_argument(
    'ascending',
    type=inputs.boolean,
    default=True,
    help="true = ascending, false = descending"
)

# -------------------------
# Individual Book Endpoints
# -------------------------
@api.route('/books/<int:id>')
@api.doc(security='basicAuth')
class Books(Resource):

    @requires_auth
    @api.response(200, "Book retrieved")
    @api.response(404, "Book not found")
    def get(self, id):
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")
        return df.loc[id].to_dict()

    @requires_auth
    @api.response(200, "Book deleted")
    @api.response(404, "Book not found")
    def delete(self, id):
        if id not in df.index:
            api.abort(404, f"Book {id} doesn't exist")
        df.drop(id, inplace=True)
        df.to_csv(csv_file, index=True)
        return {"message": f"Book {id} removed"}, 200

    @api.expect(book_model)
    @api.response(200, "Book updated")
    @api.response(400, "Invalid payload")
    @api.response(404, "Book not found")
    @requires_auth
    def put(self, id):
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
        return {"message": f"Book {id} updated"}, 200


# -------------------------
# Books Collection Endpoints
# -------------------------
@api.route('/books')
@api.doc(security='basicAuth')
class BooksList(Resource):

    @api.expect(parser)
    @api.response(200, "Books retrieved")
    @requires_auth
    def get(self):
        args = parser.parse_args()
        order_by = args.get('order')
        ascending = args.get('ascending', True)

        df_sorted = df.copy()
        if order_by:
            df_sorted = df_sorted.sort_values(by=order_by, ascending=ascending)

        return df_sorted.reset_index().to_dict(orient='records')

    @api.expect(book_model)
    @api.response(201, "Book added")
    @api.response(400, "Invalid payload")
    @requires_auth
    def post(self):
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
        return {"message": f"Book {book_id} added"}, 201


# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)