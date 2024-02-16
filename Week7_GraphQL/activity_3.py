import os
import subprocess

import flask_migrate.cli
from ariadne.constants import PLAYGROUND_HTML
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from ariadne import gql, QueryType, MutationType, make_executable_schema, graphql_sync

# Define type definitions (schema) using SDL
type_defs = gql(
    """
    type Books {
        title: String!
        description: String!
        author: String!
        }  

    type Query {
        books: [Books]
    }

    type Mutation{add_book(title: String!, description: String!, author: String!): Books}
    """
)

query = QueryType()
mutation = MutationType()


# Define resolvers
@query.field("books")
def books(*_):
    return [book.to_json() for book in Books.query.all()]

@mutation.field("add_book")
def add_book(_, info, title, description, author):
    book = Books(len(books_db) + 1, title, description, author)
    book.save()
    return book.to_json()


# Create executable schema
schema = make_executable_schema(type_defs, [query, mutation])

# initialize flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
books_db = dict()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, id=None, title=None, description=None, author=None):
        self.id = id
        self.title = title
        self.description = description
        self.author = author

    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "author": self.author,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


# Create a GraphQL Playground UI for the GraphQL schema
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML


# Create a GraphQL endpoint for executing GraphQL queries
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value={"request": request})
    status_code = 200 if success else 400
    return jsonify(result), status_code


# Run the app
if __name__ == "__main__":

    """
    Run the following commands in a terminal before running the application to setup the database
    """
    # cd to the directory
    # export FLASK_APP = activity_3.py
    # flask db init
    # flask db migrate
    # flask db upgrade

    app.run(debug=True)
