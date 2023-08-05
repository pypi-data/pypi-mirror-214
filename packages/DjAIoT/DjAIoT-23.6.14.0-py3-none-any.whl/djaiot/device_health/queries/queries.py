from django_model_query_graphs import PK_FIELD_NAME, ModelQueryGraph

from ..data.queries import \
    MACHINE_CLASS_FULL_QUERY_GRAPH, \
    MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_FULL_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_FAMILY_FULL_QUERY_GRAPH, \
    MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_FULL_QUERY_GRAPH, \
    MACHINE_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_FULL_QUERY_GRAPH

from .models import \
    EnvironmentVariable, \
    MachineFamilyHealthServiceConfig, MachineFamilyVitalDataStreamConfig, \
    AI, MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScoreMethod, MachineHealthRiskScore, \
    MachineHealthRiskAlert, \
    MachineHealthProblem, MachineHealthProblemDiagnosis, \
    MachineMaintenanceRepairAction, \
    MachineErrorCode, MachineError


ENVIRONMENT_VARIABLE_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        EnvironmentVariable,
        'key',
        'value',
        ORDER=True)

ENVIRONMENT_VARIABLE_FULL_QUERY_SET = \
    ENVIRONMENT_VARIABLE_FULL_QUERY_GRAPH.query_set()


ENVIRONMENT_VARIABLE_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        EnvironmentVariable,
        'key',
        'value',
        ORDER=True)

ENVIRONMENT_VARIABLE_STR_QUERY_SET = \
    ENVIRONMENT_VARIABLE_STR_QUERY_GRAPH.query_set()


ENVIRONMENT_VARIABLE_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        EnvironmentVariable,
        'key',
        'value',
        ORDER=False)

ENVIRONMENT_VARIABLE_STR_UNORDERED_QUERY_SET = \
    ENVIRONMENT_VARIABLE_STR_UNORDERED_QUERY_GRAPH.query_set()


ENVIRONMENT_VARIABLE_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        EnvironmentVariable,
        'key',
        'value',
        ORDER=True)

ENVIRONMENT_VARIABLE_ABBR_QUERY_SET = \
    ENVIRONMENT_VARIABLE_ABBR_QUERY_GRAPH.query_set()


ENVIRONMENT_VARIABLE_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        EnvironmentVariable,
        PK_FIELD_NAME,
        ORDER=False)

ENVIRONMENT_VARIABLE_PK_ONLY_UNORDERED_QUERY_SET = \
    ENVIRONMENT_VARIABLE_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyHealthServiceConfig,
        'incl_cat_input_machine_data_streams',
        'from_date',
        'to_date',
        'configs',
        'active',
        'comments',
        machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_FULL_QUERY_SET = \
    MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyHealthServiceConfig,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalDataStreamConfig,
        'high_corr_num_machine_data_streams',
        'auto_incl_input_machine_data_streams',
        'low_corr_num_machine_data_streams',
        'active',
        machine_family_health_service_config=MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_FULL_QUERY_GRAPH,
        vital_machine_data_stream=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        vital_machine_data_stream_profile=MACHINE_FAMILY_DATA_STREAM_PROFILE_FULL_QUERY_GRAPH,
        incl_input_machine_data_streams=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        excl_input_machine_data_streams=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_FULL_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalDataStreamConfig,
        'machine_family_health_service_config',
        'active',
        vital_machine_data_stream=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        incl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER='vital_machine_data_stream__name')

MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalDataStreamConfig,
        'machine_family_health_service_config',
        'active',
        vital_machine_data_stream=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        incl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER='vital_machine_data_stream__name')

MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalDataStreamConfig,
        'machine_family_health_service_config',
        'active',
        vital_machine_data_stream=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        incl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalDataStreamConfig,
        'machine_family_health_service_config',
        'active',
        vital_machine_data_stream=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        incl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_ABBR_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalDataStreamConfig,
        'machine_family_health_service_config',
        'active',
        vital_machine_data_stream=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        incl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER='vital_machine_data_stream__name')

MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_NAME_ONLY_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalDataStreamConfig,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyHealthServiceConfig,
        'incl_cat_input_machine_data_streams',
        'from_date',
        'to_date',
        'configs',
        'active',
        'comments',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine_family_vital_data_stream_configs=MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_STR_QUERY_SET = \
    MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyHealthServiceConfig,
        'incl_cat_input_machine_data_streams',
        'from_date',
        'to_date',
        'configs',
        'active',
        'comments',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine_family_vital_data_stream_configs=MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_STR_UNORDERED_QUERY_GRAPH.query_set()


AI_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        AI,
        'ref_data_to_date',
        'created',
        'unique_id',
        'active',
        'ref_eval_metrics',
        machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        ORDER=True)

AI_FULL_QUERY_SET = \
    AI_FULL_QUERY_GRAPH.query_set()


AI_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        AI,
        'created',
        'unique_id',
        'active',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

AI_STR_QUERY_SET = \
    AI_STR_QUERY_GRAPH.query_set()


AI_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        AI,
        'created',
        'unique_id',
        'active',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

AI_STR_UNORDERED_QUERY_SET = \
    AI_STR_UNORDERED_QUERY_GRAPH.query_set()


AI_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        AI,
        'created',
        'unique_id',
        'active',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

AI_ABBR_QUERY_SET = \
    AI_ABBR_QUERY_GRAPH.query_set()


AI_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        AI,
        'unique_id',
        ORDER='unique_id')

AI_NAME_ONLY_QUERY_SET = \
    AI_NAME_ONLY_QUERY_GRAPH.query_set()


AI_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        AI,
        PK_FIELD_NAME,
        ORDER=False)

AI_PK_ONLY_UNORDERED_QUERY_SET = \
    AI_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalAIEvalMetricProfile,
        'ref_data_to_date',
        'N',
        'R2',
        'MAE',
        'MedAE',
        'RMSE',
        machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_FULL_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalAIEvalMetricProfile,
        'ref_data_to_date',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_STR_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalAIEvalMetricProfile,
        'ref_data_to_date',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalAIEvalMetricProfile,
        'ref_data_to_date',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_ABBR_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyVitalAIEvalMetricProfile,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_METHOD_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScoreMethod,
        'name',
        'info',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_SCORE_METHOD_FULL_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_METHOD_FULL_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_METHOD_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScoreMethod,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_SCORE_METHOD_STR_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_METHOD_STR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_METHOD_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScoreMethod,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER='name')

MACHINE_HEALTH_RISK_SCORE_METHOD_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_METHOD_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScoreMethod,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_METHOD_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScoreMethod,
        'name',
        ORDER='name')

MACHINE_HEALTH_RISK_SCORE_METHOD_ABBR_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_METHOD_ABBR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScoreMethod,
        'name',
        ORDER='name')

MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_METHOD_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScoreMethod,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_HEALTH_RISK_SCORE_METHOD_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_METHOD_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScore,
        'machine_health_risk_score_value',
        machine_family_data=MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH,
        machine=MACHINE_FULL_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_SCORE_FULL_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_FULL_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScore,
        'machine_health_risk_score_value',
        machine_family_data=MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_SCORE_STR_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_STR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScore,
        'machine_health_risk_score_value',
        machine_family_data=MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_HEALTH_RISK_SCORE_STR_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScore,
        'machine_health_risk_score_value',
        machine_family_data=MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_SCORE_ABBR_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_ABBR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_SCORE_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskScore,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_HEALTH_RISK_SCORE_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_SCORE_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_ALERT_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskAlert,
        'machine_health_risk_score_value_alert_threshold',
        'from_date',
        'to_date',
        'date_range',
        'duration',
        'ongoing',
        'last_machine_health_risk_score_value',
        'cum_excess_machine_health_risk_score_value',
        'approx_average_machine_health_risk_score_value',
        'info',
        'has_machine_health_problem_diagnoses',
        'has_machine_maintenance_repair_actions',
        'has_machine_errors',
        machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        machine=MACHINE_FULL_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_ALERT_FULL_QUERY_SET = \
    MACHINE_HEALTH_RISK_ALERT_FULL_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_ALERT_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskAlert,
        'machine_health_risk_score_value_alert_threshold',
        'from_date',
        'to_date',
        'duration',
        'ongoing',
        'last_machine_health_risk_score_value',
        'cum_excess_machine_health_risk_score_value',
        'approx_average_machine_health_risk_score_value',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_ALERT_STR_QUERY_SET = \
    MACHINE_HEALTH_RISK_ALERT_STR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_ALERT_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskAlert,
        'machine_health_risk_score_value_alert_threshold',
        'from_date',
        'to_date',
        'duration',
        'ongoing',
        'last_machine_health_risk_score_value',
        'cum_excess_machine_health_risk_score_value',
        'approx_average_machine_health_risk_score_value',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH,
        ORDER=('-ongoing',
               'machine_health_risk_score_method__name',
               '-machine_health_risk_score_value_alert_threshold'))

MACHINE_HEALTH_RISK_ALERT_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_ALERT_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_ALERT_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskAlert,
        'machine_health_risk_score_value_alert_threshold',
        'from_date',
        'to_date',
        'duration',
        'ongoing',
        'last_machine_health_risk_score_value',
        'cum_excess_machine_health_risk_score_value',
        'approx_average_machine_health_risk_score_value',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_HEALTH_RISK_ALERT_STR_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_ALERT_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_ALERT_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskAlert,
        'machine_health_risk_score_value_alert_threshold',
        'from_date',
        'to_date',
        'duration',
        'ongoing',
        'last_machine_health_risk_score_value',
        'cum_excess_machine_health_risk_score_value',
        'approx_average_machine_health_risk_score_value',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_RISK_ALERT_ABBR_QUERY_SET = \
    MACHINE_HEALTH_RISK_ALERT_ABBR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_RISK_ALERT_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthRiskAlert,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_HEALTH_RISK_ALERT_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_RISK_ALERT_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblem,
        'name',
        'descriptions',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_PROBLEM_FULL_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_FULL_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblem,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_PROBLEM_STR_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_STR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblem,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER='name')

MACHINE_HEALTH_PROBLEM_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblem,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_HEALTH_PROBLEM_STR_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblem,
        'name',
        ORDER='name')

MACHINE_HEALTH_PROBLEM_ABBR_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_ABBR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblem,
        'name',
        ORDER='name')

MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblem,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_HEALTH_PROBLEM_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_DIAGNOSIS_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblemDiagnosis,
        'from_date',
        'to_date',
        'date_range',
        'duration',
        'ongoing',
        'has_machine_health_risk_alerts',
        'has_machine_maintenance_repair_actions',
        'has_machine_errors',
        machine=MACHINE_FULL_QUERY_GRAPH,
        machine_health_problems=MACHINE_HEALTH_PROBLEM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_PROBLEM_DIAGNOSIS_FULL_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_DIAGNOSIS_FULL_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblemDiagnosis,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_health_problems=MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblemDiagnosis,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_health_problems=MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH,
        ORDER=('-to_date', 'from_date'))

MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblemDiagnosis,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_health_problems=MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_UNORDERED_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_DIAGNOSIS_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblemDiagnosis,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_health_problems=MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH,
        ORDER=('-to_date', 'from_date'))

MACHINE_HEALTH_PROBLEM_DIAGNOSIS_ABBR_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_DIAGNOSIS_ABBR_QUERY_GRAPH.query_set()


MACHINE_HEALTH_PROBLEM_DIAGNOSIS_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineHealthProblemDiagnosis,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_HEALTH_PROBLEM_DIAGNOSIS_PK_ONLY_UNORDERE_QUERY_SET = \
    MACHINE_HEALTH_PROBLEM_DIAGNOSIS_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_MAINTENANCE_REPAIR_ACTION_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineMaintenanceRepairAction,
        'from_date',
        'to_date',
        'date_range',
        'duration',
        'ongoing',
        'has_machine_health_risk_alerts',
        'has_machine_health_problem_diagnoses',
        'has_machine_errors',
        machine=MACHINE_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_MAINTENANCE_REPAIR_ACTION_FULL_QUERY_SET = \
    MACHINE_MAINTENANCE_REPAIR_ACTION_FULL_QUERY_GRAPH.query_set()


MACHINE_MAINTENANCE_REPAIR_ACTION_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineMaintenanceRepairAction,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_MAINTENANCE_REPAIR_ACTION_STR_QUERY_SET = \
    MACHINE_MAINTENANCE_REPAIR_ACTION_STR_QUERY_GRAPH.query_set()


MACHINE_MAINTENANCE_REPAIR_ACTION_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineMaintenanceRepairAction,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        ORDER=('-from_date', 'to_date'))

MACHINE_MAINTENANCE_REPAIR_ACTION_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_MAINTENANCE_REPAIR_ACTION_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_MAINTENANCE_REPAIR_ACTION_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineMaintenanceRepairAction,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_MAINTENANCE_REPAIR_ACTION_STR_UNORDERED_QUERY_SET = \
    MACHINE_MAINTENANCE_REPAIR_ACTION_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_MAINTENANCE_REPAIR_ACTION_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineMaintenanceRepairAction,
        'from_date',
        'to_date',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        ORDER=('-from_date', 'to_date'))

MACHINE_MAINTENANCE_REPAIR_ACTION_ABBR_QUERY_SET = \
    MACHINE_MAINTENANCE_REPAIR_ACTION_ABBR_QUERY_GRAPH.query_set()


MACHINE_MAINTENANCE_REPAIR_ACTION_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineMaintenanceRepairAction,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_MAINTENANCE_REPAIR_ACTION_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_MAINTENANCE_REPAIR_ACTION_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_ERROR_CODE_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineErrorCode,
        'name',
        'descriptions',
        'excl_n_days_of_machine_data_before',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_ERROR_CODE_FULL_QUERY_SET = \
    MACHINE_ERROR_CODE_FULL_QUERY_GRAPH.query_set()


MACHINE_ERROR_CODE_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineErrorCode,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_ERROR_CODE_STR_QUERY_SET = \
    MACHINE_ERROR_CODE_STR_QUERY_GRAPH.query_set()


MACHINE_ERROR_CODE_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineErrorCode,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER='name')

MACHINE_ERROR_CODE_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_ERROR_CODE_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_ERROR_CODE_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineErrorCode,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_ERROR_CODE_STR_UNORDERED_QUERY_SET = \
    MACHINE_ERROR_CODE_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_ERROR_CODE_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineErrorCode,
        'name',
        ORDER='name')

MACHINE_ERROR_CODE_ABBR_QUERY_SET = \
    MACHINE_ERROR_CODE_ABBR_QUERY_GRAPH.query_set()


MACHINE_ERROR_CODE_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineErrorCode,
        'name',
        ORDER='name')

MACHINE_ERROR_CODE_NAME_ONLY_QUERY_SET = \
    MACHINE_ERROR_CODE_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_ERROR_CODE_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineErrorCode,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_ERROR_CODE_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_ERROR_CODE_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_ERROR_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineError,
        'from_utc_date_time',
        'to_utc_date_time',
        'duration',
        'date_range',
        'has_machine_health_risk_alerts',
        'has_machine_health_problem_diagnoses',
        'has_machine_maintenance_repair_actions',
        machine=MACHINE_FULL_QUERY_GRAPH,
        machine_error_code=MACHINE_ERROR_CODE_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_ERROR_FULL_QUERY_SET = \
    MACHINE_ERROR_FULL_QUERY_GRAPH.query_set()


MACHINE_ERROR_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineError,
        'from_utc_date_time',
        'to_utc_date_time',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_error_code=MACHINE_ERROR_CODE_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_ERROR_STR_QUERY_SET = \
    MACHINE_ERROR_STR_QUERY_GRAPH.query_set()


MACHINE_ERROR_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineError,
        'from_utc_date_time',
        'to_utc_date_time',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_error_code=MACHINE_ERROR_CODE_NAME_ONLY_QUERY_GRAPH,
        ORDER='-from_utc_date_time')

MACHINE_ERROR_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_ERROR_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_ERROR_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineError,
        'from_utc_date_time',
        'to_utc_date_time',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_error_code=MACHINE_ERROR_CODE_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_ERROR_STR_UNORDERED_QUERY_SET = \
    MACHINE_ERROR_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_ERROR_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineError,
        'from_utc_date_time',
        'to_utc_date_time',
        'duration',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        machine_error_code=MACHINE_ERROR_CODE_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_ERROR_ABBR_QUERY_SET = \
    MACHINE_ERROR_ABBR_QUERY_GRAPH.query_set()


MACHINE_ERROR_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineError,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_ERROR_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_ERROR_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()
