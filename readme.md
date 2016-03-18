## Overview

sqlalchemy-to-graphql does one thing: It takes as input a dictionary of the form ```{ 'query': <SQLAlchemy Object> }``` and outputs a dictionary of the form ```{ 'query': <GraphQLField>}```.

The GraphQLField object represents an entry point into your data, and GraphQL allows you to traverse your data in a product-centric, declarative way.

Suppose you have the following SQLAlchemy objects:

```
class Cat(db.Model):
    __tablename__ = 'cat'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('owner.id'))

class Owner(db.Model):
    __tablename__ = 'owner'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    cat = db.Column(db.Integer, db.ForeignKey('cat.id'))
```

This method of defining classes within SQLAlchemy uses the Declarative API, and the vision for this parser is to parse attributes from SQLAlchemy classes, and transform them into GraphQL objects that can be used within a schema. Let's set up the following dictionary:

```
requirements = {
    'cat': Cat,
    'owner': Owner,
}
```

In this dummy example, the dictionary named "requirements" is the only required input for the parser. Once parsed and converted into GraphQL object types, it's straightforward to configure a GraphQL schema:

```
from sqlalchemy-to-graphql.parser import Parser

parser = Parser(requirements)

root_schema = GraphQLSchema(query=GraphQLObjectType(
    'MyRootQuery',
    fields: lambda: {
        query: parser[query] for query in my_sqlalchemy_objects,
    }
))
```

The schema can be hooked up to any endpoint you may be using with your proeject; I've chosen Flask:

```
@app.route('/graph', methods=['POST'])
def query_schema():
    return jsonify(**graphql(root_schema, request.get_data()).data)
```

That's all there is to it! The endpoint `/graph` is now set up to access your SQLAlchemy models through standard graphql queries. You can Google GraphQl and find tons of resources on how querying works, but for completion of this README, here's a simple query you could make against the models in our dummy example:

```
query {
    cat(id: 0) {
        id,
        name,
        owner {
            id,
            name
        }
    }
}
```
returns...
```
{
    "cat": {
        "id": 233498,
        "name": "Whiskers",
        "owner": {
            "id": 234674,
            "name": "Billy-Bob"
        }
    }
}
```

A working example using the same objects can be found in `/examples`.
