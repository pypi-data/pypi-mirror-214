from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.sites import site

from silk.profiling.profiler import silk_profile

from .forms import \
    EnvironmentVariableForm

from .models import \
    EnvironmentVariable, \
    MachineFamilyDataStreamsCheckingJob, \
    MachineFamilyDataStreamsProfilingJob, MachineFamilyDataStreamCorrsProfilingJob, \
    MachineFamilyAITrainingJob, MachineFamilyAIEvaluationJob, \
    MachineFamilyDataAggJob, MachineFamilyDataAggsToDBJob, \
    MachineFamilyHealthRiskScoringJob, MachineFamilyHealthRiskScoresToDBJob


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

    search_fields = \
        'key', \
        'value'

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


@register(
    MachineFamilyDataStreamsCheckingJob,
    site=site)
class MachineFamilyDataStreamsCheckingJobAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'started', \
        'finished'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    show_full_result_count = False

    readonly_fields = \
        'machine_family', \
        'started', \
        'finished'

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamsCheckingJob._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='{}: {}'.format(
            __module__,
            MachineFamilyDataStreamsCheckingJob._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyDataStreamsProfilingJob,
    site=site)
class MachineFamilyDataStreamsProfilingJobAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'data_to_date', \
        'started', \
        'finished'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'data_to_date'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    show_full_result_count = False

    readonly_fields = \
        'machine_family', \
        'data_to_date', \
        'started', \
        'finished'

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    *MachineFamilyDataStreamsProfilingJob._meta.FIELD_NAMES.STR_SELECT_RELATED) \
                .defer(
                    *MachineFamilyDataStreamsProfilingJob._meta.FIELD_NAMES.DEFERRED_IN_STR_SELECT_RELATED)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamsProfilingJob._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamsProfilingJob._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyAITrainingJob,
    site=site)
class MachineFamilyAITrainingJobAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'ref_data_to_date', \
        'started', \
        'uuid', \
        'finished'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'ref_data_to_date'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    show_full_result_count = False

    readonly_fields = \
        'machine_family', \
        'ref_data_to_date', \
        'started', \
        'uuid', \
        'finished'

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    *MachineFamilyAITrainingJob._meta.FIELD_NAMES.STR_SELECT_RELATED) \
                .defer(
                    *MachineFamilyAITrainingJob._meta.FIELD_NAMES.DEFERRED_IN_STR_SELECT_RELATED)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyAITrainingJob._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyAITrainingJob._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyAIEvaluationJob,
    site=site)
class MachineFamilyAIEvaluationJobAdmin(ModelAdmin):
    list_display = \
        'ai', \
        'started', \
        'finished'

    list_filter = \
        'ai__machine_family__machine_class__unique_name', \
        'ai__machine_family__unique_name'

    search_fields = 'ai__unique_id',

    show_full_result_count = False

    readonly_fields = \
        'ai', \
        'started', \
        'finished'

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyAIEvaluationJob._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyAIEvaluationJob._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyHealthRiskScoringJob,
    site=site)
class MachineFamilyRiskScoringJobAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'date', \
        'started', \
        'finished'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'date'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    show_full_result_count = False

    readonly_fields = \
        'machine_family', \
        'date', \
        'started', \
        'finished'

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    *MachineFamilyHealthRiskScoringJob._meta.FIELD_NAMES.STR_SELECT_RELATED) \
                .defer(
                    *MachineFamilyHealthRiskScoringJob._meta.FIELD_NAMES.DEFERRED_IN_STR_SELECT_RELATED)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyHealthRiskScoringJob._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyHealthRiskScoringJob._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyHealthRiskScoresToDBJob,
    site=site)
class MachineFamilyRiskScoresToDBJobAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'date', \
        'started', \
        'finished'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'date'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    show_full_result_count = False

    readonly_fields = \
        'machine_family', \
        'date', \
        'started', \
        'finished'

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    *MachineFamilyHealthRiskScoresToDBJob._meta.FIELD_NAMES.STR_SELECT_RELATED) \
                .defer(
                    *MachineFamilyHealthRiskScoresToDBJob._meta.FIELD_NAMES.DEFERRED_IN_STR_SELECT_RELATED)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyHealthRiskScoresToDBJob._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyHealthRiskScoresToDBJob._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyDataAggJob,
    site=site)
class MachineFamilyDataAggJobAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'date', \
        'started', \
        'finished'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'date'

    search_fields = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name'

    show_full_result_count = False

    readonly_fields = \
        'machine_family', \
        'date', \
        'started', \
        'finished'

    def get_queryset(self, request):
        return super().get_queryset(request=request) \
                .select_related(
                    *MachineFamilyDataAggJob._meta.FIELD_NAMES.STR_SELECT_RELATED) \
                .defer(
                    *MachineFamilyDataAggJob._meta.FIELD_NAMES.DEFERRED_IN_STR_SELECT_RELATED)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataAggJob._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataAggJob._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)
