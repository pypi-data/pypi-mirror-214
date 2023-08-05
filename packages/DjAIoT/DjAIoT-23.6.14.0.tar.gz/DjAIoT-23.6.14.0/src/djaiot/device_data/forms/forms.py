from django.contrib.admin import site

from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from django.forms import ModelChoiceField, ModelMultipleChoiceField

from django_admin_hstore_widget.widgets import HStoreFormWidget
from django_json_widget.widgets import JSONEditorWidget

from dal.autocomplete import ModelSelect2, ModelSelect2Multiple
from dal.forms import FutureModelForm

from .autocompletes import \
    PhysicalDataTypeAutoComplete, \
    MeasurementUnitAutoComplete, \
    MachineClassAutoComplete, \
    MachineComponentAutoComplete, \
    MachineDataStreamAutoComplete, \
    MachineFamilyAutoComplete, \
    MachineSKUAutoComplete, \
    LocationAutoComplete, \
    MachineFamilyComponentAutoComplete

from .models import \
    EnvironmentVariable, \
    PhysicalDataType, \
    MeasurementUnit, \
    MachineClass, \
    MachineComponent, \
    MachineDataStream, \
    MachineFamily, \
    MachineSKU, \
    MachineFamilyComponent, \
    Location, \
    Machine, \
    MachineFamilyData, \
    MachineFamilyDataStreamsCheck, \
    MachineFamilyDataStreamProfile, \
    MachineFamilyDataStreamPairCorr, \
    MachineFamilyDataStreamAgg, \
    MachineData, \
    MachineDataStreamAgg

from .queries import \
    PHYSICAL_DATA_TYPE_STR_QUERY_SET, PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_SET, \
    MEASUREMENT_UNIT_STR_UNORDERED_QUERY_SET, \
    MACHINE_CLASS_STR_UNORDERED_QUERY_SET, \
    MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_SET, MACHINE_COMPONENT_STR_UNORDERED_QUERY_SET, \
    MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_SET, \
    MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_SET, MACHINE_FAMILY_STR_UNORDERED_QUERY_SET, \
    MACHINE_SKU_STR_SUBSET_ORDERED_QUERY_SET, MACHINE_SKU_STR_UNORDERED_QUERY_SET, \
    LOCATION_STR_UNORDERED_QUERY_SET, \
    MACHINE_FAMILY_COMPONENT_STR_SUBSET_ORDERED_QUERY_SET


MACHINE_CLASS_MODEL_CHOICE_FIELD = \
    ModelChoiceField(
        queryset=MACHINE_CLASS_STR_UNORDERED_QUERY_SET,
        widget=ModelSelect2(
                url=MachineClassAutoComplete.name),
            # RelatedFieldWidgetWrapper: very hard to use
            # RelatedFieldWidgetWrapper(
            #     widget=ModelSelect2(
            #             url=MachineClassAutoComplete.name),
            #     rel=???,   # MUST BE SPECIFIC TO 1 RELATION
            #     admin_site=site,
            #     can_add_related=True,
            #     can_change_related=True,
            #     can_delete_related=True,
            #     can_view_related=True)
        required=True)


MACHINE_COMPONENTS_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_SET,
        widget=ModelSelect2Multiple(
                url=MachineComponentAutoComplete.name,
                attrs={# https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html#passing-options-to-select2
                       'data-minimum-input-length': MachineComponentAutoComplete.data_min_input_len}),
        required=False)


MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_SET,
        widget=ModelSelect2Multiple(
                url=MachineDataStreamAutoComplete.name,
                attrs={'data-minimum-input-length': MachineDataStreamAutoComplete.data_min_input_len}),
        required=False)


MACHINE_FAMILIES_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_SET,
        widget=ModelSelect2Multiple(
                url=MachineFamilyAutoComplete.name,
                attrs={'data-minimum-input-length': MachineFamilyAutoComplete.data_min_input_len}),
        required=False)


MACHINE_SKUS_MODEL_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=MACHINE_SKU_STR_SUBSET_ORDERED_QUERY_SET,
        widget=ModelSelect2Multiple(
                url=MachineSKUAutoComplete.name,
                attrs={'data-minimum-input-length': MachineSKUAutoComplete.data_min_input_len}),
        required=False)


class EnvironmentVariableForm(FutureModelForm):
    class Meta:
        model = EnvironmentVariable

        fields = \
            'key', \
            'value'

        widgets = \
            dict(value=JSONEditorWidget)


class PhysicalDataTypeForm(FutureModelForm):
    same = \
        ModelMultipleChoiceField(
            queryset=PHYSICAL_DATA_TYPE_STR_QUERY_SET,
            widget=ModelSelect2Multiple(
                    url=PhysicalDataTypeAutoComplete.name),
            required=False)

    class Meta:
        model = PhysicalDataType

        fields = \
            'unique_name', \
            'min', \
            'max', \
            'same'


class MeasurementUnitForm(FutureModelForm):
    class Meta:
        model = MeasurementUnit

        fields = \
            'unique_name', \
            'descriptions'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class MachineClassForm(FutureModelForm):
    class Meta:
        model = MachineClass

        fields = \
            'unique_name', \
            'descriptions'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class MachineComponentForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    # BELOW FIELDS ARE READ-ONLY IN ADMIN
    # machine_families = MACHINE_FAMILIES_MODEL_MULTIPLE_CHOICE_FIELD
    # directly_interacting_components = MACHINE_COMPONENTS_MULTIPLE_CHOICE_FIELD
    # sub_components = MACHINE_COMPONENTS_MULTIPLE_CHOICE_FIELD
    # machine_data_streams = MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD

    machine_skus = MACHINE_SKUS_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = MachineComponent

        fields = \
            'machine_class', \
            'name', \
            'descriptions', \
            'directly_interacting_components', \
            'sub_components', \
            'machine_data_streams', \
            'machine_skus'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class MachineDataStreamForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    # BELOW FIELDS ARE READ-ONLY IN ADMIN
    # machine_components = MACHINE_COMPONENTS_MULTIPLE_CHOICE_FIELD

    physical_data_type = \
        ModelChoiceField(
            queryset=PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_SET,
            widget=ModelSelect2(
                    url=PhysicalDataTypeAutoComplete.name),
            required=False)

    measurement_unit = \
        ModelChoiceField(
            queryset=MEASUREMENT_UNIT_STR_UNORDERED_QUERY_SET,
            widget=ModelSelect2(
                    url=MeasurementUnitAutoComplete.name),
            required=False)

    machine_skus = MACHINE_SKUS_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = MachineDataStream

        fields = \
            'machine_class', \
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
            'machine_components', \
            'machine_skus'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class MachineFamilyForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    filtered_from_machine_family = \
        ModelChoiceField(
            queryset=MACHINE_FAMILY_STR_UNORDERED_QUERY_SET,
            widget=ModelSelect2(
                    url=MachineFamilyAutoComplete.name),
            required=False)

    machine_skus = MACHINE_SKUS_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = MachineFamily

        fields = \
            'machine_class', \
            'unique_name', \
            'descriptions', \
            'filtered_from_machine_family', \
            'machine_data_filter_condition', \
            'machine_skus', \
            'machine_data_streams'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class MachineSKUForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    machine_components = MACHINE_COMPONENTS_MULTIPLE_CHOICE_FIELD

    machine_data_streams = MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD

    machine_families = MACHINE_FAMILIES_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = MachineSKU

        fields = \
            'machine_class' ,\
            'unique_name', \
            'descriptions', \
            'machine_components', \
            'machine_data_streams', \
            'machine_families'

        widgets = \
            dict(descriptions=JSONEditorWidget)


class LocationForm(FutureModelForm):
    class Meta:
        model = Location

        fields = \
            'unique_name', \
            'descriptions', \
            'info'

        widgets = \
            dict(descriptions=JSONEditorWidget,
                 info=JSONEditorWidget)


MACHINE_SKU_MODEL_CHOICE_FIELD = \
    ModelChoiceField(
        queryset=MACHINE_SKU_STR_UNORDERED_QUERY_SET,
        widget=ModelSelect2(
                url=MachineSKUAutoComplete.name,
                attrs={'data-minimum-input-length': MachineSKUAutoComplete.data_min_input_len}),
        required=False)


LOCATION_MODEL_CHOICE_FIELD = \
    ModelChoiceField(
        queryset=LOCATION_STR_UNORDERED_QUERY_SET,
        widget=ModelSelect2(
                url=LocationAutoComplete.name,
                attrs={'data-minimum-input-length': LocationAutoComplete.data_min_input_len}),
        required=False)


class MachineForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    machine_sku = MACHINE_SKU_MODEL_CHOICE_FIELD

    location = LOCATION_MODEL_CHOICE_FIELD

    machine_families = MACHINE_FAMILIES_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = Machine

        fields = \
            'machine_class', \
            'machine_sku', \
            'unique_id', \
            'info', \
            'machine_families', \
            'location'

        widgets = \
            dict(info=JSONEditorWidget)


class LocationMachineInLineForm(FutureModelForm):
    machine_class = MACHINE_CLASS_MODEL_CHOICE_FIELD

    machine_sku = MACHINE_SKU_MODEL_CHOICE_FIELD

    machine_families = MACHINE_FAMILIES_MODEL_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = Machine

        fields = \
            'machine_class', \
            'machine_sku', \
            'unique_id', \
            'info', \
            'machine_families'

        widgets = \
            dict(info=JSONEditorWidget)


MACHINE_FAMILY_COMPONENTS_MULTIPLE_CHOICE_FIELD = \
    ModelMultipleChoiceField(
        queryset=MACHINE_FAMILY_COMPONENT_STR_SUBSET_ORDERED_QUERY_SET,
        widget=ModelSelect2Multiple(
                url=MachineFamilyComponentAutoComplete.name,
                attrs={'data-minimum-input-length': MachineFamilyComponentAutoComplete.data_min_input_len}),
        required=False)


class MachineFamilyComponentInLineForm(FutureModelForm):
    machine_component = \
        ModelChoiceField(
            queryset=MACHINE_COMPONENT_STR_UNORDERED_QUERY_SET,
            widget=ModelSelect2(
                    url=MachineComponentAutoComplete.name,
                    attrs={'data-minimum-input-length': MachineComponentAutoComplete.data_min_input_len}),
            required=True)

    directly_interacting_components = MACHINE_FAMILY_COMPONENTS_MULTIPLE_CHOICE_FIELD

    sub_components = MACHINE_FAMILY_COMPONENTS_MULTIPLE_CHOICE_FIELD

    machine_data_streams = MACHINE_DATA_STREAMS_MULTIPLE_CHOICE_FIELD

    class Meta:
        model = MachineFamilyComponent

        fields = \
            'machine_component', \
            'directly_interacting_components', \
            'sub_components', \
            'machine_data_streams'


class MachineFamilyDataForm(FutureModelForm):
    class Meta:
        model = MachineFamilyData

        fields = \
            'machine_family', \
            'date', \
            'url', \
            'n_cols', \
            'n_rows', \
            'schema'

        widgets = \
            dict(schema=HStoreFormWidget)


class MachineFamilyDataStreamsCheckForm(FutureModelForm):
    class Meta:
        model = MachineFamilyDataStreamsCheck

        fields = \
            'machine_family_data', \
            'machine_data_stream_names_not_in_db', \
            'machine_data_stream_names_not_on_disk'


class MachineFamilyDataStreamProfileForm(FutureModelForm):
    class Meta:
        model = MachineFamilyDataStreamProfile

        fields = \
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
            'max'


class MachineFamilyDataStreamPairCorrForm(FutureModelForm):
    class Meta:
        model = MachineFamilyDataStreamPairCorr

        fields = \
            'machine_family_data', \
            'data_to_date', \
            'machine_data_stream', \
            'other_machine_data_stream', \
            'corr', \
            'n_samples', \
            'machine_data_stream_range', \
            'other_machine_data_stream_range'


class MachineFamilyDataStreamAggForm(FutureModelForm):
    class Meta:
        model = MachineFamilyDataStreamAgg

        fields = \
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
            'weighted_average_max'


class MachineDataForm(FutureModelForm):
    class Meta:
        model = MachineData

        fields = \
            'machine', \
            'date', \
            'url', \
            'n_cols', \
            'n_rows', \
            'schema'

        widgets = \
            dict(schema=HStoreFormWidget)


class MachineDataStreamAggForm(FutureModelForm):
    class Meta:
        model = MachineDataStreamAgg

        fields = \
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
            'max'
