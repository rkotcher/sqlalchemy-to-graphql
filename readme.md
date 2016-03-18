This is a parser function that takes a dictionary of SQLAlchemy objects as input and outputs a set of GraphQL objects that can be used to configure a GraphQL schema. Configuration of a GraphQL endpoint should look something like this:

```
from sqlalchemy-to-graphql.parser import Parser
from my-sqlalchemy-models import *

my_sqlalchemy_objects = {
    'pet': Pet,
    'owner': Owner,
}

parser = Parser(my_sqlalchemy_objects)

root_schema = GraphQLSchema(query=GraphQLObjectType(
    'MyRootQuery',
    fields: lambda: {
        query: parser[query] for query in my_sqlalchemy_objects,
    }
))

# If you're using Flask, you'll want to configure your endpoint like so:
@app.route('/graph', methods=['POST'])
def query_schema():
    return jsonify(**graphql(root_schema, request.get_data()).data)

```

A post request to /graph with data='query { cat(id: 0) { id, name, owner { id, name } } }'

might return something like:

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

