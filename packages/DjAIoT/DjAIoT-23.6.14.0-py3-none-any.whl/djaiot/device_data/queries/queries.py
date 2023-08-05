from django_model_query_graphs import PK_FIELD_NAME, ModelQueryGraph

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
    MachineFamilyDataStreamProfile, \
    MachineFamilyDataStreamPairCorr, \
    MachineFamilyDataStreamAgg, \
    MachineData, \
    MachineDataStreamAgg


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


PHYSICAL_DATA_TYPE_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        'unique_name',
        'min',
        'max',
        'range',
        ORDER=True)

PHYSICAL_DATA_TYPE_FULL_QUERY_SET = \
    PHYSICAL_DATA_TYPE_FULL_QUERY_GRAPH.query_set()


PHYSICAL_DATA_TYPE_FULL_NESTED_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        'unique_name',
        'min',
        'max',
        'range',
        same=PHYSICAL_DATA_TYPE_FULL_QUERY_GRAPH,
        ORDER=True)

PHYSICAL_DATA_TYPE_FULL_NESTED_QUERY_SET = \
    PHYSICAL_DATA_TYPE_FULL_NESTED_QUERY_GRAPH.query_set()


PHYSICAL_DATA_TYPE_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        'unique_name',
        'range',
        ORDER=True)

PHYSICAL_DATA_TYPE_STR_QUERY_SET = \
    PHYSICAL_DATA_TYPE_STR_QUERY_GRAPH.query_set()


PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        'unique_name',
        'range',
        ORDER=False)

PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_SET = \
    PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH.query_set()


PHYSICAL_DATA_TYPE_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        'unique_name',
        ORDER=True)

PHYSICAL_DATA_TYPE_ABBR_QUERY_SET = \
    PHYSICAL_DATA_TYPE_ABBR_QUERY_GRAPH.query_set()


PHYSICAL_DATA_TYPE_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        'unique_name',
        ORDER=True)

PHYSICAL_DATA_TYPE_NAME_ONLY_QUERY_SET = \
    PHYSICAL_DATA_TYPE_NAME_ONLY_QUERY_GRAPH.query_set()


PHYSICAL_DATA_TYPE_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        PK_FIELD_NAME,
        ORDER=False)

PHYSICAL_DATA_TYPE_PK_ONLY_UNORDERED_QUERY_SET = \
    PHYSICAL_DATA_TYPE_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MEASUREMENT_UNIT_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MeasurementUnit,
        'unique_name',
        'descriptions',
        ORDER=True)

MEASUREMENT_UNIT_FULL_QUERY_SET = \
    MEASUREMENT_UNIT_FULL_QUERY_GRAPH.query_set()


MEASUREMENT_UNIT_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MeasurementUnit,
        'unique_name',
        ORDER=True)

MEASUREMENT_UNIT_STR_QUERY_SET = \
    MEASUREMENT_UNIT_STR_QUERY_GRAPH.query_set()


MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MeasurementUnit,
        'unique_name',
        ORDER=False)

MEASUREMENT_UNIT_STR_UNORDERED_QUERY_SET = \
    MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH.query_set()


MEASUREMENT_UNIT_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MeasurementUnit,
        'unique_name',
        ORDER=True)

MEASUREMENT_UNIT_ABBR_QUERY_SET = \
    MEASUREMENT_UNIT_ABBR_QUERY_GRAPH.query_set()


MEASUREMENT_UNIT_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MeasurementUnit,
        'unique_name',
        ORDER=True)

MEASUREMENT_UNIT_NAME_ONLY_QUERY_SET = \
    MEASUREMENT_UNIT_NAME_ONLY_QUERY_GRAPH.query_set()


MEASUREMENT_UNIT_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MeasurementUnit,
        PK_FIELD_NAME,
        ORDER=False)

MEASUREMENT_UNIT_NAME_ONLY_UNORDERED_QUERY_SET = \
    MEASUREMENT_UNIT_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_CLASS_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineClass,
        'unique_name',
        'descriptions',
        ORDER=True)

MACHINE_CLASS_FULL_QUERY_SET = \
    MACHINE_CLASS_FULL_QUERY_GRAPH.query_set()


MACHINE_CLASS_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineClass,
        'unique_name',
        ORDER=True)

MACHINE_CLASS_STR_QUERY_SET = \
    MACHINE_CLASS_STR_QUERY_GRAPH.query_set()


MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineClass,
        'unique_name',
        ORDER=False)

MACHINE_CLASS_STR_UNORDERED_QUERY_SET = \
    MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_CLASS_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineClass,
        'unique_name',
        ORDER=True)

MACHINE_CLASS_ABBR_QUERY_SET = \
    MACHINE_CLASS_ABBR_QUERY_GRAPH.query_set()


MACHINE_CLASS_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineClass,
        'unique_name',
        ORDER=True)

MACHINE_CLASS_NAME_ONLY_QUERY_SET = \
    MACHINE_CLASS_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_CLASS_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineClass,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_CLASS_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_CLASS_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        'descriptions',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_COMPONENT_FULL_QUERY_SET = \
    MACHINE_COMPONENT_FULL_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        machine_class=MACHINE_CLASS_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_COMPONENT_ABBR_QUERY_SET = \
    MACHINE_COMPONENT_ABBR_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        ORDER='name')

MACHINE_COMPONENT_NAME_ONLY_QUERY_SET = \
    MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_COMPONENT_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_COMPONENT_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        'name',
        'descriptions',
        'machine_data_stream_type',
        'logical_data_type',
        'neg_invalid',
        'pos_invalid',
        'default',
        'range',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        physical_data_type=PHYSICAL_DATA_TYPE_FULL_NESTED_QUERY_GRAPH,
        measurement_unit=MEASUREMENT_UNIT_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_FULL_QUERY_SET = \
    MACHINE_DATA_STREAM_FULL_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        'name',
        'machine_data_stream_type',
        'logical_data_type',
        'neg_invalid',
        'pos_invalid',
        'default',
        'range',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        physical_data_type=PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH,
        measurement_unit=MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_STR_QUERY_SET = \
    MACHINE_DATA_STREAM_STR_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        'name',
        'machine_data_stream_type',
        'logical_data_type',
        'neg_invalid',
        'pos_invalid',
        'default',
        'range',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        physical_data_type=PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH,
        measurement_unit=MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH,
        ORDER='name')

MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_DATA_STREAM_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        'name',
        'machine_data_stream_type',
        'logical_data_type',
        'neg_invalid',
        'pos_invalid',
        'default',
        'range',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        physical_data_type=PHYSICAL_DATA_TYPE_STR_UNORDERED_QUERY_GRAPH,
        measurement_unit=MEASUREMENT_UNIT_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_SET = \
    MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_ABBR_QUERY_SET = \
    MACHINE_DATA_STREAM_ABBR_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        'name',
        ORDER='name')

MACHINE_DATA_STREAM_NAME_ONLY_QUERY_SET = \
    MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_DATA_STREAM_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_DATA_STREAM_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        directly_interacting_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        sub_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_COMPONENT_STR_QUERY_SET = \
    MACHINE_COMPONENT_STR_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        directly_interacting_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        sub_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER='name')

MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        directly_interacting_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        sub_components=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_COMPONENT_STR_UNORDERED_QUERY_SET = \
    MACHINE_COMPONENT_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        ORDER='unique_name')

MACHINE_FAMILY_NAME_ONLY_QUERY_SET = \
    MACHINE_FAMILY_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        ORDER=False)

MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'machine_data_filter_condition',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        filtered_from_machine_family=MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_STR_QUERY_SET = \
    MACHINE_FAMILY_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'machine_data_filter_condition',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        filtered_from_machine_family=MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH,
        ORDER='unique_name')

MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_FAMILY_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'machine_data_filter_condition',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        filtered_from_machine_family=MACHINE_FAMILY_NAME_ONLY_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'descriptions',
        'machine_data_filter_condition',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'descriptions',
        'machine_data_filter_condition',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        filtered_from_machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_FULL_QUERY_SET = \
    MACHINE_FAMILY_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        machine_class=MACHINE_CLASS_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_ABBR_QUERY_SET = \
    MACHINE_FAMILY_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_SKU_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        'descriptions',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_SKU_FULL_QUERY_SET = \
    MACHINE_SKU_FULL_QUERY_GRAPH.query_set()


MACHINE_SKU_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_SKU_STR_QUERY_SET = \
    MACHINE_SKU_STR_QUERY_GRAPH.query_set()


MACHINE_SKU_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER='unique_name')

MACHINE_SKU_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_SKU_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_SKU_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        machine_class=MACHINE_CLASS_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_SKU_STR_UNORDERED_QUERY_SET = \
    MACHINE_SKU_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_SKU_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        machine_class=MACHINE_CLASS_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_SKU_ABBR_QUERY_SET = \
    MACHINE_SKU_ABBR_QUERY_GRAPH.query_set()


MACHINE_SKU_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        ORDER='unique_name')

MACHINE_SKU_NAME_ONLY_QUERY_SET = \
    MACHINE_SKU_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_SKU_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_FULL_NESTED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        'descriptions',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        machine_families=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        directly_interacting_components=MACHINE_COMPONENT_FULL_QUERY_GRAPH,
        sub_components=MACHINE_COMPONENT_FULL_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        machine_skus=MACHINE_SKU_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_COMPONENT_FULL_NESTED_QUERY_SET = \
    MACHINE_COMPONENT_FULL_NESTED_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_FULL_NESTED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStream,
        'name',
        'descriptions',
        'machine_data_stream_type',
        'logical_data_type',
        'neg_invalid',
        'pos_invalid',
        'default',
        'range',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        physical_data_type=PHYSICAL_DATA_TYPE_FULL_NESTED_QUERY_GRAPH,
        measurement_unit=MEASUREMENT_UNIT_FULL_QUERY_GRAPH,
        machine_components=MACHINE_COMPONENT_FULL_QUERY_GRAPH,
        machine_skus=MACHINE_SKU_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_FULL_NESTED_QUERY_SET = \
    MACHINE_DATA_STREAM_FULL_NESTED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_FULL_NESTED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'descriptions',
        'machine_data_filter_condition',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        machine_components=MACHINE_COMPONENT_FULL_QUERY_GRAPH,
        machine_skus=MACHINE_SKU_FULL_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_FULL_NESTED_QUERY_SET = \
    MACHINE_FAMILY_FULL_NESTED_QUERY_GRAPH.query_set()


MACHINE_SKU_FULL_NESTED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        'descriptions',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        machine_components=MACHINE_COMPONENT_FULL_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        machine_families=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_SKU_FULL_NESTED_QUERY_SET = \
    MACHINE_SKU_FULL_NESTED_QUERY_GRAPH.query_set()


LOCATION_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        'unique_name',
        'descriptions',
        'info',
        ORDER=True)

LOCATION_FULL_QUERY_SET = \
    LOCATION_FULL_QUERY_GRAPH.query_set()


LOCATION_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        'unique_name',
        ORDER=True)

LOCATION_STR_QUERY_SET = \
    LOCATION_STR_QUERY_GRAPH.query_set()


LOCATION_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        'unique_name',
        ORDER=False)

LOCATION_STR_UNORDERED_QUERY_SET = \
    LOCATION_STR_UNORDERED_QUERY_GRAPH.query_set()


LOCATION_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        'unique_name',
        ORDER=True)

LOCATION_ABBR_QUERY_SET = \
    LOCATION_ABBR_QUERY_GRAPH.query_set()


LOCATION_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        'unique_name',
        ORDER=True)

LOCATION_NAME_ONLY_QUERY_SET = \
    LOCATION_NAME_ONLY_QUERY_GRAPH.query_set()


LOCATION_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        PK_FIELD_NAME,
        ORDER=False)

LOCATION_PK_ONLY_UNORDERED_QUERY_SET = \
    LOCATION_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        Machine,
        'unique_id',
        'info',
        machine_class=MACHINE_CLASS_FULL_QUERY_GRAPH,
        machine_sku=MACHINE_SKU_FULL_QUERY_GRAPH,
        location=LOCATION_FULL_QUERY_GRAPH,
        machine_families=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FULL_QUERY_SET = \
    MACHINE_FULL_QUERY_GRAPH.query_set()


MACHINE_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        Machine,
        'unique_id',
        machine_class=MACHINE_CLASS_STR_QUERY_GRAPH,
        machine_sku=MACHINE_SKU_NAME_ONLY_QUERY_GRAPH,
        location=LOCATION_STR_QUERY_GRAPH,
        ORDER=True)

MACHINE_STR_QUERY_SET = \
    MACHINE_STR_QUERY_GRAPH.query_set()


MACHINE_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        Machine,
        'unique_id',
        machine_class=MACHINE_CLASS_STR_QUERY_GRAPH,
        machine_sku=MACHINE_SKU_NAME_ONLY_QUERY_GRAPH,
        location=LOCATION_STR_QUERY_GRAPH,
        ORDER=False)

MACHINE_STR_UNORDERED_QUERY_SET = \
    MACHINE_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        Machine,
        'unique_id',
        machine_class=MACHINE_CLASS_ABBR_QUERY_GRAPH,
        machine_sku=MACHINE_SKU_NAME_ONLY_QUERY_GRAPH,
        location=LOCATION_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_ABBR_QUERY_SET = \
    MACHINE_ABBR_QUERY_GRAPH.query_set()


MACHINE_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        Machine,
        'unique_id',
        ORDER='unique_id')

MACHINE_NAME_ONLY_QUERY_SET = \
    MACHINE_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        Machine,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        machine_component=MACHINE_COMPONENT_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_COMPONENT_FULL_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_FULL_NESTED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        machine_component=MACHINE_COMPONENT_FULL_QUERY_GRAPH,
        directly_interacting_components=MACHINE_FAMILY_COMPONENT_FULL_QUERY_GRAPH,
        sub_components=MACHINE_FAMILY_COMPONENT_FULL_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_COMPONENT_FULL_NESTED_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_FULL_NESTED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        machine_family=MACHINE_FAMILY_STR_QUERY_GRAPH,
        machine_component=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_COMPONENT_ABBR_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        machine_component=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        ORDER='machine_component__name')

MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        machine_family=MACHINE_FAMILY_STR_QUERY_GRAPH,
        machine_component=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        directly_interacting_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        sub_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_COMPONENT_STR_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        machine_family=MACHINE_FAMILY_STR_QUERY_GRAPH,
        machine_component=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        directly_interacting_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        sub_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER='machine_component__name')

MACHINE_FAMILY_COMPONENT_STR_SUBSET_ORDERED_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_STR_SUBSET_ORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        machine_family=MACHINE_FAMILY_STR_QUERY_GRAPH,
        machine_component=MACHINE_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        directly_interacting_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        sub_components=MACHINE_FAMILY_COMPONENT_NAME_ONLY_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_COMPONENT_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_COMPONENT_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyComponent,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_COMPONENT_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_COMPONENT_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        'schema',
        machine_family=MACHINE_FAMILY_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_FULL_QUERY_SET = \
    MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        machine_family=MACHINE_FAMILY_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyData,
        'date',
        machine_family=MACHINE_FAMILY_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_ABBR_QUERY_SET = \
    MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyData,
        machine_family=MACHINE_FAMILY_ABBR_QUERY_GRAPH,
        ORDER='machine_family')

MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_SET = \
    MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyData,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_DATA_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAMS_CHECK_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamsCheck,
        'machine_data_stream_names_not_in_db',
        'machine_data_stream_names_not_on_disk',
        machine_family_data=MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAMS_CHECK_FULL_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAMS_CHECK_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAMS_CHECK_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamsCheck,
        'machine_data_stream_names_not_in_db',
        'machine_data_stream_names_not_on_disk',
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAMS_CHECK_STR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAMS_CHECK_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAMS_CHECK_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamsCheck,
        'machine_data_stream_names_not_in_db',
        'machine_data_stream_names_not_on_disk',
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAMS_CHECK_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAMS_CHECK_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAMS_CHECK_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamsCheck,
        'machine_data_stream_names_not_in_db',
        'machine_data_stream_names_not_on_disk',
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAMS_CHECK_ABBR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAMS_CHECK_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAMS_CHECK_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamsCheck,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAMS_CHECK_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAMS_CHECK_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PROFILE_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
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
        machine_family_data=MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PROFILE_FULL_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_QUERY_GRAPH = \
    ModelQueryGraph(
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
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
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
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PROFILE_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
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
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PROFILE_ABBR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PROFILE_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamProfile,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAM_PROFILE_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamPairCorr,
        'data_to_date',
        'corr',
        'n_samples',
        'machine_data_stream_range',
        'other_machine_data_stream_range',
        machine_family_data=MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        other_machine_data_stream=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_FULL_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamPairCorr,
        'data_to_date',
        'corr',
        'n_samples',
        'machine_data_stream_range',
        'other_machine_data_stream_range',
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        other_machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_STR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamPairCorr,
        'data_to_date',
        'corr',
        'n_samples',
        'machine_data_stream_range',
        'other_machine_data_stream_range',
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        other_machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamPairCorr,
        'data_to_date',
        'corr',
        'n_samples',
        'machine_data_stream_range',
        'other_machine_data_stream_range',
        machine_family_data=MACHINE_FAMILY_DATA_NAME_ONLY_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_ABBR_QUERY_GRAPH,
        other_machine_data_stream=MACHINE_DATA_STREAM_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_ABBR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamPairCorr,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_AGG_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
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
        machine_family_data=MACHINE_FAMILY_DATA_FULL_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_AGG_FULL_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_AGG_FULL_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_AGG_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamAgg,
        machine_family_data=MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_AGG_STR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_AGG_STR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamAgg,
        machine_family_data=MACHINE_FAMILY_DATA_STR_UNORDERED_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAM_AGG_STR_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_AGG_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamAgg,
        machine_family_data=MACHINE_FAMILY_DATA_ABBR_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_AGG_ABBR_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_AGG_ABBR_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_AGG_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamAgg,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_FAMILY_DATA_STREAM_AGG_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_AGG_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_DATA_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        'schema',
        machine=MACHINE_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_FULL_QUERY_SET = \
    MACHINE_DATA_FULL_QUERY_GRAPH.query_set()


MACHINE_DATA_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        'schema',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STR_QUERY_SET = \
    MACHINE_DATA_STR_QUERY_GRAPH.query_set()


MACHINE_DATA_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        'schema',
        machine=MACHINE_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_DATA_STR_UNORDERED_QUERY_SET = \
    MACHINE_DATA_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_DATA_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        'schema',
        machine=MACHINE_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_ABBR_QUERY_SET = \
    MACHINE_DATA_ABBR_QUERY_GRAPH.query_set()


MACHINE_DATA_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineData,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_DATA_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_DATA_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_AGG_FULL_QUERY_GRAPH = \
    ModelQueryGraph(
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
        machine=MACHINE_FULL_QUERY_GRAPH,
        machine_family_data_stream_agg=MACHINE_FAMILY_DATA_STREAM_AGG_FULL_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_AGG_FULL_QUERY_SET = \
    MACHINE_DATA_STREAM_AGG_FULL_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_AGG_STR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStreamAgg,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_family_data_stream_agg=MACHINE_FAMILY_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_AGG_STR_QUERY_SET = \
    MACHINE_DATA_STREAM_AGG_STR_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStreamAgg,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_family_data_stream_agg=MACHINE_FAMILY_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH,
        ORDER=False)

MACHINE_DATA_STREAM_AGG_STR_UNORDERED_QUERY_SET = \
    MACHINE_DATA_STREAM_AGG_STR_UNORDERED_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_AGG_ABBR_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStreamAgg,
        machine=MACHINE_NAME_ONLY_QUERY_GRAPH,
        machine_family_data_stream_agg=MACHINE_FAMILY_DATA_STREAM_AGG_ABBR_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_AGG_ABBR_QUERY_SET = \
    MACHINE_DATA_STREAM_AGG_ABBR_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_AGG_PK_ONLY_UNORDERED_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineDataStreamAgg,
        PK_FIELD_NAME,
        ORDER=False)

MACHINE_DATA_STREAM_AGG_PK_ONLY_UNORDERED_QUERY_SET = \
    MACHINE_DATA_STREAM_AGG_PK_ONLY_UNORDERED_QUERY_GRAPH.query_set()
