from rest_framework_json_api.relations import \
    HyperlinkedRelatedField as JSONAPIHyperlinkedRelatedField, \
    ResourceRelatedField
from rest_framework_json_api.serializers import \
    ModelSerializer as JSONAPIModelSerializer, \
    RelatedField as JSONAPIRelatedField

from .....data.models import \
    MachineFamily, \
    MachineDataStream, \
    Machine

from ....models import \
    EnvironmentVariable, \
    MachineFamilyHealthServiceConfig, MachineFamilyVitalDataStreamConfig, \
    AI, \
    MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScore, \
    MachineHealthProblemDiagnosis, \
    MachineHealthRiskAlert, \
    MachineErrorCode, MachineError

from .....data.api.rest.json.serializers import \
    MachineDataStreamJSONAPISerializer, \
    MachineFamilyJSONAPISerializer, \
    MachineJSONAPISerializer, \
    MachineFamilyDataStreamProfileJSONAPISerializer

from ...field_names import \
    ENVIRONMENT_VARIABLE_API_FIELD_NAMES, \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_API_FIELD_NAMES, \
    MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_API_FIELD_NAMES, \
    AI_API_FIELD_NAMES, \
    MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_API_FIELD_NAMES, \
    MACHINE_DAILY_RISK_SCORE_API_FIELD_NAMES, \
    MACHINE_PROBLEM_DIAGNOSIS_NESTED_API_FIELD_NAMES, \
    ALERT_NESTED_API_FIELD_NAMES, \
    MACHINE_ERROR_CODE_API_FIELD_NAMES, \
    MACHINE_ERROR_NESTED_API_FIELD_NAMES


class EnvironmentVariableJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = EnvironmentVariable

        fields = \
            ENVIRONMENT_VARIABLE_API_FIELD_NAMES   # + \
            # ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = EnvironmentVariable.JSONAPIMeta.resource_name

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineFamilyVitalDataStreamConfigJSONAPISerializer(JSONAPIModelSerializer):
    vital_machine_data_stream = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    vital_machine_data_stream_profile = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    incl_input_machine_data_streams = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    excl_input_machine_data_streams = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    included_serializers = related_serializers = \
        dict(vital_machine_data_stream=MachineDataStreamJSONAPISerializer,
             vital_machine_data_stream_profile=MachineFamilyDataStreamProfileJSONAPISerializer,
             incl_input_machine_data_streams=MachineDataStreamJSONAPISerializer,
             excl_input_machine_data_streams=MachineDataStreamJSONAPISerializer)

    class Meta:
        model = MachineFamilyVitalDataStreamConfig

        fields = \
            MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_API_FIELD_NAMES   # + \
            # ('url',)   # TODO: fix

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineFamilyVitalDataStreamConfig.JSONAPIMeta.resource_name

        included_resources = \
            'vital_machine_data_stream', \
            'vital_machine_data_stream_profile', \
            'incl_input_machine_data_streams', \
            'excl_input_machine_data_streams'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineFamilyHealthServiceConfigJSONAPISerializer(JSONAPIModelSerializer):
    machine_family = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_family_vital_data_stream_configs = \
        MachineFamilyVitalDataStreamConfigJSONAPISerializer(
            read_only=True,
            many=True)

    excl_input_machine_data_streams = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    included_serializers = related_serializers = \
        dict(machine_family=MachineFamilyJSONAPISerializer,
             excl_input_machine_data_streams=MachineDataStreamJSONAPISerializer)

    class Meta:
        model = MachineFamilyHealthServiceConfig

        fields = \
            MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineFamilyHealthServiceConfig.JSONAPIMeta.resource_name

        included_resources = \
            'machine_family', \
            'excl_input_machine_data_streams'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class AIJSONAPISerializer(JSONAPIModelSerializer):
    machine_family = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(machine_family=MachineFamilyJSONAPISerializer)

    class Meta:
        model = AI

        fields = \
            AI_API_FIELD_NAMES   # + \
            # ('url',)   # TODO: fix

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = AI.JSONAPIMeta.resource_name

        included_resources = 'machine_family',

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineFamilyVitalDataStreamAIEvalMetricProfileJSONAPISerializer(JSONAPIModelSerializer):
    machine_family = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_data_stream = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(machine_family=MachineFamilyJSONAPISerializer,
             machine_data_stream=MachineDataStreamJSONAPISerializer)

    class Meta:
        model = MachineFamilyVitalAIEvalMetricProfile

        fields = \
            MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineFamilyVitalAIEvalMetricProfile.JSONAPIMeta.resource_name

        included_resources = \
            'machine_family', \
            'machine_data_stream'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineDailyRiskScoreJSONAPISerializer(JSONAPIModelSerializer):
    machine_family = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(machine_family=MachineFamilyJSONAPISerializer,
             machine=MachineJSONAPISerializer)

    class Meta:
        model = MachineHealthRiskScore

        fields = \
            MACHINE_DAILY_RISK_SCORE_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineHealthRiskScore.JSONAPIMeta.resource_name

        included_resources = \
            'machine_family', \
            'machine'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineProblemLabelJSONAPIRelatedField(JSONAPIRelatedField):
    def to_internal_value(self, data):
        # TODO
        pass

    def to_representation(self, value):
        return str(value)


class MachineProblemDiagnosisJSONAPISerializer(JSONAPIModelSerializer):
    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    labels = \
        MachineProblemLabelJSONAPIRelatedField(
            read_only=True,
            many=True)

    included_serializers = related_serializers = \
        dict(machine=MachineJSONAPISerializer)

    class Meta:
        model = MachineHealthProblemDiagnosis

        fields = \
            'id', \
            'machine', \
            'from_date', \
            'to_date', \
            'duration', \
            'labels', \
            'has_associated_alerts', \
            'has_associated_machine_errors', \
            'url'

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineHealthProblemDiagnosis.JSONAPIMeta.resource_name

        included_resources = 'machine',

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class AlertJSONAPISerializer(JSONAPIModelSerializer):
    machine_family = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(machine_family=MachineFamilyJSONAPISerializer,
             machine=MachineJSONAPISerializer)

    class Meta:
        model = MachineHealthRiskAlert

        fields = \
            'id', \
            'machine_family', \
            'machine', \
            'risk_score_name', \
            'threshold', \
            'from_date', \
            'to_date', \
            'ongoing', \
            'duration', \
            'approx_average_risk_score', \
            'last_risk_score', \
            'cum_excess_risk_score', \
            'has_associated_machine_problem_diagnoses', \
            'has_associated_machine_errors', \
            'url'

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineHealthRiskAlert.JSONAPIMeta.resource_name

        included_resources = \
            'machine_family', \
            'machine'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineErrorCodeJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = MachineErrorCode

        fields = \
            MACHINE_ERROR_CODE_API_FIELD_NAMES   # + \
            # ('url',)   # TODO: fix

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineErrorCode.JSONAPIMeta.resource_name

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineErrorJSONAPISerializer(JSONAPIModelSerializer):
    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_error_code = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(machine=MachineJSONAPISerializer,
             machine_error_code=MachineErrorCodeJSONAPISerializer)

    class Meta:
        model = MachineError

        fields = \
            'id', \
            'machine_error_code', \
            'machine', \
            'from_utc_date_time', \
            'to_utc_date_time', \
            'duration_in_days', \
            'has_associated_machine_problem_diagnoses', \
            'has_associated_alerts', \
            'url'

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineError.JSONAPIMeta.resource_name

        included_resources = \
            'machine', \
            'machine_error_code'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineProblemDiagnosisNestedJSONAPISerializer(JSONAPIModelSerializer):
    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    labels = \
        MachineProblemLabelJSONAPIRelatedField(
            read_only=True,
            many=True)

    alerts = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    machine_errors = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    included_serializers = related_serializers = \
        dict(machine=MachineJSONAPISerializer,
             alerts=AlertJSONAPISerializer,
             machine_errors=MachineErrorJSONAPISerializer)

    class Meta:
        model = MachineHealthProblemDiagnosis

        fields = \
            MACHINE_PROBLEM_DIAGNOSIS_NESTED_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineHealthProblemDiagnosis.JSONAPIMeta.resource_name

        included_resources = \
            'machine', \
            'machine_health_risk_alerts', \
            'machine_errors'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class AlertNestedJSONAPISerializer(JSONAPIModelSerializer):
    machine_family = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_problem_diagnoses = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    machine_errors = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    included_serializers = related_serializers = \
        dict(machine_family=MachineFamilyJSONAPISerializer,
             machine=MachineJSONAPISerializer,
             machine_problem_diagnoses=MachineProblemDiagnosisJSONAPISerializer,
             machine_errors=MachineErrorJSONAPISerializer)

    class Meta:
        model = MachineHealthRiskAlert

        fields = \
            ALERT_NESTED_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineHealthRiskAlert.JSONAPIMeta.resource_name

        included_resources = \
            'machine_family', \
            'machine', \
            'machine_health_problem_diagnoses', \
            'machine_errors'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineErrorNestedJSONAPISerializer(JSONAPIModelSerializer):
    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_error_code = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_problem_diagnoses = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    alerts = \
        ResourceRelatedField(
            read_only=True,
            many=True)

    included_serializers = related_serializers = \
        dict(machine=MachineJSONAPISerializer,
             machine_error_code=MachineErrorCodeJSONAPISerializer,
             machine_problem_diagnoses=MachineProblemDiagnosisJSONAPISerializer,
             alerts=AlertJSONAPISerializer)

    class Meta:
        model = MachineError

        fields = \
            MACHINE_ERROR_NESTED_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineError.JSONAPIMeta.resource_name

        included_resources = \
            'machine', \
            'machine_error_code', \
            'machine_health_problem_diagnoses', \
            'machine_health_risk_alerts'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}
