ENVIRONMENT_VARIABLE_API_FIELD_NAMES = \
    'key', \
    'value'


PHYSICAL_DATA_TYPE_API_FIELD_NAMES = \
    'unique_name', \
    'min', \
    'max', \
    'range'

PHYSICAL_DATA_TYPE_NESTED_API_FIELD_NAMES = \
    'unique_name', \
    'min', \
    'max', \
    'range', \
    'same'


MEASUREMENT_UNIT_API_FIELD_NAMES = \
    'unique_name', \
    'descriptions'


MACHINE_CLASS_API_FIELD_NAMES = \
    'unique_name', \
    'descriptions'


MACHINE_COMPONENT_API_FIELD_NAMES = \
    'id', \
    'machine_class', \
    'name', \
    'descriptions'

MACHINE_COMPONENT_NESTED_API_FIELD_NAMES = \
    'id', \
    'machine_class', \
    'name', \
    'descriptions', \
    'directly_interacting_components', \
    'sub_components', \
    'machine_data_streams', \
    'machine_skus'


MACHINE_DATA_STREAM_API_FIELD_NAMES = \
    'id', \
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
    'range'

MACHINE_DATA_STREAM_NESTED_API_FIELD_NAMES = \
    'id', \
    'machine_class', \
    'machine_components', \
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
    'machine_skus'


MACHINE_FAMILY_API_FIELD_NAMES = \
    'machine_class', \
    'unique_name', \
    'descriptions', \
    'machine_data_filter_condition'

MACHINE_FAMILY_NESTED_API_FIELD_NAMES = \
    'machine_class', \
    'unique_name', \
    'descriptions', \
    'machine_data_filter_condition', \
    'machine_skus', \
    'machine_components', \
    'machine_data_streams'


MACHINE_SKU_API_FIELD_NAMES = \
    'machine_class', \
    'unique_name', \
    'descriptions'

MACHINE_SKU_NESTED_API_FIELD_NAMES = \
    'machine_class', \
    'unique_name', \
    'descriptions', \
    'machine_components', \
    'machine_data_streams', \
    'machine_families'


LOCATION_API_FIELD_NAMES = \
    'unique_name', \
    'descriptions', \
    'info'

LOCATION_NESTED_API_FIELD_NAMES = \
    'unique_name', \
    'descriptions', \
    'info', \
    'machines'


MACHINE_API_FIELD_NAMES = \
    'machine_class', \
    'machine_sku', \
    'unique_id', \
    'info', \
    'location', \
    'machine_families'


MACHINE_DAILY_DATA_SCHEMA_API_FIELD_NAMES = \
    'schema',


MACHINE_DAILY_DATA_API_FIELD_NAMES = \
    'id', \
    'machine', \
    'date', \
    'url', \
    'n_cols', \
    'n_rows'


MACHINE_FAMILY_DATA_STREAM_PROFILE_API_FIELD_NAMES = \
    'id', \
    'machine_family_data', \
    'machine_data_stream', \
    'data_to_date', \
    'n_samples', \
    'valid_fraction', \
    'n_distinct_values', \
    'distinct_value_proportions', \
    'min', \
    'robust_min', \
    'quartile', \
    'median', \
    '_3rd_quartile', \
    'robust_max', \
    'max'


MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_API_FIELD_NAMES = \
    'id', \
    'machine_family_data', \
    'data_to_date', \
    'machine_data_stream', \
    'other_machine_data_stream', \
    'corr', \
    'n_samples', \
    'machine_data_stream_range', \
    'other_machine_data_stream_range'
