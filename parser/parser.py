from collections import defaultdict
from graphql.core.type import (
    GraphQLArgument,
    GraphQLField,
    GraphQLInt,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
)
from server.models import db
from sqlalchemy import inspect
import importlib

from server.graph.models.owner import Owner

class Parser():
    _graphql_objects = defaultdict(object)
    _query_to_sqlalchemy_class = None

    def __getitem__(self, query):
        def resolve_at_root(self, root, args, *_):
            target_class = self._query_to_sqlalchemy_class[query]
            return target_class.query.get(args['id'])

        return GraphQLField(
            self._graphql_objects[query],
            args={
                'id': GraphQLArgument(
                    description='Used to identify a base-level %s schema' % query,
                    type=GraphQLNonNull(GraphQLInt),
                )
            },
            resolver=lambda root, args, *_:
        )

    def __init__(self, query_to_sqlalchemy_class):
        self._query_to_sqlalchemy_class = query_to_sqlalchemy_class

        available_attribute_parsers = [
            '_parse_foreign_key',
            '_parse_integer',
            '_parse_string'
        ]

        def parse_attribute(query, attribute):
            for parser in available_attribute_parsers:
                getattr(self, parser)(query, attribute)

        # first pass: initialize graphql objects
        for (query, sqlalchemy_class) in query_to_sqlalchemy_class.iteritems():
            self._graphql_objects[query] = GraphQLObjectType(
                query,
                description='TODO: graphql should be introspective!',
                fields={}
            )

        # second pass: set fields for each attribute
        for (query, sqlalchemy_class) in query_to_sqlalchemy_class.iteritems():
            for column in inspect(sqlalchemy_class).columns:
                parse_attribute(query, column)

    def _parse_integer(self, query, attribute):
        if str(attribute.type) == 'INTEGER' and len(attribute.foreign_keys) == 0:
            self._graphql_objects[query]._fields[attribute.key] = \
                GraphQLField(GraphQLNonNull(GraphQLInt))

    def _parse_string(self, query, attribute):
        if 'VARCHAR' in str(attribute.type):
            self._graphql_objects[query]._fields[attribute.key] = \
                GraphQLField(GraphQLNonNull(GraphQLString))

    def _parse_foreign_key(self, query, attribute):
        def _parse_foreign_key_fullname(fullname):
            target_attribute = fullname.split('.')[1]
            target_class = None

            for (query, sqlalchemy_class) in self._query_to_sqlalchemy_class.iteritems():
                if sqlalchemy_class.__tablename__ == fullname.split('.')[0]:
                    target_class = sqlalchemy_class

            return {
                'target_attribute': target_attribute,
                'target_class': target_class,
            }

        if str(attribute.type) == 'INTEGER' and len(attribute.foreign_keys) == 1:
            for target in attribute.foreign_keys:
                break

            target = _parse_foreign_key_fullname(target.target_fullname)

            def get_remote_query(sqlalchemy_class):
                for (query, sqlalchemy_object) in self._query_to_sqlalchemy_class.iteritems():
                    if sqlalchemy_class is sqlalchemy_object:
                        return query

            def resolver(root, args, *_):
                return target['target_class'].query.get(
                    root.__dict__[_[0].field_name]
                )

            self._graphql_objects[query]._fields[attribute.key] = \
                GraphQLField(
                    self._graphql_objects[
                      get_remote_query(target['target_class'])
                    ],
                    description='TODO: graphql should be introspective!',
                    resolver=resolver
                )

