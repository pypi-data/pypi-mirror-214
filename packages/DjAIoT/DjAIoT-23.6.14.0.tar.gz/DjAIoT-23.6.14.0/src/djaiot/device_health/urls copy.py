from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .api.rest.core.views import \
    EnvironmentVariableViewSet, \
    MachineFamilyHealthServiceConfigViewSet, \
    AIViewSet, \
    MachineFamilyVitalDataStreamAIEvalMetricProfileViewSet, \
    MachineDailyRiskScoreViewSet, \
    MachineProblemDiagnosisViewSet, \
    AlertViewSet, \
    MachineErrorCodeViewSet, MachineErrorViewSet

from .api.rest.json.views import \
    EnvironmentVariableJSONAPIViewSet, \
    MachineFamilyHealthServiceConfigJSONAPIViewSet, \
    AIJSONAPIViewSet, \
    MachineFamilyVitalDataStreamAIEvalMetricProfileJSONAPIViewSet, \
    MachineDailyRiskScoreJSONAPIViewSet, \
    MachineProblemDiagnosisJSONAPIViewSet, \
    AlertJSONAPIViewSet, \
    MachineErrorCodeJSONAPIViewSet, MachineErrorJSONAPIViewSet

from .autocompletes import AUTOCOMPLETE_URL_PATTERNS


API_END_POINT_PREFIX = __name__.split('.')[-2]

ENVIRONMENT_VARIABLES_PREFIX = \
    'environment-variables'
MACHINE_FAMILY_HEALTH_SERVICE_CONFIGS_PREFIX = \
    'machine-family-health-service-configs'
AI_PREFIX = \
    'ai'
MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILES_PREFIX = \
    'machine-family-vital-data-stream-ai-eval-metric-profiles'
MACHINE_DAILY_RISK_SCORES_PREFIX = \
    'machine-daily-risk-scores'
MACHINE_PROBLEM_DIAGNOSES_PREFIX = \
    'machine-problem-diagnoses'
ALERTS_PREFIX = \
    'alerts'
MACHINE_ERROR_CODES_PREFIX = \
    'machine-error-codes'
MACHINE_ERRORS_PREFIX = \
    'machine-errors'


CORE_REST_API_ROUTER = \
    DefaultRouter(
        trailing_slash=False)

CORE_REST_API_ROUTER.register(
    prefix=ENVIRONMENT_VARIABLES_PREFIX,
    viewset=EnvironmentVariableViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_HEALTH_SERVICE_CONFIGS_PREFIX,
    viewset=MachineFamilyHealthServiceConfigViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=AI_PREFIX,
    viewset=AIViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILES_PREFIX,
    viewset=MachineFamilyVitalDataStreamAIEvalMetricProfileViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_DAILY_RISK_SCORES_PREFIX,
    viewset=MachineDailyRiskScoreViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_PROBLEM_DIAGNOSES_PREFIX,
    viewset=MachineProblemDiagnosisViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=ALERTS_PREFIX,
    viewset=AlertViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_ERROR_CODES_PREFIX,
    viewset=MachineErrorCodeViewSet,
    basename=None)

CORE_REST_API_ROUTER.register(
    prefix=MACHINE_ERRORS_PREFIX,
    viewset=MachineErrorViewSet,
    basename=None)


JSON_REST_API_ROUTER = \
    DefaultRouter(
        trailing_slash=False)

JSON_REST_API_ROUTER.register(
    prefix=ENVIRONMENT_VARIABLES_PREFIX,
    viewset=EnvironmentVariableJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_HEALTH_SERVICE_CONFIGS_PREFIX,
    viewset=MachineFamilyHealthServiceConfigJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=AI_PREFIX,
    viewset=AIJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILES_PREFIX,
    viewset=MachineFamilyVitalDataStreamAIEvalMetricProfileJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_DAILY_RISK_SCORES_PREFIX,
    viewset=MachineDailyRiskScoreJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_PROBLEM_DIAGNOSES_PREFIX,
    viewset=MachineProblemDiagnosisJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=ALERTS_PREFIX,
    viewset=AlertJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_ERROR_CODES_PREFIX,
    viewset=MachineErrorCodeJSONAPIViewSet,
    basename=None)

JSON_REST_API_ROUTER.register(
    prefix=MACHINE_ERRORS_PREFIX,
    viewset=MachineErrorJSONAPIViewSet,
    basename=None)


URL_PATTERNS = [
    # API URLs
    path('api/rest/core/{}/'.format(API_END_POINT_PREFIX),
         include(CORE_REST_API_ROUTER.urls)),

    path('api/rest/json/{}/'.format(API_END_POINT_PREFIX),
         include(JSON_REST_API_ROUTER.urls))

] + AUTOCOMPLETE_URL_PATTERNS
