from rest_framework.authentication import \
    BasicAuthentication, RemoteUserAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_json_api.pagination import JsonApiLimitOffsetPagination
from rest_framework_json_api.renderers import \
    JSONRenderer as JSONAPIJSONRenderer
from rest_framework_json_api.views import \
    ModelViewSet as JSONAPIModelViewSet, \
    ReadOnlyModelViewSet as JSONAPIReadOnlyModelViewSet, \
    RelationshipView

from silk.profiling.profiler import silk_profile

from ....admin import \
    EnvironmentVariableAdmin, \
    MachineFamilyHealthServiceConfigAdmin, \
    AIAdmin, \
    MachineFamilyVitalDataStreamAIEvalMetricProfileAdmin, \
    MachineDailyRiskScoreAdmin, \
    MachineProblemDiagnosisAdmin, \
    MachineHealthRiskAlertAdmin, \
    MachineErrorCodeAdmin, MachineErrorAdmin

from ....filters import \
    EnvironmentVariableFilter, \
    MachineFamilyHealthServiceConfigFilter, \
    AIFilter, \
    MachineFamilyVitalDataStreamAIEvalMetricProfileFilter, \
    MachineDailyRiskScoreFilter, \
    MachineProblemDiagnosisFilter, \
    AlertFilter, \
    MachineErrorCodeFilter, MachineErrorFilter

from ....models import \
    EnvironmentVariable, \
    MachineFamilyHealthServiceConfig, \
    AI, \
    MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScore, \
    MachineHealthProblemDiagnosis, \
    MachineHealthRiskAlert, \
    MachineErrorCode, MachineError

from ..queries import \
    ENVIRONMENT_VARIABLE_REST_API_QUERY_SET, \
    MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_REST_API_QUERY_SET, \
    AI_REST_API_QUERY_SET, \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_REST_API_QUERY_SET, \
    MACHINE_DAILY_RISK_SCORE_REST_API_QUERY_SET, \
    MACHINE_PROBLEM_DIAGNOSIS_NESTED_REST_API_QUERY_SET, \
    ALERT_NESTED_REST_API_QUERY_SET, \
    MACHINE_ERROR_CODE_REST_API_QUERY_SET, \
    MACHINE_ERROR_NESTED_REST_API_QUERY_SET

from .serializers import \
    EnvironmentVariableJSONAPISerializer, \
    MachineFamilyHealthServiceConfigJSONAPISerializer, \
    AIJSONAPISerializer, \
    MachineFamilyVitalDataStreamAIEvalMetricProfileJSONAPISerializer, \
    MachineDailyRiskScoreJSONAPISerializer, \
    MachineProblemDiagnosisNestedJSONAPISerializer, \
    AlertNestedJSONAPISerializer, \
    MachineErrorCodeJSONAPISerializer, MachineErrorNestedJSONAPISerializer


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
        name='{}: JSON API: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyHealthServiceConfigJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, unpaginated list of Machine Family Health Service Configs

    retrieve:
    `GET` the Machine Family Health Service Config specified by `id`
    """
    queryset = MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_REST_API_QUERY_SET

    prefetch_for_includes = {
        # '__all__': ()
    }

    serializer_class = MachineFamilyHealthServiceConfigJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineFamilyHealthServiceConfigFilter.get_fields()

    search_fields = MachineFamilyHealthServiceConfigAdmin.search_fields

    ordering_fields = \
        'active', \
        'machine_family'

    ordering = \
        '-active', \
        'machine_family'

    pagination_class = None

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyHealthServiceConfig._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyHealthServiceConfig._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class AIJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of AIs

    retrieve:
    `GET` the AI specified by `unique_id`
    """
    queryset = AI_REST_API_QUERY_SET

    serializer_class = AIJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = AIFilter.get_fields()

    search_fields = AIAdmin.search_fields

    ordering_fields = \
        'machine_family', \
        'ref_data_to_date', \
        'created'

    ordering = \
        'machine_family', \
        '-ref_data_to_date', \
        '-created'

    pagination_class = JsonApiLimitOffsetPagination

    lookup_field = 'unique_id'

    lookup_url_kwarg = 'ai_unique_id'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                AI._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                AI._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineFamilyVitalDataStreamAIEvalMetricProfileJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Family Vital Data Stream AI Benchmark Metric Profiles

    retrieve:
    `GET` the Machine Family Vital Data Stream AI Benchmark Metric Profile specified by `id`
    """
    queryset = MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_REST_API_QUERY_SET

    serializer_class = MachineFamilyVitalDataStreamAIEvalMetricProfileJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineFamilyVitalDataStreamAIEvalMetricProfileFilter.get_fields()

    search_fields = MachineFamilyVitalDataStreamAIEvalMetricProfileAdmin.search_fields

    ordering_fields = \
        'machine_family', \
        'machine_data_stream', \
        'ref_data_to_date'

    ordering = \
        'machine_family', \
        'machine_data_stream', \
        '-ref_data_to_date'

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyVitalAIEvalMetricProfile._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineFamilyVitalAIEvalMetricProfile._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineDailyRiskScoreJSONAPIViewSet(JSONAPIReadOnlyModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Daily Risk Scores

    retrieve:
    `GET` the Machine Daily Risk Score specified by `id`
    """
    queryset = MACHINE_DAILY_RISK_SCORE_REST_API_QUERY_SET

    serializer_class = MachineDailyRiskScoreJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineDailyRiskScoreFilter.get_fields()

    search_fields = MachineDailyRiskScoreAdmin.search_fields

    ordering_fields = \
        'machine_family', \
        'machine', \
        'risk_score_name', \
        'date'

    # ordering = ()   # too numerous to order by default

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineHealthRiskScore._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineHealthRiskScore._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineProblemDiagnosisJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Problem Diagnoses

    retrieve:
    `GET` the Machine Problem Diagnosis specified by `id`

    partial_update:
    `PATCH` the `diagnosis_status` of the Machine Problem Diagnosis specified by `id`
    """
    queryset = MACHINE_PROBLEM_DIAGNOSIS_NESTED_REST_API_QUERY_SET

    serializer_class = MachineProblemDiagnosisNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineProblemDiagnosisFilter.get_fields()

    search_fields = MachineProblemDiagnosisAdmin.search_fields

    ordering_fields = \
        'from_date', \
        'to_date'

    ordering = \
        '-to_date', \
        'from_date'

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineHealthProblemDiagnosis._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineHealthProblemDiagnosis._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class AlertJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Alerts

    retrieve:
    `GET` the Alert specified by `id`

    partial_update:
    `PATCH` the `diagnosis_status` of the Alert specified by `id`
    """
    queryset = ALERT_NESTED_REST_API_QUERY_SET

    serializer_class = AlertNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = AlertFilter.get_fields()

    search_fields = MachineHealthRiskAlertAdmin.search_fields

    ordering_fields = \
        'ongoing', \
        'risk_score_name', \
        'threshold', \
        'cum_excess_risk_score'

    ordering = \
        '-ongoing', \
        'risk_score_name', \
        '-threshold', \
        '-cum_excess_risk_score'

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineHealthRiskAlert._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineHealthRiskAlert._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineErrorCodeJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Error Codes

    retrieve:
    `GET` the Machine Error Code specified by `unique_name`

    partial_update:
    `PATCH` the Machine Error Code specified by `unique_name`
    """
    queryset = MACHINE_ERROR_CODE_REST_API_QUERY_SET

    serializer_class = MachineErrorCodeJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = \
        list(set(MachineErrorCodeFilter.get_fields())
             - {'description'})

    search_fields = MachineErrorCodeAdmin.search_fields

    ordering_fields = 'unique_name',

    ordering = 'unique_name',

    pagination_class = JsonApiLimitOffsetPagination

    lookup_field = 'unique_name'

    lookup_url_kwarg = 'machine_error_code_unique_name'

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineErrorCode._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineErrorCode._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class MachineErrorJSONAPIViewSet(JSONAPIModelViewSet):
    """
    list:
    `GET` a filterable, paginated list of Machine Errors

    retrieve:
    `GET` the Machine Error specified by `id`

    partial_update:
    `PATCH` the Machine Error specified by `id`
    """
    queryset = MACHINE_ERROR_NESTED_REST_API_QUERY_SET

    serializer_class = MachineErrorNestedJSONAPISerializer
    resource_name = serializer_class.JSONAPIMeta.resource_name

    authentication_classes = \
        BasicAuthentication, \
        RemoteUserAuthentication, \
        SessionAuthentication, \
        TokenAuthentication

    permission_classes = IsAuthenticated,

    filterset_fields = MachineErrorFilter.get_fields()

    search_fields = MachineErrorAdmin.search_fields

    ordering_fields = \
        'machine', \
        'from_utc_date_time', \
        'to_utc_date_time'

    ordering = \
        '-to_utc_date_time', \
        'from_utc_date_time'

    pagination_class = JsonApiLimitOffsetPagination

    renderer_classes = JSONAPIJSONRenderer,

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineError._meta.verbose_name_plural))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @silk_profile(
        name='{}: JSON API: {}'.format(
                __module__,
                MachineError._meta.verbose_name))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
