from django_model_query_graphs import ModelQueryGraph

from ...models import \
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
    MachineFamilyData, \
    MachineData, \
    MachineFamilyDataStreamProfile, \
    MachineFamilyDataStreamPairCorr

from ...queries import \
    PHYSICAL_DATA_TYPE_NAME_ONLY_QUERY_GRAPH

from ..field_names import \
    ENVIRONMENT_VARIABLE_API_FIELD_NAMES, \
    MEASUREMENT_UNIT_API_FIELD_NAMES, \
    MACHINE_CLASS_API_FIELD_NAMES, \
    LOCATION_API_FIELD_NAMES


ENVIRONMENT_VARIABLE_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        EnvironmentVariable,
        *ENVIRONMENT_VARIABLE_API_FIELD_NAMES,
        ORDER=True)

ENVIRONMENT_VARIABLE_REST_API_QUERY_SET = \
    ENVIRONMENT_VARIABLE_REST_API_QUERY_GRAPH.query_set()


PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        PhysicalDataType,
        'unique_name',
        'min',
        'max',
        'range',
        same=PHYSICAL_DATA_TYPE_NAME_ONLY_QUERY_GRAPH,
        ORDER=True)

PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_SET = \
    PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_GRAPH.query_set()


MEASUREMENT_UNIT_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MeasurementUnit,
        *MEASUREMENT_UNIT_API_FIELD_NAMES,
        ORDER=True)

MEASUREMENT_UNIT_REST_API_QUERY_SET = \
    MEASUREMENT_UNIT_REST_API_QUERY_GRAPH.query_set()


MACHINE_CLASS_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineClass,
        *MACHINE_CLASS_API_FIELD_NAMES,
        ORDER=True)

MACHINE_CLASS_REST_API_QUERY_SET = \
    MACHINE_CLASS_REST_API_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        'descriptions',
        machine_class=MACHINE_CLASS_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_COMPONENT_REST_API_QUERY_SET = \
    MACHINE_COMPONENT_REST_API_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH = \
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
        machine_class=MACHINE_CLASS_REST_API_QUERY_GRAPH,
        physical_data_type=PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_GRAPH,
        measurement_unit=MEASUREMENT_UNIT_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_REST_API_QUERY_SET = \
    MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH.query_set()


MACHINE_FAMILY_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'descriptions',
        'machine_data_filter_condition',
        machine_class=MACHINE_CLASS_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_REST_API_QUERY_SET = \
    MACHINE_FAMILY_REST_API_QUERY_GRAPH.query_set()


MACHINE_SKU_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        'descriptions',
        machine_class=MACHINE_CLASS_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_SKU_REST_API_QUERY_SET = \
    MACHINE_SKU_REST_API_QUERY_GRAPH.query_set()


MACHINE_COMPONENT_NESTED_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineComponent,
        'name',
        'descriptions',
        machine_class=MACHINE_CLASS_REST_API_QUERY_GRAPH,
        directly_interacting_components=MACHINE_COMPONENT_REST_API_QUERY_GRAPH,
        sub_components=MACHINE_COMPONENT_REST_API_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH,
        machine_skus=MACHINE_SKU_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_COMPONENT_NESTED_REST_API_QUERY_SET = \
    MACHINE_COMPONENT_NESTED_REST_API_QUERY_GRAPH.query_set()


MACHINE_DATA_STREAM_NESTED_REST_API_QUERY_GRAPH = \
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
        machine_class=MACHINE_CLASS_REST_API_QUERY_GRAPH,
        machine_components=MACHINE_COMPONENT_REST_API_QUERY_GRAPH,
        physical_data_type=PHYSICAL_DATA_TYPE_NESTED_REST_API_QUERY_GRAPH,
        measurement_unit=MEASUREMENT_UNIT_REST_API_QUERY_GRAPH,
        machine_skus=MACHINE_SKU_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_STREAM_NESTED_REST_API_QUERY_SET = \
    MACHINE_DATA_STREAM_NESTED_REST_API_QUERY_GRAPH.query_set()


MACHINE_FAMILY_NESTED_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamily,
        'unique_name',
        'descriptions',
        'machine_data_filter_condition',
        machine_skus=MACHINE_SKU_REST_API_QUERY_GRAPH,
        machine_components=MACHINE_COMPONENT_REST_API_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_NESTED_REST_API_QUERY_SET = \
    MACHINE_FAMILY_NESTED_REST_API_QUERY_GRAPH.query_set()


MACHINE_SKU_NESTED_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineSKU,
        'unique_name',
        'descriptions',
        machine_components=MACHINE_COMPONENT_REST_API_QUERY_GRAPH,
        machine_data_streams=MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH,
        machine_families=MACHINE_FAMILY_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_SKU_NESTED_REST_API_QUERY_SET = \
    MACHINE_SKU_NESTED_REST_API_QUERY_GRAPH.query_set()


LOCATION_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        *LOCATION_API_FIELD_NAMES,
        ORDER=True)

LOCATION_REST_API_QUERY_SET = \
    LOCATION_REST_API_QUERY_GRAPH.query_set()


MACHINE_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        Machine,
        'unique_id',
        'info',
        machine_class=MACHINE_CLASS_REST_API_QUERY_GRAPH,
        machine_sku=MACHINE_SKU_REST_API_QUERY_GRAPH,
        location=LOCATION_REST_API_QUERY_GRAPH,
        machine_families=MACHINE_FAMILY_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_REST_API_QUERY_SET = \
    MACHINE_REST_API_QUERY_GRAPH.query_set()


LOCATION_NESTED_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        Location,
        'unique_name',
        'descriptions',
        'info',
        machines=MACHINE_FAMILY_REST_API_QUERY_GRAPH,
        ORDER=True)

LOCATION_NESTED_REST_API_QUERY_SET = \
    LOCATION_NESTED_REST_API_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        'schema',
        machine=MACHINE_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_REST_API_QUERY_SET = \
    MACHINE_FAMILY_DATA_REST_API_QUERY_GRAPH.query_set()


MACHINE_DATA_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineData,
        'date',
        'url',
        'n_cols',
        'n_rows',
        'schema',
        machine=MACHINE_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_DATA_REST_API_QUERY_SET = \
    MACHINE_DATA_REST_API_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PROFILE_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamProfile,
        'data_to_date',
        'n_samples',
        'valid_fraction',
        'n_distinct_values',
        'distinct_value_proportions',
        'min',
        'robust_min',
        'quartile',
        'median',
        '_3rd_quartile',
        'robust_max',
        'max',
        machine_family_data=MACHINE_FAMILY_DATA_REST_API_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PROFILE_REST_API_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_REST_API_QUERY_GRAPH.query_set()


MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_REST_API_QUERY_GRAPH = \
    ModelQueryGraph(
        MachineFamilyDataStreamPairCorr,
        'data_to_date',
        'corr',
        'n_samples',
        'machine_data_stream_range',
        'other_machine_data_stream_range',
        machine_family_data=MACHINE_FAMILY_DATA_REST_API_QUERY_GRAPH,
        machine_data_stream=MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH,
        other_machine_data_stream=MACHINE_DATA_STREAM_REST_API_QUERY_GRAPH,
        ORDER=True)

MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_REST_API_QUERY_SET = \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_REST_API_QUERY_GRAPH.query_set()
