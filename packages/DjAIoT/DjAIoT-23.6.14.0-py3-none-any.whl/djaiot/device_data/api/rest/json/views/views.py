from rest_framework.authentication import \
    BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework_json_api.pagination import JsonApiLimitOffsetPagination, JsonApiPageNumberPagination
from rest_framework_json_api.renderers import \
    JSONRenderer as JSONAPIJSONRenderer
from rest_framework_json_api.views import \
    ModelViewSet as JSONAPIModelViewSet, \
    ReadOnlyModelViewSet as JSONAPIReadOnlyModelViewSet, \
    RelationshipView

from silk.profiling.profiler import silk_profile

from ....admin import \
    EnvironmentVariableAdmin, \
    PhysicalDataTypeAdmin, \
    MeasurementUnitAdmin, \
    MachineClassAdmin, \
    MachineComponentAdmin, \
    MachineDataStreamAdmin, \
    MachineFamilyAdmin, \
    MachineSKUAdmin, \
    LocationAdmin, \
    MachineAdmin, \
    MachineDataAdmin, \
    MachineDataStreamAggAdmin, \
    MachineFamilyDataStreamProfileAdmin, \
    MachineFamilyDataStreamPairCorrAdmin

from ....filters import \
    EnvironmentVariableFilter, \
    PhysicalDataTypeFilter, \
    MeasurementUnitFilter, \
    MachineClassFilter, \
    MachineComponentFilter, \
    MachineDataStreamFilter, \
    MachineFamilyFilter, \
    MachineSKUFilter, \
    LocationFilter, \
    MachineFilter, \
    MachineDailyDataFilter, \
    MachineDataStreamDailyAggFilter, \
    MachineFamilyDataStreamProfileFilter, \
    MachineFamilyDataStreamPairCorrFilter

from ..queries import \
    ENVIRONMENT_VARIABLE_REST_API_QUERY_SET, \
    PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_SET, \
    MEASUREMENT_UNIT_REST_API_QUERY_SET, \
    MACHINE_CLASS_REST_API_QUERY_SET, \
    MACHINE_COMPONENT_NESTED_REST_API_QUERY_SET, \
    MACHINE_DATA_STREAM_NESTED_REST_API_QUERY_SET, \
    MACHINE_FAMILY_NESTED_REST_API_QUERY_SET, \
    MACHINE_SKU_NESTED_REST_API_QUERY_SET, \
    LOCATION_NESTED_REST_API_QUERY_SET, \
    MACHINE_REST_API_QUERY_SET, \
    MACHINE_DATA_REST_API_QUERY_SET, \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_REST_API_QUERY_SET, \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_REST_API_QUERY_SET

from ....models import \
    EnvironmentVariable, \
    PhysicalDataType, \
    MeasurementUnit, \
    MachineClass, \
    MachineComponent, \
    MachineDataStream, \
    MachineFamily, \
    MachineSKU, \
    Location, \
    Machine, \
    MachineData, \
    MachineDataStreamAgg, \
    MachineFamilyDataStreamProfile, \
    MachineFamilyDataStreamPairCorr

from .serializers import \
    EnvironmentVariableJSONAPISerializer, \
    PhysicalDataTypeNestedJSONAPISerializer, \
    MeasurementUnitJSONAPISerializer, \
    MachineClassJSONAPISerializer, \
    MachineComponentNestedJSONAPISerializer, \
    MachineDataStreamNestedJSONAPISerializer, \
    MachineFamilyNestedJSONAPISerializer, \
    MachineSKUNestedJSONAPISerializer, \
    LocationNestedJSONAPISerializer, \
    MachineJSONAPISerializer, \
    MachineDailyDataJSONAPISerializer, \
    MachineDataStreamDailyAggJSONAPISerializer, \
    MachineFamilyDataStreamProfileJSONAPISerializer, \
    MachineFamilyDataStreamPairCorrJSONAPISerializer


class EnvironmentVariableJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Environment Variables

    retrieve:
    `GET` the Environment Variable specified by `key`

    create:
    `POST` a new Environment Variable by `key`

    update:
    `PUT` updated data for the Environment Variable specified by `key`

    partial_update:
    `PATCH` the Environment Variable specified by `key`

    destroy:
    `DELETE` the Environment Variable specified by `key`
    """
    queryset = ENVIRONMENT_VARIABLE_REST_API_QUERY_SET

    serializer_class = EnvironmentVariableJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = \
        list(set(EnvironmentVariableFilter.get_fields())
             - {'value'})

    search_fields = EnvironmentVariableAdmin.search_fields

    ordering_fields = 'key',

    ordering = 'key',

    pagination_class = None

    lookup_field = 'key'

    lookup_url_kwarg = 'environment_variable_key'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class PhysicalDataTypeJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` an filterable, unpaginated list of Physical Data Types

    retrieve:
    `GET` the Physical Data Type specified by `unique_name`
    """
    queryset = PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_SET

    serializer_class = PhysicalDataTypeNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    filterset_fields = PhysicalDataTypeFilter.get_fields()

    search_fields = PhysicalDataTypeAdmin.search_fields

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = None

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'physical_data_type_unique_name'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                PhysicalDataType._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                PhysicalDataType._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MeasurementUnitJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Measurement Units

    retrieve:
    `GET` the Measurement Unit specified by `unique_name`

    create:
    `POST` a new Measurement Unit by `unique_name`

    update:
    `PUT` updated data for the Measurement Unit specified by `unique_name`

    partial_update:
    `PATCH` the Measurement Unit specified by `unique_name`

    destroy:
    `DELETE` the Measurement Unit specified by `unique_name`
    """
    queryset = MEASUREMENT_UNIT_REST_API_QUERY_SET

    serializer_class = MeasurementUnitJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    # TODO: fix
    filterset_fields = \
        list(set(MeasurementUnitFilter.get_fields())
             - {'descriptions'})

    search_fields = MeasurementUnitAdmin.search_fields

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = None

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'measurement_unit_unique_name'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MeasurementUnit._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MeasurementUnit._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineClassJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Machine Classes

    retrieve:
    `GET` the Machine Class specified by `unique_name`

    create:
    `POST` a new Machine Class by `unique_name`

    update:
    `PUT` updated data for the Machine Class specified by `unique_name`

    partial_update:
    `PATCH` the Machine Class specified by `unique_name`

    destroy:
    `DELETE` the Machine Class specified by `unique_name`
    """
    queryset = MACHINE_CLASS_REST_API_QUERY_SET

    serializer_class = MachineClassJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    # TODO: fix
    filterset_fields = \
        list(set(MachineClassFilter.get_fields())
             - {'descriptions'})

    search_fields = MachineClassAdmin.search_fields

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = None

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'machine_class_unique_name'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineClass._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineClass._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineComponentJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Machine Components

    retrieve:
    `GET` the Machine Component specified by `id`

    create:
    `POST` a new Machine Component

    update:
    `PUT` updated data for the Machine Component specified by `id`

    partial_update:
    `PATCH` the Machine Component specified by `id`

    destroy:
    `DELETE` the Machine Component specified by `id`
    """
    queryset = MACHINE_COMPONENT_NESTED_REST_API_QUERY_SET

    prefetch_for_includes = {
        # '__all__': (),
    }

    serializer_class = MachineComponentNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    # TODO: fix
    filterset_fields = \
        list(set(MachineComponentFilter.get_fields())
             - {'descriptions'})

    search_fields = MachineComponentAdmin.search_fields

    ordering_fields = \
        'machine_class', \
        'name'

    ordering = \
        'machine_class', \
        'name'

    pagination_class = None

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineComponent._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineComponent._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineDataStreamJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Machine Data Streams

    retrieve:
    `GET` the Machine Data Stream specified by `id`

    create:
    `POST` a new Machine Data Stream

    update:
    `PUT` updated data for the Machine Data Stream specified by `id`

    partial_update:
    `PATCH` the Machine Data Stream specified by `id`

    destroy:
    `DELETE` the Machine Data Stream specified by `id`
    """
    queryset = MACHINE_DATA_STREAM_NESTED_REST_API_QUERY_SET

    serializer_class = MachineDataStreamNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    # TODO: fix
    filterset_fields = \
        list(set(MachineDataStreamFilter.get_fields())
             - {'descriptions'})

    search_fields = MachineDataStreamAdmin.search_fields

    ordering_fields = \
        'machine_class', \
        'name', \
        'machine_data_stream_type', \
        'logical_data_type', \
        'measurement_unit'

    ordering = \
        'machine_class', \
        'name'

    pagination_class = None

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineDataStream._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineDataStream._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Machine Families

    retrieve:
    `GET` the Machine Family specified by `unique_name`

    create:
    `POST` a new Machine Family

    update:
    `PUT` updated data for the Machine Family specified by `unique_name`

    partial_update:
    `PATCH` the Machine Family specified by `unique_name`

    destroy:
    `DELETE` the Machine Family specified by `unique_name`
    """
    queryset = MACHINE_FAMILY_NESTED_REST_API_QUERY_SET

    serializer_class = MachineFamilyNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'machine_family_unique_name'

    # TODO: fix
    filterset_fields = \
        list(set(MachineFamilyFilter.get_fields())
             - {'descriptions'})

    search_fields = MachineFamilyAdmin.search_fields

    ordering_fields = \
        'machine_class', \
        'unique_name'

    ordering = \
        'machine_class', \
        'unique_name'

    pagination_class = None

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineFamily._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineFamily._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineSKUJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Machine SKUs

    retrieve:
    `GET` the Machine SKU specified by `id`

    create:
    `POST` a new Machine SKU

    update:
    `PUT` updated data for the Machine SKU specified by `id`

    partial_update:
    `PATCH` the Machine SKU specified by `id`

    destroy:
    `DELETE` the Machine SKU specified by `id`
    """
    queryset = MACHINE_SKU_NESTED_REST_API_QUERY_SET

    serializer_class = MachineSKUNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    # TODO: fix
    filterset_fields = \
        list(set(MachineSKUFilter.get_fields())
             - {'descriptions'})

    search_fields = MachineSKUAdmin.search_fields

    ordering_fields = \
        'machine_class', \
        'unique_name'

    ordering = \
        'machine_class', \
        'unique_name'

    pagination_class = None

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineSKU._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineSKU._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class LocationJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Locations

    retrieve:
    `GET` the Location specified by `unique_name`

    create:
    `POST` a new Location

    update:
    `PUT` updated data for the Location specified by `unique_name`

    partial_update:
    `PATCH` the Location specified by `unique_name`

    destroy:
    `DELETE` the Location specified by `unique_name`
    """
    queryset = LOCATION_NESTED_REST_API_QUERY_SET

    serializer_class = LocationNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    # TODO: fix
    filterset_fields = \
        list(set(LocationFilter.get_fields())
             - {'info'})

    search_fields = LocationAdmin.search_fields

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = JsonApiLimitOffsetPagination

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'location_unique_name'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                Location._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                Location._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machines

    retrieve:
    `GET` the Machine specified by `unique_id`

    create:
    `POST` a new Machine

    update:
    `PUT` updated data for the Machine specified by `unique_id`

    partial_update:
    `PATCH` the Machine specified by `unique_id`

    destroy:
    `DELETE` the Machine specified by `unique_id`
    """
    queryset = MACHINE_REST_API_QUERY_SET

    serializer_class = MachineJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    # TODO: fix
    filterset_fields = \
        list(set(MachineFilter.get_fields())
             - {'info'})

    search_fields = MachineAdmin.search_fields

    ordering_fields = \
        'machine_class', \
        'machine_sku', \
        'unique_id', \
        'location'

    ordering = \
        'machine_class', \
        'machine_sku', \
        'unique_id'

    pagination_class = JsonApiLimitOffsetPagination

    lookup_field = 'unique_id'

    lookup_url_kwarg = 'machine_unique_id'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                Machine._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                Machine._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineDailyDataJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Daily Data records

    retrieve:
    `GET` the Machine Daily Data record specified by `id`
    """
    queryset = MACHINE_DATA_REST_API_QUERY_SET

    serializer_class = MachineDailyDataJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineDailyDataFilter.get_fields()

    search_fields = MachineDataAdmin.search_fields

    ordering_fields = \
        'machine', \
        'date'

    ordering = \
        'machine', \
        'date'

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineData._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineData._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineDataStreamDailyAggJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Data Field Daily Aggs

    retrieve:
    `GET` the Machine Data Field Daily Agg specified by `id`
    """
    queryset = \
        MachineDataStreamAgg.objects \
        .select_related(
            'machine',
            'machine_data_stream', 'machine_data_stream__machine_class', 'machine_data_stream__machine_data_stream_type')

    serializer_class = MachineDataStreamDailyAggJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineDataStreamDailyAggFilter.get_fields()

    search_fields = MachineDataStreamAggAdmin.search_fields

    ordering_fields = \
        'machine', \
        'machine_data_stream', \
        'date'

    # ordering = ()   # too numerous to order by default

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineDataStreamAgg._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON REST API: {}'.format(
                __module__,
                MachineDataStreamAgg._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyDataStreamProfileJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Family Data Stream Profiles

    retrieve:
    `GET` the Machine Family Data Stream Profile specified by `id`
    """
    queryset = MACHINE_FAMILY_DATA_STREAM_PROFILE_REST_API_QUERY_SET

    serializer_class = MachineFamilyDataStreamProfileJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineFamilyDataStreamProfileFilter.get_fields()

    search_fields = MachineFamilyDataStreamProfileAdmin.search_fields

    ordering_fields = \
        'machine_family', \
        'machine_data_stream', \
        'data_to_date'

    ordering = \
        'machine_family', \
        'machine_data_stream', \
        '-data_to_date'

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyDataStreamProfile._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyDataStreamProfile._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyDataStreamPairCorrJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Family Data Stream Pairwise Correlations

    retrieve:
    `GET` the Machine Family Data Stream Pairwise Correlation specified by `id`
    """
    queryset = MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_REST_API_QUERY_SET

    serializer_class = MachineFamilyDataStreamPairCorrJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineFamilyDataStreamPairCorrFilter.get_fields()

    search_fields = MachineFamilyDataStreamPairCorrAdmin.search_fields

    ordering_fields = \
        'machine_family', \
        'machine_data_stream', \
        'other_machine_data_stream', \
        'data_to_date', \
        'corr'

    ordering = \
        'machine_family', \
        '-data_to_date', \
        '-corr'

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyDataStreamPairCorr._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyDataStreamPairCorr._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
