from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token

from rest_framework.authentication import \
    BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.generics import GenericAPIView, \
    ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import \
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer, \
    HTMLFormRenderer, StaticHTMLRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rest_framework.filters import OrderingFilter
from rest_framework_filters.backends import ComplexFilterBackend, RestFrameworkFilterBackend

from silk.profiling.profiler import silk_profile

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

from .serializers import \
    EnvironmentVariableSerializer, \
    PhysicalDataTypeNestedSerializer, \
    MeasurementUnitSerializer, \
    MachineClassSerializer, \
    MachineComponentNestedSerializer, \
    MachineDataStreamNestedSerializer, \
    MachineFamilyNestedSerializer, \
    MachineSKUNestedSerializer, \
    LocationNestedSerializer, \
    MachineSerializer, \
    MachineDailyDataSerializer, \
    MachineDataStreamDailyAggSerializer, \
    MachineFamilyDataStreamProfileSerializer, \
    MachineFamilyDataStreamPairCorrSerializer


class EnvironmentVariableViewSet(ModelViewSet):
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

    serializer_class = EnvironmentVariableSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = EnvironmentVariableFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = 'key',

    ordering = 'key',

    pagination_class = None

    lookup_field = 'key'

    lookup_url_kwarg = 'environment_variable_key'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class PhysicalDataTypeViewSet(ModelViewSet):
    """
    list:
    `GET` an filterable, unpaginated list of Physical Data Types

    retrieve:
    `GET` the Physical Data Type specified by `unique_name`
    """
    queryset = PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_SET

    serializer_class = PhysicalDataTypeNestedSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    filter_class = PhysicalDataTypeFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = None

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'physical_data_type_unique_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                PhysicalDataType._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                PhysicalDataType._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MeasurementUnitViewSet(ModelViewSet):
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

    serializer_class = MeasurementUnitSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticatedOrReadOnly,

    filter_class = MeasurementUnitFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = None

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'measurement_unit_unique_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MeasurementUnit._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MeasurementUnit._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineClassViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, non-paginated list of Machine Classes

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

    serializer_class = MachineClassSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = MachineClassFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = None

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'machine_class_unique_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineClass._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineClass._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineComponentViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, non-paginated list of Machine Components

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

    serializer_class = MachineComponentNestedSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = MachineComponentFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = \
        'machine_class', \
        'name'

    ordering = \
        'machine_class', \
        'name'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineComponent._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineComponent._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineDataStreamViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, non-paginated list of Machine Data Streams

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

    serializer_class = MachineDataStreamNestedSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = MachineDataStreamFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

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

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineDataStream._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineDataStream._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, non-paginated list of Machine Families

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

    serializer_class = MachineFamilyNestedSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'machine_family_unique_name'

    filter_class = MachineFamilyFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = \
        'machine_class', \
        'unique_name'

    ordering = \
        'machine_class', \
        'unique_name'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineFamily._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineFamily._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineSKUViewSet(ModelViewSet):
    """
    list:
    `GET` a filterable, non-paginated list of Machine SKUs

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

    serializer_class = MachineSKUNestedSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = MachineSKUFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = \
        'machine_class', \
        'unique_name'

    ordering = \
        'machine_class', \
        'unique_name'

    pagination_class = None

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineSKU._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineSKU._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class LocationViewSet(ModelViewSet):
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

    serializer_class = LocationNestedSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = LocationFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = LimitOffsetPagination

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'location_unique_name'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                Location._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                Location._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineViewSet(ModelViewSet):
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

    serializer_class = MachineSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = MachineFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = \
        'machine_class', \
        'machine_sku', \
        'unique_id', \
        'location'

    ordering = \
        'machine_class', \
        'machine_sku', \
        'unique_id'

    pagination_class = LimitOffsetPagination

    lookup_field = 'unique_id'

    lookup_url_kwarg = 'machine_unique_id'

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                Machine._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                Machine._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineDailyDataViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Daily Data records

    retrieve:
    `GET` the Machine Daily Data record specified by `id`
    """
    queryset = MACHINE_DATA_REST_API_QUERY_SET

    serializer_class = MachineDailyDataSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = MachineDailyDataFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = \
        'machine', \
        'date'

    ordering = \
        'machine', \
        'date'

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineData._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
                __module__,
                MachineData._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineDataStreamDailyAggViewSet(ReadOnlyModelViewSet):
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

    serializer_class = MachineDataStreamDailyAggSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filter_class = MachineDataStreamDailyAggFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = \
        'machine', \
        'machine_data_stream', \
        'date'

    # ordering = ()   # too numerous to order by default

    pagination_class = LimitOffsetPagination

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    @silk_profile(
        name='{}: Core REST API: {}'.format(
            __module__,
            MachineDataStreamAgg._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core REST API: {}'.format(
            __module__,
            MachineDataStreamAgg._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyDataStreamProfileViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Family Data Stream Profiles

    retrieve:
    `GET` the Machine Family Data Stream Profile specified by `id`
    """
    queryset = MACHINE_FAMILY_DATA_STREAM_PROFILE_REST_API_QUERY_SET

    serializer_class = MachineFamilyDataStreamProfileSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = IsAuthenticated,

    filter_class = MachineFamilyDataStreamProfileFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

    ordering_fields = \
        'machine_family', \
        'machine_data_stream', \
        'data_to_date'

    ordering = \
        'machine_family', \
        'machine_data_stream', \
        '-data_to_date'

    pagination_class = LimitOffsetPagination

    @silk_profile(
        name='{}: Core API: {}'.format(
                __module__,
                MachineFamilyDataStreamProfile._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core API: {}'.format(
                __module__,
                MachineFamilyDataStreamProfile._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyDataStreamPairCorrViewSet(ReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Family Data Stream Pairwise Correlations

    retrieve:
    `GET` the Machine Family Data Stream Pairwise Correlation specified by `id`
    """
    queryset = MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_REST_API_QUERY_SET

    serializer_class = MachineFamilyDataStreamPairCorrSerializer

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    renderer_classes = \
        CoreJSONRenderer, \
        JSONRenderer

    permission_classes = IsAuthenticated,

    filter_class = MachineFamilyDataStreamPairCorrFilter

    filter_backends = \
        OrderingFilter, \
        ComplexFilterBackend, \
        RestFrameworkFilterBackend

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

    pagination_class = LimitOffsetPagination

    @silk_profile(
        name='{}: Core API: {}'.format(
                __module__,
                MachineFamilyDataStreamPairCorr._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: Core API: {}'.format(
                __module__,
                MachineFamilyDataStreamPairCorr._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


# request.data
# Response(serializer.data, status=HTTP_201_CREATED)
# Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
