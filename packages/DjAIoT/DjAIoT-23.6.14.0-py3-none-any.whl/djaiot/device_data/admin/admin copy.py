from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.options import StackedInline, TabularInline
from django.contrib.admin.sites import site
from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from django.forms.models import BaseInlineFormSet

from django_admin_relation_links import AdminChangeLinksMixin

from django_model_query_graphs import ModelQueryGraph

from silk.profiling.profiler import silk_profile

from .forms import \
    EnvironmentVariableForm, \
    PhysicalDataTypeForm, \
    MeasurementUnitForm, \
    MachineClassForm, \
    MachineComponentForm, \
    MachineDataStreamForm, \
    MachineFamilyForm, MachineFamilyComponentInLineForm, \
    MachineSKUForm, \
    LocationForm, LocationMachineInLineForm, \
    MachineForm, \
    MachineFamilyDataForm, \
    MachineFamilyDataStreamsCheckForm, \
    MachineFamilyDataStreamProfileForm, \
    MachineFamilyDataStreamPairCorrForm, \
    MachineFamilyDataStreamAggForm, \
    MachineDataForm, \
    MachineDataStreamAggForm

from .models import \
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
    MachineFamilyComponent, \
    MachineFamilyData, \
    MachineFamilyDataStreamsCheck, \
    MachineData, \
    MachineDataStreamAgg, \
    MachineFamilyDataStreamProfile, \
    MachineFamilyDataStreamPairCorr, \
    MachineFamilyDataStreamAgg

from .queries import \
    PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH, PHYSICAL_DATA_TYPE_NAME_ONLY_QUERY_GRAPH, \
    PHYSICAL_DATA_TYPE_PK_ONLY_UNORDERED_QUERY_GRAPH, \
    MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH, \
    MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_COMPONENT_PK_ONLY_UNORDERED_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_DATA_STREAM_PK_ONLY_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_PK_ONLY_UNORDERED_QUERY_GRAPH, \
    MACHINE_SKU_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH, \
    LOCATION_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_PK_ONLY_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH, MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH, \
    MACHINE_FAMILY_DATA_STREAM_AGG_ABBR_QUERY_GRAPH


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


@register(
    PhysicalDataType,
    site=site)
class PhysicalDataTypeAdmin(ModelAdmin):
    list_display = \
        'unique_name', \
        'range', \
        'same_as'

    list_display_links = 'unique_name',

    search_fields = PhysicalDataType.search_fields()

    show_full_result_count = False

    form = PhysicalDataTypeForm

    readonly_fields = 'range',

    # ref: https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
    def same_as(self, obj):
        return ', '.join(physical_data_type.unique_name
                         for physical_data_type in obj.same.all()
                         # TODO: FIX BUG
                         # why does .values_list cause inefficient "N + 1" queries, failing to use cached prefetches?!
                         # obj.same.values_list('unique_name', flat=True, named=False)
                        ) \
            if obj.same.count() \
          else ''

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    PhysicalDataType,
                    'unique_name',
                    'min',
                    'max',
                    'range',
                    same=PHYSICAL_DATA_TYPE_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    PhysicalDataType,
                    'unique_name',
                    'range',
                    same=PHYSICAL_DATA_TYPE_NAME_ONLY_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                PhysicalDataType._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                PhysicalDataType._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MeasurementUnit,
    site=site)
class MeasurementUnitAdmin(ModelAdmin):
    list_display = \
        'unique_name', \
        'descriptions', \
        'updated'

    list_display_links = \
        'unique_name', \
        'descriptions'

    search_fields = MeasurementUnit.search_fields()

    show_full_result_count = False

    form = MeasurementUnitForm

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
                MeasurementUnit._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)
    
    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MeasurementUnit._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineClass,
    site=site)
class MachineClassAdmin(ModelAdmin):
    list_display = \
        'unique_name', \
        'descriptions', \
        'updated'

    list_display_links = \
        'unique_name', \
        'descriptions'

    search_fields = MachineClass.search_fields()

    show_full_result_count = False

    form = MachineClassForm

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
                MachineClass._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)
    
    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineClass._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineComponent,
    site=site)
class MachineComponentAdmin(AdminChangeLinksMixin, ModelAdmin):
    list_display = \
        'machine_class', \
        'name', \
        'descriptions', \
        'machine_family_list', \
        'directly_interacting_component_list', \
        'sub_component_list', \
        'machine_data_stream_list', \
        'n_machine_skus', \
        'updated'

    list_display_links = 'name',
    
    # changelist_links = 'machine_class',   # TODO

    list_filter = 'machine_class__unique_name',

    search_fields = MachineComponent.search_fields()

    show_full_result_count = False

    # using Django-AutoComplete-Light
    form = MachineComponentForm

    # if using default Admin AutoComplete
    # autocomplete_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineDataStream._meta.FIELD_NAMES.M2M, \
    #     MachineSKU._meta.FIELD_NAMES.M2M

    # if using Grappelli AutoComplete
    # raw_id_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineDataStream._meta.FIELD_NAMES.M2M, \
    #     MachineSKU._meta.FIELD_NAMES.M2M
    # autocomplete_lookup_fields = \
    #     dict(fk=(MachineClass._meta.FIELD_NAMES.SELF,),
    #          m2m=(MachineDataStream._meta.FIELD_NAMES.M2M,
    #               MachineSKU._meta.FIELD_NAMES.M2M,))

    # change_links = 'machine_class',   TODO

    readonly_fields = \
        'machine_families', \
        'directly_interacting_components', \
        'sub_components', \
        'machine_data_streams', \
        'created', \
        'updated'

    def machine_family_list(self, obj):
        n = obj.machine_families.count()

        return '{}: {}'.format(
                n, ', '.join(machine_family.unique_name
                             for machine_family in obj.machine_families.all())) \
            if n \
          else ''

    def directly_interacting_component_list(self, obj):
        n = obj.directly_interacting_components.count()

        return '{}: {}'.format(
                n, ', '.join(machine_component.name
                             for machine_component in obj.directly_interacting_components.all())) \
            if n \
          else ''

    def sub_component_list(self, obj):
        n = obj.sub_components.count()

        return '{}: {}'.format(
                n, ', '.join(machine_component.name
                             for machine_component in obj.sub_components.all())) \
            if n \
          else ''

    def machine_data_stream_list(self, obj):
        n = obj.machine_data_streams.count()

        return '{}: {}'.format(
                n, ', '.join(str(machine_data_stream)
                             for machine_data_stream in obj.machine_data_streams.all())) \
            if n \
          else ''

    def n_machine_skus(self, obj):
        n = obj.machine_skus.count()

        return n \
            if n \
          else ''

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineComponent,
                    'name',
                    'descriptions',
                    'created',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_families=MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    directly_interacting_components=MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    sub_components=MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_data_streams=MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_skus=MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineComponent,
                    'name',
                    'descriptions',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_families=MACHINE_FAMILY_NAME_ONLY_QUERY_GRAPH,
                    directly_interacting_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                    sub_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                    machine_data_streams=MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    machine_skus=MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineComponent._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineComponent._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineDataStream,
    site=site)
class MachineDataStreamAdmin(ModelAdmin):
    list_display = \
        'machine_class', \
        'machine_component_list', \
        'name', \
        'descriptions', \
        'machine_data_stream_type', \
        'logical_data_type', \
        'physical_data_type', \
        'measurement_unit', \
        'neg_invalid', \
        'pos_invalid', \
        'default', \
        'range', \
        'n_machine_skus', \
        'updated'

    list_display_links = 'name',

    list_filter = \
        'machine_class__unique_name', \
        'machine_data_stream_type', \
        'logical_data_type', \
        'physical_data_type__unique_name', \
        'measurement_unit__unique_name', \
        'neg_invalid', \
        'pos_invalid', \
        'default', \
        'name'

    search_fields = MachineDataStream.search_fields()

    show_full_result_count = False

    # using Django-AutoComplete-Light
    form = MachineDataStreamForm

    # if using default Admin AutoComplete
    # autocomplete_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MeasurementUnit._meta.FIELD_NAMES.SELF, \
    #     MachineComponent._meta.FIELD_NAMES.M2M, \
    #     MachineSKU._meta.FIELD_NAMES.M2M

    # if using Grappelli AutoComplete
    # raw_id_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineComponent._meta.FIELD_NAMES.M2M, \
    #     MeasurementUnit._meta.FIELD_NAMES.SELF, \
    #     MachineSKU._meta.FIELD_NAMES.M2M
    # autocomplete_lookup_fields = \
    #     dict(fk=(MachineClass._meta.FIELD_NAMES.SELF,
    #              MeasurementUnit._meta.FIELD_NAMES.SELF),
    #          m2m=(MachineComponent._meta.FIELD_NAMES.M2M,
    #               MachineSKU._meta.FIELD_NAMES.M2M))

    readonly_fields = \
        'machine_class', \
        'machine_components', \
        'name', \
        'created', \
        'updated'

    def machine_component_list(self, obj):
        n = obj.machine_components.count()

        return '{}: {}'.format(
                n, ', '.join(machine_component.name
                             for machine_component in obj.machine_components.all())) \
            if n \
          else ''

    def n_machine_skus(self, obj):
        n = obj.machine_skus.count()

        return n \
            if n \
          else ''

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineDataStream,
                    'name',
                    'descriptions',
                    'machine_data_stream_type',
                    'logical_data_type',
                    'neg_invalid',
                    'pos_invalid',
                    'default',
                    'range',
                    'created',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_components=MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    physical_data_type=PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH,
                    measurement_unit=MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH,
                    machine_skus=MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineDataStream,
                    'name',
                    'descriptions',
                    'machine_data_stream_type',
                    'logical_data_type',
                    'neg_invalid',
                    'pos_invalid',
                    'default',
                    'range',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                    physical_data_type=PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH,
                    measurement_unit=MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH,
                    machine_skus=MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineDataStream._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineDataStream._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


class MachineFamilyComponentInLine(StackedInline):
    model = MachineFamilyComponent

    fields = \
        'machine_component', \
        'directly_interacting_components', \
        'sub_components', \
        'machine_data_streams'

    form = MachineFamilyComponentInLineForm

    readonly_fields = \
        'created', \
        'updated'

    extra = 0

    def get_queryset(self, request):
        return ModelQueryGraph(
                MachineFamilyComponent,
                machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                machine_component=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                directly_interacting_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                sub_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
                ORDER='machine_component__name') \
            .query_set(
                init=super().get_queryset(request=request))


@register(
    MachineFamily,
    site=site)
class MachineFamilyAdmin(ModelAdmin):
    list_display = \
        'machine_class', \
        'unique_name', \
        'descriptions', \
        'filtered_from', \
        'machine_data_filter_condition', \
        'machine_component_list', \
        'machine_sku_list', \
        'n_machine_data_streams', \
        'n_machines', \
        'n_machines_approx', \
        'updated'

    list_display_links = 'unique_name',

    list_filter = 'machine_class__unique_name',

    search_fields = MachineFamily.search_fields()

    show_full_result_count = False

    # using Django-AutoComplete-Light
    form = MachineFamilyForm

    # if using default Admin AutoComplete
    # autocomplete_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineSKU._meta.FIELD_NAMES.M2M, \
    #     MachineComponent._meta.FIELD_NAMES.M2M, \
    #     MachineDataStream._meta.FIELD_NAMES.M2M

    # if using Grappelli Auto-Complete
    # raw_id_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineSKU._meta.FIELD_NAMES.M2M, \
    #     MachineComponent._meta.FIELD_NAMES.M2M, \
    #     MachineDataStream._meta.FIELD_NAMES.M2M
    # autocomplete_lookup_fields = \
    #     dict(fk=(MachineClass._meta.FIELD_NAMES.SELF,),
    #          m2m=(MachineSKU._meta.FIELD_NAMES.M2M,
    #               MachineComponent._meta.FIELD_NAMES.M2M,
    #               MachineDataStream._meta.FIELD_NAMES.M2M))

    inlines = MachineFamilyComponentInLine,

    readonly_fields = \
        'machine_data_streams', \
        'created', \
        'updated'

    def filtered_from(self, obj):
        return obj.filtered_from_machine_family.unique_name \
            if obj.filtered_from_machine_family \
          else ''

    def machine_component_list(self, obj):
        n = obj.machine_components.count()

        return '{}: {}'.format(
                n, ', '.join(machine_component.name
                             for machine_component in obj.machine_components.all())) \
            if n \
          else ''

    def machine_sku_list(self, obj):
        n = obj.machine_skus.count()

        return '{}: {}'.format(
                n, ', '.join(machine_sku.unique_name
                             for machine_sku in obj.machine_skus.all())) \
            if n \
          else ''

    def n_machine_data_streams(self, obj):
        n = obj.machine_data_streams.count()

        return n \
            if n \
          else ''

    def n_machines(self, obj):
        n = obj.machines.count()

        return n \
            if n \
          else ''

    def n_machines_approx(self, obj):
        n = sum(machine_sku.machines.count()
                for machine_sku in obj.machine_skus.all()) \
            if obj.machine_skus.count() \
            else 0

        return n \
            if n \
          else ''

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamily,
                    'unique_name',
                    'descriptions',
                    'machine_data_filter_condition',
                    'created',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    filtered_from_machine_family=MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH,
                    machine_skus=MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    machine_data_streams=MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamily,
                    'unique_name',
                    'descriptions',
                    'machine_data_filter_condition',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    filtered_from_machine_family=MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH,
                    machine_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                    machine_skus=
                        ModelQueryGraph(
                            MachineSKU,
                            'unique_name',
                            machines=
                                ModelQueryGraph(
                                    Machine,
                                    'machine_sku',   # TODO: verify whether necessary
                                    ORDER=False),
                            ORDER='unique_name'),
                    machine_data_streams=MACHINE_DATA_STREAM_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    machines=MACHINE_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamily._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamily._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineSKU,
    site=site)
class MachineSKUAdmin(ModelAdmin):
    list_display = \
        'machine_class', \
        'unique_name', \
        'descriptions', \
        'machine_component_list', \
        'n_machine_data_streams', \
        'machine_family_list', \
        'n_machines', \
        'updated'
    
    list_display_links = 'unique_name',

    list_filter = 'machine_class__unique_name',

    search_fields = MachineSKU.search_fields()

    show_full_result_count = False

    # using Django-AutoComplete-Light
    form = MachineSKUForm

    # if using default Admin AutoComplete
    # autocomplete_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineComponent._meta.FIELD_NAMES.M2M, \
    #     MachineDataStream._meta.FIELD_NAMES.M2M

    # if using Grappelli AutoComplete
    # raw_id_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineDataStream._meta.FIELD_NAMES.M2M, \
    #     MachineFamily._meta.FIELD_NAMES.M2M
    # autocomplete_lookup_fields = \
    #     dict(fk=(MachineClass._meta.FIELD_NAMES.SELF,),
    #          m2m=(MachineDataStream._meta.FIELD_NAMES.M2M,))

    readonly_fields = \
        'created', \
        'updated'

    def machine_component_list(self, obj):
        n = obj.machine_components.count()

        return '{}: {}'.format(
                n, ', '.join(machine_component.name
                             for machine_component in obj.machine_components.all())) \
            if n \
          else ''

    def n_machine_data_streams(self, obj):
        n = obj.machine_data_streams.count()

        return n \
            if n \
          else ''

    def machine_family_list(self, obj):
        n = obj.machine_families.count()

        return '{}: {}'.format(
                n, ', '.join(machine_family.unique_name
                             for machine_family in obj.machine_families.all())) \
            if n \
          else ''

    def n_machines(self, obj):
        n = obj.machines.count()

        return n \
            if n \
          else ''

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineSKU,
                    'unique_name',
                    'descriptions',
                    'created',
                    'updated',                    
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_components=MACHINE_COMPONENT_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    machine_data_streams=MACHINE_DATA_STREAM_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    machine_families=MACHINE_FAMILY_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineSKU,
                    'unique_name',
                    'descriptions',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
                    machine_data_streams=MACHINE_DATA_STREAM_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    machine_families=MACHINE_FAMILY_NAME_ONLY_QUERY_GRAPH,
                    machines=
                        ModelQueryGraph(
                            Machine,
                            'machine_sku',
                            ORDER=False),
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineSKU._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineSKU._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


class LocationMachineInLine(StackedInline):
    model = Machine

    fields = \
        'machine_class', \
        'machine_sku', \
        'unique_id', \
        'info', \
        'machine_families'

    form = LocationMachineInLineForm

    readonly_fields = \
        'created', \
        'updated'

    extra = 0

    def get_queryset(self, request):
        return ModelQueryGraph(
                Machine,
                'unique_id',
                'info',
                machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                machine_sku=MACHINE_SKU_STR_UNORDERED_QUERY_GRAPH,
                location=LOCATION_STR_UNORDERED_QUERY_GRAPH,
                machine_families=MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_GRAPH,
                ORDER=True) \
            .query_set(
                init=super().get_queryset(request=request))


@register(
    Location,
    site=site)
class LocationAdmin(ModelAdmin):
    list_display = \
        'unique_name', \
        'descriptions', \
        'info', \
        'n_machines', \
        'updated'

    list_display_links = 'unique_name',

    search_fields = Location.search_fields()

    show_full_result_count = False

    form = LocationForm

    readonly_fields = \
        'created', \
        'updated'

    inlines = LocationMachineInLine,

    def n_machines(self, obj):
        n = obj.machines.count()

        return n \
            if n \
          else ''

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return query_set \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    Location,
                    'unique_name',
                    'descriptions',
                    'info',
                    'updated',
                    machines=
                        ModelQueryGraph(
                            Machine,
                            'location',
                            ORDER=False),
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                Location._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                Location._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    Machine,
    site=site)
class MachineAdmin(ModelAdmin):
    list_display = \
        'machine_class', \
        'machine_sku', \
        'unique_id', \
        'info', \
        'location', \
        'updated'

    list_display_links = 'unique_id',

    list_filter = \
        'machine_class__unique_name', \
        'machine_sku__unique_name', \
        'location__unique_name'

    search_fields = Machine.search_fields()

    show_full_result_count = False

    # using Django-AutoComplete-Light
    form = MachineForm

    # if using default Admin AutoComplete
    # autocomplete_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineSKU._meta.FIELD_NAMES.SELF, \
    #     Location._meta.FIELD_NAMES.SELF

    # if using Grappelli AutoComplete
    # raw_id_fields = \
    #     MachineClass._meta.FIELD_NAMES.SELF, \
    #     MachineSKU._meta.FIELD_NAMES.SELF, \
    #     Location._meta.FIELD_NAMES.SELF
    # autocomplete_lookup_fields = \
    #     dict(fk=(MachineClass._meta.FIELD_NAMES.SELF,
    #              MachineSKU._meta.FIELD_NAMES.SELF,
    #              Location._meta.FIELD_NAMES.SELF))

    readonly_fields = \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    Machine,
                    'unique_id',
                    'info',
                    'created',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_sku=MACHINE_SKU_STR_UNORDERED_QUERY_GRAPH,
                    machine_families=MACHINE_FAMILY_PK_ONLY_UNORDERED_QUERY_GRAPH,
                    location=LOCATION_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    Machine,
                    'unique_id',
                    'info',
                    'updated',
                    machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
                    machine_sku=MACHINE_SKU_STR_UNORDERED_QUERY_GRAPH,
                    location=LOCATION_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                Machine._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                Machine._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyData,
    site=site)
class MachineFamilyDataAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'date', \
        'url', \
        'n_cols', \
        'n_rows', \
        'updated'

    list_display_links = \
        'machine_family', \
        'url'

    list_filter = \
        'machine_family__machine_class__unique_name', \
        'machine_family__unique_name', \
        'date'

    search_fields = MachineFamilyData.search_fields()

    show_full_result_count = False

    form = MachineFamilyDataForm

    readonly_fields = \
        'machine_family', \
        'date', \
        'url', \
        'n_cols', \
        'n_rows', \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamilyData,
                    'date',
                    'url',
                    'n_cols',
                    'n_rows',
                    'schema',
                    'created',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamilyData,
                    'date',
                    'url',
                    'n_cols',
                    'n_rows',
                    'updated',
                    machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyData._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyData._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyDataStreamsCheck,
    site=site)
class MachineFamilyDataStreamsCheckAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'machine_data_stream_names_not_in_db', \
        'machine_data_stream_names_not_on_disk', \
        'updated'

    list_display_links = \
        'machine_family', \
        'machine_data_stream_names_not_in_db', \
        'machine_data_stream_names_not_on_disk'

    list_filter = \
        'machine_family_data__machine_family__machine_class__unique_name', \
        'machine_family_data__machine_family__unique_name'

    search_fields = MachineFamilyDataStreamsCheck.search_fields()

    show_full_result_count = False

    form = MachineFamilyDataStreamsCheckForm

    readonly_fields = \
        'machine_family_data', \
        'machine_data_stream_names_not_in_db', \
        'machine_data_stream_names_not_on_disk', \
        'updated'

    def machine_family(self, obj):
        return obj.machine_family_data.machine_family

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamilyDataStreamsCheck,
                    'machine_data_stream_names_not_in_db',
                    'machine_data_stream_names_not_on_disk',
                    'created',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamilyDataStreamsCheck,
                    'machine_data_stream_names_not_in_db',
                    'machine_data_stream_names_not_on_disk',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamsCheck._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamsCheck._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyDataStreamProfile,
    site=site)
class MachineFamilyDataStreamProfileAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'data_to_date', \
        'machine_data_stream', \
        'n_samples', \
        'valid_fraction', \
        'n_distinct_values', \
        'distinct_value_proportions', \
        'strictly_outlier_robust_proportion', \
        'min', \
        'robust_min', \
        'quartile', \
        'median', \
        '_3rd_quartile', \
        'robust_max', \
        'max', \
        'updated'

    list_display_links = \
        'machine_family', \
        'data_to_date', \
        'machine_data_stream'

    list_filter = \
        'machine_family_data__machine_family__machine_class__unique_name', \
        'machine_family_data__machine_family__unique_name', \
        'data_to_date', \
        'machine_data_stream__name', \
        'machine_data_stream__machine_data_stream_type', \
        'machine_data_stream__logical_data_type', \
        'machine_data_stream__physical_data_type__unique_name', \
        'machine_data_stream__measurement_unit__unique_name', \
        'machine_data_stream__neg_invalid', \
        'machine_data_stream__pos_invalid', \
        'machine_data_stream__default'

    search_fields = MachineFamilyDataStreamProfile.search_fields()

    ordering = \
        'machine_family_data__machine_family', \
        '-data_to_date', \
        '-n_distinct_values'

    show_full_result_count = False

    form = MachineFamilyDataStreamProfileForm

    readonly_fields = \
        'machine_family_data', \
        'data_to_date', \
        'machine_data_stream', \
        'n_samples', \
        'valid_fraction', \
        'n_distinct_values', \
        'distinct_value_proportions', \
        'strictly_outlier_robust_proportion', \
        'min', \
        'robust_min', \
        'quartile', \
        'median', \
        '_3rd_quartile', \
        'robust_max', \
        'max', \
        'created', \
        'updated'

    def machine_family(self, obj):
        return obj.machine_family_data.machine_family

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamilyDataStreamProfile,
                    'data_to_date',
                    'n_samples',
                    'valid_fraction',
                    'n_distinct_values',
                    'distinct_value_proportions',
                    'strictly_outlier_robust_proportion',
                    'min',
                    'robust_min',
                    'quartile',
                    'median',
                    '_3rd_quartile',
                    'robust_max',
                    'max',
                    'created',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamilyDataStreamProfile,
                    'data_to_date',
                    'n_samples',
                    'valid_fraction',
                    'n_distinct_values',
                    'distinct_value_proportions',
                    'strictly_outlier_robust_proportion',
                    'min',
                    'robust_min',
                    'quartile',
                    'median',
                    '_3rd_quartile',
                    'robust_max',
                    'max',
                    'created',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamProfile._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)
    
    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamProfile._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyDataStreamPairCorr,
    site=site)
class MachineFamilyDataStreamPairCorrAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'data_to_date', \
        'machine_data_stream', \
        'other_machine_data_stream', \
        'corr', \
        'n_samples', \
        'machine_data_stream_range', \
        'other_machine_data_stream_range', \
        'updated'

    list_display_links = \
        'machine_family', \
        'data_to_date', \
        'machine_data_stream', \
        'other_machine_data_stream', \

    list_filter = MachineFamilyDataStreamProfileAdmin.list_filter

    search_fields = MachineFamilyDataStreamPairCorr.search_fields()

    ordering = \
        'machine_family_data__machine_family', \
        '-data_to_date', \
        '-corr'

    show_full_result_count = False

    form = MachineFamilyDataStreamPairCorrForm

    readonly_fields = \
        'machine_family_data', \
        'data_to_date', \
        'machine_data_stream', \
        'other_machine_data_stream', \
        'corr', \
        'n_samples', \
        'machine_data_stream_range', \
        'other_machine_data_stream_range', \
        'created', \
        'updated'

    def machine_family(self, obj):
        return obj.machine_family_data.machine_family

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamilyDataStreamPairCorr,
                    'data_to_date',
                    'corr',
                    'n_samples',
                    'machine_data_stream_range',
                    'other_machine_data_stream_range',
                    'created',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    other_machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamilyDataStreamPairCorr,
                    'data_to_date',
                    'corr',
                    'n_samples',
                    'machine_data_stream_range',
                    'other_machine_data_stream_range',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    other_machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamPairCorr._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamPairCorr._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineFamilyDataStreamAgg,
    site=site)
class MachineFamilyDataStreamAggAdmin(ModelAdmin):
    list_display = \
        'machine_family', \
        'date', \
        'machine_data_stream', \
        'count_incl_invalid', \
        'distinct_value_proportions_incl_invalid', \
        'count_excl_invalid', \
        'distinct_value_proportions_excl_invalid', \
        'weighted_average_min', \
        'weighted_average_robust_min', \
        'weighted_average_quartile', \
        'weighted_average_median', \
        'weighted_average_mean', \
        'weighted_average_3rd_quartile', \
        'weighted_average_robust_max', \
        'weighted_average_max', \
        'updated'

    list_display_links = \
        'machine_family', \
        'date', \
        'machine_data_stream'

    list_filter = \
        'machine_family_data__machine_family__machine_class__unique_name', \
        'machine_family_data__machine_family__unique_name', \
        'machine_family_data__date', \
        'machine_data_stream__name', \
        'machine_data_stream__machine_data_stream_type', \
        'machine_data_stream__logical_data_type', \
        'machine_data_stream__physical_data_type__unique_name', \
        'machine_data_stream__measurement_unit__unique_name', \
        'machine_data_stream__neg_invalid', \
        'machine_data_stream__pos_invalid', \
        'machine_data_stream__default'

    show_full_result_count = False

    search_fields = MachineFamilyDataStreamAgg.search_fields()

    form = MachineFamilyDataStreamAggForm

    readonly_fields = \
        'machine_family_data', \
        'machine_data_stream', \
        'count_incl_invalid', \
        'counts_incl_invalid', \
        'distinct_value_counts_incl_invalid', \
        'distinct_value_proportions_incl_invalid', \
        'count_excl_invalid', \
        'counts_excl_invalid', \
        'distinct_value_proportions_excl_invalid', \
        'weighted_average_min', \
        'weighted_average_robust_min', \
        'weighted_average_quartile', \
        'weighted_average_median', \
        'weighted_average_mean', \
        'weighted_average_3rd_quartile', \
        'weighted_average_robust_max', \
        'weighted_average_max', \
        'created', \
        'updated'

    def machine_family(self, obj):
        return obj.machine_family_data.machine_family

    def date(self, obj):
        return obj.machine_family_data.date

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineFamilyDataStreamAgg,
                    'count_incl_invalid',
                    'counts_incl_invalid',
                    'distinct_value_counts_incl_invalid',
                    'distinct_value_proportions_incl_invalid',
                    'count_excl_invalid',
                    'counts_excl_invalid',
                    'distinct_value_proportions_excl_invalid',
                    'weighted_average_min',
                    'weighted_average_robust_min',
                    'weighted_average_quartile',
                    'weighted_average_median',
                    'weighted_average_mean',
                    'weighted_average_3rd_quartile',
                    'weighted_average_robust_max',
                    'weighted_average_max',
                    'created',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineFamilyDataStreamAgg,
                    'count_incl_invalid',
                    'distinct_value_counts_incl_invalid',
                    'distinct_value_proportions_incl_invalid',
                    'count_excl_invalid',
                    'distinct_value_proportions_excl_invalid',
                    'weighted_average_min',
                    'weighted_average_robust_min',
                    'weighted_average_quartile',
                    'weighted_average_median',
                    'weighted_average_mean',
                    'weighted_average_3rd_quartile',
                    'weighted_average_robust_max',
                    'weighted_average_max',
                    'updated',
                    machine_family_data=MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH,
                    machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamAgg._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineFamilyDataStreamAgg._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineData,
    site=site)
class MachineDataAdmin(ModelAdmin):
    list_display = \
        'machine', \
        'date', \
        'url', \
        'n_cols', \
        'n_rows', \
        'updated'

    list_filter = \
        'machine__machine_class__unique_name', \
        'machine__machine_sku__unique_name', \
        'date'

    search_fields = MachineData.search_fields()

    show_full_result_count = False

    form = MachineDataForm

    readonly_fields = \
        'machine', \
        'date', \
        'url', \
        'n_cols', \
        'n_rows', \
        'created', \
        'updated'

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineData,
                    'date',
                    'url',
                    'n_cols',
                    'n_rows',
                    'schema',
                    'created',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineData,
                    'date',
                    'url',
                    'n_cols',
                    'n_rows',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineData._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineData._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)


@register(
    MachineDataStreamAgg,
    site=site)
class MachineDataStreamAggAdmin(ModelAdmin):
    list_display = \
        'machine', \
        'machine_family', \
        'date', \
        'machine_data_stream', \
        'count_incl_invalid', \
        'distinct_value_proportions_incl_invalid', \
        'count_excl_invalid', \
        'distinct_value_proportions_excl_invalid', \
        'min', \
        'robust_min', \
        'quartile', \
        'median', \
        'mean', \
        '_3rd_quartile', \
        'robust_max', \
        'max', \
        'updated'

    list_display_links = \
        'machine', \
        'machine_family', \
        'date', \
        'machine_data_stream'

    list_filter = \
        'machine_family_data_stream_agg__machine_family_data__machine_family__machine_class__unique_name', \
        'machine_family_data_stream_agg__machine_family_data__machine_family__unique_name', \
        'machine_family_data_stream_agg__machine_family_data__date', \
        'machine_family_data_stream_agg__machine_data_stream__name', \
        'machine_family_data_stream_agg__machine_data_stream__machine_data_stream_type', \
        'machine_family_data_stream_agg__machine_data_stream__logical_data_type', \
        'machine_family_data_stream_agg__machine_data_stream__physical_data_type__unique_name', \
        'machine_family_data_stream_agg__machine_data_stream__measurement_unit__unique_name', \
        'machine_family_data_stream_agg__machine_data_stream__neg_invalid', \
        'machine_family_data_stream_agg__machine_data_stream__pos_invalid', \
        'machine_family_data_stream_agg__machine_data_stream__default', \
        'machine__machine_class__unique_name', \
        'machine__machine_sku__unique_name', \
        'machine__location__unique_name'

    show_full_result_count = False

    search_fields = MachineDataStreamAgg.search_fields()

    form = MachineDataStreamAggForm

    readonly_fields = \
        'machine', \
        'machine_family_data_stream_agg', \
        'count_incl_invalid', \
        'distinct_value_counts_incl_invalid', \
        'distinct_value_proportions_incl_invalid', \
        'count_excl_invalid', \
        'distinct_value_proportions_excl_invalid', \
        'min', \
        'robust_min', \
        'quartile', \
        'median', \
        'mean', \
        '_3rd_quartile', \
        'robust_max', \
        'max', \
        'created', \
        'updated'

    def machine_family(self, obj):
        return obj.machine_family_data_stream_agg.machine_family_data.machine_family

    def date(self, obj):
        return obj.machine_family_data_stream_agg.machine_family_data.date

    def machine_data_stream(self, obj):
        return obj.machine_family_data_stream_agg.machine_data_stream

    def get_queryset(self, request):
        query_set = super().get_queryset(request=request)

        return (ModelQueryGraph(
                    MachineDataStreamAgg,
                    'count_incl_invalid',
                    'distinct_value_counts_incl_invalid',
                    'distinct_value_proportions_incl_invalid',
                    'count_excl_invalid',
                    'distinct_value_proportions_excl_invalid',
                    'min',
                    'robust_min',
                    'quartile',
                    'median',
                    'mean',
                    '_3rd_quartile',
                    'robust_max',
                    'max',
                    'created',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_family_data_stream_agg=MACHINE_FAMILY_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH,
                    ORDER=False)
                .query_set(
                    init=query_set)) \
            if request.resolver_match.url_name.endswith('_change') \
          else (ModelQueryGraph(
                    MachineDataStreamAgg,
                    'count_incl_invalid',
                    'distinct_value_proportions_incl_invalid',
                    'count_excl_invalid',
                    'distinct_value_proportions_excl_invalid',
                    'min',
                    'robust_min',
                    'quartile',
                    'median',
                    'mean',
                    '_3rd_quartile',
                    'robust_max',
                    'max',
                    'updated',
                    machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
                    machine_family_data_stream_agg=MACHINE_FAMILY_DATA_STREAM_AGG_ABBR_QUERY_GRAPH,
                    ORDER=True)
                .query_set(
                    init=query_set))

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineDataStreamAgg._meta.verbose_name_plural))
    def changelist_view(self, *args, **kwargs):
        return super().changelist_view(*args, **kwargs)

    @silk_profile(
        name='{}: {}'.format(
                __module__,
                MachineDataStreamAgg._meta.verbose_name))
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)
