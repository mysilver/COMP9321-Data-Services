from flask import Flask
from flask import request
from flask_restplus import Resource, Api
import pandas as pd
import json

from flask_restplus import fields

app = Flask(__name__)
api = Api(app,
          default="Books",  # Default namespace
          title="Book Dataset",  # Documentation Title
          description="This is just a simple example to show how publish data as a service.")  # Documentation Description

# The following is the schema of Book
book_model = api.model('Book', {
    'Identifier': fields.Integer,
    'Title': fields.String,
    'Author': fields.String,
    'Date_of_Publication': fields.Integer,
    'Place_of_Publication': fields.String,
    'Publisher': fields.String,
    'Flickr_URL': fields.String,
})



@api.route('/books/')
@api.expect(fields=book_model, validate=True)
class BooksList(Resource):
    """
    Booked published in somewhere
    """

    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.marshal_with(book_model)
    @api.expect(book_model)
    def post(self):
        book = request.json
        return book, 201


@api.route('/books/<int:id>')
@api.expect(fields=book_model, validate=True)
@api.param('id', 'The Book identifier')
class Books(Resource):
    """
    Booked published in somewhere
    """

    @api.response(404, 'Book was not found')
    @api.response(200, 'Successful')
    @api.marshal_with(book_model)
    @api.doc(description="Get a book by its ID", summary="hello")
    def get(self, id):
        # return json.loads(df.to_json(orient='records'))
        ret = json.loads(df.query("Identifier==" + str(id)).to_json(orient='records'))
        if ret:
            return ret[0]

        api.abort(404, "Book {} doesn't exist".format(id))

    @api.response(404, 'Book was not found')
    @api.response(200, 'Successful')
    def delete(self, id):
        try:
            df.drop(id, inplace=True)
        except ValueError:
            api.abort(404, "Book {} doesn't exist".format(id))

        return {"message": "Book removed"}, 200


if __name__ == '__main__':
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)
    df.drop(columns_to_drop, inplace=True, axis=1)

    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date
    df.columns = [c.replace(' ', '_') for c in df.columns]

    df.set_index('Identifier', inplace=True)

    app.run(debug=True)
