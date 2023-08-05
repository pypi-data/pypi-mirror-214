from django.forms import ModelChoiceField, ModelMultipleChoiceField

from django_json_widget.widgets import JSONEditorWidget

from dal.autocomplete import ModelSelect2, ModelSelect2Multiple
from dal.forms import FutureModelForm

from ..data.autocompletes import \
    MachineFamilyAutoComplete, \
    MachineAutoComplete

from ..data.forms import \
    MACHINE_CLASS_MODEL_CHOICE_FIELD, \
    MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD

from ..data.queries import \
    MACHINE_FAMILY_STR_UNORDERED_QUERY_SET, \
    MACHINE_STR_UNORDERED_QUERY_SET

from .autocompletes import \
    MachineHealthProblemAutoComplete

from .models import \
    EnvironmentVariable, \
    MachineFamilyHealthServiceConfig, MachineFamilyVitalDataStreamConfig, \
    AI, MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScoreMethod, MachineHealthRiskScore, \
    MachineHealthRiskAlert, \
    MachineHealthProblem, MachineHealthProblemDiagnosis, \
    MachineMaintenanceRepairAction, \
    MachineErrorCode, MachineError

from .queries import \
    MACHINE_HEALTH_PROBLEM_STR_SUBSET_ORDERED_QUERY_SET


class EnvironmentVariableForm(FutureModelForm):
    class Meta:
        model = EnvironmentVariable

        fields = \
            'key', \
            'value'

        widgets = \
            dict(value=JSONEditorWidget)


class MachineFamilyHealthServiceConfigForm(FutureModelForm):
    # DISABLING below because vital_machine_data_stream is rendered as read-only
    machine_family = \
        ModelChoiceField(
            queryset=MACHINE_FAMILY_STR_UNORDERED_QUERY_SET,
            widget=ModelSelect2(
                    url=MachineFamilyAutoComplete.name))

    excl_input_machine_data_streams = MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = MachineFamilyHealthServiceConfig

        fields = '__all__'


class MachineFamilyVitalDataStreamConfigForm(FutureModelForm):
    # DISABLING below because vital_machine_data_stream is rendered as read-only
    # vital_machine_data_stream = \
    #     ModelChoiceField(
    #         queryset=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_SET,
    #         widget=ModelSelect2(
    #                 url=MachineDataStreamAutoComplete.name,
    #                 attrs={'data-minimum-input-length': 1}))

    incl_input_machine_data_streams = MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD

    excl_input_machine_data_streams = MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = MachineFamilyVitalDataStreamConfig

        exclude = 'machine_family_health_service_config',


class AIForm(FutureModelForm):
    class Meta:
        model = AI

        fields = \
            'machine_family', \
            'ref_data_to_date', \
            'unique_id', \
            'active', \
            'ref_eval_metrics'

        widgets = \
            dict(ref_eval_metrics=JSONEditorWidget)


class MachineFamilyVitalDataStreamAIEvalMetricProfileForm(FutureModelForm):
    class Meta:
        model = MachineFamilyVitalAIEvalMetricProfile

        fields = \
            'machine_family', \
            'machine_data_stream', \
            'ref_data_to_date', \
            'N', \
            'R2', \
            'MAE', \
            'MedAE', \
            'RMSE'


class MachineHealthRiskScoreMethodForm(FutureModelForm):
    class Meta:
        model = MachineHealthRiskScoreMethod

        fields = \
            'machine_class', \
            'name', \
            'info'

        widgets = \
            dict(info=JSONEditorWidget)


class MachineHealthRiskScoreForm(FutureModelForm):
    class Meta:
        model = MachineHealthRiskScore

        fields = \
            'machine_family_data', \
            'machine', \
            'machine_health_risk_score_method', \
            'machine_health_risk_score_value'


class MachineHealthRiskAlertForm(FutureModelForm):
    class Meta:
        model = MachineHealthRiskAlert

        fields = \
            'machine_family', \
            'machine', \
            'machine_health_risk_score_method', \
            'machine_health_risk_score_value_alert_threshold', \
            'from_date', \
            'to_date', \
            'date_range', \
            'duration', \
            'ongoing', \
            'last_machine_health_risk_score_value', \
            'cum_excess_machine_health_risk_score_value', \
            'approx_average_machine_health_risk_score_value', \
            'info', \
            'has_machine_health_problem_diagnoses', \
            'machine_health_problem_diagnoses', \
            'has_machine_maintenance_repair_actions', \
            'machine_maintenance_repair_actions', \
            'has_machine_errors', \
            'machine_errors'

        widgets = \
            dict(info=JSONEditorWidget)


class MachineHealthProblemForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    class Meta:
        model = MachineHealthProblem

        fields = \
            'machine_class', \
            'name', \
            'descriptions'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class MachineProblemDiagnosisForm(FutureModelForm):
    machine = \
        ModelChoiceField(
            queryset=MACHINE_STR_UNORDERED_QUERY_SET,
            widget=ModelSelect2(
                    url=MachineAutoComplete.name,
                    attrs={'data-minimum-input-length': MachineAutoComplete.data_min_input_len}))

    machine_health_problems = \
        ModelMultipleChoiceField(
            queryset=MACHINE_HEALTH_PROBLEM_STR_SUBSET_ORDERED_QUERY_SET,
            widget=ModelSelect2Multiple(
                    url=MachineHealthProblemAutoComplete.name,
                    attrs={'data-minimum-input-length': MachineHealthProblemAutoComplete.data_min_input_len}))

    class Meta:
        model = MachineHealthProblemDiagnosis

        fields = \
            'machine', \
            'from_date', \
            'to_date', \
            'date_range', \
            'duration', \
            'ongoing', \
            'machine_health_problems', \
            'has_machine_health_risk_alerts', \
            'machine_health_risk_alerts', \
            'has_machine_maintenance_repair_actions', \
            'machine_maintenance_repair_actions', \
            'has_machine_errors', \
            'machine_errors'


class MachineMaintenanceRepairActionForm(FutureModelForm):
    machine = \
        ModelChoiceField(
            queryset=MACHINE_STR_UNORDERED_QUERY_SET,
            widget=ModelSelect2(
                    url=MachineAutoComplete.name,
                    attrs={'data-minimum-input-length': MachineAutoComplete.data_min_input_len}))

    class Meta:
        model = MachineMaintenanceRepairAction

        fields = \
            'machine', \
            'from_date', \
            'to_date', \
            'date_range', \
            'duration', \
            'ongoing', \
            'has_machine_health_risk_alerts', \
            'machine_health_risk_alerts', \
            'has_machine_health_problem_diagnoses', \
            'machine_health_problem_diagnoses', \
            'has_machine_errors', \
            'machine_errors'


class MachineErrorCodeForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    class Meta:
        model = MachineErrorCode

        fields = \
            'machine_class', \
            'name', \
            'descriptions', \
            'excl_n_days_of_machine_data_before'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class MachineErrorForm(FutureModelForm):
    class Meta:
        model = MachineError

        fields = \
            'machine', \
            'machine_error_code', \
            'from_utc_date_time', \
            'to_utc_date_time', \
            'duration', \
            'date_range', \
            'has_machine_health_risk_alerts', \
            'machine_health_risk_alerts', \
            'has_machine_health_problem_diagnoses', \
            'machine_health_problem_diagnoses', \
            'has_machine_maintenance_repair_actions', \
            'machine_maintenance_repair_actions'
