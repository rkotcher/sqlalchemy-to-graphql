from flask import Flask, g, jsonify, request
from graphql.core import graphql
from graphql.core.type import *

from server.models import db

from parser.parser import Parser

from example.models.cat import Cat
from example.models.owner import Owner

import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

my_sqlalchemy_objects = {
    'cat': Cat,
    'owner': Owner,
}

parser = Parser(my_sqlalchemy_objects)

root_schema = GraphQLSchema(query=GraphQLObjectType(
    'MyRootQuery',
    fields=lambda: {
        query: parser[query] for query in my_sqlalchemy_objects
    },
))

@app.route('/graph', methods=['POST'])
def query_schema():
    return jsonify(**graphql(root_schema, request.get_data()).data)

if __name__ == '__main__':
    app.run()

