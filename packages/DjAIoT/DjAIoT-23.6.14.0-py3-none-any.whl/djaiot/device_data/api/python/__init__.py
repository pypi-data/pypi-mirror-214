import matplotlib
matplotlib.use('Agg')

from plotnine import \
    ggplot, aes, geom_line, \
    scale_x_datetime, \
    ggtitle, element_text, theme

from collections import Counter
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
import logging
import numpy
import os
import pandas
from pathlib import Path
from psycopg2.extras import NumericRange
import pytz
import ray
import re
from ruamel import yaml
from scipy.stats import pearsonr
import sys
import tempfile
from tqdm import tqdm

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application
from django.db.models.query_utils import Q

from .util import parse_from_date_and_to_date

from ... import \
    LogicalDataTypeChoices, \
    PhysicalDataTypeMinChoices, PhysicalDataTypeMaxChoices, \
    MachineDataStreamTypeChoices

from .... import CONFIG_DIR_PATH
from ....util import _PARQUET_EXT, _YAML_EXT, OptionalStrType, snake_case, coerce_bool, coerce_float, coerce_int

from arimo.util.aws import key_pair, s3

from arimo.util.data_backend import chkRay, initRay

from infx.df.from_files import ArrowXDF
from infx.df.spark import SparkXDF
from infx.df.spark_from_files import ArrowSparkXDF

from arimo.util import Namespace, fs
from arimo.util.date_time import DATE_COL, month_end, month_str
from arimo.util.iterables import to_iterable
from arimo.util.log import STDOUT_HANDLER

from arimo.util.types.python import datetime

from arimo.util.types.arrow import \
    _ARROW_NULL_TYPE, \
    _ARROW_BOOL_TYPE, \
    _ARROW_STR_TYPE, \
    _ARROW_BINARY_TYPE, \
    uint8, int8, uint16, int16, uint32, int32, uint64, int64, \
    float16, float32, float64, \
    date32, \
    timestamp

from arimo.util.types.spark_sql import \
    _NULL_TYPE, \
    _BOOL_TYPE, \
    _STR_TYPE, \
    _BINARY_TYPE, \
    __byte_type as _byte_type, _TINYINT_TYPE, \
    __short_type as _short_type, _SMALLINT_TYPE, \
    __int_type as _int_type, _INT_TYPE, \
    __long_type as _long_type, _BIGINT_TYPE, \
    _FLOAT_TYPE, \
    _DOUBLE_TYPE, \
    __decimal_10_0_type as _decimal_10_0_type, _DECIMAL_10_0_TYPE, \
    __decimal_38_18_type as _decimal_38_18_type, _DECIMAL_38_18_TYPE, \
    _DATE_TYPE, \
    _TIMESTAMP_TYPE, \
    _array_signed_int_typecode_ctype_mappings, _array_unsigned_int_typecode_ctype_mappings, _array_type_mappings

import arimo.debug


os.makedirs(
    CONFIG_DIR_PATH,
    exist_ok=True)


class Client:
    _CONTROL_MACHINE_DATA_STREAM_TYPE_NAME = 'control'
    _SENSOR_MACHINE_DATA_STREAM_TYPE_NAME = 'sensor'
    _CALC_MACHINE_DATA_STREAM_TYPE_NAME = 'calc'
    _ALARM_MACHINE_DATA_STREAM_TYPE_NAME = 'alarm'

    _MACHINE_UNIQUE_ID_COL_NAME = 'equipment_instance_id'
    _LOCAL_DATE_TIME_COL_NAME = 'date_time'

    _INDEX_COL_NAMES = \
        {_MACHINE_UNIQUE_ID_COL_NAME,
         DATE_COL,
         _LOCAL_DATE_TIME_COL_NAME}

    _DEFAULT_PARAMS = \
        dict(
            api=dict(
                ENDPOINT_URL_ENVIRONMENT_VARIABLE_KEY='API_ENDPOINT_URL',
                endpoint_url=None,

                USER_ENVIRONMENT_VARIABLE_KEY='API_USER',
                user=None,

                PASSWORD_ENVIRONMENT_VARIABLE_KEY='API_PASSWORD',
                password=None),

            db=dict(
                host=None,
                user=None, password=None,
                db_name=None),

            s3=dict(
                BUCKET_NAME_ENVIRONMENT_VARIABLE_KEY='S3_BUCKET',
                bucket=None,

                ACCESS_KEY_ID_ENVIRONMENT_VARIABLE_KEY='AWS_ACCESS_KEY_ID',
                access_key_id=None,

                SECRET_ACCESS_KEY_ENVIRONMENT_VARIABLE_KEY='AWS_SECRET_ACCESS_KEY',
                secret_access_key=None,

                machine_data=dict(
                    raw_dir_prefix='.arimo/PredMaint/EquipmentData/raw',   # TODO: 'tmp/RawMachineData'
                    day_agg_dir_prefix='.arimo/PredMaint/EquipmentData/DailyAgg',   # TODO: 'tmp/DayAggMachineData'
                    machine_family_raw_dir_prefix='.arimo/PredMaint/EquipmentData/PreConso',   # TODO: 'tmp/MachineFamilyPreConsoData'
                    machine_family_conso_dir_prefix='.arimo/PredMaint/EquipmentData'   # TODO: 'tmp/MachineFamilyConsoData'
                )))
    
    _DAY_AGG_SUFFIXES = \
        Namespace(
            LIST='__dayList',

            COUNT_INCL_INVALID='__dayCountInclInvalid',
            DISTINCT_VALUE_COUNTS_INCL_INVALID='__dayDistinctValueCountsInclInvalid',
            DISTINCT_VALUE_PROPORTIONS_INCL_INVALID='__dayDistinctValueProportionsInclInvalid',

            COUNT_EXCL_INVALID='__dayCount',
            DISTINCT_VALUE_PROPORTIONS_EXCL_INVALID='__dayDistinctValueProportions',

            MIN='__dayMin', ROBUST_MIN='__dayRobustMin',
            QUARTILE='__dayQuartile',
            MEAN='__dayMean', MEDIAN='__dayMed',
            _3RD_QUARTILE='__day3rdQuartile',
            ROBUST_MAX='__dayRobustMax', MAX='__dayMax')

    _MAX_N_DISTINCT_VALUES_TO_PROFILE = 30

    _MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME = 10 ** 3

    # avoid django.db.utils.InternalError: invalid memory alloc request size 1073741824
    _DB_BULK_CREATE_OR_UPDATE_BATCH_SIZE = 10 ** 5

    def __init__(
            self, name='test', # TODO: /,
            *, params={}, **kwargs):
        self.name = name

        params.update(
            parse_config_file(
                path=os.path.join(
                        CONFIG_DIR_PATH,
                        name + _YAML_EXT)))
        self.params = Namespace(**self._DEFAULT_PARAMS)
        self.params.update(params, **kwargs)

        # docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        import_spec = \
            spec_from_file_location(
                name='settings',
                location=(Path(__file__)
                          .parent.parent.parent.parent.parent.parent
                          / 'settings.py'))
        infx_machine_intel_settings = module_from_spec(spec=import_spec)
        import_spec.loader.exec_module(module=infx_machine_intel_settings)

        django_db_settings = infx_machine_intel_settings.DATABASES['default']
        django_db_settings['HOST'] = self.params.db.HOST
        django_db_settings['ENGINE'] = self.params.db.ENGINE
        django_db_settings['USER'] = self.params.db.USER
        django_db_settings['PASSWORD'] = self.params.db.PASSWORD
        django_db_settings['NAME'] = self.params.db.NAME

        # Django 3: setting keys must be upper-case
        settings.configure(
            **{SETTING_KEY: setting_value
               for SETTING_KEY, setting_value in infx_machine_intel_settings.__dict__.items()
               if SETTING_KEY.isupper()})

        get_wsgi_application()

        for db_key in infx_machine_intel_settings.DATABASES:
            self.stdout_logger.info(
                msg='Migrating {} Database...'
                    .format(db_key.upper()))

            call_command(
                'migrate',
                database=db_key)

        from ...models import \
            EnvironmentVariable, \
            PhysicalDataType, MeasurementUnit, \
            MachineClass, \
            MachineComponent, MachineDataStream, \
            MachineFamily, MachineSKU, \
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

        from ....jobs.models import \
            MachineFamilyDataStreamsCheckingJob, \
            MachineFamilyDataStreamsProfilingJob, MachineFamilyDataStreamCorrsProfilingJob, \
            MachineFamilyDataAggJob, MachineFamilyDataAggsToDBJob

        self.db = \
            Namespace(
                EnvironmentVariables=EnvironmentVariable.objects,

                PhysicalDataTypes=PhysicalDataType.objects,
                MeasurementUnits=MeasurementUnit.objects,

                MachineClasses=MachineClass.objects,

                MachineComponents=MachineComponent.objects,
                MachineDataStreams=MachineDataStream.objects,

                MachineFamilies=MachineFamily.objects,
                MachineSKUs=MachineSKU.objects,

                MachineFamilyComponents=MachineFamilyComponent.objects,

                Locations=Location.objects,

                Machines=Machine.objects,

                MachineFamilyData=MachineFamilyData.objects,

                MachineFamilyDataStreamsChecks=MachineFamilyDataStreamsCheck.objects,

                MachineFamilyDataStreamProfiles=MachineFamilyDataStreamProfile.objects,
                MachineFamilyDataStreamPairCorrs=MachineFamilyDataStreamPairCorr.objects,

                MachineFamilyDataStreamAggs=MachineFamilyDataStreamAgg.objects,

                MachineData=MachineData.objects,

                MachineDataStreamAggs=MachineDataStreamAgg.objects,

                MachineFamilyDataStreamsCheckingJobs=MachineFamilyDataStreamsCheckingJob.objects,

                MachineFamilyDataStreamsProfilingJobs=MachineFamilyDataStreamsProfilingJob.objects,
                MachineFamilyDataStreamCorrsProfilingJobs=MachineFamilyDataStreamCorrsProfilingJob.objects,

                MachineFamilyDataAggJobs=MachineFamilyDataAggJob.objects,
                MachineFamilyDataAggsToDBJobs=MachineFamilyDataAggsToDBJob.objects)

        self._setup_logical_data_types()
        self._setup_physical_data_types()
        self._setup_machine_data_stream_types()

        if not self.params.s3.bucket:
            self.params.s3.bucket = \
                self.db.EnvironmentVariables.get_or_create(
                    key=self.params.s3.BUCKET_NAME_ENVIRONMENT_VARIABLE_KEY)[0].value

        if self.params.s3.bucket is not None:
            assert isinstance(self.params.s3.bucket, str) \
               and self.params.s3.bucket, \
                '*** S3 BUCKET = {} ***'.format(self.params.s3.bucket)

            if self.params.s3.access_key_id:
                assert self.params.s3.secret_access_key

            else:
                self.params.s3.access_key_id = \
                    self.db.EnvironmentVariables.get_or_create(
                        key=self.params.s3.ACCESS_KEY_ID_ENVIRONMENT_VARIABLE_KEY)[0].value

                if self.params.s3.access_key_id is not None:
                    self.params.s3.secret_access_key = \
                        self.db.EnvironmentVariables.get_or_create(
                            key=self.params.s3.SECRET_ACCESS_KEY_ENVIRONMENT_VARIABLE_KEY)[0].value

                    assert self.params.s3.secret_access_key is not None
                
                else:
                    self.params.s3.access_key_id, \
                    self.params.s3.secret_access_key = \
                        key_pair(profile='default')

            # if self.params.s3.access_key_id is None:
            #     warnings.warning(
            #         '*** AWS ACCESS KEY ID = {} ***'.format(self.params.s3.access_key_id))
            # else:
            #     assert isinstance(self.params.s3.access_key_id, _STR_CLASSES), \
            #         '*** AWS ACCESS KEY ID = {} ***'.format(self.params.s3.access_key_id)

            # if self.params.s3.secret_access_key is None:
            #     warnings.warning(
            #         '*** AWS SECRET ACCESS KEY = {} ***'.format(self.params.s3.secret_access_key))
            # else:
            #     assert isinstance(self.params.s3.secret_access_key, _STR_CLASSES), \
            #         '*** AWS SECRET ACCESS KEY = {} ***'.format(self.params.s3.secret_access_key)

            self.s3_client = \
                s3.client(
                    access_key_id=self.params.s3.access_key_id,
                    secret_access_key=self.params.s3.secret_access_key)

            self.params.s3.bucket_path = \
                's3://{}'.format(self.params.s3.bucket)

            self.params.s3.machine_data.raw_dir_path = \
                os.path.join(
                    self.params.s3.bucket_path,
                    self.params.s3.machine_data.raw_dir_prefix)

            self.params.s3.machine_data.day_agg_dir_path = \
                os.path.join(
                    self.params.s3.bucket_path,
                    self.params.s3.machine_data.day_agg_dir_prefix)

            self.params.s3.machine_data.machine_family_raw_dir_path = \
                os.path.join(
                    self.params.s3.bucket_path,
                    self.params.s3.machine_data.machine_family_raw_dir_prefix)

            self.params.s3.machine_data.machine_family_conso_dir_path = \
                os.path.join(
                    self.params.s3.bucket_path,
                    self.params.s3.machine_data.machine_family_conso_dir_prefix)

    def _setup_logical_data_types(self):
        self.CAT_LOGICAL_DATA_TYPE = LogicalDataTypeChoices.CAT

        self.NUM_ORDINAL_LOGICAL_DATA_TYPE = LogicalDataTypeChoices.NUM_ORD

        self.NUM_INTERVAL_OR_RATIO_LOGICAL_DATA_TYPE = LogicalDataTypeChoices.NUM_ITV_RAT

        self.NUM_LOGICAL_DATA_TYPES = \
            self.NUM_ORDINAL_LOGICAL_DATA_TYPE, \
            self.NUM_INTERVAL_OR_RATIO_LOGICAL_DATA_TYPE

    def _setup_physical_data_types(self):
        # NULL Type
        self.NA_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name='na',
                defaults=dict(
                            min=None,
                            max=None))

        self.NAN_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(numpy.nan),
                defaults=dict(
                            min=None,
                            max=None))

        self.NONE_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(None).lower(),
                defaults=dict(
                            min=None,
                            max=None))

        self.NULL_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(_ARROW_NULL_TYPE),
                defaults=dict(
                            min=None,
                            max=None))

        # Boolean Type
        self.BOOL_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(_ARROW_BOOL_TYPE),
                defaults=dict(
                            min=0,
                            max=1))

        self.BOOLEAN_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_BOOL_TYPE,
                defaults=dict(
                            min=0,
                            max=1))

        # String Type
        self.STR_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str.__name__,
                defaults=dict(
                            min=None,
                            max=None))

        self.STRING_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(_ARROW_STR_TYPE),
                defaults=dict(
                            min=None,
                            max=None))

        self.UNICODE_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name='unicode',
                defaults=dict(
                            min=None,
                            max=None))

        # Binary Type
        self.BINARY_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(_ARROW_BINARY_TYPE),
                defaults=dict(
                            min=None,
                            max=None))

        self.BYTEARRAY_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=bytearray.__name__,
                defaults=dict(
                            min=None,
                            max=None))

        # Integer Types
        self.BYTE_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_byte_type.typeName(),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT8,
                            max=PhysicalDataTypeMaxChoices.INT8))

        self.TINYINT_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_TINYINT_TYPE,
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT8,
                            max=PhysicalDataTypeMaxChoices.INT8))

        self.SHORT_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_short_type.typeName(),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT16,
                            max=PhysicalDataTypeMaxChoices.INT16))

        self.SMALLINT_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_SMALLINT_TYPE,
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT16,
                            max=PhysicalDataTypeMaxChoices.INT16))

        self.INTEGER_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_int_type.typeName(),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT32,
                            max=PhysicalDataTypeMaxChoices.INT32))

        self.INT_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_INT_TYPE,
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT32,
                            max=PhysicalDataTypeMaxChoices.INT32))

        self.LONG_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_long_type.typeName(),
                defaults=dict(
                            min=None,   # TODO: PhysicalDataTypeMinChoices.INT64
                            max=None    # TODO: PhysicalDataTypeMaxChoices.INT64
                            ))

        self.BIGINT_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_BIGINT_TYPE,
                defaults=dict(
                            min=None,   # TODO: PhysicalDataTypeMinChoices.INT64
                            max=None    # TODO: PhysicalDataTypeMaxChoices.INT64
                            ))

        self.UINT8_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(uint8()),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.ZERO,
                            max=PhysicalDataTypeMaxChoices.UINT8))

        self.INT8_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(int8()),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT8,
                            max=PhysicalDataTypeMaxChoices.INT8))

        self.UINT16_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(uint16()),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.ZERO,
                            max=PhysicalDataTypeMaxChoices.UINT16))

        self.INT16_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(int16()),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT16,
                            max=PhysicalDataTypeMaxChoices.INT16))

        self.UINT32_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(uint32()),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.ZERO,
                            max=PhysicalDataTypeMaxChoices.UINT32))

        self.INT32_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(int32()),
                defaults=dict(
                            min=PhysicalDataTypeMinChoices.INT32,
                            max=PhysicalDataTypeMaxChoices.INT32))

        self.UINT64_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(uint64()),
                defaults=dict(
                            min=None,   # TODO: PhysicalDataTypeMinChoices.ZERO,
                            max=None    # TODO: PhysicalDataTypeMaxChoices.UINT64
                            ))

        self.INT64_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(int64()),
                defaults=dict(
                            min=None,   # TODO: PhysicalDataTypeMinChoices.INT64,
                            max=None    # TODO: PhysicalDataTypeMaxChoices.INT64
                            ))

        # Float Types
        self.FLOAT_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_FLOAT_TYPE,
                defaults=dict(
                            min=None,
                            max=None))

        self.DOUBLE_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_DOUBLE_TYPE,
                defaults=dict(
                            min=None,
                            max=None))

        self.FLOAT16_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(float16()),
                defaults=dict(
                            min=None,
                            max=None))

        self.FLOAT32_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(float32()),
                defaults=dict(
                            min=None,
                            max=None))

        self.FLOAT64_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(float64()),
                defaults=dict(
                            min=None,
                            max=None))

        # Decimal Type
        self.DECIMAL_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_decimal_10_0_type.typeName(),
                defaults=dict(
                            min=None,
                            max=None))

        self.DECIMAL_10_0_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_DECIMAL_10_0_TYPE,
                defaults=dict(
                            min=None,
                            max=None))

        self.DECIMAL_38_18_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_DECIMAL_38_18_TYPE,
                defaults=dict(
                            min=None,
                            max=None))

        # Date Type
        self.DATE_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_DATE_TYPE,
                defaults=dict(
                            min=None,
                            max=None))

        self.DATE32_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(date32()),
                defaults=dict(
                            min=None,
                            max=None))

        # Timestamp Type
        self.DATETIME_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=datetime.__name__,
                defaults=dict(
                            min=None,
                            max=None))

        self.TIMESTAMP_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=_TIMESTAMP_TYPE,
                defaults=dict(
                            min=None,
                            max=None))

        self.TIMESTAMP_SECOND_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(timestamp(unit='s', tz=None)),
                defaults=dict(
                            min=None,
                            max=None))

        self.TIMESTAMP_MILLISECOND_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(timestamp(unit='ms', tz=None)),
                defaults=dict(
                            min=None,
                            max=None))

        self.TIMESTAMP_MICROSECOND_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(timestamp(unit='us', tz=None)),
                defaults=dict(
                            min=None,
                            max=None))

        self.TIMESTAMP_NANOSECOND_PHYSICAL_DATA_TYPE, _ = \
            self.db.PhysicalDataTypes.update_or_create(
                unique_name=str(timestamp(unit='ns', tz=None)),
                defaults=dict(
                            min=None,
                            max=None))

        # same types
        SAME_TYPE_COLLECTIONS = \
            [(self.NA_PHYSICAL_DATA_TYPE, self.NAN_PHYSICAL_DATA_TYPE, self.NONE_PHYSICAL_DATA_TYPE, self.NULL_PHYSICAL_DATA_TYPE),
             (self.BOOL_PHYSICAL_DATA_TYPE, self.BOOLEAN_PHYSICAL_DATA_TYPE),
             (self.STR_PHYSICAL_DATA_TYPE, self.STRING_PHYSICAL_DATA_TYPE, self.UNICODE_PHYSICAL_DATA_TYPE),
             (self.BINARY_PHYSICAL_DATA_TYPE, self.BYTEARRAY_PHYSICAL_DATA_TYPE),
             (self.BYTE_PHYSICAL_DATA_TYPE, self.TINYINT_PHYSICAL_DATA_TYPE, self.INT8_PHYSICAL_DATA_TYPE),
             (self.SHORT_PHYSICAL_DATA_TYPE, self.SMALLINT_PHYSICAL_DATA_TYPE, self.INT16_PHYSICAL_DATA_TYPE),
             (self.INT_PHYSICAL_DATA_TYPE, self.INTEGER_PHYSICAL_DATA_TYPE, self.INT32_PHYSICAL_DATA_TYPE),
             (self.INT_PHYSICAL_DATA_TYPE, self.LONG_PHYSICAL_DATA_TYPE, self.BIGINT_PHYSICAL_DATA_TYPE, self.INT64_PHYSICAL_DATA_TYPE),
             (self.FLOAT_PHYSICAL_DATA_TYPE, self.FLOAT32_PHYSICAL_DATA_TYPE),
             (self.FLOAT_PHYSICAL_DATA_TYPE, self.DOUBLE_PHYSICAL_DATA_TYPE, self.FLOAT64_PHYSICAL_DATA_TYPE),
             (self.DATE_PHYSICAL_DATA_TYPE, self.DATE32_PHYSICAL_DATA_TYPE),
             (self.DATETIME_PHYSICAL_DATA_TYPE, self.TIMESTAMP_PHYSICAL_DATA_TYPE, self.TIMESTAMP_MICROSECOND_PHYSICAL_DATA_TYPE),
             (self.DATETIME_PHYSICAL_DATA_TYPE, self.TIMESTAMP_PHYSICAL_DATA_TYPE, self.TIMESTAMP_NANOSECOND_PHYSICAL_DATA_TYPE)]

        int_type_code_ctype_mappings = _array_signed_int_typecode_ctype_mappings.copy()
        int_type_code_ctype_mappings.update(_array_unsigned_int_typecode_ctype_mappings)

        for int_type_code, ctype in int_type_code_ctype_mappings.items():
            SAME_TYPE_COLLECTIONS.append(
                (self.db.PhysicalDataTypes.get_or_create(
                    unique_name=int_type_code)[0],
                 self.db.PhysicalDataTypes.get_or_create(
                    unique_name=ctype.__name__[2:])[0]))

        for float_type_code, spark_sql_type in _array_type_mappings.items():
            if float_type_code.islower():
                SAME_TYPE_COLLECTIONS.append(
                    (self.db.PhysicalDataTypes.get_or_create(
                        unique_name=float_type_code)[0],
                     self.db.PhysicalDataTypes.get_or_create(
                        unique_name=spark_sql_type.typeName())[0],
                     self.db.PhysicalDataTypes.get_or_create(
                        unique_name=spark_sql_type().simpleString())[0]))

        for same_type_collection in SAME_TYPE_COLLECTIONS:
            for i, physical_data_type in enumerate(same_type_collection[:-1]):
                for same_physical_data_type in same_type_collection[(i + 1):]:
                    physical_data_type.same.add(same_physical_data_type)
                    same_physical_data_type.same.add(physical_data_type)

    def _setup_machine_data_stream_types(self):
        self.CONTROL_MACHINE_DATA_STREAM_TYPE = MachineDataStreamTypeChoices.CONTROL

        self.SENSOR_MACHINE_DATA_STREAM_TYPE = MachineDataStreamTypeChoices.SENSOR

        self.CALC_MACHINE_DATA_STREAM_TYPE = MachineDataStreamTypeChoices.CALC

        self.ALARM_MACHINE_DATA_STREAM_TYPE = MachineDataStreamTypeChoices.ALARM

    @classmethod
    def __qual_name__(cls):
        return '{}.{}'.format(
                cls.__module__,
                cls.__name__)

    def __repr__(self):
        return '{}{}'.format(
                '"{}" '.format(self.name)
                    if self.name
                    else '',
                self.__qual_name__())

    def __str__(self):
        return repr(self)

    @classmethod
    def class_logger(cls, *handlers, **kwargs):
        logger = logging.getLogger(name=cls.__qual_name__())

        level = kwargs.get('level')

        if level is None:
            level = logging.DEBUG \
                if arimo.debug.ON \
              else logging.INFO

        logger.setLevel(level)

        if kwargs.get('verbose'):
            handlers += (STDOUT_HANDLER,)

        for handler in handlers:
            logger.addHandler(handler)

        return logger

    @classmethod
    def class_stdout_logger(cls):
        return cls.class_logger(
                level=logging.DEBUG,
                verbose=True)

    def logger(self, *handlers, **kwargs):
        logger = logging.getLogger(name=str(self))

        level = kwargs.get('level')

        if level is None:
            level = logging.DEBUG \
                if arimo.debug.ON \
              else logging.INFO

        logger.setLevel(level)

        if kwargs.get('verbose'):
            handlers += (STDOUT_HANDLER,)

        for handler in handlers:
            logger.addHandler(handler)

        return logger

    @property
    def stdout_logger(self):
        return self.logger(
                level=logging.DEBUG,
                verbose=True)

    def update_measurement_units(self, measurement_unit_unique_names_and_descriptions, verbose=True):
        assert isinstance(measurement_unit_unique_names_and_descriptions, dict)

        measurement_units = {}

        for measurement_unit_unique_name, measurement_unit_descriptions in \
                measurement_unit_unique_names_and_descriptions.items():
            measurement_unit_unique_name = measurement_unit_unique_name.strip()

            measurement_units[measurement_unit_unique_name] = \
                measurement_unit = \
                self.db.MeasurementUnits.update_or_create(
                    unique_name=measurement_unit_unique_name,
                    defaults=dict(
                        descriptions=measurement_unit_descriptions))[0]

            if verbose:
                self.stdout_logger.info(
                    msg='{}: {}'.format(
                        measurement_unit,
                        measurement_unit.descriptions))

        return measurement_units

    def check_missing_machine_classes(self, machine_class_unique_names, verbose=True):
        missing_machine_class_unique_names = set()

        for machine_class_unique_name in machine_class_unique_names:
            machine_class_unique_name = snake_case(machine_class_unique_name)

            if not self.db.MachineClasses.filter(unique_name=machine_class_unique_name).first():
                if verbose:
                    self.stdout_logger.warning(
                        msg='*** MISSING Machine Class: {} ***'.format(
                            machine_class_unique_name))

                missing_machine_class_unique_names.add(machine_class_unique_name)

        return missing_machine_class_unique_names

    def update_machine_data_streams(self, machine_class_and_machine_data_stream_names_and_info, verbose=True):
        assert isinstance(machine_class_and_machine_data_stream_names_and_info, dict)

        machine_classes = {}
        machine_data_streams = {}
        physical_data_types = {}
        measurement_units = {}

        for (machine_class_unique_name, machine_data_stream_name), machine_data_stream_info in \
                machine_class_and_machine_data_stream_names_and_info.items():
            machine_class_unique_name = snake_case(machine_class_unique_name)

            if machine_class_unique_name not in machine_classes:
                machine_classes[machine_class_unique_name] = \
                    self.db.MachineClasses.get(
                        unique_name=machine_class_unique_name)

            machine_class = machine_classes[machine_class_unique_name]

            machine_data_stream_name = snake_case(machine_data_stream_name)

            control = machine_data_stream_info['control']

            machine_data_stream = \
                self.db.MachineDataStreams.filter(
                    machine_class=machine_class,
                    name=machine_data_stream_name) \
                .first()

            if machine_data_stream:
                if control:
                    if machine_data_stream.machine_data_stream_type != self.CONTROL_MACHINE_DATA_STREAM_TYPE:
                        machine_data_stream.machine_data_stream_type = self.CONTROL_MACHINE_DATA_STREAM_TYPE

                elif machine_data_stream.machine_data_stream_type == self.CONTROL_MACHINE_DATA_STREAM_TYPE:
                    machine_data_stream.machine_data_stream_type = self.SENSOR_MACHINE_DATA_STREAM_TYPE

            else:
                machine_data_stream, _ = \
                    self.db.MachineDataStreams.get_or_create(
                        machine_class=machine_class,
                        name=machine_data_stream_name,
                        machine_data_stream_type=
                            self.CONTROL_MACHINE_DATA_STREAM_TYPE
                            if control
                            else self.SENSOR_MACHINE_DATA_STREAM_TYPE)

            if 'physical_data_type_unique_name' in machine_data_stream_info:
                physical_data_type_unique_name = machine_data_stream_info['physical_data_type_unique_name'].strip()

                if physical_data_type_unique_name not in physical_data_types:
                    physical_data_types[physical_data_type_unique_name], _ = \
                        self.db.PhysicalDataTypes.get_or_create(
                            unique_name=physical_data_type_unique_name)

                machine_data_stream.physical_data_type = physical_data_types[physical_data_type_unique_name]

            if 'measurement_unit_unique_name' in machine_data_stream_info:
                measurement_unit_unique_name = machine_data_stream_info['measurement_unit_unique_name']

                if measurement_unit_unique_name:
                    measurement_unit_unique_name = measurement_unit_unique_name.strip()

                if measurement_unit_unique_name:
                    if measurement_unit_unique_name not in measurement_units:
                        measurement_units[measurement_unit_unique_name] = \
                            self.db.MeasurementUnits.get(
                                unique_name=measurement_unit_unique_name)

                    machine_data_stream.measurement_unit = measurement_units[measurement_unit_unique_name]

                else:
                    machine_data_stream.measurement_unit = None

            machine_data_stream.descriptions = machine_data_stream_info['descriptions']

            machine_data_stream.save()

            machine_data_streams[(machine_class_unique_name, machine_data_stream_name)] = machine_data_stream

            if verbose:
                self.stdout_logger.info(
                    msg='{}: {}'.format(
                        machine_data_stream,
                        machine_data_stream.descriptions))

        return machine_data_streams

    def _delete_machine_data_streams(
            self,
            machine_class_names, machine_data_stream_names):
        machine_classes = \
            self.db.MachineClasses.filter(
                unique_name__in=
                    {snake_case(machine_class_name)
                     for machine_class_name in to_iterable(machine_class_names)})

        machine_data_streams = \
            self.db.MachineDataStreams.filter(
                machine_class__in=machine_classes,
                name__in=
                    {snake_case(machine_data_stream_name)
                     for machine_data_stream_name in to_iterable(machine_data_stream_names)})

        self.stdout_logger.warning(
            msg='*** DELETED MachineFamilyDataStreamProfiles of {}: {} ***'.format(
                machine_data_streams,
                self.db.MachineFamilyDataStreamProfiles.filter(
                    machine_family__machine_class__in=machine_classes,
                    machine_data_stream__in=machine_data_streams)
                .delete()))

        self.stdout_logger.warning(
            msg='*** DELETED MachineFamilyDataStreamPairCorrs involving {}: {} ***'.format(
                machine_data_streams,
                self.db.MachineFamilyDataStreamPairCorrs.filter(
                    Q(machine_family__machine_class__in=machine_classes),
                    Q(machine_data_stream__in=machine_data_streams) |
                    Q(other_machine_data_stream__in=machine_data_streams))
                .delete()))

        self.stdout_logger.warning(
            msg='*** DELETING MachineFamilyDataStreamAggs involving {}... ***'
                .format(machine_data_streams))

        self.stdout_logger.info(
            msg='{}'.format(
                self.db.MachineFamilyDataStreamAggs.filter(
                    machine_family__machine_class__in=machine_classes,
                    machine_data_stream__in=machine_data_streams)
                .delete()))

        self.stdout_logger.warning(
            msg='*** DELETING MachineDataStreamAggs involving {}... ***'
                .format(machine_data_streams))

        self.stdout_logger.info(
            msg='{}'.format(
                self.db.MachineDataStreamAggs.filter(
                    machine__machine_class__in=machine_classes,
                    machine_data_stream__in=machine_data_streams)
                .delete()))

        self.stdout_logger.warning(
            msg='*** DELETED {}: {} ***'.format(
                machine_data_streams,
                machine_data_streams.delete()))

    def update_machine_skus(self, machine_class_and_machine_sku_unique_names_and_descriptions, verbose=True):
        assert isinstance(machine_class_and_machine_sku_unique_names_and_descriptions, dict)

        machine_classes = {}
        machine_skus = {}

        for (machine_class_unique_name, machine_sku_unique_name), machine_sku_descriptions in \
                machine_class_and_machine_sku_unique_names_and_descriptions.items():
            machine_class_unique_name = snake_case(machine_class_unique_name)

            if machine_class_unique_name in machine_classes:
                machine_class = machine_classes[machine_class_unique_name]

            else:
                machine_classes[machine_class_unique_name] = \
                    machine_class = \
                    self.db.MachineClasses.get(
                        unique_name=machine_class_unique_name)

            machine_sku_unique_name = snake_case(machine_sku_unique_name)

            machine_skus[(machine_class_unique_name, machine_sku_unique_name)] = \
                machine_sku = \
                self.db.MachineSKUs.update_or_create(
                    machine_class=machine_class,
                    unique_name=machine_sku_unique_name,
                    defaults=dict(
                        machine_class=machine_class,
                        descriptions=machine_sku_descriptions))[0]

            if verbose:
                self.stdout_logger.info(
                    msg='{}: {}'.format(
                        machine_sku,
                        machine_sku.descriptions))

        return machine_skus

    def update_machine_skus_machine_data_streams(
            self,
            machine_class_and_machine_sku_unique_names_and_machine_data_stream_names,
            verbose=True):
        assert isinstance(machine_class_and_machine_sku_unique_names_and_machine_data_stream_names, dict)

        machine_data_streams = {}
        machine_skus_and_machine_data_streams = {}

        for (machine_class_unique_name, machine_sku_unique_name), machine_data_stream_names in \
                tqdm(machine_class_and_machine_sku_unique_names_and_machine_data_stream_names.items()):
            machine_class_unique_name = snake_case(machine_class_unique_name)
            machine_sku_unique_name = snake_case(machine_sku_unique_name)

            try:
                machine_sku = \
                    self.db.MachineSKUs.get(
                        machine_class__unique_name=machine_class_unique_name,
                        unique_name=machine_sku_unique_name)

            except Exception as err:
                self.stdout_logger.error(
                    msg='{}: {}: *** {} ***'.format(
                        machine_class_unique_name,
                        machine_sku_unique_name,
                        err))

            existing_machine_sku_machine_data_streams = set(machine_sku.machine_data_streams.all())

            machine_sku_machine_data_streams = set()

            for machine_data_stream_name in machine_data_stream_names:
                machine_data_stream_name = snake_case(machine_data_stream_name)

                _tup = machine_class_unique_name, machine_data_stream_name
                
                if _tup in machine_data_streams:
                    machine_data_stream = machine_data_streams[_tup]

                else:
                    try:
                        machine_data_stream = \
                            self.db.MachineDataStreams.get(
                                machine_class__unique_name=machine_class_unique_name,
                                name=machine_data_stream_name)

                    except Exception as err:
                        self.stdout_logger.error(
                            msg='{}: {}: *** {} ***'.format(
                                machine_class_unique_name,
                                machine_data_stream_name,
                                err))

                    machine_data_streams[_tup] = machine_data_stream

                machine_sku_machine_data_streams.add(machine_data_stream)

            machine_sku.machine_data_streams.set(machine_sku_machine_data_streams)
            machine_sku.save()

            machine_skus_and_machine_data_streams[(machine_class_unique_name, machine_sku_unique_name)] = \
                machine_sku, machine_sku_machine_data_streams

            if verbose:
                added_machine_data_stream_names = \
                    sorted(
                        machine_data_stream.name
                        for machine_data_stream in
                            (machine_sku_machine_data_streams - existing_machine_sku_machine_data_streams))

                _added_machine_data_stream_names_str = \
                    '\n[+] Machine Data Streams ADDED: {}'.format(added_machine_data_stream_names) \
                    if added_machine_data_stream_names \
                    else ''

                removed_machine_data_stream_names = \
                    sorted(
                        machine_data_stream.name
                        for machine_data_stream in
                            (existing_machine_sku_machine_data_streams - machine_sku_machine_data_streams))

                _removed_machine_data_stream_names_str = \
                    '\n[-] Machine Data Streams REMOVED: {}'.format(removed_machine_data_stream_names) \
                    if removed_machine_data_stream_names \
                    else ''

                if _added_machine_data_stream_names_str or _removed_machine_data_stream_names_str:
                    self.stdout_logger.info(
                        msg='{}:{}{}'.format(
                            machine_sku,
                            _added_machine_data_stream_names_str,
                            _removed_machine_data_stream_names_str))

        return machine_skus_and_machine_data_streams

    def update_locations(self, location_unique_names_and_info, verbose=True):
        assert isinstance(location_unique_names_and_info, dict)

        locations = {}

        for location_unique_name, location_info in \
                tqdm(location_unique_names_and_info.items()):
            locations[location_unique_name] = \
                location = \
                    self.db.Locations.update_or_create(
                        unique_name=location_unique_name,
                        defaults=dict(
                            info=location_info))[0]

            if verbose:
                self.stdout_logger.info(
                    msg='{}: {}'.format(
                        location, location.info))

        return locations

    def update_machines(self, machine_unique_ids_and_info):
        assert isinstance(machine_unique_ids_and_info, dict)

        machine_classes = {}
        machine_skus = {}
        locations = {}
        machines = {}

        for machine_unique_id, machine_info in tqdm(machine_unique_ids_and_info.items()):
            machine_class_unique_name = snake_case(machine_info['machine_class_unique_name'])

            if machine_class_unique_name not in machine_classes:
                machine_classes[machine_class_unique_name] = \
                    self.db.MachineClasses.get(
                        unique_name=machine_class_unique_name)

            machine_class = machine_classes[machine_class_unique_name]

            machine_sku_unique_name = snake_case(machine_info['machine_sku_unique_name'])

            if machine_sku_unique_name:
                _tup = machine_class_unique_name, machine_sku_unique_name

                if _tup not in machine_skus:
                    machine_skus[_tup] = \
                        self.db.MachineSKUs.get(
                            machine_class=machine_class,
                            unique_name=machine_sku_unique_name)

                machine_sku = machine_skus[_tup]

            else:
                machine_sku = None

            machine_unique_id = snake_case(machine_unique_id)

            location_unique_name = snake_case(machine_info['location_unique_name'])

            if location_unique_name:
                if location_unique_name not in locations:
                    locations[location_unique_name] = \
                        self.db.Locations.get(
                            unique_name=location_unique_name)

                location = locations[location_unique_name]

            else:
                location = None

            machines[machine_unique_id] = \
                self.db.Machines.update_or_create(
                    unique_id=machine_unique_id,
                    defaults=dict(
                        machine_class=machine_class,
                        machine_sku=machine_sku,
                        info=machine_info['info'],
                        location=location))[0]

        return machines

    def update_machine_families_machine_skus(
            self, machine_class_and_machine_family_unique_names_and_machine_sku_unique_names,
            verbose=True):
        assert isinstance(machine_class_and_machine_family_unique_names_and_machine_sku_unique_names, dict)

        machine_classes = {}
        machine_skus = {}
        machine_families_and_machine_skus_to_add_or_remove = {}

        for (machine_class_unique_name, machine_family_unique_name), machine_sku_unique_names in \
                machine_class_and_machine_family_unique_names_and_machine_sku_unique_names.items():
            machine_class_unique_name = snake_case(machine_class_unique_name)

            if machine_class_unique_name not in machine_classes:
                machine_classes[machine_class_unique_name] = \
                    self.db.MachineClasses.get(
                        unique_name=machine_class_unique_name)

            machine_class = machine_classes[machine_class_unique_name]

            machine_family_machine_skus = set()

            for machine_sku_unique_name in machine_sku_unique_names:
                machine_sku_unique_name = snake_case(machine_sku_unique_name)

                _tup = machine_class_unique_name, machine_sku_unique_name

                if _tup not in machine_skus:
                    try:
                        machine_skus[_tup] = \
                            self.db.MachineSKUs.get(
                                machine_class=machine_class,
                                unique_name=machine_sku_unique_name)

                    except Exception as err:
                        self.stdout_logger.error(
                            msg='{}: {}: *** {} ***'.format(
                                machine_class_unique_name,
                                machine_sku_unique_name,
                                err))

                machine_family_machine_skus.add(machine_skus[_tup])

            machine_family_unique_name = snake_case(machine_family_unique_name)

            machine_family, _ = \
                self.db.MachineFamilies.get_or_create(
                    machine_class=machine_class,
                    unique_name=machine_family_unique_name)

            existing_machine_family_machine_skus = set(machine_family.machine_skus.all())

            machine_families_and_machine_skus_to_add_or_remove[
                    (machine_class_unique_name, machine_family_unique_name)] = \
                machine_family_machine_skus_to_add_or_remove = {}

            machine_sku_unique_names_to_add = \
                sorted(
                    machine_sku.unique_name
                    for machine_sku in (machine_family_machine_skus - existing_machine_family_machine_skus))

            if machine_sku_unique_names_to_add:
                machine_family_machine_skus_to_add_or_remove['add'] = machine_sku_unique_names_to_add

            machine_sku_unique_names_to_remove = \
                sorted(
                    machine_sku.unique_name
                    for machine_sku in (existing_machine_family_machine_skus - machine_family_machine_skus))

            if machine_sku_unique_names_to_remove:
                machine_family_machine_skus_to_add_or_remove['remove'] = machine_sku_unique_names_to_remove

            if machine_family_machine_skus_to_add_or_remove:
                if verbose:
                    self.stdout_logger.info(
                        msg='{}:{}{}'.format(
                            machine_family,
                            '\n[+] Machine SKUs to ADD: {}'.format(machine_sku_unique_names_to_add)
                                if machine_sku_unique_names_to_add
                                else '',
                            '\n[-] Machine SKUs to REMOVE: {}'.format(machine_sku_unique_names_to_remove)
                                if machine_sku_unique_names_to_remove
                                else ''))

                machine_family.machine_skus.set(machine_family_machine_skus)

        return machine_families_and_machine_skus_to_add_or_remove

    def update_machine_families_machines(
            self, machine_class_and_machine_family_unique_names_and_machine_unique_ids):
        assert isinstance(machine_class_and_machine_family_unique_names_and_machine_unique_ids, dict)

        machine_classes = {}

        for (machine_class_unique_name, machine_family_unique_name), machine_unique_ids in \
                machine_class_and_machine_family_unique_names_and_machine_unique_ids.items():
            machine_class_unique_name = snake_case(machine_class_unique_name)

            if machine_class_unique_name not in machine_classes:
                machine_classes[machine_class_unique_name] = \
                    self.db.MachineClasses.get(
                        unique_name=machine_class_unique_name)

            machine_class = machine_classes[machine_class_unique_name]

            machine_family_unique_name = snake_case(machine_family_unique_name)

            machine_family, _ = \
                self.db.MachineFamilies.get_or_create(
                    machine_class=machine_class,
                    unique_name=machine_family_unique_name)

            machines = self.db.Machines.filter(unique_id__in=machine_unique_ids)

            machine_family.machines.set(machines)

    def machine_class(self, machine_class_name, create=False):
        unique_name = snake_case(machine_class_name)

        return self.db.MachineClasses.get_or_create(unique_name=unique_name)[0] \
            if create \
          else self.db.MachineClasses.get(unique_name=unique_name)

    def machine_family(self, machine_family_name, create=False, machine_class_name=None):
        unique_name = snake_case(machine_family_name)

        return self.db.MachineFamilies.get_or_create(
                machine_class=self.machine_class(machine_class_name=machine_class_name),
                unique_name=unique_name)[0] \
            if create \
          else self.db.MachineFamilies.get(unique_name=unique_name)

    def filter_machine_family(
            self,
            from_machine_family_name: str, to_machine_family_name: str,
            additional_machine_data_filter_condition: str) -> None:
        from_machine_family = \
            self.machine_family(
                machine_family_name=from_machine_family_name,
                create=False)

        machine_class_name = from_machine_family.machine_class.unique_name

        to_machine_family = \
            self.machine_family(
                machine_family_name=to_machine_family_name,
                create=True,
                machine_class_name=machine_class_name)

        to_machine_family.filtered_from_machine_family = from_machine_family
        to_machine_family.machine_data_filter_condition = additional_machine_data_filter_condition
        to_machine_family.save()

    def machine_sku(self, machine_sku_name, create=False, machine_class_name=None):
        unique_name = snake_case(machine_sku_name)

        return self.db.MachineSKUs.get_or_create(
                machine_class=self.machine_class(
                                machine_class_name=machine_class_name,
                                create=True),
                unique_name=unique_name)[0] \
            if create \
          else self.db.MachineSKUs.get(unique_name=unique_name)

    def copy_machine_family_components(
            self,
            machine_class_name,
            from_machine_family_name,
            to_machine_family_name):
        from_machine_family = \
            self.machine_family(
                machine_family_name=from_machine_family_name,
                create=True,
                machine_class_name=machine_class_name)

        to_machine_family = \
            self.machine_family(
                machine_family_name=to_machine_family_name,
                create=True,
                machine_class_name=machine_class_name)

        from_machine_family_components = \
            from_machine_family.machine_family_components.all()

        for from_machine_family_component in \
                tqdm(from_machine_family_components,
                     total=from_machine_family_components.count()):
            to_machine_family_component, _ = \
                self.db.MachineFamilyComponents.get_or_create(
                    machine_family=to_machine_family,
                    machine_component=from_machine_family_component.machine_component)

            to_machine_family_component.directly_interacting_components.add(
                *(self.db.MachineFamilyComponents.get_or_create(
                    machine_family=to_machine_family,
                    machine_component=directly_interacting_component.machine_component)[0]
                  for directly_interacting_component in from_machine_family_component.directly_interacting_components.all()))

            to_machine_family_component.sub_components.add(
                *(self.db.MachineFamilyComponents.get_or_create(
                    machine_family=to_machine_family,
                    machine_component=sub_component.machine_component)[0]
                  for sub_component in from_machine_family_component.sub_components.all()))

            to_machine_family_component.machine_data_streams.add(
                *from_machine_family_component.machine_data_streams.all())

            self.stdout_logger.info(
                msg='{}'.format(to_machine_family_component))

    def machine_data_stream(self, machine_class_name, machine_data_stream_name, create=False):
        machine_class = self.machine_class(machine_class_name)

        machine_data_stream_name = snake_case(machine_data_stream_name)

        return self.db.MachineDataStreams.get_or_create(
                machine_class=machine_class,
                name=machine_data_stream_name)[0] \
            if create \
          else self.db.MachineDataStreams.get(
                machine_class=machine_class,
                name=machine_data_stream_name)

    def update_or_create_machine(
            self, machine_class_name, machine_unique_id, machine_sku_name=None, create=False,
            **kwargs):
        if machine_sku_name:
            kwargs['machine_sku'] = \
                self.machine_sku(
                    machine_sku_name=machine_sku_name,
                    create=create,
                    machine_class_name=machine_class_name)

        try:
            return self.db.Machines.update_or_create(
                    machine_class=self.machine_class(
                                    machine_class_name=machine_class_name,
                                    create=create),
                    unique_id=snake_case(str(machine_unique_id)),
                    defaults=kwargs)[0]

        except Exception as err:
            self.stdout_logger.error(
                msg='*** {} #{}: {} ***'
                    .format(machine_class_name, machine_unique_id, err))

    def machine(self, machine_unique_id):
        return self.db.Machines.get(
                unique_id=snake_case(str(machine_unique_id)))

    def load_machine_data(
            self, machine_unique_id_or_data_set_name, machine_family_conso=True,
            _from_files=True, _spark=False,
            set_i_col=True, set_t_col=True,
            verbose=True, **kwargs):
        path = os.path.join(
                    self.params.s3.machine_data.machine_family_conso_dir_path,
                    machine_unique_id_or_data_set_name + _PARQUET_EXT) \
            if machine_family_conso \
            else os.path.join(
                    self.params.s3.machine_data.raw_dir_path,
                    '{}={}'.format(self._MACHINE_UNIQUE_ID_COL_NAME, machine_unique_id_or_data_set_name))

        xdf = (ArrowSparkXDF(
                    path=path, mergeSchema=True,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=self._MACHINE_UNIQUE_ID_COL_NAME
                         if set_i_col
                         else None,
                    tCol=self._LOCAL_DATE_TIME_COL_NAME
                         if set_t_col
                         else None,
                    verbose=verbose,
                    **kwargs)
               if _spark
               else ArrowXDF(
                    path=path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=self._MACHINE_UNIQUE_ID_COL_NAME
                         if set_i_col
                         else None,
                    tCol=self._LOCAL_DATE_TIME_COL_NAME
                         if set_t_col
                         else None,
                    verbose=verbose,
                    **kwargs)) \
            if _from_files \
            else SparkXDF.load(
                    path=path,
                    format='parquet', mergeSchema=True,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=self._MACHINE_UNIQUE_ID_COL_NAME
                         if set_i_col
                         else None,
                    tCol=self._LOCAL_DATE_TIME_COL_NAME
                         if set_t_col
                         else None,
                    verbose=verbose,
                    **kwargs)

        assert self._INDEX_COL_NAMES.issubset(xdf.columns)

        return xdf

    def machine_family_conventional_full_name(
            self,
            machine_class_name,
            machine_family_name):
        return '{}---{}'.format(
                machine_class_name.upper(),
                machine_family_name)

    def conso_machine_family_data_file_paths(
            self,
            machine_class_name, machine_family_name,
            date, to_date=None,
            shutdown_ray=False,
            _force_re_conso=False,
            verbose=False):
        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        machine_data_paths = \
            {i['unique_id']:
                os.path.join(
                    self.params.s3.machine_data.raw_dir_path,
                    '{}={}'.format(self._MACHINE_UNIQUE_ID_COL_NAME, i['unique_id']))
             for i in machine_family.machines.all().values('unique_id')}

        machine_family_data_set_name = \
            self.machine_family_conventional_full_name(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name)

        machine_family_raw_data_dir_path = \
            os.path.join(
                self.params.s3.machine_data.machine_family_raw_dir_path,
                machine_family_data_set_name + _PARQUET_EXT)

        if not chkRay():
            initRay(verbose=False)

        @ray.remote(
            num_return_vals=None,
                # This is only for remote functions.
                # It specifies the number of object IDs returned by the remote function invocation.

            num_cpus=1,
                # The quantity of CPU cores to reserve for this task or for the lifetime of the actor

            num_gpus=0,
                # The quantity of GPUs to reserve for this task or for the lifetime of the actor

            resources=None,
                # The quantity of various custom resources to reserve for this task or for the lifetime of the actor.
                # This is a dictionary mapping strings (resource names) to numbers.

            max_calls=1,
                # Only for remote functions.
                # This specifies the maximum number of times that a given worker can execute
                # the given remote function before it must exit
                # (this can be used to address memory leaks in third-party libraries or to reclaim resources
                # that cannot easily be released, e.g., GPU memory that was acquired by TensorFlow).
                # By default this is infinite.

            # max_reconstructions=0,   # The keyword 'max_reconstructions' is not allowed for remote functions
                # Only for actors.
                # This specifies the maximum number of times that the actor should be reconstructed when it dies unexpectedly.
                # The minimum valid value is 0 (default), which indicates that the actor doesn’t need to be reconstructed.
                # And the maximum valid value is ray.ray_constants.INFINITE_RECONSTRUCTIONS.
        )
        def s3_sync_task(
                machine_unique_id, machine_data_path, date_str,
                _machine_unique_id_col_name=self._MACHINE_UNIQUE_ID_COL_NAME,
                _access_key_id=self.params.s3.access_key_id,
                _secret_access_key=self.params.s3.secret_access_key):
            _date_partition_str = \
                '{}={}'.format(DATE_COL, date_str)

            machine_family_raw_data_dir_path_for_date = \
                os.path.join(
                    machine_family_raw_data_dir_path,
                    _date_partition_str)

            s3.sync(
                from_dir_path=
                    os.path.join(
                        machine_data_path,
                        _date_partition_str),
                to_dir_path=
                    os.path.join(
                        machine_family_raw_data_dir_path_for_date,
                        '{}={}'.format(_machine_unique_id_col_name, machine_unique_id)),
                delete=True,
                quiet=True,
                access_key_id=_access_key_id,
                secret_access_key=_secret_access_key,
                verbose=verbose)

        for _date in (tqdm(pandas.date_range(start=date, end=to_date).date)
                      if to_date
                      else (date,)):
            date_str = str(_date)   # avoid inefficient pickling of date-time objects

            msg = 'Consolidating {} Data File Paths for {}...'.format(machine_family_data_set_name, _date)
            self.stdout_logger.info(msg)

            ray.get(
                [s3_sync_task.remote(
                    machine_unique_id=machine_unique_id,
                    machine_data_path=machine_data_path,
                    date_str=date_str)
                 for machine_unique_id, machine_data_path in tqdm(machine_data_paths.items())])
            
            self.stdout_logger.info(msg + ' done!')

        if shutdown_ray:
            ray.shutdown()

    def conso_machine_family_data(
            self,
            machine_class_name, machine_family_name,
            date, to_date=None,
            _force_re_conso=False):
        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        machine_family_data_set_name = \
            self.machine_family_conventional_full_name(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name) \
            + _PARQUET_EXT

        machine_family_raw_data_dir_prefix = \
            os.path.join(
                self.params.s3.machine_data.machine_family_raw_dir_prefix,
                machine_family_data_set_name)

        machine_family_raw_data_dir_path = \
            os.path.join(
                self.params.s3.machine_data.machine_family_raw_dir_path,
                machine_family_data_set_name)

        machine_family_conso_data_dir_prefix = \
            os.path.join(
                self.params.s3.machine_data.machine_family_conso_dir_prefix,
                machine_family_data_set_name)

        machine_family_conso_data_dir_path = \
            os.path.join(
                self.params.s3.machine_data.machine_family_conso_dir_path,
                machine_family_data_set_name)

        for _date in (tqdm(pandas.date_range(start=date, end=to_date).date)
                      if to_date
                      else (date,)):
            _date_partition_str = \
                '{}={}'.format(DATE_COL, _date)

            machine_family_conso_data_dir_prefix_for_date = \
                os.path.join(
                    machine_family_conso_data_dir_prefix,
                    _date_partition_str)

            if _force_re_conso or \
                    ('Contents' not in
                        self.s3_client.list_objects_v2(
                            Bucket=self.params.s3.bucket,
                            Prefix=machine_family_conso_data_dir_prefix_for_date)):
                machine_family_raw_data_dir_prefix_for_date = \
                    os.path.join(
                        machine_family_raw_data_dir_prefix,
                        _date_partition_str)

                if _force_re_conso or \
                        ('Contents' not in
                            self.s3_client.list_objects_v2(
                                Bucket=self.params.s3.bucket,
                                Prefix=machine_family_raw_data_dir_prefix_for_date)):
                    self.conso_machine_family_data_file_paths(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name,
                        date=_date, to_date=None,
                        shutdown_ray=False)

                if 'Contents' in \
                        self.s3_client.list_objects_v2(
                            Bucket=self.params.s3.bucket,
                            Prefix=machine_family_raw_data_dir_prefix_for_date):
                    SparkXDF._consoParquet(
                        os.path.join(
                            machine_family_conso_data_dir_path,
                            _date_partition_str),
                        os.path.join(
                            machine_family_raw_data_dir_path,
                            _date_partition_str),
                        aws_access_key_id=self.params.s3.access_key_id,
                        aws_secret_access_key=self.params.s3.secret_access_key,
                        filter=machine_family.machine_data_full_filter_condition,
                        partitionBy=None,
                        restartSpark=False)

    @lru_cache(maxsize=None, typed=False)
    def load_machine_family_data(
            self, machine_class_name, machine_family_name,
            _from_files=True, _spark=False,
            set_i_col=True, set_t_col=True,
            verbose=True, **kwargs):
        return self.load_machine_data(
                machine_unique_id_or_data_set_name=
                    self.machine_family_conventional_full_name(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name),
                machine_family_conso=True,
                _from_files=_from_files, _spark=_spark,
                set_i_col=set_i_col, set_t_col=set_t_col,
                verbose=verbose, **kwargs)

    def filter_machine_family_data(
            self, machine_class_name: str, from_machine_family_name: str, to_machine_family_name: str,
            date: str, to_date: str = None, monthly=False):
        from_machine_family_arrow_spark_xdf = \
            self.load_machine_family_data(
                machine_class_name=machine_class_name,
                machine_family_name=from_machine_family_name,
                _from_files=True, _spark=True,
                set_i_col=False, set_t_col=False,
                verbose=True) \
            .filterPartitions(
                (DATE_COL,
                 date,
                 to_date)
                if to_date
                else (DATE_COL,
                      date))

        date, to_date = \
            parse_from_date_and_to_date(
                from_date=date,
                to_date=to_date)

        to_machine_family = \
            self.machine_family(
                machine_family_name=to_machine_family_name,
                create=False)

        filter_condition = to_machine_family.machine_data_full_filter_condition
        assert filter_condition

        to_s3_dir_path = \
            os.path.join(
                self.params.s3.machine_data.machine_family_conso_dir_path,
                self.machine_family_conventional_full_name(
                    machine_class_name=machine_class_name,
                    machine_family_name=to_machine_family_name)
                + _PARQUET_EXT)

        for _date in tqdm(pandas.date_range(start=date, end=to_date).date):
            try:
                from_machine_family_arrow_spark_xdf_for_date = \
                    from_machine_family_arrow_spark_xdf.filterPartitions(
                        (DATE_COL,
                         _date))

            except Exception as err:
                self.stdout_logger.warning(
                    msg='*** CANNOT LOAD DATA FOR FOR {}: {} ***'
                        .format(_date, err))

                continue

            from_machine_family_arrow_spark_xdf_for_date \
            .filter(condition=filter_condition) \
            .repartition(1) \
            .save(
                path=os.path.join(
                        to_s3_dir_path,
                        '{}={}'.format(
                            DATE_COL,
                            _date)),
                format='parquet',
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=True)

    def register_machine_family_data(
            self,
            machine_class_name: str, machine_family_name: str,
            date: OptionalStrType = None, to_date: OptionalStrType = None) \
            -> None:
        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        machine_family_arrow_xdf = \
            self.load_machine_family_data(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name,
                _from_files=True, _spark=False,
                set_i_col=True, set_t_col=True)

        machine_family_data_path = machine_family_arrow_xdf.path

        schema = \
            {col_name: str(col_type)
             for col_name, col_type in machine_family_arrow_xdf.srcTypesInclPartitionKVs.items()
             if col_name not in self._INDEX_COL_NAMES}

        n_cols = len(machine_family_arrow_xdf.contentCols)

        assert len(schema) == n_cols, \
            ValueError(f'*** {machine_family_data_path}: {n_cols} != No. of Columns of {schema} ***')

        # if Machine Family Data does not yet exist, then create
        machine_family_data, machine_family_data_created = \
            self.db.MachineFamilyData.get_or_create(
                machine_family=machine_family,
                date=None,
                n_rows=None,
                defaults=dict(
                            url=machine_family_data_path,
                            schema=schema,
                            n_cols=n_cols))

        if machine_family_data_created:
            # to re-register entire Machine Family Data for all dates
            date = to_date = None

            to_update_machine_family_data_again = False

        else:
            existing_schema = machine_family_data.schema

            # check if schema has changed
            changed_schema_items = \
                dict(set(schema.items())
                    .difference(existing_schema.items()))

            if changed_schema_items:
                to_update_machine_family_data_again = True

                self.stdout_logger.info(
                    msg=f'To Re-Register Machine Family Data for {machine_family} '
                        f'to Account for Changed Schema Items {changed_schema_items}...')

                # check if schema has changed inconsistently
                if set(changed_schema_items).intersection(existing_schema):
                    # to re-register entire Machine Family Data for all dates
                    date = to_date = None

            else:
                to_update_machine_family_data_again = \
                    (machine_family_data_path != machine_family_data.url)

        if date:
            date, to_date = \
                parse_from_date_and_to_date(
                    from_date=date,
                    to_date=to_date)

            machine_family_arrow_xdf = \
                machine_family_arrow_xdf.filterPartitions(
                    (DATE_COL,
                     date,
                     to_date)
                    if to_date
                    else (DATE_COL,
                          date))

        else:
            assert not to_date

        for piece_path in tqdm(machine_family_arrow_xdf.piecePaths):
            date = re.search(f'{DATE_COL}=(.*?)/', piece_path).group(1)

            piece_cache = \
                machine_family_arrow_xdf._read_metadata_and_schema(
                    piecePath=piece_path)

            daily_schema = \
                {col_name: str(col_type)
                 for col_name, col_type in piece_cache.srcTypesExclPartitionKVs.items()
                 if col_name not in self._INDEX_COL_NAMES}

            daily_n_cols = piece_cache.nCols - 2

            assert len(daily_schema) == daily_n_cols, \
                ValueError(f'*** {piece_path}: {daily_n_cols} != No. of Columns of {daily_schema} ***')

            new_schema_items = \
                dict(set(daily_schema.items())
                    .difference(schema.items()))

            if new_schema_items:
                to_update_machine_family_data_again = True

                self.stdout_logger.info(
                    msg=f'Re-Registering Machine Family Data for {machine_family} '
                        f'to Account for New Schema Items {new_schema_items} ({date})...')

                for col_name, col_type in new_schema_items.items():
                    assert col_name not in schema, \
                        ValueError(f'*** {date} ALREADY IN {schema} ***')

                    schema[col_name] = col_type
                    n_cols += 1

            machine_family_daily_data, _ = \
                self.db.MachineFamilyData.update_or_create(
                    machine_family=machine_family,
                    date=date,
                    defaults=dict(
                                url=piece_path,
                                schema=daily_schema,
                                n_cols=daily_n_cols,
                                n_rows=piece_cache.nRows))

        if to_update_machine_family_data_again:
            self.stdout_logger.info(
                msg=f'Re-Registering Machine Family Data for {machine_family}...')

            assert len(schema) == n_cols, \
                ValueError(f'*** {machine_family_data_path}: {n_cols} != No. of Columns of {schema} ***')

            machine_family_data.url = machine_family_data_path
            machine_family_data.schema = schema
            machine_family_data.n_cols = n_cols
            machine_family_data.save()

    def register_machine_data(
            self, machine_unique_id: str,
            date: OptionalStrType = None, to_date: OptionalStrType = None) \
            -> None:
        try:
            machine_arrow_xdf = \
                self.load_machine_data(
                    machine_unique_id, machine_family_conso=False,
                    _from_files=True, _spark=False,
                    set_i_col=True, set_t_col=True)

        except Exception as err:
            return

        machine = \
            self.machine(
                machine_unique_id=machine_unique_id)

        machine_data_path = machine_arrow_xdf.path

        schema = \
            {col_name: str(col_type)
             for col_name, col_type in machine_arrow_xdf.srcTypesInclPartitionKVs.items()
             if col_name not in self._INDEX_COL_NAMES}

        n_cols = len(machine_arrow_xdf.contentCols)

        assert len(schema) == n_cols, \
            ValueError(f'*** {machine_data_path}: {n_cols} != No. of Columns of {schema} ***')

        # if Machine Data does not yet exist, then create
        machine_data, machine_data_created = \
            self.db.MachineData.get_or_create(
                machine=machine,
                date=None,
                n_rows=None,
                defaults=dict(
                            url=machine_data_path,
                            schema=schema,
                            n_cols=n_cols))

        if machine_data_created:
            # to re-register entire Machine Data for all dates
            date = to_date = None

            to_update_machine_data_again = False

        else:
            existing_schema = machine_data.schema

            # check if schema has changed
            changed_schema_items = \
                dict(set(schema.items())
                     .difference(existing_schema.items()))

            if changed_schema_items:
                to_update_machine_data_again = True

                self.stdout_logger.info(
                    msg=f'To Re-Register Machine Data for {machine} '
                        f'to Account for Changed Schema Items {changed_schema_items}...')

                # check if schema has changed inconsistently
                if set(changed_schema_items).intersection(existing_schema):
                    # to re-register entire Machine Family Data for all dates
                    date = to_date = None

            else:
                to_update_machine_data_again = \
                    (machine_data_path != machine_data.url)

        if date:
            date, to_date = \
                parse_from_date_and_to_date(
                    from_date=date,
                    to_date=to_date)

            machine_arrow_xdf = \
                machine_arrow_xdf.filterPartitions(
                    (DATE_COL,
                     date,
                     to_date)
                    if to_date
                    else (DATE_COL,
                          date))

        else:
            assert not to_date

        for piece_path in tqdm(machine_arrow_xdf.piecePaths):
            date = re.search(f'{DATE_COL}=(.*?)/', piece_path).group(1)

            piece_cache = \
                machine_arrow_xdf._read_metadata_and_schema(
                    piecePath=piece_path)

            daily_schema = \
                {col_name: str(col_type)
                 for col_name, col_type in piece_cache.srcTypesExclPartitionKVs.items()
                 if col_name not in self._INDEX_COL_NAMES}

            daily_n_cols = piece_cache.nCols - 1

            assert len(daily_schema) == daily_n_cols, \
                ValueError(f'*** {piece_path}: {daily_n_cols} != No. of Columns of {daily_schema} ***')

            new_schema_items = \
                dict(set(daily_schema.items())
                     .difference(schema.items()))

            if new_schema_items:
                to_update_machine_data_again = True

                self.stdout_logger.info(
                    msg=f'Re-Registering Machine Family Data for {machine} '
                        f'to Account for New Schema Items {new_schema_items} ({date})...')

                for col_name, col_type in new_schema_items.items():
                    assert col_name not in schema, \
                        ValueError(f'*** {col_name} ALREADY IN {schema} ***')

                    schema[col_name] = col_type
                    n_cols += 1

            machine_daily_data, _ = \
                self.db.MachineData.update_or_create(
                    machine=machine,
                    date=date,
                    defaults=dict(
                                url=piece_path,
                                schema=daily_schema,
                                n_cols=daily_n_cols,
                                n_rows=piece_cache.nRows))

            self.db.MachineDataStreamAggs \
            .filter(
                machine=machine,
                machine_family_data_stream_agg__machine_family_data__date=date) \
            .update(
                machine_data=machine_daily_data)

            fs.rm(
                path=piece_cache.localOrHDFSPath,
                hdfs=False,
                is_dir=False)

        if to_update_machine_data_again:
            self.stdout_logger.info(
                msg=f'Re-Registering Machine Data for {machine}...')

            assert len(schema) == n_cols, \
                ValueError(f'*** {machine_data_path}: {n_cols} != No. of Columns of {schema} ***')

            machine_data.url = machine_data_path
            machine_data.schema = schema
            machine_data.n_cols = n_cols
            machine_data.save()

    @classmethod
    def _distinct_machine_unique_ids_from_arrow_xdf(cls, arrow_xdf):
        assert isinstance(arrow_xdf, ArrowXDF)

        return numpy.unique(
                arrow_xdf.map(mapper=lambda pandas_df: pandas_df[cls._MACHINE_UNIQUE_ID_COL_NAME].unique())
                         .collect(cls._MACHINE_UNIQUE_ID_COL_NAME, reducer=numpy.hstack))

    def _create_or_update_same_name_machine_sku_and_family_metadata(
            self,
            machine_class_name,
            machine_family_name,
            excl_machine_data_stream_names=()):
        machine_sku = \
            self.machine_sku(
                machine_sku_name=machine_family_name,
                create=True,
                machine_class_name=machine_class_name)

        machine_family_xdf = \
            self.load_machine_family_data(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name,
                _from_files=True, _spark=False,
                set_i_col=True, set_t_col=True)

        machine_unique_ids = \
            self._distinct_machine_unique_ids_from_arrow_xdf(machine_family_xdf)

        machine_sku.machine_data_streams.set(
            {self.machine_data_stream(
                machine_class_name=machine_class_name,
                machine_data_stream_name=machine_data_stream_name,
                create=True)
             for machine_data_stream_name in
                set(machine_family_xdf.possibleFeatureContentCols)
                .difference(to_iterable(excl_machine_data_stream_names))
             if not machine_data_stream_name.startswith('_')})

        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name,
                create=True,
                machine_class_name=machine_class_name)

        machine_family.machine_skus.add(machine_sku)

        machines = {}

        for machine_unique_id in tqdm(machine_unique_ids):
            machines[machine_unique_id] = \
                machine = \
                self.update_or_create_machine(
                    machine_class_name=machine_class_name,
                    machine_unique_id=machine_unique_id,
                    machine_sku_name=machine_family_name,
                    create=True)

            machine.machine_families.add(machine_family)

        return machines

    def count_n_machines(self, machine_class_name=None, machine_family_name=None):
        n_machines = \
            Namespace(**{
                machine_class_name:
                    Namespace(**{
                        machine_family_name: None
                    })
                    if machine_family_name
                    else Namespace(**{
                        machine_family_name: None
                        for machine_family_name in
                            self.machine_class(machine_class_name=machine_class_name).machine_families.values_list('unique_name', flat=True)
                    })
            }) \
            if machine_class_name \
            else Namespace(**{
                machine_class.unique_name:
                    Namespace(**{
                        machine_family_name: None
                        for machine_family_name in machine_class.machine_families.values_list('unique_name', flat=True)
                    })
                for machine_class in self.db.MachineClasses.all()
            })

        for machine_class_name, machine_family_names in tqdm(n_machines.items()):
            for machine_family_name in tqdm(machine_family_names):
                machine_family_data_set_name = \
                    self.machine_family_conventional_full_name(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name)

                try:
                    machine_family_arrow_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=False,
                            set_i_col=True, set_t_col=False,
                            verbose=True)

                except Exception as err:
                    self.stdout_logger.warning(
                        msg='*** CANNOT LOAD MACHINE DATA FOR {}: {} ***'
                            .format(machine_family_data_set_name, err))

                    continue

                n_machines[machine_class_name][machine_family_name] = \
                    len(self._distinct_machine_unique_ids_from_arrow_xdf(machine_family_arrow_xdf))

        return n_machines

    def check_machine_family_data_streams(self, machine_class_name=None, machine_family_name=None):
        results = \
            Namespace(**{
                machine_class_name:
                    Namespace(**{
                        machine_family_name: None
                    })
                    if machine_family_name
                    else Namespace(**{
                        machine_family_name: None
                        for machine_family_name in
                            self.machine_class(machine_class_name=machine_class_name).machine_families.values_list('unique_name', flat=True)
                    })
            }) \
            if machine_class_name \
            else Namespace(**{
                machine_class.unique_name:
                    Namespace(**{
                        machine_family_name: None
                        for machine_family_name in machine_class.machine_families.values_list('unique_name', flat=True)
                    })
                for machine_class in self.db.MachineClasses.all()
            })

        for machine_class_name, machine_family_names in tqdm(results.items()):
            for machine_family_name in tqdm(machine_family_names):
                machine_family = \
                    self.machine_family(
                        machine_family_name=machine_family_name)

                machine_family_data = \
                    self.db.MachineFamilyData \
                        .filter(
                        machine_family=machine_family,
                        date=None) \
                        .first()

                if not machine_family_data:
                    self.register_machine_family_data(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name,
                        date=None, to_date=None)

                    machine_family_data = \
                        self.db.MachineFamilyData.get(
                            machine_family=machine_family,
                            date=None)

                machine_family_data_streams_checking_job, _ = \
                    self.db.MachineFamilyDataStreamsCheckingJobs.update_or_create(
                        machine_family=machine_family,
                        defaults=dict(
                                    started=make_aware(
                                                value=datetime.utcnow(),
                                                timezone=pytz.UTC,
                                                is_dst=None),
                                    finished=None))

                machine_family_data_set_name = \
                    self.machine_family_conventional_full_name(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name)

                try:
                    machine_family_arrow_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=False,
                            set_i_col=True, set_t_col=True,
                            verbose=True)

                except Exception as err:
                    self.stdout_logger.warning(
                        msg='*** CANNOT LOAD MACHINE DATA FOR {}: {} ***'
                            .format(machine_family_data_set_name, err))

                    continue

                db_machine_family_data_stream_names = \
                    set(machine_family.machine_data_streams.values_list('name', flat=True))

                s3_machine_data_possible_feature_content_col_names = \
                    set(machine_family_arrow_xdf.possibleFeatureContentCols)

                machine_data_stream_names_not_in_db = \
                    sorted(s3_machine_data_possible_feature_content_col_names -
                           db_machine_family_data_stream_names)

                machine_data_stream_names_not_on_disk = \
                    sorted(db_machine_family_data_stream_names -
                           s3_machine_data_possible_feature_content_col_names)

                results[machine_class_name][machine_family_name], _ = \
                    self.db.MachineFamilyDataStreamsChecks.update_or_create(
                        machine_family_data=machine_family_data,
                        defaults=dict(
                                    machine_data_stream_names_not_in_db=
                                        machine_data_stream_names_not_in_db
                                        if machine_data_stream_names_not_in_db
                                        else None,
                                    machine_data_stream_names_not_on_disk=
                                        machine_data_stream_names_not_on_disk
                                        if machine_data_stream_names_not_on_disk
                                        else None))

                machine_family_data_streams_checking_job.finished = \
                    make_aware(
                        value=datetime.utcnow(),
                        timezone=pytz.UTC,
                        is_dst=None)

                machine_family_data_streams_checking_job.save()

        return results

    def profile_machine_family_data_streams(self, machine_class_name=None, machine_family_name=None, to_month=None):
        machine_class_and_family_names = \
            Namespace(**{
                machine_class_name:
                    Namespace(**{
                        machine_family_name: None
                    })
                    if machine_family_name
                    else Namespace(**{
                        machine_family_name: None
                        for machine_family_name in
                            self.machine_class(machine_class_name=machine_class_name).machine_families.values_list('unique_name', flat=True)
                    })
            }) \
            if machine_class_name \
            else Namespace(**{
                machine_class.unique_name:
                    Namespace(**{
                        machine_family_name: None
                        for machine_family_name in machine_class.machine_families.values_list('unique_name', flat=True)
                    })
                for machine_class in self.db.MachineClasses.all()
            })

        for machine_class_name, machine_family_names in tqdm(machine_class_and_family_names.items()):
            for machine_family_name in tqdm(machine_family_names):
                machine_family = \
                    self.machine_family(
                        machine_family_name=machine_family_name)

                machine_family_data = \
                    self.db.MachineFamilyData \
                    .filter(
                        machine_family=machine_family,
                        date=None) \
                    .first()

                if not machine_family_data:
                    self.register_machine_family_data(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name,
                        date=None, to_date=None)

                    machine_family_data = \
                        self.db.MachineFamilyData.get(
                            machine_family=machine_family,
                            date=None)

                machine_family_data_set_name = \
                    self.machine_family_conventional_full_name(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name)

                try:
                    machine_family_arrow_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=False,
                            set_i_col=True, set_t_col=False,
                            verbose=True)

                except Exception as err:
                    self.stdout_logger.warning(
                        msg='*** CANNOT LOAD MACHINE DATA FOR {}: {} ***'
                            .format(machine_family_data_set_name, err))

                    continue

                if to_month:
                    to_date = month_end(to_month)

                    machine_family_arrow_xdf = \
                        machine_family_arrow_xdf.filterPartitions(
                            (DATE_COL,
                             str((datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                                  relativedelta(months=self.REF_N_MONTHS - 1)).date()),
                             str(to_date)))

                else:
                    to_date = None

                machine_data_streams = \
                    machine_family.machine_class.machine_data_streams.filter(
                        name__in=machine_family_arrow_xdf.possibleFeatureContentCols)

                assert machine_data_streams.count()

                machine_family_repr_sample_df = machine_family_arrow_xdf.reprSample

                machine_data_streams = \
                    machine_data_streams.filter(
                        name__in=machine_family_repr_sample_df.columns)

                n_machine_data_streams = machine_data_streams.count()

                assert n_machine_data_streams

                machine_family_data_streams_profiling_job, _ = \
                    self.db.MachineFamilyDataStreamsProfilingJobs.update_or_create(
                        machine_family=machine_family,
                        data_to_date=to_date,
                        defaults=dict(
                                    started=make_aware(
                                                value=datetime.utcnow(),
                                                timezone=pytz.UTC,
                                                is_dst=None),
                                    finished=None))

                self.db.MachineFamilyDataStreamProfiles \
                .filter(
                    machine_family_data=machine_family_data,
                    data_to_date=to_date) \
                .exclude(
                    machine_data_stream__in=machine_data_streams) \
                .delete()

                if to_month:
                    machine_family_health_service_config = None

                else:
                    from ....health.models import MachineFamilyHealthServiceConfig
                    
                    machine_family_health_service_config = \
                        MachineFamilyHealthServiceConfig.objects.filter(
                            machine_family=machine_family) \
                        .first()

                n_samples = len(machine_family_repr_sample_df)

                for machine_data_stream in tqdm(machine_data_streams, total=n_machine_data_streams):
                    machine_data_stream_name = machine_data_stream.name

                    _type_is_num = machine_family_arrow_xdf.typeIsNum(machine_data_stream_name)

                    if _type_is_num:
                        machine_family_arrow_xdf._nulls[machine_data_stream_name] = \
                            machine_data_stream.neg_invalid, \
                            machine_data_stream.pos_invalid

                    _distinct_values = \
                        {(coerce_int(machine_data_stream_distinct_value, return_orig=True)
                          if _type_is_num
                          else machine_data_stream_distinct_value):
                            machine_data_stream_distinct_value_proportion
                         for machine_data_stream_distinct_value,
                             machine_data_stream_distinct_value_proportion in
                            machine_family_arrow_xdf.distinct(machine_data_stream_name).iteritems()}
                        
                    _n_distinct_values = len(_distinct_values)

                    machine_family_data_stream_profile, _ = \
                        self.db.MachineFamilyDataStreamProfiles.update_or_create(
                            machine_family_data=machine_family_data,
                            data_to_date=to_date,
                            machine_data_stream=machine_data_stream,
                            defaults=dict(
                                        n_samples=n_samples,
                                        valid_fraction=machine_family_arrow_xdf.nonNullProportion(machine_data_stream_name),
                                        n_distinct_values=_n_distinct_values))

                    machine_family_data_stream_profile.distinct_value_proportions = \
                        _distinct_values \
                        if _n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE \
                        else None

                    if _type_is_num:
                        machine_family_machine_data_stream_repr_sample_series = \
                            machine_family_repr_sample_df[machine_data_stream_name]

                        quartiles = \
                            machine_family_machine_data_stream_repr_sample_series \
                            .describe(
                                percentiles=(.25, .5, .75)) \
                            .drop(
                                index='count',
                                level=None,
                                inplace=False,
                                errors='raise') \
                            .to_dict()

                        machine_family_data_stream_profile.min = \
                            quartiles['min']

                        machine_family_data_stream_profile.robust_min = \
                            robust_min = \
                            machine_family_arrow_xdf.outlierRstMin(machine_data_stream_name)

                        machine_family_data_stream_profile.quartile = \
                            quartiles['25%']

                        machine_family_data_stream_profile.median = \
                            quartiles['50%']

                        machine_family_data_stream_profile._3rd_quartile = \
                            quartiles['75%']

                        machine_family_data_stream_profile.robust_max = \
                            robust_max = \
                            machine_family_arrow_xdf.outlierRstMax(machine_data_stream_name)

                        machine_family_data_stream_profile.max = \
                            quartiles['max']

                        machine_family_data_stream_profile.strictly_outlier_robust_proportion = \
                            machine_family_machine_data_stream_repr_sample_series \
                            .between(
                                left=robust_min,
                                right=robust_max,
                                inclusive=False) \
                            .sum() / n_samples

                    machine_family_data_stream_profile.save()

                    if machine_family_health_service_config:
                        machine_family_health_service_config \
                        .machine_family_vital_data_stream_configs \
                        .filter(
                            vital_machine_data_stream=machine_data_stream) \
                        .update(
                            vital_machine_data_stream_profile=machine_family_data_stream_profile)

                machine_family_data_streams_profiling_job.finished = \
                    make_aware(
                        value=datetime.utcnow(),
                        timezone=pytz.UTC,
                        is_dst=None)

                machine_family_data_streams_profiling_job.save()

    def analyze_machine_data_stream_attrs(self, machine_class_name=None):
        machine_family_data_stream_profiles = \
            self.db.MachineFamilyDataStreamProfiles.filter(
                data_to_date__isnull=True)

        if machine_class_name:
            machine_family_data_stream_profiles = \
                machine_family_data_stream_profiles.filter(
                    machine_family__machine_class__unique_name=snake_case(machine_class_name))

        candidate_logical_data_types = {}
        candidate_physical_data_types = {}

        possible_default_values = {}

        min_neg = {}
        min_0 = {}
        min_0_max_1 = {}

        for machine_family_data_stream_profile in \
                tqdm(machine_family_data_stream_profiles.all(),
                     total=machine_family_data_stream_profiles.count()):
            # TODO: optimize to get multiple field values from 1 query
            machine_data_stream = machine_family_data_stream_profile.machine_data_stream

            valid_fraction = machine_family_data_stream_profile.valid_fraction

            n_distinct_values = machine_family_data_stream_profile.n_distinct_values
            distinct_value_proportions = machine_family_data_stream_profile.distinct_value_proportions

            min = machine_family_data_stream_profile.min
            robust_min = machine_family_data_stream_profile.robust_min
            quartile = machine_family_data_stream_profile.quartile
            median = machine_family_data_stream_profile.median
            _3rd_quartile = machine_family_data_stream_profile._3rd_quartile
            robust_max = machine_family_data_stream_profile.robust_max
            max = machine_family_data_stream_profile.max

            if valid_fraction:
                if n_distinct_values > self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                    # detect and set Interval-or-Ratio Numerical Machine Data Streams
                    # this may be inappropriate for characterizing Integer IDs
                    # but would not matter in AI modeling
                    if not ((min is None) or
                            (robust_min is None) or
                            (quartile is None) or
                            (median is None) or
                            (_3rd_quartile is None) or
                            (robust_max is None) or
                            (max is None)):
                        if machine_data_stream.logical_data_type != self.NUM_INTERVAL_OR_RATIO_LOGICAL_DATA_TYPE:
                            msg = 'Setting {} Logical Data Type to NUM_ITV_RAT...'.format(machine_data_stream)
                            self.stdout_logger.info(msg)

                            machine_data_stream.logical_data_type = self.NUM_INTERVAL_OR_RATIO_LOGICAL_DATA_TYPE
                            machine_data_stream.save()

                            self.stdout_logger.info(msg + ' done: {}'.format(machine_data_stream))

                elif n_distinct_values > 1:
                    pass

                elif n_distinct_values == 1:
                    for only_value, proportion in distinct_value_proportions.items():
                        assert proportion == 1

                        f = coerce_float(only_value)

                        if f is not None:
                            if machine_data_stream in possible_default_values:
                                possible_default_values[machine_data_stream].add(f)
                            else:
                                possible_default_values[machine_data_stream] = {f}

        for machine_data_stream, _possible_default_values in possible_default_values.items():
            if len(_possible_default_values) == 1:
                possible_default_value = _possible_default_values.pop()

                if machine_data_stream.default != possible_default_value:
                    self.stdout_logger.warning(
                        '*** {} Default could be {} ***'.format(
                            machine_data_stream, possible_default_value))

            else:
                self.stdout_logger.warning(
                    '*** {} Default could be among {} ***'.format(
                        machine_data_stream, _possible_default_values))

    def profile_machine_family_num_data_stream_pair_corrs(
            self,
            machine_class_name=None, machine_family_name=None,
            to_month=None):
        _MIN_N_SAMPLES_FOR_CORR = 1000

        machine_class_and_family_names = \
            Namespace(**{
                machine_class_name:
                    Namespace(**{
                        machine_family_name: None
                    })
                    if machine_family_name
                    else Namespace(**{
                        machine_family_name: None
                        for machine_family_name in
                            self.machine_class(machine_class_name=machine_class_name).machine_families.values_list('unique_name', flat=True)
                    })
            }) \
            if machine_class_name \
            else Namespace(**{
                machine_class.unique_name:
                    Namespace(**{
                        machine_family_name: None
                        for machine_family_name in machine_class.machine_families.values_list('unique_name', flat=True)
                    })
                for machine_class in self.db.MachineClasses.all()
            })

        for machine_class_name, machine_family_names in tqdm(machine_class_and_family_names.items()):
            for machine_family_name in tqdm(machine_family_names):
                machine_family = \
                    self.machine_family(
                        machine_family_name=machine_family_name)

                machine_family_data = \
                    self.db.MachineFamilyData \
                    .filter(
                        machine_family=machine_family,
                        date=None) \
                    .first()

                if not machine_family_data:
                    self.register_machine_family_data(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name,
                        date=None, to_date=None)

                    machine_family_data = \
                        self.db.MachineFamilyData.get(
                            machine_family=machine_family,
                            date=None)

                machine_family_data_set_name = \
                    self.machine_family_conventional_full_name(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name)

                try:
                    machine_family_arrow_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=False,
                            set_i_col=True, set_t_col=False,
                            verbose=True)

                except Exception as err:
                    self.stdout_logger.warning(
                        msg='*** CANNOT LOAD MACHINE DATA FOR {}: {} ***'
                            .format(machine_family_data_set_name, err))

                    continue

                if to_month:
                    to_date = month_end(to_month)

                    machine_family_arrow_xdf = \
                        machine_family_arrow_xdf.filterPartitions(
                            (DATE_COL,
                             str((datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                                  relativedelta(months=self.REF_N_MONTHS - 1)).date()),
                             str(to_date)))

                else:
                    to_date = None

                machine_family = \
                    self.machine_family(
                        machine_family_name=machine_family_name)

                num_machine_data_streams = \
                    machine_family.machine_class.machine_data_streams.filter(
                        logical_data_type__in=self.NUM_LOGICAL_DATA_TYPES,
                        name__in=machine_family_arrow_xdf.possibleNumContentCols)

                assert num_machine_data_streams.count() > 1, \
                    '*** ONLY {} NUMERICAL ***'.format(num_machine_data_streams)

                machine_family_repr_sample_df = machine_family_arrow_xdf.reprSample

                num_machine_data_streams_robust_indices = {}

                for num_machine_data_stream in tqdm(num_machine_data_streams):
                    num_machine_data_stream_name = num_machine_data_stream.name

                    if num_machine_data_stream_name in machine_family_repr_sample_df.columns:
                        machine_family_arrow_xdf._nulls[num_machine_data_stream_name] = \
                            num_machine_data_stream.neg_invalid, \
                            num_machine_data_stream.pos_invalid

                        num_machine_data_stream_robust_min = \
                            machine_family_arrow_xdf.outlierRstMin(num_machine_data_stream_name)
                        num_machine_data_stream_robust_max = \
                            machine_family_arrow_xdf.outlierRstMax(num_machine_data_stream_name)

                        if num_machine_data_stream_robust_min < num_machine_data_stream_robust_max:
                            machine_data_stream_robust_indices = \
                                machine_family_repr_sample_df[num_machine_data_stream_name].between(
                                    left=num_machine_data_stream_robust_min,
                                    right=num_machine_data_stream_robust_max,
                                    inclusive=False)

                            if len(machine_data_stream_robust_indices):
                                num_machine_data_streams_robust_indices[num_machine_data_stream] = \
                                    machine_data_stream_robust_indices

                num_machine_data_streams = list(num_machine_data_streams_robust_indices)

                self.db.MachineFamilyDataStreamPairCorrs \
                .filter(
                    machine_family_data=machine_family_data,
                    data_to_date=to_date) \
                .exclude(
                    machine_data_stream__in=num_machine_data_streams,
                    other_machine_data_stream__in=num_machine_data_streams) \
                .delete()

                n_num_machine_data_streams = len(num_machine_data_streams)
                assert n_num_machine_data_streams > 1
                
                num_machine_data_stream_pairs = []
                for i in range(n_num_machine_data_streams - 1):
                    for j in range(i + 1, n_num_machine_data_streams):
                        num_machine_data_stream_pairs.append(
                            (num_machine_data_streams[i],
                             num_machine_data_streams[j]))

                for num_machine_data_stream, other_num_machine_data_stream in tqdm(num_machine_data_stream_pairs):
                    num_machine_data_stream_name = num_machine_data_stream.name
                    other_num_machine_data_stream_name = other_num_machine_data_stream.name

                    sample_df = \
                        machine_family_repr_sample_df.loc[
                            num_machine_data_streams_robust_indices[num_machine_data_stream] &
                            num_machine_data_streams_robust_indices[other_num_machine_data_stream],
                            [num_machine_data_stream_name, other_num_machine_data_stream_name]]

                    n_samples = len(sample_df)

                    if n_samples > _MIN_N_SAMPLES_FOR_CORR:
                        num_machine_data_stream_series = sample_df[num_machine_data_stream_name]

                        num_machine_data_stream_robust_min = float(num_machine_data_stream_series.min())
                        num_machine_data_stream_robust_max = float(num_machine_data_stream_series.max())

                        if num_machine_data_stream_robust_min < num_machine_data_stream_robust_max:
                            other_num_machine_data_stream_series = sample_df[other_num_machine_data_stream_name]

                            other_num_machine_data_stream_robust_min = float(other_num_machine_data_stream_series.min())
                            other_num_machine_data_stream_robust_max = float(other_num_machine_data_stream_series.max())

                            if other_num_machine_data_stream_robust_min < other_num_machine_data_stream_robust_max:
                                _delete_pair_corr = False

                                corr, _p_val = \
                                    pearsonr(
                                        x=num_machine_data_stream_series,
                                        y=other_num_machine_data_stream_series)

                                _field_values_to_insert = \
                                    dict(machine_data_stream_range=
                                            NumericRange(
                                                lower=num_machine_data_stream_robust_min,
                                                upper=num_machine_data_stream_robust_max,
                                                bounds='[]',
                                                empty=False),
                                         other_machine_data_stream_range=
                                             NumericRange(
                                                 lower=other_num_machine_data_stream_robust_min,
                                                 upper=other_num_machine_data_stream_robust_max,
                                                 bounds='[]',
                                                 empty=False),
                                         n_samples=n_samples,
                                         corr=corr)

                                self.db.MachineFamilyDataStreamPairCorrs.update_or_create(
                                    machine_family_data=machine_family_data,
                                    data_to_date=to_date,
                                    machine_data_stream=num_machine_data_stream,
                                    other_machine_data_stream=other_num_machine_data_stream,
                                    defaults=_field_values_to_insert)

                                self.db.MachineFamilyDataStreamPairCorrs.update_or_create(
                                    machine_family_data=machine_family_data,
                                    data_to_date=to_date,
                                    machine_data_stream=other_num_machine_data_stream,
                                    other_machine_data_stream=num_machine_data_stream,
                                    defaults=_field_values_to_insert)

                            else:
                                _delete_pair_corr = True

                        else:
                            _delete_pair_corr = True

                    else:
                        _delete_pair_corr = True

                    if _delete_pair_corr:
                        self.db.MachineFamilyDataStreamPairCorrs.filter(
                            (Q(machine_data_stream=num_machine_data_stream) &
                             Q(other_machine_data_stream=other_num_machine_data_stream)) |
                            (Q(machine_data_stream=other_num_machine_data_stream) &
                             Q(other_machine_data_stream=num_machine_data_stream)),
                            machine_family_data=machine_family_data,
                            data_to_date=to_date) \
                        .delete()

    def agg_machine_family_day_data(
            self,
            machine_class_name, machine_family_name,
            date, to_date=None, monthly=False, _force_re_agg=False):
        machine_family_data_set_name = \
            self.machine_family_conventional_full_name(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name)

        s3_dir_prefix = \
            os.path.join(
                self.params.s3.machine_data.day_agg_dir_prefix,
                machine_family_data_set_name + _PARQUET_EXT)

        s3_dir_path = \
            os.path.join(
                self.params.s3.machine_data.day_agg_dir_path,
                machine_family_data_set_name + _PARQUET_EXT)

        machine_family_arrow_spark_xdf = None

        machine_data_stream_invalid_values = \
            {d[0]: (d[1], d[2])
             for d in self.machine_class(machine_class_name=machine_class_name).machine_data_streams
                        .values_list('name', 'neg_invalid', 'pos_invalid')}
        assert all((v[0] < 0 < v[1])
                   for v in machine_data_stream_invalid_values.values())

        if monthly:
            mth_str = date
            assert len(mth_str) == 7

            if to_date:
                to_mth_str = to_date
                assert len(to_mth_str) == 7 and (to_mth_str > mth_str)

                to_date += '-31'

            else:
                to_mth_str = mth_str

            _mth_str = mth_str

            while _mth_str <= to_mth_str:
                self.stdout_logger.info(
                    msg='Aggregating {} Daily Machine Data for {}...'
                        .format(machine_family_data_set_name, _mth_str))

                if not machine_family_arrow_spark_xdf:
                    machine_family_arrow_spark_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=True,
                            set_i_col=True, set_t_col=False)

                try:
                    machine_family_arrow_spark_xdf_for_month = \
                        machine_family_arrow_spark_xdf.filterPartitions(
                            (DATE_COL,
                             _mth_str + '-01',
                             _mth_str + '-31'))

                except Exception as err:
                    self.stdout_logger.warning(
                        msg='*** CANNOT LOAD DATA FOR "{}" IN {}: {} ***'
                            .format(machine_family_data_set_name, _mth_str, err))

                    _mth_str = month_str(_mth_str, n_months_offset=1)

                    continue

                agg_col_strs = ['COUNT(*) AS {}'.format(self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID)]

                for col in set(machine_family_arrow_spark_xdf_for_month.possibleFeatureContentCols) \
                            .difference(self._INDEX_COL_NAMES):
                    if to_date:
                        repr_sample_machine_family_arrow_spark_xdf = \
                            machine_family_arrow_spark_xdf.reprSample

                        n_distinct_values = \
                            len((machine_family_arrow_spark_xdf
                                 if col in repr_sample_machine_family_arrow_spark_xdf.possibleFeatureContentCols
                                 else machine_family_arrow_spark_xdf_for_month).distinct(col))

                    else:
                        n_distinct_values = \
                            len(machine_family_arrow_spark_xdf_for_month.distinct(col))

                    snake_case_col = snake_case(col)

                    if machine_family_arrow_spark_xdf_for_month.typeIsNum(col):
                        invalid_values = machine_data_stream_invalid_values.get(snake_case_col)
                        col_str = \
                            'IF((`{0}` > {1}) AND (`{0}` < {2}), `{0}`, NULL)'.format(col, *invalid_values) \
                            if invalid_values \
                            else "IF(STRING(`{0}`) = 'NaN', NULL, `{0}`)".format(col)

                        agg_col_strs += \
                            ['COUNT({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.COUNT_EXCL_INVALID),
                             'MIN({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MIN),
                             'PERCENTILE_APPROX({}, 0.05) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.ROBUST_MIN),
                             'PERCENTILE_APPROX({}, 0.25) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.QUARTILE),
                             'AVG({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MEAN),
                             'PERCENTILE_APPROX({}, 0.5) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MEDIAN),
                             'PERCENTILE_APPROX({}, 0.75) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES._3RD_QUARTILE),
                             'PERCENTILE_APPROX({}, 0.95) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.ROBUST_MAX),
                             'MAX({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MAX)]

                        if n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                            agg_col_strs.append(
                                'COLLECT_LIST({}) AS {}{}'
                                .format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.LIST))

                    else:
                        agg_col_strs.append(
                            'COUNT(`{}`) AS {}{}'
                            .format(col, snake_case_col, self._DAY_AGG_SUFFIXES.COUNT_EXCL_INVALID))

                        if n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                            agg_col_strs.append(
                                'COLLECT_LIST(`{}`) AS {}{}'
                                .format(col, snake_case_col, self._DAY_AGG_SUFFIXES.LIST))

                _tmp_dir_path = tempfile.mkdtemp()

                if machine_family_arrow_spark_xdf_for_month.nPieces == 1:
                    machine_family_arrow_spark_xdf_for_month.tCol = self._LOCAL_DATE_TIME_COL_NAME

                machine_family_arrow_spark_xdf_for_month(
                    'SELECT \
                        {0}, \
                        {1}, \
                        {2} \
                    FROM \
                        this \
                    GROUP BY \
                        {0}, \
                        {1}'
                    .format(
                        self._MACHINE_UNIQUE_ID_COL_NAME,
                        DATE_COL,
                        ', '.join(agg_col_strs))) \
                .save(
                    path=_tmp_dir_path,
                    format='parquet',
                    partitionBy=DATE_COL,
                    verbose=True)

                if fs._ON_LINUX_CLUSTER_WITH_HDFS:
                    fs.get(
                        from_hdfs=_tmp_dir_path,
                        to_local=_tmp_dir_path,
                        is_dir=True, overwrite=True, _mv=True,
                        must_succeed=True)

                for partition_key in \
                        tqdm(sorted(
                            partition_key
                            for partition_key in os.listdir(_tmp_dir_path)
                            if partition_key.startswith('{}='.format(DATE_COL)))):
                    s3.sync(
                        from_dir_path=os.path.join(_tmp_dir_path, partition_key),
                        to_dir_path=os.path.join(s3_dir_path, partition_key),
                        delete=True, quiet=True,
                        access_key_id=self.params.s3.access_key_id,
                        secret_access_key=self.params.s3.secret_access_key,
                        verbose=False)

                fs.rm(path=_tmp_dir_path,
                      is_dir=True,
                      hdfs=False)

                _mth_str = month_str(_mth_str, n_months_offset=1)

        else:
            if to_date:
                assert (len(to_date) == 10) and (to_date > date)

            else:
                to_date = date

            for _date in tqdm(pandas.date_range(start=date, end=to_date).date):
                if (not _force_re_agg) and \
                        ('Contents' in
                            self.s3_client.list_objects_v2(
                                Bucket=self.params.s3.bucket,
                                Prefix=os.path.join(
                                         s3_dir_prefix,
                                         '{}={}'.format(DATE_COL, _date)))):
                    # TODO: test load to make sure

                    continue

                self.stdout_logger.info(
                    msg='Aggregating {} Daily Machine Data for {}...'
                        .format(machine_family_data_set_name, _date))

                if not machine_family_arrow_spark_xdf:
                    machine_family_arrow_spark_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=True,
                            set_i_col=True, set_t_col=False)

                try:
                    machine_family_arrow_spark_xdf_for_date = \
                        machine_family_arrow_spark_xdf.filterPartitions(
                            (DATE_COL,
                             _date))

                except Exception as err:
                    self.stdout_logger.warning(
                        msg='*** CANNOT LOAD DATA FOR "{}" IN {}: {} ***'
                            .format(machine_family_data_set_name, _date, err))

                    continue

                agg_col_strs = ['COUNT(*) AS {}'.format(self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID)]

                for col in set(machine_family_arrow_spark_xdf_for_date.possibleFeatureContentCols) \
                            .difference(self._INDEX_COL_NAMES):
                    if to_date > date:
                        repr_sample_machine_family_arrow_spark_xdf = \
                            machine_family_arrow_spark_xdf.reprSample

                        n_distinct_values = \
                            len((machine_family_arrow_spark_xdf
                                 if col in repr_sample_machine_family_arrow_spark_xdf.possibleFeatureContentCols
                                 else machine_family_arrow_spark_xdf_for_date).distinct(col))

                    else:
                        n_distinct_values = \
                            len(machine_family_arrow_spark_xdf_for_date.distinct(col))

                    snake_case_col = snake_case(col)

                    if machine_family_arrow_spark_xdf_for_date.typeIsNum(col):
                        invalid_values = machine_data_stream_invalid_values.get(snake_case_col)
                        col_str = \
                            'IF((`{0}` > {1}) AND (`{0}` < {2}), `{0}`, NULL)'.format(col, *invalid_values) \
                            if invalid_values \
                            else "IF(STRING(`{0}`) = 'NaN', NULL, `{0}`)".format(col)

                        agg_col_strs += \
                            ['COUNT({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.COUNT_EXCL_INVALID),
                             'MIN({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MIN),
                             'PERCENTILE_APPROX({}, 0.05) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.ROBUST_MIN),
                             'PERCENTILE_APPROX({}, 0.25) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.QUARTILE),
                             'AVG({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MEAN),
                             'PERCENTILE_APPROX({}, 0.5) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MEDIAN),
                             'PERCENTILE_APPROX({}, 0.75) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES._3RD_QUARTILE),
                             'PERCENTILE_APPROX({}, 0.95) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.ROBUST_MAX),
                             'MAX({}) AS {}{}'.format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.MAX)]

                        if n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                            agg_col_strs.append(
                                'COLLECT_LIST({}) AS {}{}'
                                .format(col_str, snake_case_col, self._DAY_AGG_SUFFIXES.LIST))

                    else:
                        agg_col_strs.append(
                            'COUNT(`{}`) AS {}{}'
                            .format(col, snake_case_col, self._DAY_AGG_SUFFIXES.COUNT_EXCL_INVALID))

                        if n_distinct_values <= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                            agg_col_strs.append(
                                'COLLECT_LIST(`{}`) AS {}{}'
                                .format(col, snake_case_col, self._DAY_AGG_SUFFIXES.LIST))

                machine_family_arrow_spark_xdf_for_date(
                    'SELECT \
                        {0}, \
                        {1} \
                    FROM \
                        this \
                    GROUP BY \
                        {0}'
                    .format(
                        self._MACHINE_UNIQUE_ID_COL_NAME,
                        ', '.join(agg_col_strs))) \
                .repartition(1) \
                .save(
                    path=os.path.join(
                            s3_dir_path,
                            '{}={}'.format(
                                DATE_COL,
                                _date)),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    format='parquet',
                    verbose=True)

    def machine_family_data_stream_day_aggs_to_db(
            self,
            machine_class_name, machine_family_name,
            date, to_date=None, monthly=False):
        self.register_machine_family_data(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name,
            date=date, to_date=to_date)

        if monthly:
            assert len(date) == 7

            if to_date:
                assert len(to_date) == 7 and (to_date > date)

                to_date = month_end(to_date)

            else:
                to_date = month_end(date)

            date = datetime.strptime(date + '-01', '%Y-%m-%d').date()

        else:
            if to_date:
                assert (len(to_date) == 10) and (to_date > date)

                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

            date = datetime.strptime(date, '%Y-%m-%d').date()

        machine_family_data_set_name = \
            self.machine_family_conventional_full_name(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name)

        machine_family_arrow_xdf = \
            self.load_machine_family_data(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name,
                _from_files=True, _spark=False,
                set_i_col=True, set_t_col=False,
                reCache=True) \
            .filterPartitions(
                (DATE_COL,
                 date,
                 to_date)
                if to_date
                else (DATE_COL,
                      date))

        # exhaustively get all Machines
        # and hence download all possible Machine Data Stream names
        _machine_unique_ids = \
            {snake_case(str(machine_unique_id))
             for machine_unique_id in
                self._distinct_machine_unique_ids_from_arrow_xdf(machine_family_arrow_xdf)}

        machine_family_data_stream_day_aggs_arrow_xdf = \
            ArrowXDF(
                path=os.path.join(
                        self.params.s3.machine_data.day_agg_dir_path,
                        machine_family_data_set_name + _PARQUET_EXT),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=True) \
            .filterPartitions(
                (DATE_COL,
                 date,
                 to_date)
                if to_date
                else (DATE_COL,
                      date))

        # exhaustively get all Machines
        # and hence download all possible Machine Data Stream Aggs
        machine_unique_ids = \
            {snake_case(str(machine_unique_id))
             for machine_unique_id in
                self._distinct_machine_unique_ids_from_arrow_xdf(machine_family_data_stream_day_aggs_arrow_xdf)}

        _wrong_unique_ids = machine_unique_ids.difference(_machine_unique_ids)
        assert not _wrong_unique_ids, \
            '*** {} NOT AMONG ORIGINAL DATA ***'.format(_wrong_unique_ids)

        machines = \
            {machine_unique_id:
                self.update_or_create_machine(
                    machine_class_name=machine_class_name,
                    machine_unique_id=machine_unique_id)
             for machine_unique_id in tqdm(machine_unique_ids)}

        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        machine_data_streams = \
            {machine_data_stream.name:
                Namespace(
                    obj=machine_data_stream,

                    is_num=machine_family_arrow_xdf.typeIsNum(machine_data_stream.name),
                    neg_invalid=machine_data_stream.neg_invalid,
                    pos_invalid=machine_data_stream.pos_invalid,

                    is_bool=machine_family_arrow_xdf.typeIsBool(machine_data_stream.name),

                    day_list_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.LIST),

                    day_distinct_value_counts_incl_invalid_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.DISTINCT_VALUE_COUNTS_INCL_INVALID),

                    day_distinct_value_proportions_incl_invalid_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.DISTINCT_VALUE_PROPORTIONS_INCL_INVALID),

                    day_count_excl_invalid_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.COUNT_EXCL_INVALID),

                    day_distinct_value_proportions_excl_invalid_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.DISTINCT_VALUE_PROPORTIONS_EXCL_INVALID),

                    day_min_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.MIN),

                    day_robust_min_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.ROBUST_MIN),

                    day_quartile_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.QUARTILE),

                    day_mean_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.MEAN),

                    day_median_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.MEDIAN),

                    day_3rd_quartile_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES._3RD_QUARTILE),

                    day_robust_max_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.ROBUST_MAX),

                    day_max_col_name=
                        '{}{}'.format(
                            machine_data_stream.name,
                            self._DAY_AGG_SUFFIXES.MAX))

             for machine_data_stream in machine_family.machine_class.machine_data_streams.all()
                if (machine_data_stream.name in machine_family_arrow_xdf.possibleFeatureContentCols) and
                   ('{}{}'.format(machine_data_stream.name, self._DAY_AGG_SUFFIXES.COUNT_EXCL_INVALID) in
                    machine_family_data_stream_day_aggs_arrow_xdf.possibleFeatureContentCols)}

        assert machine_data_streams, \
            '*** {}: NO RELEVANT MACHINE DATA STREAMS ***'.format(machine_family)

        assert all((machine_data_stream_details.neg_invalid < 0 < machine_data_stream_details.pos_invalid)
                   for machine_data_stream_details in machine_data_streams.values())

        existing_machine_family_data_stream_aggs = \
            self.db.MachineFamilyDataStreamAggs.filter(
                machine_family_data__machine_family=machine_family)

        existing_machine_data_stream_aggs = \
            self.db.MachineDataStreamAggs.filter(
                machine_family_data_stream_agg__machine_family_data__machine_family=machine_family)

        machine_family_data_stream_day_aggs_by_date = {}
        machine_data_stream_day_aggs_by_date = {}

        for machine_family_data_stream_day_aggs_df in \
                tqdm(iter(machine_family_data_stream_day_aggs_arrow_xdf),
                     total=machine_family_data_stream_day_aggs_arrow_xdf.nPieces):
            date = machine_family_data_stream_day_aggs_df[DATE_COL].iloc[0]

            machine_family_data_stream_day_aggs_df.drop(
                columns=DATE_COL,
                level=None,
                inplace=True,
                errors='raise')

            machine_family_data_stream_day_aggs_df.loc[:, self._MACHINE_UNIQUE_ID_COL_NAME] = \
                machine_family_data_stream_day_aggs_df[self._MACHINE_UNIQUE_ID_COL_NAME].map(
                    lambda machine_unique_id: snake_case(str(machine_unique_id)))

            _n_aggs_rows_before_dedup = len(machine_family_data_stream_day_aggs_df)

            machine_family_data_stream_day_aggs_df.drop_duplicates(
                subset=self._MACHINE_UNIQUE_ID_COL_NAME,
                keep='first',
                inplace=True)

            _n_aggs_rows_after_dedup = len(machine_family_data_stream_day_aggs_df)
            assert _n_aggs_rows_after_dedup

            _n_dup_aggs_rows_dropped = _n_aggs_rows_before_dedup - _n_aggs_rows_after_dedup
            if _n_dup_aggs_rows_dropped:
                self.stdout_logger.warning(
                    msg='*** {}: DROPPED {:,} DUPLICATE ROW(S) ***'
                        .format(date, _n_dup_aggs_rows_dropped))

            machine_family_data_stream_day_aggs_df.set_index(
                keys=self._MACHINE_UNIQUE_ID_COL_NAME,
                drop=True,
                append=False,
                inplace=True,
                verify_integrity=True)

            machine_family_daily_data = \
                self.db.MachineFamilyData.get(
                    machine_family=machine_family,
                    date=date)

            if self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID in machine_family_data_stream_day_aggs_df.columns:
                day_count_incl_invalid_series = \
                    machine_family_data_stream_day_aggs_df[self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID]

            else:
                # *** BELOW DOESN'T WORK BECAUSE COLLECT_LIST(...) DOESN'T KEEP NULLS ***
                # _first_day_list_col_name = \
                #     next(machine_data_stream_details.day_list_col_name
                #          for machine_data_stream_details in machine_data_streams.values()
                #          if machine_data_stream_details.day_list_col_name in machine_family_data_stream_day_aggs_df.columns)
                # machine_family_data_stream_day_aggs_df.loc[:, self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID] = \
                #     day_count_incl_invalid_series = \
                #     machine_family_data_stream_day_aggs_df[_first_day_list_col_name].map(
                #         lambda machine_family_data_stream_day_list: len(machine_family_data_stream_day_list))

                machine_family_data_stream_day_aggs_df.loc[:, self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID] = \
                    day_count_incl_invalid_series = \
                    machine_family_data_stream_day_aggs_df[
                        list({machine_data_stream_details.day_count_excl_invalid_col_name
                              for machine_data_stream_details in machine_data_streams.values()}
                             .intersection(machine_family_data_stream_day_aggs_df.columns))] \
                        .max(axis='columns',
                             skipna=False,
                             level=None,
                             numeric_only=True)

            assert day_count_incl_invalid_series.notnull().all() \
               and (day_count_incl_invalid_series > 0).all(), \
                '*** {} ***'.format(day_count_incl_invalid_series)

            day_total_count_incl_invalid = \
                machine_family_data_stream_day_aggs_df[self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID].sum()

            machine_family_data_stream_day_aggs_by_date[date] = \
                machine_family_data_stream_day_aggs_for_date_by_machine_data_stream = {}

            machine_family_data_stream_day_aggs_for_date_to_bulk_update = set()

            has_day_count_excl_invalid = {}
            day_count_excl_invalid_pos_indices = {}
            has_pos_day_count_excl_invalid = {}

            has_day_list = {}

            for machine_data_stream_name, machine_data_stream_details in tqdm(machine_data_streams.items()):
                machine_data_stream_obj = machine_data_stream_details.obj
            
                machine_data_stream_day_count_excl_invalid_col_name = \
                    machine_data_stream_details.day_count_excl_invalid_col_name

                has_day_count_excl_invalid[machine_data_stream_name] = \
                    _has_machine_data_stream_day_count_excl_invalid = \
                    (machine_data_stream_day_count_excl_invalid_col_name in
                     machine_family_data_stream_day_aggs_df.columns)

                if _has_machine_data_stream_day_count_excl_invalid:
                    machine_data_stream_day_count_excl_invalid_series = \
                        machine_family_data_stream_day_aggs_df[machine_data_stream_day_count_excl_invalid_col_name]
                    assert machine_data_stream_day_count_excl_invalid_series.notnull().all()

                    day_count_excl_invalid_pos_indices[machine_data_stream_name] = \
                        _machine_data_stream_day_count_excl_invalid_pos_indices = \
                        (machine_data_stream_day_count_excl_invalid_series > 0)

                    has_pos_day_count_excl_invalid[machine_data_stream_name] = \
                        _machine_data_stream_day_has_pos_count_excl_invalid = \
                        _machine_data_stream_day_count_excl_invalid_pos_indices.any()

                    if _machine_data_stream_day_has_pos_count_excl_invalid:
                        machine_family_data_stream_day_total_count_excl_invalid = \
                            machine_data_stream_day_count_excl_invalid_series.sum(
                                axis=None,
                                skipna=False,
                                level=None,
                                min_count=0)

                        machine_family_data_stream_day_aggs_for_date_by_machine_data_stream[machine_data_stream_obj] = \
                            machine_family_data_stream_day_agg = \
                            self.db.MachineFamilyDataStreamAggs.update_or_create(
                                machine_family_data=machine_family_daily_data,
                                machine_data_stream=machine_data_stream_obj,

                                defaults=dict(
                                            count_incl_invalid=
                                                day_total_count_incl_invalid,
                                            counts_incl_invalid=
                                                {machine_unique_id: machine_data_stream_day_count_incl_invalid
                                                 for machine_unique_id, machine_data_stream_day_count_incl_invalid in
                                                    day_count_incl_invalid_series.items()},

                                            count_excl_invalid=
                                                machine_family_data_stream_day_total_count_excl_invalid,
                                            counts_excl_invalid=
                                                {machine_unique_id: machine_data_stream_day_count_excl_invalid
                                                 for machine_unique_id, machine_data_stream_day_count_excl_invalid in
                                                    machine_data_stream_day_count_excl_invalid_series.loc[
                                                        _machine_data_stream_day_count_excl_invalid_pos_indices].items()}))[0]

                        machine_data_stream_day_list_col_name = machine_data_stream_details.day_list_col_name

                        has_day_list[machine_data_stream_name] = \
                            _has_day_list = \
                            (machine_data_stream_day_list_col_name in machine_family_data_stream_day_aggs_df.columns)

                        if _has_day_list:
                            machine_family_data_stream_day_aggs_df[
                                    machine_data_stream_details.day_distinct_value_counts_incl_invalid_col_name] = \
                                machine_data_stream_day_distinct_value_counts_incl_invalid_dict_series = \
                                machine_family_data_stream_day_aggs_df[machine_data_stream_day_list_col_name].map(
                                    lambda machine_data_stream_day_value_list:
                                        {(coerce_int(machine_data_stream_distinct_value, return_orig=True)
                                          if machine_data_stream_details.is_num
                                          else (coerce_bool(machine_data_stream_distinct_value)
                                                    # to avoid: TypeError: keys must be str, int, float, bool or None, not numpy.bool_
                                                if machine_data_stream_details.is_bool
                                                else machine_data_stream_distinct_value)):
                                            machine_data_stream_distinct_value_day_count
                                         for machine_data_stream_distinct_value,
                                             machine_data_stream_distinct_value_day_count in
                                            Counter(machine_data_stream_day_value_list).items()}
                                        if isinstance(machine_data_stream_day_value_list, numpy.ndarray) and
                                           machine_data_stream_day_value_list.size
                                        else None)

                            machine_family_data_stream_day_count_incl_invalid = 0
                            machine_family_data_stream_day_distinct_value_counts_incl_invalid = {}

                            machine_family_data_stream_day_count_excl_invalid = 0

                            for machine_data_stream_day_distinct_value_counts_incl_invalid_dict in \
                                    machine_data_stream_day_distinct_value_counts_incl_invalid_dict_series:
                                if machine_data_stream_day_distinct_value_counts_incl_invalid_dict is not None:
                                    for machine_data_stream_distinct_value, \
                                            machine_data_stream_day_distinct_value_count in \
                                            machine_data_stream_day_distinct_value_counts_incl_invalid_dict.items():
                                        machine_family_data_stream_day_count_incl_invalid += \
                                            machine_data_stream_day_distinct_value_count

                                        if machine_data_stream_distinct_value in \
                                                machine_family_data_stream_day_distinct_value_counts_incl_invalid:
                                            machine_family_data_stream_day_distinct_value_counts_incl_invalid[machine_data_stream_distinct_value] += \
                                                machine_data_stream_day_distinct_value_count

                                        else:
                                            machine_family_data_stream_day_distinct_value_counts_incl_invalid[machine_data_stream_distinct_value] = \
                                                machine_data_stream_day_distinct_value_count

                                        if (not machine_data_stream_details.is_num) or \
                                                (pandas.notnull(machine_data_stream_distinct_value) and
                                                 (machine_data_stream_details.neg_invalid <
                                                  machine_data_stream_distinct_value <
                                                  machine_data_stream_details.pos_invalid)):
                                            machine_family_data_stream_day_count_excl_invalid += \
                                                machine_data_stream_day_distinct_value_count

                            if machine_family_data_stream_day_count_incl_invalid < day_total_count_incl_invalid:
                                assert not {None, numpy.nan}.issubset(machine_family_data_stream_day_distinct_value_counts_incl_invalid)

                                machine_family_data_stream_day_distinct_value_counts_incl_invalid[numpy.nan] = \
                                    int(day_total_count_incl_invalid - machine_family_data_stream_day_count_incl_invalid)
                                    # ^ cast to int(...) to avoid TypeError: Object of type int64 is not JSON serializable ^

                                machine_family_data_stream_day_count_incl_invalid = day_total_count_incl_invalid

                            if machine_family_data_stream_day_count_excl_invalid \
                                    != machine_family_data_stream_day_total_count_excl_invalid:
                                self.stdout_logger.warning(
                                    msg='*** {}: {}: {}: TOTAL VALUE COUNT EXCL. INVALID {:,} INCONSISTENT WITH DISTINCT VALUE COUNTS INCL. INVALID {} ***'.format(
                                        machine_family_data_stream_day_aggs_arrow_xdf.path,
                                        date,
                                        machine_data_stream_obj,
                                        machine_family_data_stream_day_total_count_excl_invalid,
                                        machine_family_data_stream_day_distinct_value_counts_incl_invalid))

                            _machine_family_data_stream_day_distinct_value_counts_incl_invalid = {}
                            _machine_family_data_stream_day_distinct_value_proportions_incl_invalid = {}

                            _machine_family_data_stream_day_distinct_value_proportions_excl_invalid = {}

                            for machine_data_stream_distinct_value, \
                                    machine_family_data_stream_day_distinct_value_count in \
                                    machine_family_data_stream_day_distinct_value_counts_incl_invalid.items():
                                _machine_family_data_stream_day_distinct_value_counts_incl_invalid[
                                        machine_data_stream_distinct_value] = \
                                    machine_family_data_stream_day_distinct_value_count

                                _machine_family_data_stream_day_distinct_value_proportions_incl_invalid[
                                        machine_data_stream_distinct_value] = \
                                    machine_family_data_stream_day_distinct_value_count / \
                                    machine_family_data_stream_day_count_incl_invalid

                                if pandas.notnull(machine_data_stream_distinct_value) and \
                                        ((not machine_data_stream_details.is_num) or
                                         (machine_data_stream_details.neg_invalid <
                                          machine_data_stream_distinct_value <
                                          machine_data_stream_details.pos_invalid)):
                                    _machine_family_data_stream_day_distinct_value_proportions_excl_invalid[
                                            machine_data_stream_distinct_value] = \
                                        machine_family_data_stream_day_distinct_value_count / \
                                        machine_family_data_stream_day_count_excl_invalid

                            machine_family_data_stream_day_agg.distinct_value_counts_incl_invalid = \
                                _machine_family_data_stream_day_distinct_value_counts_incl_invalid

                            machine_family_data_stream_day_agg.distinct_value_proportions_incl_invalid = \
                                _machine_family_data_stream_day_distinct_value_proportions_incl_invalid

                            machine_family_data_stream_day_agg.distinct_value_proportions_excl_invalid = \
                                _machine_family_data_stream_day_distinct_value_proportions_excl_invalid

                            machine_family_data_stream_day_aggs_for_date_to_bulk_update.add(
                                machine_family_data_stream_day_agg)

                        if machine_data_stream_details.is_num:
                            def weighted_average_quantile(
                                    col_name,
                                    data_valid_indices=None,
                                    return_data_valid_indices=False):
                                if data_valid_indices is None:
                                    data_valid_indices = \
                                        machine_family_data_stream_day_aggs_df[col_name].between(
                                            left=machine_data_stream_details.neg_invalid,
                                            right=machine_data_stream_details.pos_invalid,
                                            inclusive=False)

                                result = numpy.average(
                                            a=machine_family_data_stream_day_aggs_df.loc[
                                                _machine_data_stream_day_count_excl_invalid_pos_indices &
                                                data_valid_indices,
                                                col_name],
                                            axis=None,
                                            weights=machine_data_stream_day_count_excl_invalid_series.loc[
                                                    _machine_data_stream_day_count_excl_invalid_pos_indices &
                                                    data_valid_indices],
                                            returned=False) \
                                    if data_valid_indices.any() \
                                  else None

                                return (result, data_valid_indices) \
                                    if return_data_valid_indices \
                                  else result

                            machine_family_data_stream_day_agg.weighted_average_min, \
                                machine_data_stream_day_min_valid_indices = \
                                weighted_average_quantile(
                                    machine_data_stream_details.day_min_col_name,
                                    return_data_valid_indices=True)

                            machine_family_data_stream_day_agg.weighted_average_robust_min = \
                                weighted_average_quantile(machine_data_stream_details.day_robust_min_col_name)

                            machine_family_data_stream_day_agg.weighted_average_quartile = \
                                weighted_average_quantile(machine_data_stream_details.day_quartile_col_name)

                            machine_family_data_stream_day_agg.weighted_average_median = \
                                weighted_average_quantile(machine_data_stream_details.day_median_col_name)

                            machine_family_data_stream_day_agg.weighted_average_3rd_quartile = \
                                weighted_average_quantile(machine_data_stream_details.day_3rd_quartile_col_name)

                            machine_family_data_stream_day_agg.weighted_average_robust_max = \
                                weighted_average_quantile(machine_data_stream_details.day_robust_max_col_name)

                            machine_family_data_stream_day_agg.weighted_average_max, \
                                machine_data_stream_day_max_valid_indices = \
                                weighted_average_quantile(
                                    machine_data_stream_details.day_max_col_name,
                                    return_data_valid_indices=True)

                            machine_family_data_stream_day_agg.weighted_average_mean = \
                                weighted_average_quantile(
                                    machine_data_stream_details.day_mean_col_name,
                                    data_valid_indices=
                                        machine_data_stream_day_min_valid_indices &
                                        machine_data_stream_day_max_valid_indices)

                            machine_family_data_stream_day_aggs_for_date_to_bulk_update.add(
                                machine_family_data_stream_day_agg)

            # *** Django 2: Can't bulk-create a multi-table inherited model ***
            if machine_family_data_stream_day_aggs_for_date_to_bulk_update:
                self.db.MachineFamilyDataStreamAggs.bulk_update(
                    machine_family_data_stream_day_aggs_for_date_to_bulk_update,

                    fields=('distinct_value_counts_incl_invalid',
                            'distinct_value_proportions_incl_invalid',
                            'distinct_value_proportions_excl_invalid',

                            'weighted_average_min',
                            'weighted_average_robust_min',
                            'weighted_average_quartile',
                            'weighted_average_median',
                            'weighted_average_3rd_quartile',
                            'weighted_average_robust_max',
                            'weighted_average_max',
                            'weighted_average_mean'),

                    batch_size=self._DB_BULK_CREATE_OR_UPDATE_BATCH_SIZE)

            existing_machine_family_data_stream_aggs \
            .filter(
                machine_family_data__date=date) \
            .exclude(
                machine_data_stream__in=machine_family_data_stream_day_aggs_for_date_by_machine_data_stream) \
            .delete()

            existing_machine_data_stream_aggs_for_date = \
                existing_machine_data_stream_aggs \
                .filter(
                    machine_family_data_stream_agg__machine_family_data__date=date)

            machine_data_stream_day_aggs_by_date[date] = \
                machine_data_stream_day_aggs_for_date_by_machine = {}

            for i in tqdm(range(0, _n_aggs_rows_after_dedup, self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)):
                _machine_data_stream_day_aggs_df = \
                    machine_family_data_stream_day_aggs_df.iloc[i:(i + self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)]

                machine_data_stream_day_aggs_for_date_for_batch_to_bulk_update = set()

                for machine_unique_id, row in \
                        tqdm(_machine_data_stream_day_aggs_df.iterrows(),
                             total=len(_machine_data_stream_day_aggs_df)):
                    machine = machines[machine_unique_id]

                    machine_data_stream_day_aggs_for_date_by_machine[machine] = \
                        machine_data_stream_day_aggs_for_date_for_machine_by_machine_family_data_stream_agg = {}

                    day_count_incl_invalid = row[self._DAY_AGG_SUFFIXES.COUNT_INCL_INVALID]

                    for machine_data_stream_name, machine_data_stream_details in machine_data_streams.items():
                        machine_data_stream_obj = machine_data_stream_details.obj

                        if has_day_count_excl_invalid[machine_data_stream_name] and has_pos_day_count_excl_invalid[machine_data_stream_name]:
                            machine_data_stream_day_count_excl_invalid = \
                                row[machine_data_stream_details.day_count_excl_invalid_col_name]
                            assert pandas.notnull(machine_data_stream_day_count_excl_invalid)

                            if machine_data_stream_day_count_excl_invalid:
                                machine_family_data_stream_agg = \
                                    machine_family_data_stream_day_aggs_for_date_by_machine_data_stream[machine_data_stream_obj]

                                machine_data_stream_day_aggs_for_date_for_machine_by_machine_family_data_stream_agg[machine_family_data_stream_agg] = \
                                    machine_data_stream_day_agg = \
                                    self.db.MachineDataStreamAggs.update_or_create(
                                        machine_family_data_stream_agg=machine_family_data_stream_agg,
                                        machine=machine,
                                        defaults=dict(
                                                    count_incl_invalid=day_count_incl_invalid,
                                                    count_excl_invalid=machine_data_stream_day_count_excl_invalid))[0]

                                if has_day_list[machine_data_stream_name]:
                                    machine_data_stream_day_distinct_value_counts_incl_invalid = \
                                        row[machine_data_stream_details.day_distinct_value_counts_incl_invalid_col_name]

                                    machine_family_data_stream_day_count_incl_invalid = \
                                        sum(machine_data_stream_day_distinct_value_counts_incl_invalid.values())

                                    if machine_family_data_stream_day_count_incl_invalid < day_count_incl_invalid:
                                        assert not {None, numpy.nan}.issubset(machine_data_stream_day_distinct_value_counts_incl_invalid)

                                        machine_data_stream_day_distinct_value_counts_incl_invalid[numpy.nan] = \
                                            int(day_count_incl_invalid - machine_family_data_stream_day_count_incl_invalid)
                                            # ^ cast to int(...) to avoid TypeError: Object of type int64 is not JSON serializable ^

                                        machine_family_data_stream_day_count_incl_invalid = day_count_incl_invalid

                                    assert machine_data_stream_day_count_excl_invalid \
                                        == sum(machine_data_stream_day_distinct_value_count
                                               for machine_data_stream_distinct_value,
                                                    machine_data_stream_day_distinct_value_count in
                                                    machine_data_stream_day_distinct_value_counts_incl_invalid.items()
                                               if pandas.notnull(machine_data_stream_distinct_value) and
                                                    ((not machine_data_stream_details.is_num) or
                                                     (machine_data_stream_details.neg_invalid <
                                                      machine_data_stream_distinct_value <
                                                      machine_data_stream_details.pos_invalid))), \
                                        '*** {}: {}: {}: {}: TOTAL VALID VALUE COUNT {:,} INCONSISTENT WITH DISTINCT VALUE COUNTS {} ***'.format(
                                            machine_family_data_stream_day_aggs_arrow_xdf.path,
                                            date,
                                            machine_unique_id,
                                            machine_data_stream_obj,
                                            machine_data_stream_day_count_excl_invalid,
                                            machine_data_stream_day_distinct_value_counts_incl_invalid)

                                    machine_data_stream_day_agg.distinct_value_counts_incl_invalid = \
                                        machine_data_stream_day_distinct_value_counts_incl_invalid

                                    machine_data_stream_day_agg.distinct_value_proportions_incl_invalid = \
                                        {machine_data_stream_distinct_value:
                                            machine_data_stream_day_distinct_value_count /
                                            machine_family_data_stream_day_count_incl_invalid
                                         for machine_data_stream_distinct_value,
                                             machine_data_stream_day_distinct_value_count in
                                            machine_data_stream_day_distinct_value_counts_incl_invalid.items()}

                                    machine_data_stream_day_agg.distinct_value_proportions_excl_invalid = \
                                        {machine_data_stream_distinct_value:
                                            machine_data_stream_day_distinct_value_count /
                                            machine_data_stream_day_count_excl_invalid
                                         for machine_data_stream_distinct_value,
                                            machine_data_stream_day_distinct_value_count in
                                            machine_data_stream_day_distinct_value_counts_incl_invalid.items()
                                         if (not machine_data_stream_details.is_num) or
                                            (pandas.notnull(machine_data_stream_distinct_value) and
                                             (machine_data_stream_details.neg_invalid <
                                              machine_data_stream_distinct_value <
                                              machine_data_stream_details.pos_invalid))}

                                    machine_data_stream_day_aggs_for_date_for_batch_to_bulk_update.add(
                                        machine_data_stream_day_agg)

                                if machine_data_stream_details.is_num:
                                    machine_data_stream_day_agg.min = \
                                        row[machine_data_stream_details.day_min_col_name]

                                    machine_data_stream_day_agg.robust_min = \
                                        row[machine_data_stream_details.day_robust_min_col_name]

                                    machine_data_stream_day_agg.quartile = \
                                        row[machine_data_stream_details.day_quartile_col_name]

                                    machine_data_stream_day_agg.median = \
                                        row[machine_data_stream_details.day_median_col_name]

                                    machine_data_stream_day_agg.mean = \
                                        row[machine_data_stream_details.day_mean_col_name]

                                    machine_data_stream_day_agg._3rd_quartile = \
                                        row[machine_data_stream_details.day_3rd_quartile_col_name]

                                    machine_data_stream_day_agg.robust_max = \
                                        row[machine_data_stream_details.day_robust_max_col_name]

                                    machine_data_stream_day_agg.max = \
                                        row[machine_data_stream_details.day_max_col_name]

                                    machine_data_stream_day_aggs_for_date_for_batch_to_bulk_update.add(
                                        machine_data_stream_day_agg)

                    existing_machine_data_stream_aggs_for_date \
                    .filter(
                        machine=machine) \
                    .exclude(
                        machine_family_data_stream_agg__in=machine_data_stream_day_aggs_for_date_for_machine_by_machine_family_data_stream_agg) \
                    .delete()

                    # free up memory
                    machine_data_stream_day_aggs_for_date_by_machine[machine] = None

                # *** Django 2: Can't bulk-create a multi-table inherited model ***
                if machine_data_stream_day_aggs_for_date_for_batch_to_bulk_update:
                    self.stdout_logger.debug(
                        msg='*** BULK-UPDATING {:,} Machine Data Stream Aggs... ***'.format(
                            len(machine_data_stream_day_aggs_for_date_for_batch_to_bulk_update)))

                    self.db.MachineDataStreamAggs.bulk_update(
                        machine_data_stream_day_aggs_for_date_for_batch_to_bulk_update,

                        fields=('distinct_value_counts_incl_invalid',
                                'distinct_value_proportions_incl_invalid',
                                'distinct_value_proportions_excl_invalid',

                                'min',
                                'robust_min',
                                'quartile',
                                'median',
                                'mean',
                                '_3rd_quartile',
                                'robust_max',
                                'max'),

                        batch_size=self._DB_BULK_CREATE_OR_UPDATE_BATCH_SIZE)

            existing_machine_data_stream_aggs_for_date \
            .exclude(
                machine__in=machine_data_stream_day_aggs_for_date_by_machine) \
            .delete()

            # free up memory
            machine_family_data_stream_day_aggs_by_date[date] = None
            machine_data_stream_day_aggs_by_date[date] = None

        if to_date:
            self.stdout_logger.warning(
                msg='*** DELETING STALE MachineFamilyDataStreamAggs... ***')

            self.stdout_logger.info(
                msg='{}'.format(
                    existing_machine_family_data_stream_aggs
                    .filter(
                        machine_family_data__date__range=(date, to_date))
                    .exclude(
                        machine_family_data__date__in=machine_family_data_stream_day_aggs_by_date)
                    .delete()))

            self.stdout_logger.warning(
                msg='*** DELETING STALE MachineDataStreamAggs... ***')

            self.stdout_logger.info(
                msg='{}'.format(
                    existing_machine_data_stream_aggs
                    .filter(
                        machine_family_data_stream_agg__machine_family_data__date__range=(date, to_date))
                    .exclude(
                        machine_family_data_stream_agg__machine_family_data__date__in=machine_family_data_stream_day_aggs_by_date)
                    .delete()))

    def viz_machine_family_data_stream_wt_avg_day_aggs(
            self,
            machine_class_name, machine_family_name,
            s3_dir_path_prefix='.arimo/PredMaint/viz/equipment-data-field-weighted-average-daily-aggs'   # TODO: update
        ):
        WT_AVG_COL_NAME = 'Weighted Average'
        DAY_AGG_COL_NAME = 'Daily Aggregate'

        dir_name = \
            self.machine_family_conventional_full_name(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name)

        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        machine_data_streams = machine_family.machine_class.machine_data_streams.all()
        assert machine_data_streams.count()

        _tmp_dir_path = tempfile.mkdtemp()

        for machine_data_stream in tqdm(machine_data_streams, total=machine_data_streams.count()):
            machine_family_data_stream_wt_avg_day_aggs_df = \
                pandas.DataFrame(
                    data=self.db.MachineFamilyDataStreamAggs.filter(
                            machine_family=machine_family,
                            machine_data_stream=machine_data_stream)
                        .values(
                            DATE_COL,
                            'weighted_average_min',
                            'weighted_average_robust_min',
                            'weighted_average_quartile',
                            'weighted_average_mean',
                            'weighted_average_median',
                            'weighted_average_3rd_quartile',
                            'weighted_average_robust_max',
                            'weighted_average_max')) \
                .rename(
                    columns=dict(weighted_average_min='0.000: Min',
                                 weighted_average_robust_min='0.005: Robust Min',
                                 weighted_average_quartile='0.25: Quartile',
                                 weighted_average_mean='0.5: Median',
                                 weighted_average_median='Mean',
                                 weighted_average_3rd_quartile='0.75: 3rd Quartile',
                                 weighted_average_robust_max='0.995: Robust Max',
                                 weighted_average_max='1: Max'))

            if len(machine_family_data_stream_wt_avg_day_aggs_df):
                plot = \
                    ggplot(
                        aes(x=DATE_COL,
                            y=WT_AVG_COL_NAME,
                            color=DAY_AGG_COL_NAME,
                            group=DAY_AGG_COL_NAME),
                        data=pandas.melt(
                                frame=machine_family_data_stream_wt_avg_day_aggs_df,
                                id_vars=[DATE_COL],
                                value_vars=None,
                                var_name=DAY_AGG_COL_NAME,
                                value_name=WT_AVG_COL_NAME,
                                col_level=None)) + \
                    geom_line() + \
                    scale_x_datetime(
                        date_breaks='1 month',
                        date_labels='%Y-%m') + \
                    ggtitle(str(machine_data_stream)) + \
                    theme(axis_text_x=element_text(rotation=90))

                file_name = '{}.png'.format(machine_data_stream.name)

                plot.save(
                    filename=file_name,
                    path=_tmp_dir_path,
                    width=None, height=None, dpi=300,
                    verbose=False)

            else:
                self.stdout_logger.warning(
                    msg='*** {}: NO AGG DATA TO VISUALIZE ***'.format(machine_data_stream))

        s3.sync(
            from_dir_path=_tmp_dir_path,
            to_dir_path=
                os.path.join(
                    self.params.s3.bucket_path,
                    s3_dir_path_prefix,
                    dir_name),
            delete=True,
            quiet=True,
            access_key_id=self.params.s3.access_key_id,
            secret_access_key=self.params.s3.secret_access_key,
            verbose=True)

        fs.rm(
            path=_tmp_dir_path,
            hdfs=False,
            is_dir=True)

    def _force_conso_and_agg_and_viz_machine_family_data(
            self,
            machine_class_name, machine_family_name,
            date, to_date=None):
        self.conso_machine_family_data(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name,
            date=date, to_date=to_date,
            _force_re_conso=True)

        self.agg_machine_family_day_data(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name,
            date=date, to_date=to_date, monthly=False,
            _force_re_agg=True)

        self.machine_family_data_stream_day_aggs_to_db(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name,
            date=date, to_date=to_date,
            monthly=False)

        self.viz_machine_family_data_stream_wt_avg_day_aggs(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name)

    # *** BELOW METHODS ARE EXPERIMENTAL >>>
    def update_or_create_equipment_unique_type_group(
            self, equipment_general_type_name, equipment_unique_type_group_name,
            equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set()):
        equipment_unique_type_group = \
            self.data.EquipmentUniqueTypeGroups.get_or_create(
                equipment_general_type=
                self.equipment_general_type(
                    equipment_general_type_name=equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_group_name))[0]

        if equipment_unique_type_names_excl or equipment_unique_type_names_incl:
            equipment_unique_type_names_excl = \
                {clean_lower_str(equipment_unique_type_names_excl)} \
                    if isinstance(equipment_unique_type_names_excl, _STR_CLASSES) \
                    else {clean_lower_str(equipment_unique_type_name)
                          for equipment_unique_type_name in equipment_unique_type_names_excl}

            equipment_unique_types = []
            equipment_unique_type_names = []

            for equipment_unique_type in \
                    equipment_unique_type_group.equipment_unique_types.filter(
                        equipment_general_type__name=clean_lower_str(equipment_general_type_name)):
                equipment_unique_type_name = equipment_unique_type.name
                if equipment_unique_type_name not in equipment_unique_type_names_excl:
                    equipment_unique_types.append(equipment_unique_type)
                    equipment_unique_type_names.append(equipment_unique_type_name)

            for equipment_unique_type_name in \
                    ({clean_lower_str(equipment_unique_type_names_incl)}
                    if isinstance(equipment_unique_type_names_incl, _STR_CLASSES)
                    else {clean_lower_str(equipment_unique_type_name)
                          for equipment_unique_type_name in equipment_unique_type_names_incl}) \
                            .difference(equipment_unique_type_names_excl, equipment_unique_type_names):
                equipment_unique_types.append(
                    self.update_or_create_equipment_unique_type(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_unique_type_name=equipment_unique_type_name))

            equipment_unique_type_group.equipment_unique_types = equipment_unique_types

            equipment_unique_type_group.save()

        return equipment_unique_type_group

    def update_or_create_equipment_unique_type(
            self, equipment_general_type_name, equipment_unique_type_name,
            equipment_unique_type_group_names_incl=set(), equipment_unique_type_group_names_excl=set()):
        equipment_unique_type = \
            self.data.EquipmentUniqueTypes.get_or_create(
                equipment_general_type=
                self.get_or_create_equipment_general_type(
                    equipment_general_type_name=equipment_general_type_name),
                name=clean_lower_str(equipment_unique_type_name))[0]

        if equipment_unique_type_group_names_excl or equipment_unique_type_group_names_incl:
            equipment_unique_type_group_names_excl = \
                {clean_lower_str(equipment_unique_type_group_names_excl)} \
                    if isinstance(equipment_unique_type_group_names_excl, _STR_CLASSES) \
                    else {clean_lower_str(equipment_unique_type_group_name)
                          for equipment_unique_type_group_name in equipment_unique_type_group_names_excl}

            equipment_unique_type_groups = []
            equipment_unique_type_group_names = []

            for equipment_unique_type_group in \
                    equipment_unique_type.groups.filter(
                        equipment_general_type__name=clean_lower_str(equipment_general_type_name)):
                equipment_unique_type_group_name = equipment_unique_type_group.name
                if equipment_unique_type_group_name not in equipment_unique_type_group_names_excl:
                    equipment_unique_type_groups.append(equipment_unique_type_group)
                    equipment_unique_type_group_names.append(equipment_unique_type_group_name)

            for equipment_unique_type_group_name in \
                    ({clean_lower_str(equipment_unique_type_group_names_incl)}
                    if isinstance(equipment_unique_type_group_names_incl, _STR_CLASSES)
                    else {clean_lower_str(equipment_unique_type_group_name)
                          for equipment_unique_type_group_name in equipment_unique_type_group_names_incl}) \
                            .difference(equipment_unique_type_group_names_excl, equipment_unique_type_group_names):
                equipment_unique_type_groups.append(
                    self.update_or_create_equipment_unique_type_group(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_unique_type_group_name=equipment_unique_type_group_name))

            equipment_unique_type.groups = equipment_unique_type_groups

            equipment_unique_type.save()

        return equipment_unique_type

    def update_or_create_equipment_data_field(
                self, equipment_general_type_name, equipment_data_field_name, equipment_data_field_type='measure', cat=None,
                equipment_unique_type_names_incl=set(), equipment_unique_type_names_excl=set(),
                **kwargs):
        equipment_data_field_types = \
                dict(control=self.CONTROL_EQUIPMENT_DATA_FIELD_TYPE,
                     measure=self.MEASURE_EQUIPMENT_DATA_FIELD_TYPE,
                     calc=self.CALC_EQUIPMENT_DATA_FIELD_TYPE,
                     alarm=self.ALARM_EQUIPMENT_DATA_FIELD_TYPE)

        if cat is not None:
            kwargs['data_type'] = \
                self.CAT_DATA_TYPE \
                    if cat \
                    else self.NUM_DATA_TYPE

        equipment_data_field = \
            self.data.EquipmentDataFields.update_or_create(
                equipment_general_type=
                self.equipment_general_type(
                    equipment_general_type_name=equipment_general_type_name),
                equipment_data_field_type=
                equipment_data_field_types[equipment_data_field_type],
                name=clean_lower_str(equipment_data_field_name),
                defaults=kwargs)[0]

        if equipment_unique_type_names_excl or equipment_unique_type_names_incl:
            equipment_unique_type_names_excl = \
                {clean_lower_str(equipment_unique_type_names_excl)} \
                    if isinstance(equipment_unique_type_names_excl, _STR_CLASSES) \
                    else {clean_lower_str(equipment_unique_type_name)
                          for equipment_unique_type_name in equipment_unique_type_names_excl}

            equipment_unique_types = []
            equipment_unique_type_names = []

            for equipment_unique_type in \
                    equipment_data_field.equipment_unique_types.filter(
                        equipment_general_type__name=clean_lower_str(equipment_general_type_name)):
                equipment_unique_type_name = equipment_unique_type.name
                if equipment_unique_type_name not in equipment_unique_type_names_excl:
                    equipment_unique_types.append(equipment_unique_type)
                    equipment_unique_type_names.append(equipment_unique_type_name)

            for equipment_unique_type_name in \
                    ({clean_lower_str(equipment_unique_type_names_incl)}
                    if isinstance(equipment_unique_type_names_incl, _STR_CLASSES)
                    else {clean_lower_str(equipment_unique_type_name)
                          for equipment_unique_type_name in equipment_unique_type_names_incl}) \
                            .difference(equipment_unique_type_names_excl, equipment_unique_type_names):
                equipment_unique_types.append(
                    self.equipment_unique_type(
                        equipment_general_type_name=equipment_general_type_name,
                        equipment_unique_type_name=equipment_unique_type_name))

            equipment_data_field.equipment_unique_types = equipment_unique_types

            equipment_data_field.save()

        return equipment_data_field

    def update_or_create_equipment_instance(
            self, equipment_general_type_name, name, equipment_unique_type_name=None,
            **kwargs):
        if equipment_unique_type_name:
            kwargs['equipment_unique_type'] = \
                self.update_or_create_equipment_unique_type(
                    equipment_general_type_name=equipment_general_type_name,
                    equipment_unique_type_name=equipment_unique_type_name)

        try:
            equipment_instance = \
                self.data.EquipmentInstances.update_or_create(
                    equipment_general_type=
                    self.equipment_general_type(
                        equipment_general_type_name=equipment_general_type_name),
                    name=clean_lower_str(name),
                    defaults=kwargs)[0]

        except Exception as err:
            print('*** {} #{} ***'.format(equipment_general_type_name, name))
            raise err

        return equipment_instance
    
    def check_equipment_data_integrity(self, equipment_instance_id_or_data_set_name):
        from arimo.data.distributed_parquet import S3ParquetDistributedDataFrame
        from arimo.util.date_time import DATE_COL
        from arimo.util.types.spark_sql import _DATE_TYPE

        file_adf = \
            S3ParquetDistributedDataFrame(
                path=os.path.join(
                    self.params.s3.equipment_data.dir_path,
                    equipment_instance_id_or_data_set_name + _PARQUET_EXT),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=None, tCol=None,
                verbose=True)

        assert file_adf.type(DATE_COL) == _DATE_TYPE, \
            '*** Date Col not of Date Type (likely because of NULL Date-Times) ***'

        equipment_instance_ids = \
            file_adf('SELECT DISTINCT {} FROM this'
                     .format(self._EQUIPMENT_INSTANCE_ID_COL_NAME)) \
                .toPandas().iloc[:, 0]

        non_compliant_equipment_instance_ids = \
            {equipment_instance_id
             for equipment_instance_id in equipment_instance_ids
             if clean_lower_str(equipment_instance_id) != equipment_instance_id}

        if non_compliant_equipment_instance_ids:
            print('*** NON-COMPLIANT EQUIPMENT INSTANCE IDs: {} ***'.format(non_compliant_equipment_instance_ids))

        equipment_instance_ids_w_dups = \
            {equipment_instance_id
             for equipment_instance_id, count in
             Counter([clean_lower_str(equipment_instance_id)
                      for equipment_instance_id in equipment_instance_ids]).items()
             if count > 1}

        if equipment_instance_ids_w_dups:
            print('*** DUPLICATED EQUIPMENT INSTANCE IDs: {} ***'.format(equipment_instance_ids_w_dups))

    def equipment_unique_type_names(self, equipment_general_type_name):
        return sorted(
            equipment_unique_type.name
            for equipment_unique_type in
            self.data.EquipmentUniqueTypes.filter(
                equipment_general_type__name=clean_lower_str(equipment_general_type_name)))

    def equipment_unique_type_names_and_equipment_data_field_names(self, equipment_general_type_name):
        return {equipment_unique_type.name:
                    {equipment_data_field.name
                     for equipment_data_field in equipment_unique_type.data_fields.all()}
                for equipment_unique_type in
                self.data.EquipmentUniqueTypes.filter(
                    equipment_general_type__name=clean_lower_str(equipment_general_type_name))}

    def associated_equipment_instances(self, equipment_instance_name, from_date=None, to_date=None):
        kwargs = {}

        if from_date:
            kwargs['date__gte'] = datetime.strptime(from_date, "%Y-%m-%d").date()

        if to_date:
            kwargs['date__lte'] = datetime.strptime(to_date, "%Y-%m-%d").date()

        equipment_systems = \
            self.data.EquipmentSystems.filter(
                equipment_instances__name=clean_lower_str(equipment_instance_name))

        if equipment_systems:
            return equipment_systems[0].equipment_instances.all().union(
                *(equipment_system.equipment_instances.all()
                  for equipment_system in equipment_systems[1:]),
                all=False)

        else:
            return self.data.EquipmentInstances.filter(
                name=clean_lower_str(equipment_instance_name))

    def test_equipment_data_date_vs_date_time(self, equipment_instance_id_or_data_set_name):
        from pyspark.sql.functions import to_date
        from arimo.util.date_time import DATE_COL

        equipment_data_adf = \
            self.load_equipment_data(
                equipment_instance_id_or_data_set_name=equipment_instance_id_or_data_set_name,
                _from_files=True, _spark=True,
                set_i_col=False, set_t_col=False,
                verbose=True) \
                [[self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                  DATE_COL,
                  self._DATE_TIME_COL_NAME]]

        equipment_data_adf_w_diff_date_vs_date_time = \
            equipment_data_adf.filter(
                to_date(equipment_data_adf[self._DATE_TIME_COL_NAME])
                != equipment_data_adf[DATE_COL])

        equipment_data_adf_w_diff_date_vs_date_time.cache()

        if equipment_data_adf_w_diff_date_vs_date_time.nRows:
            path = 's3://{}/tmp/{}---DATE-vs-DATE-TIME{}'.format(
                self.params.s3.bucket,
                equipment_instance_id_or_data_set_name,
                _JSON_EXT)

            equipment_data_adf_w_diff_date_vs_date_time.repartition(1).save(
                path=path,
                format='json',
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key)

            raise ValueError('*** ERRONEOUS ROWS SAVED TO "{}" ***'.format(path))

    def _equipment_general_types_n_equipment_data_fields(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_data_fields=Count('equipment_data_field'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_data_fields'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_data_fields == 0] \
            if only0 \
            else df

    def _equipment_general_types_n_equipment_unique_type_groups(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_unique_type_groups=Count('equipment_unique_type_group'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_unique_type_groups'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_type_groups == 0] \
            if only0 \
            else df

    def _equipment_general_types_n_equipment_unique_types(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_unique_types=Count('equipment_unique_type'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_unique_types'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_types == 0] \
            if only0 \
            else df

    def _equipment_general_types_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentGeneralTypes
                .values('name')
                .annotate(n_equipment_instances=Count('equipment_instance'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
            else df

    def _equipment_data_fields_n_equipment_unique_types(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentDataFields
                .values('equipment_general_type__name', 'equipment_data_field_type__name', 'name')
                .annotate(n_equipment_unique_types=Count('equipment_unique_types'))
                .order_by('equipment_general_type__name', 'equipment_data_field_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'equipment_data_field_type__name', 'name', 'n_equipment_unique_types'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_types == 0] \
            if only0 \
            else df

    def _equipment_data_fields_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentDataFields
                .values('equipment_general_type__name', 'equipment_data_field_type__name', 'name')
                .annotate(n_equipment_instances=Count('equipment_instance'))
                .order_by('equipment_general_type__name', 'equipment_data_field_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'equipment_data_field_type__name', 'name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
            else df

    def _equipment_unique_type_groups_n_equipment_unique_types(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentUniqueTypeGroups
                .values('equipment_general_type__name', 'name')
                .annotate(n_equipment_unique_types=Count('equipment_unique_types'))
                .order_by('equipment_general_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'name', 'n_equipment_unique_types'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_types == 0] \
            if only0 \
            else df

    def _equipment_unique_types_n_equipment_unique_type_groups(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentUniqueTypes
                .values('equipment_general_type__name', 'name')
                .annotate(n_equipment_unique_type_groups=Count('groups'))
                .order_by('equipment_general_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'name', 'n_equipment_unique_type_groups'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_unique_type_groups == 0] \
            if only0 \
            else df

    def _equipment_unique_types_n_equipment_data_fields(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentUniqueTypes
                .values('equipment_general_type__name', 'name')
                .annotate(n_equipment_data_fields=Count('data_fields'))
                .order_by('equipment_general_type__name', 'name'),
            index=None,
            exclude=None,
            columns=['equipment_general_type__name', 'name', 'n_equipment_data_fields'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_data_fields == 0] \
            if only0 \
            else df

    def _equipment_data_field_names_n_counts(self, only_multi=True):
        d = {(i['equipment_general_type__name'], i['name']): i['n']
             for i in self.data.EquipmentDataFields
                 .values('equipment_general_type__name', 'name')
                 .annotate(n=Count('name'))
                 .order_by('equipment_general_type__name', 'name')}

        return {k: v
                for k, v in d.items()
                if v > 1} \
            if only_multi \
            else d

    def _equipment_facilities_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentFacilities
                .values('name')
                .annotate(n_equipment_instances=Count('equipment_instance'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
            else df

    def _equipment_facilities_n_equipment_systems(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentFacilities
                .values('name')
                .annotate(n_equipment_systems=Count('equipment_system'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_systems'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_systems == 0] \
            if only0 \
            else df

    def _equipment_systems_n_equipment_instances(self, only0=True):
        df = pandas.DataFrame.from_records(
            data=self.data.EquipmentSystems
                .values('name')
                .annotate(n_equipment_instances=Count('equipment_instances'))
                .order_by('name'),
            index=None,
            exclude=None,
            columns=['name', 'n_equipment_instances'],
            coerce_float=False,
            nrows=None)

        return df.loc[df.n_equipment_instances == 0] \
            if only0 \
            else df
    
    def _load_equipment_instance_data(
            self,
            equipment_instance_name,
            equipment_general_type_name=None, equipment_unique_type_group_name=None,
            date=None, to_date=None):
        from arimo.data.parquet import S3ParquetDataFeeder
        from arimo.data.distributed import DDF
        from arimo.data.distributed_parquet import S3ParquetDistributedDataFrame
        from arimo.util.date_time import DATE_COL

        if equipment_general_type_name or equipment_unique_type_group_name:
            assert equipment_general_type_name and equipment_unique_type_group_name

            equipment_instance_id_or_data_set_name = \
                '{}---{}'.format(
                    equipment_general_type_name.upper(),
                    equipment_unique_type_group_name)

            if date and (not to_date):
                return DDF.load(
                    path=os.path.join(
                        self.params.s3.equipment_data.dir_path,
                        equipment_instance_id_or_data_set_name + _PARQUET_EXT,
                        '{}={}'.format(DATE_COL, date)),
                    mergeSchema=True,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=None,
                    tCol=None,
                    verbose=True) \
                    .filter(
                    condition='{}={}'.format(
                        self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                        equipment_instance_name))

            else:
                s3_parquet_ddf = \
                    self.load_equipment_data(
                        equipment_instance_id_or_data_set_name,
                        _from_files=True,
                        _spark=True,
                        set_i_col=False,
                        set_t_col=False)

                if date and to_date:
                    s3_parquet_ddf = \
                        s3_parquet_ddf.filterByPartitionKeys(
                            (DATE_COL,
                             date,
                             to_date))

                return s3_parquet_ddf.filter(
                    condition="{}='{}'".format(
                        self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                        equipment_instance_name))

        elif date and (not to_date):
            return S3ParquetDataFeeder(
                path=os.path.join(
                    self.params.s3.equipment_data.raw_dir_path,
                    '{}={}'.format(
                        self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                        equipment_instance_name),
                    '{}={}'.format(DATE_COL, date)),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=None,
                tCol=None,
                verbose=True)

        else:
            s3_parquet_df = \
                S3ParquetDataFeeder(
                    path=os.path.join(
                        self.params.s3.equipment_data.raw_dir_path,
                        '{}={}'.format(
                            self._EQUIPMENT_INSTANCE_ID_COL_NAME,
                            equipment_instance_name)),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=None,
                    tCol=None,
                    verbose=True)

            return s3_parquet_df.filterByPartitionKeys((DATE_COL, date, to_date)) \
                if date and to_date \
              else s3_parquet_df

    def rm_s3_tmp(self):
        assert self.params.s3.bucket

        s3.rm(path='s3://{}/{}'.format(self.params.s3.bucket, ArrowXDF._TMP_DIR_S3_KEY),
              dir=True,
              access_key_id=self.params.s3.access_key_id,
              secret_access_key=self.params.s3.secret_access_key,
              quiet=True,
              verbose=True)
