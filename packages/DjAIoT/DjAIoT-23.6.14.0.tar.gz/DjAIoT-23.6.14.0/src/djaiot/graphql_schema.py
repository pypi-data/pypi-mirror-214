from graphene import Field, ObjectType, Schema

from graphene_django.debug import DjangoDebug

from .data.api.graphql.schema.mutations import Mutation as DataMutation
from .data.api.graphql.schema.queries import Query as DataQuery

from .health.api.graphql.schema.mutations import Mutation as HealthMutation


class Query(
        DataQuery,
        ObjectType):
    debug = Field(DjangoDebug, name='_debug')


class Mutation(
        DataMutation,
        HealthMutation,
        ObjectType):
    pass


schema = \
    Schema(
        query=Query,
        # mutation=Mutation,
        subscription=None,
        auto_camelcase=True   # comply w GraphQL standards
    )
