from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from ariadne import gql, QueryType, MutationType, make_executable_schema, graphql_sync

# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
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
    """
)

query = QueryType()

# Define resolvers
@query.field("books")
def books(*_):
    return [book.to_json() for book in books_db.values()]


# Create executable schema
schema = make_executable_schema(type_defs, [query])

# initialize flask app
app = Flask(__name__)
books_db = dict()


class Books:
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
    books_db[1] = Books(len(books_db) + 1,"Data Services", "A Fake Book", "No Body")
    books_db[2] = Books(len(books_db) + 1,"Advance Data Services", "A Fake Book", "No Body")
    app.run(debug=True)
