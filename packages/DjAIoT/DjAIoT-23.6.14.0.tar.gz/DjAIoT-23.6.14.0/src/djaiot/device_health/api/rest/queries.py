from django.db.models import Prefetch

from ....data.models import \
    MachineDataStream

from ....data.api.rest.queries import \
    MACHINE_DATA_STREAM_REST_API_QUERY_SET

from ...models import \
    EnvironmentVariable, \
    MachineFamilyHealthServiceConfig, MachineFamilyVitalDataStreamConfig, \
    AI, \
    MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScore, \
    MachineHealthProblemDiagnosis, \
    MachineHealthRiskAlert, \
    MachineErrorCode, MachineError

from ..field_names import \
    ENVIRONMENT_VARIABLE_API_FIELD_NAMES, \
    MACHINE_ERROR_CODE_API_FIELD_NAMES


ENVIRONMENT_VARIABLE_REST_API_QUERY_SET = \
    EnvironmentVariable.objects \
    .only(*ENVIRONMENT_VARIABLE_API_FIELD_NAMES)


MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_REST_API_QUERY_SET = \
    MachineFamilyHealthServiceConfig.objects.all() #\
    #.select_related(
    #    *MachineFamilyHealthServiceConfig._meta.FIELD_NAMES.SELECT_RELATED) \
    #.defer(
    #    *MachineFamilyHealthServiceConfig._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES) \
    #.prefetch_related(
    #    Prefetch(
    #        lookup=MachineFamilyVitalDataStreamConfig._meta.FIELD_NAMES.M2M,
    #        queryset=
    #            MachineFamilyVitalDataStreamConfig.objects
    #            .select_related(
    #                *MachineFamilyVitalDataStreamConfig._meta.FIELD_NAMES.FULL_SELECT_RELATED)
    #            .defer(
    #                *MachineFamilyVitalDataStreamConfig._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES)
    #            .prefetch_related(
    #                Prefetch(
    #                    lookup='incl_input_{}'.format(MachineDataStream._meta.FIELD_NAMES.M2M),
    #                    queryset=MACHINE_DATA_STREAM_REST_API_QUERY_SET),
    #                Prefetch(
    #                    lookup='excl_input_{}'.format(MachineDataStream._meta.FIELD_NAMES.M2M),
    #                    queryset=MACHINE_DATA_STREAM_REST_API_QUERY_SET))),
    #    Prefetch(
    #        lookup='excl_input_{}'.format(MachineDataStream._meta.FIELD_NAMES.M2M),
    #        queryset=MACHINE_DATA_STREAM_REST_API_QUERY_SET))


AI_REST_API_QUERY_SET = \
    AI.objects.all() #\
    #.select_related(
    #    *AI._meta.FIELD_NAMES.SELECT_RELATED) \
    #.defer(
    #    *AI._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES)


MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_REST_API_QUERY_SET = \
    MachineFamilyVitalAIEvalMetricProfile.objects.all() #\
    #.select_related(
    #    *MachineFamilyVitalAIEvalMetricProfile._meta.FIELD_NAMES.SELECT_RELATED) \
    #.defer(
    #    *MachineFamilyVitalAIEvalMetricProfile._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES)


MACHINE_DAILY_RISK_SCORE_REST_API_QUERY_SET = \
    MachineHealthRiskScore.objects.all() #\
    #.select_related(
    #    *MachineHealthRiskScore._meta.FIELD_NAMES.FULL_SELECT_RELATED) \
    #.defer(
    #    *MachineHealthRiskScore._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES)


MACHINE_PROBLEM_DIAGNOSIS_REST_API_QUERY_SET = \
    MachineHealthProblemDiagnosis.objects.all() #\
    #.select_related(
    #    *MachineHealthProblemDiagnosis._meta.FIELD_NAMES.FULL_SELECT_RELATED) \
    #.defer(
    #    *MachineHealthProblemDiagnosis._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES) \
    #.prefetch_related(
    #    Prefetch(
    #        lookup='labels'))


ALERT_REST_API_QUERY_SET = \
    MachineHealthRiskAlert.objects.all() #\
    #.select_related(
    #    *MachineHealthRiskAlert._meta.FIELD_NAMES.FULL_SELECT_RELATED) \
    #.defer(
    #    *MachineHealthRiskAlert._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES)


MACHINE_ERROR_CODE_REST_API_QUERY_SET = \
    MachineErrorCode.objects \
    .only(*MACHINE_ERROR_CODE_API_FIELD_NAMES)


MACHINE_ERROR_REST_API_QUERY_SET = \
    MachineError.objects #\
    #.select_related(
    #    *MachineError._meta.FIELD_NAMES.FULL_SELECT_RELATED) \
    #.defer(
    #    *MachineError._meta.FIELD_NAMES.DEFERRED_IN_FULL_QUERIES)


MACHINE_PROBLEM_DIAGNOSIS_NESTED_REST_API_QUERY_SET = \
    MACHINE_PROBLEM_DIAGNOSIS_REST_API_QUERY_SET #\
    #.prefetch_related(
    #    Prefetch(
    #        lookup=MachineHealthRiskAlert._meta.FIELD_NAMES.M2M,
    #        queryset=ALERT_REST_API_QUERY_SET),
    #    Prefetch(
    #        lookup=MachineError._meta.FIELD_NAMES.M2M,
    #        queryset=MACHINE_ERROR_REST_API_QUERY_SET))


ALERT_NESTED_REST_API_QUERY_SET = \
    ALERT_REST_API_QUERY_SET #\
    #.prefetch_related(
    #    Prefetch(
    #        lookup=MachineHealthProblemDiagnosis._meta.FIELD_NAMES.M2M,
    #        queryset=MACHINE_PROBLEM_DIAGNOSIS_REST_API_QUERY_SET),
    #    Prefetch(
    #        lookup=MachineError._meta.FIELD_NAMES.M2M,
    #        queryset=MACHINE_ERROR_REST_API_QUERY_SET))


MACHINE_ERROR_NESTED_REST_API_QUERY_SET = \
    MACHINE_ERROR_REST_API_QUERY_SET #\
    #.prefetch_related(
    #    Prefetch(
    #        lookup=MachineHealthProblemDiagnosis._meta.FIELD_NAMES.M2M,
    #        queryset=MACHINE_PROBLEM_DIAGNOSIS_REST_API_QUERY_SET),
    #    Prefetch(
    #        lookup=MachineHealthRiskAlert._meta.FIELD_NAMES.M2M,
    #        queryset=ALERT_REST_API_QUERY_SET))
