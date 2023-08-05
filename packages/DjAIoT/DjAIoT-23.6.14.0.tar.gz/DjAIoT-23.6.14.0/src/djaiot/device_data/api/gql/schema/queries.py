from graphene.relay import Connection, ConnectionField, Node

from graphene_django.filter import DjangoFilterConnectionField

import graphene_django_optimizer
from graphene_django_optimizer import OptimizedDjangoObjectType

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

from .types import \
    EnvironmentVariableNode, \
    MeasurementUnitNode, \
    MachineClassNode, \
    MachineComponentNode, \
    MachineDataStreamNode, \
    MachineFamilyNode, \
    MachineSKUNode, \
    LocationNode, \
    MachineNode


class Query:
    data_environment_variable = \
        Node.Field(EnvironmentVariableNode)

    data_environment_variables = \
        DjangoFilterConnectionField(
            EnvironmentVariableNode,
            filterset_class=EnvironmentVariableFilter)

    # https://github.com/tfoxy/graphene-django-optimizer
    # but ^ does not work:
    # https://github.com/tfoxy/graphene-django-optimizer/issues/24
    def resolve_data_environment_variables(self, info, **kwargs):
        return graphene_django_optimizer.query(
            queryset=EnvironmentVariable.objects.all(),
            info=info,
            **kwargs) \
            if info.context.user.is_authenticated \
            else EnvironmentVariable.objects.all()   # TODO: none()

    measurement_unit = \
        Node.Field(MeasurementUnitNode)
    measurement_units = \
        DjangoFilterConnectionField(
            MeasurementUnitNode,
            filterset_class=MeasurementUnitFilter)

    machine_class = \
        Node.Field(MachineClassNode)
    machine_classes = \
        DjangoFilterConnectionField(
            MachineClassNode,
            filterset_class=MachineClassFilter)

    machine_component = \
        Node.Field(MachineComponentNode)
    machine_components = \
        DjangoFilterConnectionField(
            MachineComponentNode,
            filterset_class=MachineComponentFilter)

    machine_data_stream = \
        Node.Field(MachineDataStreamNode)
    machine_data_streams = \
        DjangoFilterConnectionField(
            MachineDataStreamNode,
            filterset_class=MachineDataStreamFilter)

    machine_family = \
        Node.Field(MachineFamilyNode)
    machine_families = \
        DjangoFilterConnectionField(
            MachineFamilyNode,
            filterset_class=MachineFamilyFilter)

    machine_sku = \
        Node.Field(MachineSKUNode)
    machine_skus = \
        DjangoFilterConnectionField(
            MachineSKUNode,
            filterset_class=MachineSKUFilter)

    location = \
        Node.Field(LocationNode)
    locations = \
        DjangoFilterConnectionField(
            LocationNode,
            filterset_class=LocationFilter)

    machine = \
        Node.Field(MachineNode)
    machines = \
        DjangoFilterConnectionField(
            MachineNode,
            filterset_class=MachineFilter)
