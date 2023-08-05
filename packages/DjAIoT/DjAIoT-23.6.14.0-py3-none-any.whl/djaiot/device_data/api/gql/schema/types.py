from graphene import Field, List, ObjectType
from graphene.relay import Connection, ConnectionField, Node

from graphene_django.types import DjangoObjectType

from ....filters import \
    EnvironmentVariableFilter, \
    MeasurementUnitFilter, \
    MachineClassFilter, \
    MachineComponentFilter, \
    MachineDataStreamFilter, \
    MachineFamilyFilter, \
    MachineSKUFilter, \
    LocationFilter, \
    MachineFilter

from ....models import \
    EnvironmentVariable, \
    MeasurementUnit, \
    MachineClass, \
    MachineComponent, \
    MachineDataStream, \
    MachineFamily, \
    MachineSKU, \
    Location, \
    Machine

from ...field_names import \
    ENVIRONMENT_VARIABLE_API_FIELD_NAMES, \
    MEASUREMENT_UNIT_API_FIELD_NAMES, \
    MACHINE_CLASS_API_FIELD_NAMES, \
    MACHINE_COMPONENT_NESTED_API_FIELD_NAMES, \
    MACHINE_DATA_STREAM_NESTED_API_FIELD_NAMES, \
    MACHINE_FAMILY_NESTED_API_FIELD_NAMES, \
    MACHINE_SKU_NESTED_API_FIELD_NAMES, \
    LOCATION_API_FIELD_NAMES, \
    MACHINE_API_FIELD_NAMES


class EnvironmentVariableNode(DjangoObjectType):
    class Meta:
        model = EnvironmentVariable

        only_fields = ENVIRONMENT_VARIABLE_API_FIELD_NAMES

        # filterset_class = EnvironmentVariableFilter
        # SETTING filterset_class DIRECTLY in DjangoFilterConnectionField below BECAUSE OF BUG:
        # https://github.com/graphql-python/graphene-django/issues/302
        # https://github.com/graphql-python/graphene-django/issues/550

        interfaces = Node,


class MeasurementUnitNode(DjangoObjectType):
    class Meta:
        model = MeasurementUnit

        only_fields = MEASUREMENT_UNIT_API_FIELD_NAMES

        # filterset_class = MeasurementUnitFilter

        interfaces = Node,


class MachineClassNode(DjangoObjectType):
    class Meta:
        model = MachineClass

        only_fields = MACHINE_CLASS_API_FIELD_NAMES

        # filterset_class = MachineClassFilter

        interfaces = Node,


class MachineComponentNode(DjangoObjectType):
    class Meta:
        model = MachineComponent

        only_fields = MACHINE_COMPONENT_NESTED_API_FIELD_NAMES

        # filterset_class = MachineComponentFilter

        interfaces = Node,


class MachineDataStreamNode(DjangoObjectType):
    class Meta:
        model = MachineDataStream

        only_fields = MACHINE_DATA_STREAM_NESTED_API_FIELD_NAMES

        # filterset_class = MachineDataStreamFilter

        interfaces = Node,


class MachineFamilyNode(DjangoObjectType):
    class Meta:
        model = MachineFamily

        only_fields = MACHINE_FAMILY_NESTED_API_FIELD_NAMES

        # filterset_class = MachineFamilyFilter

        interfaces = Node,


class MachineSKUNode(DjangoObjectType):
    class Meta:
        model = MachineSKU

        only_fields = MACHINE_SKU_NESTED_API_FIELD_NAMES

        # filterset_class = MachineSKUFilter

        interfaces = Node,


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location

        only_fields = LOCATION_API_FIELD_NAMES

        # filterset_class = LocationFilter

        interfaces = Node,


class MachineNode(DjangoObjectType):
    class Meta:
        model = Machine

        only_fields = MACHINE_API_FIELD_NAMES

        # filterset_class = MachineFilter

        interfaces = Node,
