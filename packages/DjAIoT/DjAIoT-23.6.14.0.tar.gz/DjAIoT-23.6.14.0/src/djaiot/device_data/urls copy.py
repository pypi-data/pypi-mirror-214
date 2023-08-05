from django.urls import include, path

from rest_framework.routers import DefaultRouter

from rest_framework_nested.routers import NestedDefaultRouter

from .api.rest.core.views import \
    EnvironmentVariableViewSet, \
    PhysicalDataTypeViewSet, \
    MeasurementUnitViewSet, \
    MachineClassViewSet, \
    MachineComponentViewSet, \
    MachineDataStreamViewSet, \
    MachineFamilyViewSet, \
    MachineSKUViewSet, \
    LocationViewSet, \
    MachineViewSet, \
    MachineDailyDataViewSet, \
    MachineDataStreamDailyAggViewSet, \
    MachineFamilyDataStreamProfileViewSet, \
    MachineFamilyDataStreamPairCorrViewSet

from .api.rest.json.views import \
    EnvironmentVariableJSONAPIViewSet, \
    PhysicalDataTypeJSONAPIViewSet, \
    MeasurementUnitJSONAPIViewSet, \
    MachineClassJSONAPIViewSet, \
    MachineComponentJSONAPIViewSet, \
    MachineDataStreamJSONAPIViewSet, \
    MachineFamilyJSONAPIViewSet, \
    MachineSKUJSONAPIViewSet, \
    LocationJSONAPIViewSet, \
    MachineJSONAPIViewSet, \
    MachineDailyDataJSONAPIViewSet, \
    MachineDataStreamDailyAggJSONAPIViewSet, \
    MachineFamilyDataStreamProfileJSONAPIViewSet, \
    MachineFamilyDataStreamPairCorrJSONAPIViewSet

from .autocompletes import AUTOCOMPLETE_URL_PATTERNS


API_END_POINT_PREFIX = __name__.split('.')[-2]

ENVIRONMENT_VARIABLES_PREFIX = 'environment-variables'
PHYSICAL_DATA_TYPES_PREFIX = 'physical-data-types'
MEASUREMENT_UNITS_PREFIX = 'measurement-units'
MACHINE_DATA_STREAM_TYPES_PREFIX ='machine-data-stream-types'
MACHINE_CLASSES_PREFIX = 'machine-classes'
MACHINE_COMPONENTS_PREFIX = 'machine-components'
MACHINE_DATA_STREAMS_PREFIX = 'machine-data-streams'
MACHINE_FAMILIES_PREFIX = 'machine-families'
MACHINE_SKUS_PREFIX = 'machine-skus'
LOCATIONS_PREFIX = 'locations'
MACHINES_PREFIX = 'machines'
MACHINE_DAILY_DATA_PREFIX = 'machine-daily-data'
MACHINE_FAMILY_DATA_STREAM_PROFILES_PREFIX = 'machine-family-data-stream-profiles'
MACHINE_FAMILY_DATA_STREAM_PAIR_CORRS_PREFIX = 'machine-family-data-stream-pair-corrs'


CORE_REST_API_ROUTER = \
    DefaultRouter(
        trailing_slash=False)

CORE_REST_API_ROUTER.register(
    prefix=ENVIRONMENT_VARIABLES_PREFIX,
    viewset=EnvironmentVariableViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=PHYSICAL_DATA_TYPES_PREFIX,
    viewset=PhysicalDataTypeViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MEASUREMENT_UNITS_PREFIX,
    viewset=MeasurementUnitViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_CLASSES_PREFIX,
    viewset=MachineClassViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_COMPONENTS_PREFIX,
    viewset=MachineComponentViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_DATA_STREAMS_PREFIX,
    viewset=MachineDataStreamViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILIES_PREFIX,
    viewset=MachineFamilyViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_SKUS_PREFIX,
    viewset=MachineSKUViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=LOCATIONS_PREFIX,
    viewset=LocationViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINES_PREFIX,
    viewset=MachineViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_DAILY_DATA_PREFIX,
    viewset=MachineDailyDataViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix='machine-data-stream-daily-aggs',
    viewset=MachineDataStreamDailyAggViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_DATA_STREAM_PROFILES_PREFIX,
    viewset=MachineFamilyDataStreamProfileViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_DATA_STREAM_PAIR_CORRS_PREFIX,
    viewset=MachineFamilyDataStreamPairCorrViewSet,
    basename=None)


JSON_REST_API_ROUTER = \
    DefaultRouter(
        trailing_slash=False)

JSON_REST_API_ROUTER.register(
    prefix=ENVIRONMENT_VARIABLES_PREFIX,
    viewset=EnvironmentVariableJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=PHYSICAL_DATA_TYPES_PREFIX,
    viewset=PhysicalDataTypeJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MEASUREMENT_UNITS_PREFIX,
    viewset=MeasurementUnitJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_CLASSES_PREFIX,
    viewset=MachineClassJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_COMPONENTS_PREFIX,
    viewset=MachineComponentJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_DATA_STREAMS_PREFIX,
    viewset=MachineDataStreamJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILIES_PREFIX,
    viewset=MachineFamilyJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_SKUS_PREFIX,
    viewset=MachineSKUJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=LOCATIONS_PREFIX,
    viewset=LocationJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINES_PREFIX,
    viewset=MachineJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_DAILY_DATA_PREFIX,
    viewset=MachineDailyDataJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix='machine-data-stream-daily-aggs',
    viewset=MachineDataStreamDailyAggJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_DATA_STREAM_PROFILES_PREFIX,
    viewset=MachineFamilyDataStreamProfileJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_DATA_STREAM_PAIR_CORRS_PREFIX,
    viewset=MachineFamilyDataStreamPairCorrJSONAPIViewSet,
    basename=None)


URL_PATTERNS = [
    path('api/rest/core/{}/'.format(API_END_POINT_PREFIX),
         include(CORE_REST_API_ROUTER.urls)),

    path('api/rest/json/{}/'.format(API_END_POINT_PREFIX),
         include(JSON_REST_API_ROUTER.urls))

] + AUTOCOMPLETE_URL_PATTERNS
