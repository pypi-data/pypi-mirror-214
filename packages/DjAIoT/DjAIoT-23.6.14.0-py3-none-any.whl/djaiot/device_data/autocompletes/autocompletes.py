from django.urls.conf import path
from django_util.autocompletes import autocomplete_factory

from .models import \
    PhysicalDataType, \
    MeasurementUnit, \
    MachineClass, \
    MachineComponent, \
    MachineDataStream, \
    MachineFamily, \
    MachineSKU, \
    Location, \
    Machine, \
    MachineFamilyComponent


PhysicalDataTypeAutoComplete = \
    autocomplete_factory(
        PhysicalDataType,
        min_input_len=0)


MeasurementUnitAutoComplete = \
    autocomplete_factory(
        MeasurementUnit,
        min_input_len=0)


MachineClassAutoComplete = \
    autocomplete_factory(
        MachineClass,
        min_input_len=0)


MachineComponentAutoComplete = \
    autocomplete_factory(
        MachineComponent,
        min_input_len=1)


MachineDataStreamAutoComplete = \
    autocomplete_factory(
        MachineDataStream,
        min_input_len=1)


MachineFamilyAutoComplete = \
    autocomplete_factory(
        MachineFamily,
        min_input_len=1)


MachineSKUAutoComplete = \
    autocomplete_factory(
        MachineSKU,
        min_input_len=1)


LocationAutoComplete = \
    autocomplete_factory(
        Location,
        min_input_len=1)


MachineAutoComplete = \
    autocomplete_factory(
        Machine,
        min_input_len=1)


MachineFamilyComponentAutoComplete = \
    autocomplete_factory(
        MachineFamilyComponent,
        min_input_len=1)


AUTOCOMPLETE_URL_PATTERNS = [
    path(f'{PhysicalDataTypeAutoComplete.name}/',
         PhysicalDataTypeAutoComplete.as_view(),
         name=PhysicalDataTypeAutoComplete.name),

    path(f'{MeasurementUnitAutoComplete.name}/',
         MeasurementUnitAutoComplete.as_view(),
         name=MeasurementUnitAutoComplete.name),

    path(f'{MachineClassAutoComplete.name}/',
         MachineClassAutoComplete.as_view(),
         name=MachineClassAutoComplete.name),

    path(f'{MachineComponentAutoComplete.name}/',
         MachineComponentAutoComplete.as_view(),
         name=MachineComponentAutoComplete.name),

    path(f'{MachineDataStreamAutoComplete.name}/',
         MachineDataStreamAutoComplete.as_view(),
         name=MachineDataStreamAutoComplete.name),

    path(f'{MachineFamilyAutoComplete.name}/',
         MachineFamilyAutoComplete.as_view(),
         name=MachineFamilyAutoComplete.name),

    path(f'{MachineSKUAutoComplete.name}/',
         MachineSKUAutoComplete.as_view(),
         name=MachineSKUAutoComplete.name),

    path(f'{LocationAutoComplete.name}/',
         LocationAutoComplete.as_view(),
         name=LocationAutoComplete.name),

    path(f'{MachineAutoComplete.name}/',
         MachineAutoComplete.as_view(),
         name=MachineAutoComplete.name),

    path(f'{MachineFamilyComponentAutoComplete.name}/',
         MachineFamilyComponentAutoComplete.as_view(),
         name=MachineFamilyComponentAutoComplete.name)
]
