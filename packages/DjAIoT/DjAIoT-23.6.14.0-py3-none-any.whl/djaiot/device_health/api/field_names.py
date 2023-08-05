ENVIRONMENT_VARIABLE_API_FIELD_NAMES = \
    'key', \
    'value'


MACHINE_FAMILY_VITAL_DATA_STREAM_CONFIG_API_FIELD_NAMES = \
    'vital_machine_data_stream', \
    'vital_machine_data_stream_profile', \
    'high_corr_num_machine_data_streams', \
    'auto_incl_input_machine_data_streams', \
    'incl_input_machine_data_streams', \
    'low_corr_num_machine_data_streams', \
    'excl_input_machine_data_streams', \
    'active', \
    'comments'


MACHINE_FAMILY_HEALTH_SERVICE_CONFIG_API_FIELD_NAMES = \
    'machine_family', \
    'vital_and_incl_excl_machine_data_streams', \
    'incl_cat_input_machine_data_streams', \
    'active', \
    'from_date', \
    'to_date', \
    'configs', \
    'comments', \
    'updated'
    #MachineFamilyHealthServiceConfig._meta.FIELD_NAMES.USED_IN_QUERIES


AI_API_FIELD_NAMES = \
    'machine_family', \
    'ref_data_to_date', \
    'created', \
    'unique_id', \
    'active'   # , \
    # 'reference_evaluation_metrics'


MACHINE_FAMILY_VITAL_DATA_STREAM_AI_EVAL_METRIC_PROFILE_API_FIELD_NAMES = \
    'id', \
    'machine_family', \
    'machine_data_stream', \
    'ref_data_to_date', \
    'N', \
    'R2', \
    'MAE', \
    'MedAE', \
    'RMSE'


MACHINE_DAILY_RISK_SCORE_API_FIELD_NAMES = \
    ('id',) #+ \
    #MachineHealthRiskScore._meta.FIELD_NAMES.USED_IN_QUERIES


MACHINE_PROBLEM_DIAGNOSIS_API_FIELD_NAMES = \
    ('id',) #+ \
    #MachineHealthProblemDiagnosis._meta.FIELD_NAMES.USED_IN_STR_QUERIES

MACHINE_PROBLEM_DIAGNOSIS_NESTED_API_FIELD_NAMES = \
    ('id',) #+ \
    #MachineHealthProblemDiagnosis._meta.FIELD_NAMES.USED_IN_FULL_QUERIES


ALERT_API_FIELD_NAMES = \
    ('id',) #+ \
    #MachineHealthRiskAlert._meta.FIELD_NAMES.USED_IN_STR_QUERIES

ALERT_NESTED_API_FIELD_NAMES = \
    ('id',) #+ \
    #MachineHealthRiskAlert._meta.FIELD_NAMES.USED_IN_FULL_QUERIES


MACHINE_ERROR_CODE_API_FIELD_NAMES = \
    ('id',) #MachineErrorCode._meta.FIELD_NAMES.USED_IN_FULL_QUERIES


MACHINE_ERROR_API_FIELD_NAMES = \
    ('id',) #+ \
    #MachineError._meta.FIELD_NAMES.USED_IN_STR_QUERIES

MACHINE_ERROR_NESTED_API_FIELD_NAMES = \
    ('id',) #+ \
    #MachineError._meta.FIELD_NAMES.USED_IN_FULL_QUERIES
