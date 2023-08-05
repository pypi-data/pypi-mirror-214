from graphene import Mutation

from graphene_django.forms.mutation import DjangoFormMutation, DjangoModelFormMutation
from graphene_django.rest_framework.mutation import ClientIDMutation, SerializerMutation

from graphql_relay import from_global_id


from ...rest.core.serializers import \
    EnvironmentVariableSerializer


class EnvironmentVariableMutation(SerializerMutation):
    class Meta:
        serializer_class = EnvironmentVariableSerializer

        model_operations = \
            'create', \
            'update'

        lookup_field = 'key'


class EnvironmentVariableRelayMutation(ClientIDMutation):
    @classmethod
    def mutate_and_get_payload(cls, root, info, *args, **kwargs):
        pass


class Mutation:
    pass
