import json
import pandas as pd
from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/books/<int:id>')
class Books(Resource):
    # @api.marshal_with(book_model)
    def get(self, id):
        filtered_df = df.query("Identifier==" + str(id))
        books = filtered_df.to_json(orient='records')
        ret = json.loads(books)

        if ret:
            # Book has been found
            book = ret[0]
            book['Identifier'] = id
            return ret[0]

        # There is no such a book
        api.abort(404, "Book {} doesn't exist".format(id))


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

    # drop unnecessary columns
    df.drop(columns_to_drop, inplace=True, axis=1)

    # clean the date of publication & convert it to numeric data
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date

    # replace spaces in the name of columns
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # set the index column; this will help us to find books with their ids
    df.set_index('Identifier', inplace=True)

    # run the application
    app.run(debug=True)
