from django.contrib.admin import ModelAdmin, register, StackedInline
from django.contrib.admin.sites import site
from django.db.models import Prefetch

from django_admin_relation_links import AdminChangeLinksMixin

from django_model_query_graphs import ModelQueryGraph

import pandas

from silk.profiling.profiler import silk_profile

from ..data.queries import \
    MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_STR_QUERY_GRAPH, \
    MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_UNORDERED_QUERY_GRAPH

from .forms import \
    EnvironmentVariableForm, \
    MachineFamilyHealthServiceConfigForm, MachineFamilyVitalDataStreamConfigForm, \
    AIForm, MachineFamilyVitalDataStreamAIEvalMetricProfileForm, \
    MachineHealthRiskScoreMethodForm, MachineHealthRiskScoreForm, \
    MachineHealthRiskAlertForm, \
    MachineHealthProblemForm, MachineProblemDiagnosisForm, \
    MachineMaintenanceRepairActionForm, \
    MachineErrorCodeForm, MachineErrorForm

from .models import \
    EnvironmentVariable, \
    MachineFamilyVitalDataStreamConfig, \
    MachineFamilyHealthServiceConfig, \
    AI, AIModel, \
    MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScoreMethod, MachineHealthRiskScore, \
    MachineHealthRiskAlert, \
    MachineHealthProblem, MachineHealthProblemDiagnosis, \
    MachineMaintenanceRepairAction, \
    MachineErrorCode, MachineError

from .queries import \
    MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_GRAPH, \
    MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_HEALTH_RISK_ALERT_STR_SUBSET_ORDERED_QUERY_GRAPH, \
    MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_SUBSET_ORDERED_QUERY_GRAPH, \
    MACHINE_MAINTENANCE_REPAIR_ACTION_STR_SUBSET_ORDERED_QUERY_GRAPH, \
    MACHINE_ERROR_CODE_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_ERROR_STR_SUBSET_ORDERED_QUERY_GRAPH


@register(
    EnvironmentVariable,
    site=site)
class EnvironmentVariableAdmin(ModelAdmin):
    list_display = \
        'key', \
        'value', \
        'updated'

    list_display_links = \
        'key', \
        'value'

    search_fields = EnvironmentVariable.search_fields()

    show_full_result_count = False

    form = EnvironmentVariableForm

    readonly_fields = \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return query_set \
            if request.resolver_match.url_name.endswith('_change') \
          else query_set.only(*self.list_display)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                EnvironmentVariable._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


class MachineFamilyVitalDataStreamConfigStackedInline(StackedInline):
    model = MachineFamilyVitalDataStreamConfig

    fields = \
        'vital_machine_data_stream', \
        'vital_machine_data_stream_profile', \
        'high_corr_num_machine_data_streams', \
        'auto_incl_input_machine_data_streams', \
        'incl_input_machine_data_streams', \
        'low_corr_num_machine_data_streams', \
        'excl_input_machine_data_streams', \
        'active', \
        'comments'

    extra = 0

    # using Django-AutoComplete-Light
    form = MachineFamilyVitalDataStreamConfigForm

    # if using default Admin AutoComplete
    # autocomplete_fields = \
    #     'vital_machine_data_stream',
    #     'incl_input_machine_data_streams',
    #     'excl_input_machine_data_streams'

    # if using Grappelli AutoComplete
    # raw_id_fields = \
    #     'vital_machine_data_stream', \
    #     'incl_input_machine_data_streams', \
    #     'excl_input_machine_data_streams',
    # autocomplete_lookup_fields = \
    #     dict(fk=('vital_machine_data_stream',),
    #          m2m=('incl_input_machine_data_streams',
    #               'excl_input_machine_data_streams',))

    readonly_fields = \
        'vital_machine_data_stream', \
        'vital_machine_data_stream_profile', \
        'high_corr_num_machine_data_streams', \
        'auto_incl_input_machine_data_streams', \
        'low_corr_num_machine_data_streams', \
        'created', \
        'updated'
    
    def get_queryset(self, request):
        return ModelQueryGraph(
                MachineFamilyVitalDataStreamConfig,
                'high_corr_num_machine_data_streams',
                'auto_incl_input_machine_data_streams',
                'low_corr_num_machine_data_streams',
                'active',
                'comments',
                vital_machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                vital_machine_data_stream_profile=MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_UNORDERED_QUERY_GRAPH,
                incl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
                excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
                ORDER=True) \
            .query_set(
                init=super().get_queryset(request=request))


@register(
    MachineFamilyHealthServiceConfig,
    site=site)
class MachineFamilyHealthServiceConfigAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'vital_and_incl_excl_machine_data_stream_names', \
        'incl_cat_input_machine_data_streams', \
        'from_date', \
        'to_date', \
        'configs', \
        'active', \
        'comments', \
        'updated'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'active'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    show_full_result_count = False

    # using Django-AutoComplete-Light
    form = MachineFamilyHealthServiceConfigForm

    # if using default Admin AutoComplete
    # autocomplete_fields = 'excl_input_machine_data_streams',

    # if using Grappelli AutoComplete
    # raw_id_fields = 'excl_input_machine_data_streams',
    # autocomplete_lookup_fields = \
    #     dict(m2m=('excl_input_machine_data_streams',))

    readonly_fields = \
        'machine_family', \
        'created', \
        'updated'

    inlines = MachineFamilyVitalDataStreamConfigStackedInline,
    
    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamilyHealthServiceConfig,
                    'incl_cat_input_machine_data_streams',
                    'from_date',
                    'to_date',
                    'configs',
                    'active',
                    'comments',
                    'created',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    machine_family_vital_data_stream_configs=
                        MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamilyHealthServiceConfig,
                    'incl_cat_input_machine_data_streams',
                    'from_date',
                    'to_date',
                    'configs',
                    'active',
                    'comments',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    machine_family_vital_data_stream_configs=
                        MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    excl_input_machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyHealthServiceConfig._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyHealthServiceConfig._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


class AIModelStackedInline(StackedInline):
    model = AIModel

    fields = \
        'target_machine_data_stream', \
        'input_machine_data_streams'

    extra = 0

    readonly_fields = \
        'target_machine_data_stream', \
        'input_machine_data_streams'

    def get_queryset(self, request):
        return ModelQueryGraph(
                AIModel,
                target_machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                input_machine_data_streams=MACHINE_DATA_STREAM_STR_QUERY_GRAPH,
                ORDER=True) \
            .query_set(
                init=super().get_queryset(request=request))


@register(
    AI,
    site=site)
class AIAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'ref_data_to_date', \
        'created', \
        'unique_id', \
        'active', \
        'reference_evaluation_metrics', \
        'updated'

    list_display_links = 'unique_id',

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'ref_data_to_date', \
        'created', \
        'active'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'unique_id'

    show_full_result_count = False

    form = AIForm

    readonly_fields = \
        'machine_family', \
        'ref_data_to_date', \
        'unique_id', \
        'created', \
        'updated'
        # 'ref_eval_metrics'   # TOO HUGE TO RENDER AS READ-ONLY -- WILL CRASH SERVER

    inlines = AIModelStackedInline,

    def reference_evaluation_metrics(self, obj):
        if obj.ref_eval_metrics:
            d = {}

            for label_var_name, ref_eval_metrics in obj.ref_eval_metrics.items():
                global_ref_eval_metrics = ref_eval_metrics['GLOBAL']

                good = True

                r2 = global_ref_eval_metrics['R2']
                if pandas.notnull(r2):
                    r2_text = '{:.1f}%'.format(100 * r2)
                    if r2 < .68:
                        good = False
                        r2_text += ' (< 68%)'
                else:
                    r2_text = 'na'
                    good = False

                mae = global_ref_eval_metrics['MAE']
                medae = global_ref_eval_metrics['MedAE']
                mae_medae_ratio = mae / medae
                mae_medae_ratio_text = '{:.3g}x'.format(mae_medae_ratio)
                if mae_medae_ratio > 3:
                    good = False
                    mae_medae_ratio_text += ' (> 3x)'

                d[label_var_name.upper()
                  if good
                  else label_var_name] = \
                    dict(good=good,
                         R2_text=r2_text,
                         MAE=mae,
                         MedAE=medae,
                         MAE_MedAE_ratio_text=mae_medae_ratio_text)

            return '; '.join(
                    '{}: R2 {}, MAE {:.3g} / MedAE {:.3g} = {}'.format(
                        k,
                        v['R2_text'],
                        v['MAE'],
                        v['MedAE'],
                        v['MAE_MedAE_ratio_text'])
                    for k, v in sorted(d.items(), key=lambda i: i[1]['good'], reverse=True))

    def get_queryset(self, request):
        return ModelQueryGraph(
                AI,
                'ref_data_to_date',
                'created',
                'unique_id',
                'active',
                'ref_eval_metrics',
                'updated',
                machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                ORDER=not request.resolver_match.url_name.endswith('_change')) \
            .query_set(
                init=super().get_queryset(request=request))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                AI._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                AI._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyVitalAIEvalMetricProfile,
    site=site)
class MachineFamilyVitalDataStreamAIEvalMetricProfileAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'machine_data_stream', \
        'ref_data_to_date', \
        'N', \
        'R2', \
        'MAE', \
        'MedAE', \
        'MAE_over_MedAE_ratio', \
        'RMSE', \
        'updated'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'machine_data_stream__name', \
        'ref_data_to_date'

    search_fields = MachineFamilyVitalAIEvalMetricProfile.search_fields()

    show_full_result_count = False

    form = MachineFamilyVitalDataStreamAIEvalMetricProfileForm

    readonly_fields = \
        'machine_family', \
        'machine_data_stream', \
        'ref_data_to_date', \
        'N', \
        'R2', \
        'MAE', \
        'MedAE', \
        'RMSE', \
        'created', \
        'updated'

    def MAE_over_MedAE_ratio(self, obj):
        return obj.MAE / obj.MedAE

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamilyVitalAIEvalMetricProfile,
                    'ref_data_to_date',
                    'N',
                    'R2',
                    'MAE',
                    'MedAE',
                    'RMSE',
                    'created',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamilyVitalAIEvalMetricProfile,
                    'ref_data_to_date',
                    'N',
                    'R2',
                    'MAE',
                    'MedAE',
                    'RMSE',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))
    
    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyVitalAIEvalMetricProfile._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyVitalAIEvalMetricProfile._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineHealthRiskScoreMethod,
    site=site)
class MachineHealthRiskScoreMethodAdmin(ModelAdmin):
    list_display = \
        'machine_class', \
        'name', \
        'info', \
        'updated'

    list_display_links = \
        'machine_class', \
        'name'

    list_filter = 'machine_class__unique_name',

    search_fields = MachineHealthRiskScoreMethod.search_fields()

    show_full_result_count = False

    form = MachineHealthRiskScoreMethodForm

    readonly_fields = \
        'machine_class', \
        'name', \
        'info', \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineHealthRiskScoreMethod,
                    'name',
                    'info',
                    'created',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineHealthRiskScoreMethod,
                    'name',
                    'info',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthRiskScoreMethod._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthRiskScoreMethod._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineHealthRiskScore,
    site=site)
class MachineDailyRiskScoreAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'machine', \
        'date', \
        'machine_health_risk_score_method', \
        'machine_health_risk_score_value', \
        'updated'

    list_filter = \
        'machine_family_data__machine_family__machine_class__unique_name', \
        'machine_family_data__machine_family__unique_name', \
        'machine_family_data__date', \
        'machine_health_risk_score_method__name'

    search_fields = MachineHealthRiskScore.search_fields()

    show_full_result_count = False

    form = MachineHealthRiskScoreForm

    readonly_fields = \
        'machine_family_data', \
        'machine', \
        'machine_health_risk_score_method', \
        'machine_health_risk_score_value', \
        'created', \
        'updated'

    def machine_family(self, obj):
        return obj.machine_family_data.machine_family

    def date(self, obj):
        return obj.machine_family_data.date

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineHealthRiskScore,
                    'machine_health_risk_score_value',
                    'created',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH,
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineHealthRiskScore,
                    'machine_health_risk_score_value',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH,
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthRiskScore._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthRiskScore._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineHealthRiskAlert,
    site=site)
class MachineHealthRiskAlertAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'machine', \
        'machine_health_risk_score_method', \
        'machine_health_risk_score_value_alert_threshold', \
        'from_date', \
        'to_date', \
        'duration', \
        'ongoing', \
        'approx_average_machine_health_risk_score_value', \
        'last_machine_health_risk_score_value', \
        'cum_excess_machine_health_risk_score_value', \
        'has_machine_health_problem_diagnoses', \
        'has_machine_maintenance_repair_actions', \
        'has_machine_errors', \
        'updated'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'machine_health_risk_score_method__name', \
        'machine_health_risk_score_value_alert_threshold', \
        'from_date', \
        'to_date', \
        'ongoing', \
        'has_machine_health_problem_diagnoses', \
        'has_machine_maintenance_repair_actions', \
        'has_machine_errors'

    search_fields = MachineHealthRiskAlert.search_fields()

    show_full_result_count = False

    form = MachineHealthRiskAlertForm

    readonly_fields = \
        'machine_family', \
        'machine', \
        'machine_health_risk_score_method', \
        'machine_health_risk_score_value_alert_threshold', \
        'from_date', \
        'to_date', \
        'date_range', \
        'duration', \
        'ongoing', \
        'approx_average_machine_health_risk_score_value', \
        'last_machine_health_risk_score_value', \
        'cum_excess_machine_health_risk_score_value', \
        'info', \
        'has_machine_health_problem_diagnoses', \
        'machine_health_problem_diagnoses', \
        'has_machine_maintenance_repair_actions', \
        'machine_maintenance_repair_actions', \
        'has_machine_errors', \
        'machine_errors', \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request)

        return (ModelQueryGraph(
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
                    'created',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_problem_diagnoses=MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_maintenance_repair_actions=MACHINE_MAINTENANCE_REPAIR_ACTION_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_errors=MACHINE_ERROR_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineHealthRiskAlert,
                    'machine_health_risk_score_value_alert_threshold',
                    'from_date',
                    'to_date',
                    'duration',
                    'ongoing',
                    'last_machine_health_risk_score_value',
                    'cum_excess_machine_health_risk_score_value',
                    'approx_average_machine_health_risk_score_value',
                    'has_machine_health_problem_diagnoses',
                    'has_machine_maintenance_repair_actions',
                    'has_machine_errors',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_risk_score_method=MACHINE_HEALTH_RISK_SCORE_METHOD_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthRiskAlert._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthRiskAlert._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineHealthProblem,
    site=site)
class MachineHealthProblemAdmin(ModelAdmin):
    list_display = \
        'machine_class', \
        'name', \
        'descriptions', \
        'updated'

    list_display_links = \
        'machine_class', \
        'name'

    list_filter = 'machine_class__unique_name',

    search_fields = MachineHealthProblem.search_fields()

    show_full_result_count = False

    form = MachineHealthProblemForm

    readonly_fields = \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request)

        return (ModelQueryGraph(
                    MachineHealthProblem,
                    'name',
                    'descriptions',
                    'created',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineHealthProblem,
                    'name',
                    'descriptions',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthProblem._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthProblem._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineHealthProblemDiagnosis,
    site=site)
class MachineProblemDiagnosisAdmin(ModelAdmin):
    list_display = \
        'machine', \
        'from_date', \
        'to_date', \
        'duration', \
        'problems', \
        'has_machine_health_risk_alerts', \
        'has_machine_maintenance_repair_actions', \
        'has_machine_errors', \
        'updated'

    list_filter = \
        'machine__machine_class__unique_name', \
        'ongoing', \
        'has_machine_health_risk_alerts', \
        'has_machine_maintenance_repair_actions', \
        'has_machine_errors'

    search_fields = MachineHealthProblemDiagnosis.search_fields()

    show_full_result_count = False

    # using Django-AutoComplete-Light
    form = MachineProblemDiagnosisForm

    # if using Grappelli AutoComplete
    # raw_id_fields = 'machine',
    #  autocomplete_lookup_fields = \
    #     dict(fk=('machine',),)

    readonly_fields = \
        'date_range', \
        'duration', \
        'ongoing', \
        'has_machine_health_risk_alerts', \
        'machine_health_risk_alerts', \
        'has_machine_maintenance_repair_actions', \
        'machine_maintenance_repair_actions', \
        'has_machine_errors', \
        'machine_errors', \
        'created', \
        'updated'

    def problems(self, obj):
        return ', '.join(i.name
                         for i in obj.machine_health_problems.all())

    def get_queryset(self, request):
        query_set = super().get_queryset(request)

        return (ModelQueryGraph(
                    MachineHealthProblemDiagnosis,
                    'from_date',
                    'to_date',
                    'date_range',
                    'duration',
                    'ongoing',
                    'has_machine_health_risk_alerts',
                    'has_machine_maintenance_repair_actions',
                    'has_machine_errors',
                    'created',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_problems=MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH,
                    machine_health_risk_alerts=MACHINE_HEALTH_RISK_ALERT_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_maintenance_repair_actions=MACHINE_MAINTENANCE_REPAIR_ACTION_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_errors=MACHINE_ERROR_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineHealthProblemDiagnosis,
                    'from_date',
                    'to_date',
                    'duration',
                    'has_machine_health_risk_alerts',
                    'has_machine_maintenance_repair_actions',
                    'has_machine_errors',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_problems=MACHINE_HEALTH_PROBLEM_NAME_ONLY_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthProblemDiagnosis._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineHealthProblemDiagnosis._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineMaintenanceRepairAction,
    site=site)
class MachineMaintenanceRepairActionAdmin(ModelAdmin):
    list_display = \
        'machine', \
        'from_date', \
        'to_date', \
        'duration', \
        'has_machine_health_risk_alerts', \
        'has_machine_health_problem_diagnoses', \
        'has_machine_errors', \
        'updated'

    list_filter = \
        'machine__machine_class__unique_name', \
        'ongoing', \
        'has_machine_health_risk_alerts', \
        'has_machine_health_problem_diagnoses', \
        'has_machine_errors'

    search_fields = MachineMaintenanceRepairAction.search_fields()

    show_full_result_count = False

    form = MachineMaintenanceRepairActionForm

    readonly_fields = \
        'date_range', \
        'duration', \
        'ongoing', \
        'has_machine_health_risk_alerts', \
        'machine_health_risk_alerts', \
        'has_machine_health_problem_diagnoses', \
        'machine_health_problem_diagnoses', \
        'has_machine_errors', \
        'machine_errors', \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request)

        return (ModelQueryGraph(
                    MachineMaintenanceRepairAction,
                    'from_date',
                    'to_date',
                    'date_range',
                    'duration',
                    'ongoing',
                    'has_machine_health_risk_alerts',
                    'has_machine_health_problem_diagnoses',
                    'has_machine_errors',
                    'created',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_risk_alerts=MACHINE_HEALTH_RISK_ALERT_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_health_problem_diagnoses=MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_errors=MACHINE_ERROR_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineMaintenanceRepairAction,
                    'from_date',
                    'to_date',
                    'duration',
                    'has_machine_health_risk_alerts',
                    'has_machine_health_problem_diagnoses',
                    'has_machine_errors',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineMaintenanceRepairAction._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineMaintenanceRepairAction._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineErrorCode,
    site=site)
class MachineErrorCodeAdmin(ModelAdmin):
    list_display = \
        'machine_class', \
        'name', \
        'descriptions', \
        'excl_n_days_of_machine_data_before', \
        'updated'

    list_display_links = \
        'machine_class', \
        'name'

    list_filter = 'machine_class__unique_name',

    search_fields = MachineErrorCode.search_fields()

    show_full_result_count = False

    form = MachineErrorCodeForm

    readonly_fields = \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request)

        return (ModelQueryGraph(
                    MachineErrorCode,
                    'name',
                    'descriptions',
                    'excl_n_days_of_machine_data_before',
                    'created',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineErrorCode,
                    'name',
                    'descriptions',
                    'excl_n_days_of_machine_data_before',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineErrorCode._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineErrorCode._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineError,
    site=site)
class MachineErrorAdmin(ModelAdmin):
    list_display = \
        'machine', \
        'machine_error_code', \
        'from_utc_date_time', \
        'to_utc_date_time', \
        'duration', \
        'has_machine_health_risk_alerts', \
        'has_machine_health_problem_diagnoses', \
        'has_machine_maintenance_repair_actions', \
        'updated'

    list_filter = \
        'machine__machine_class__unique_name', \
        'machine_error_code__name', \
        'from_utc_date_time', \
        'to_utc_date_time', \
        'has_machine_health_risk_alerts', \
        'has_machine_health_problem_diagnoses', \
        'has_machine_maintenance_repair_actions'

    search_fields = MachineError.search_fields()

    show_full_result_count = False

    form = MachineErrorForm

    readonly_fields = \
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
        'machine_maintenance_repair_actions', \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request)

        return (ModelQueryGraph(
                    MachineError,
                    'from_utc_date_time',
                    'to_utc_date_time',
                    'duration',
                    'date_range',
                    'has_machine_health_risk_alerts',
                    'has_machine_health_problem_diagnoses',
                    'has_machine_maintenance_repair_actions',
                    'created',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_error_code=MACHINE_ERROR_CODE_STR_UNORDERED_QUERY_GRAPH,
                    machine_health_risk_alerts=MACHINE_HEALTH_RISK_ALERT_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_health_problem_diagnoses=MACHINE_HEALTH_PROBLEM_DIAGNOSIS_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_maintenance_repair_actions=MACHINE_MAINTENANCE_REPAIR_ACTION_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineError,
                    'from_utc_date_time',
                    'to_utc_date_time',
                    'duration',
                    'has_machine_health_risk_alerts',
                    'has_machine_health_problem_diagnoses',
                    'has_machine_maintenance_repair_actions',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_error_code=MACHINE_ERROR_CODE_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineError._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineError._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)
