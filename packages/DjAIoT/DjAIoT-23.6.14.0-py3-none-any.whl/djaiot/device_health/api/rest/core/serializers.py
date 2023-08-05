from rest_framework.serializers import \
    ModelSerializer, \
    RelatedField

from .....data.api.rest.core.serializers import \
    MACHINE_DATA_STREAM_RELATED_FIELD, MACHINE_DATA_STREAMS_RELATED_FIELD, \
    MACHINE_FAMILY_RELATED_FIELD, \
    MACHINE_RELATED_FIELD, \
    MachineFamilyDataStreamProfileSerializer

from ....models import \
    EnvironmentVariable, \
    MachineFamilyHealthServiceConfig, MachineFamilyVitalDataStreamConfig, \
    AI, \
    MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScore, \
    MachineHealthProblemDiagnosis, \
    MachineHealthRiskAlert, \
    MachineErrorCode, MachineError

from ...field_names import \
    ENVIRONMENT_VARIABLE_API_FIELD_NAMES, \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_API_FIELD_NAMES, \
    MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_API_FIELD_NAMES, \
    AI_API_FIELD_NAMES, \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_API_FIELD_NAMES, \
    MACHINE_DAILY_RISK_SCORE_API_FIELD_NAMES, \
    MACHINE_PROBLEM_DIAGNOSIS_API_FIELD_NAMES, MACHINE_PROBLEM_DIAGNOSIS_NESTED_API_FIELD_NAMES, \
    ALERT_API_FIELD_NAMES, ALERT_NESTED_API_FIELD_NAMES, \
    MACHINE_ERROR_CODE_API_FIELD_NAMES, \
    MACHINE_ERROR_API_FIELD_NAMES, MACHINE_ERROR_NESTED_API_FIELD_NAMES


class EnvironmentVariableSerializer(ModelSerializer):
    class Meta:
        model = EnvironmentVariable

        fields = ENVIRONMENT_VARIABLE_API_FIELD_NAMES


class MachineFamilyVitalDataStreamConfigSerializer(ModelSerializer):
    vital_machine_data_stream = MACHINE_DATA_STREAM_RELATED_FIELD

    vital_machine_data_stream_profile = \
        MachineFamilyDataStreamProfileSerializer(
            read_only=False,
            many=False,
            required=False)

    incl_input_machine_data_streams = MACHINE_DATA_STREAMS_RELATED_FIELD

    excl_input_machine_data_streams = MACHINE_DATA_STREAMS_RELATED_FIELD

    class Meta:
        model = MachineFamilyVitalDataStreamConfig

        fields = MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_API_FIELD_NAMES


class MachineFamilyHealthServiceConfigSerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    machine_family_vital_data_stream_configs = \
        MachineFamilyVitalDataStreamConfigSerializer(
            read_only=True,
            many=True,
            required=False)

    excl_input_machine_data_streams = MACHINE_DATA_STREAMS_RELATED_FIELD

    class Meta:
        model = MachineFamilyHealthServiceConfig

        fields = MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_API_FIELD_NAMES


class AISerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    class Meta:
        model = AI

        fields = AI_API_FIELD_NAMES


class MachineFamilyVitalDataStreamAIEvalMetricProfileSerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    machine_data_stream = MACHINE_DATA_STREAMS_RELATED_FIELD

    class Meta:
        model = MachineFamilyVitalAIEvalMetricProfile

        fields = MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_API_FIELD_NAMES


class MachineDailyRiskScoreSerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    machine = MACHINE_RELATED_FIELD

    class Meta:
        model = MachineHealthRiskScore

        fields = MACHINE_DAILY_RISK_SCORE_API_FIELD_NAMES


class MachineProblemLabelRelatedField(RelatedField):
    def to_internal_value(self, data):
        # TODO
        pass

    def to_representation(self, value):
        return str(value)


MACHINE_PROBLEM_LABELS_RELATED_FIELD = \
    MachineProblemLabelRelatedField(
        read_only=True,
        many=True,
        required=False)


class MachineProblemDiagnosisSerializer(ModelSerializer):
    machine = MACHINE_RELATED_FIELD

    labels = MACHINE_PROBLEM_LABELS_RELATED_FIELD

    class Meta:
        model = MachineHealthProblemDiagnosis

        fields = MACHINE_PROBLEM_DIAGNOSIS_API_FIELD_NAMES


MACHINE_PROBLEM_DIAGNOSES_RELATED_FIELD = \
    MachineProblemDiagnosisSerializer(
        read_only=True,
        many=True,
        required=False)


class AlertSerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    machine = MACHINE_RELATED_FIELD

    class Meta:
        model = MachineHealthRiskAlert

        fields = ALERT_API_FIELD_NAMES


ALERTS_RELATED_FIELD = \
    AlertSerializer(
        read_only=True,
        many=True,
        required=False)


class MachineErrorCodeSerializer(ModelSerializer):
    class Meta:
        model = MachineErrorCode

        fields = MACHINE_ERROR_CODE_API_FIELD_NAMES


class MachineErrorSerializer(ModelSerializer):
    machine = MACHINE_RELATED_FIELD

    machine_error_code = \
        MachineErrorCodeSerializer(
            read_only=False,
            many=False,
            required=True)

    class Meta:
        model = MachineError

        fields = MACHINE_ERROR_API_FIELD_NAMES


MACHINE_ERRORS_RELATED_FIELD = \
    MachineErrorSerializer(
        read_only=True,
        many=True,
        required=False)


class MachineProblemDiagnosisNestedSerializer(ModelSerializer):
    machine = MACHINE_RELATED_FIELD

    labels = MACHINE_PROBLEM_LABELS_RELATED_FIELD

    alerts = ALERTS_RELATED_FIELD

    machine_errors = MACHINE_ERRORS_RELATED_FIELD

    class Meta:
        model = MachineHealthProblemDiagnosis

        fields = MACHINE_PROBLEM_DIAGNOSIS_NESTED_API_FIELD_NAMES


class AlertNestedSerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    machine = MACHINE_RELATED_FIELD

    machine_problem_diagnoses = MACHINE_PROBLEM_DIAGNOSES_RELATED_FIELD

    machine_errors = MACHINE_ERRORS_RELATED_FIELD

    class Meta:
        model = MachineHealthRiskAlert

        fields = ALERT_NESTED_API_FIELD_NAMES


class MachineErrorNestedSerializer(ModelSerializer):
    machine = MACHINE_RELATED_FIELD

    machine_problem_diagnoses = MACHINE_PROBLEM_DIAGNOSES_RELATED_FIELD

    alerts = ALERTS_RELATED_FIELD

    class Meta:
        model = MachineError

        fields = MACHINE_ERROR_NESTED_API_FIELD_NAMES
