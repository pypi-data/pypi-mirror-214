__all__ = \
    'EnvVar', 'EnvironmentVariable'


import logging
import pandas
import sys

from django.core.serializers.json import DjangoJSONEncoder

from django.db.models.base import Model

from django.db.models.constraints import \
    CheckConstraint, \
    UniqueConstraint

from django.db.models.deletion import \
    PROTECT, SET_DEFAULT, SET, DO_NOTHING

from django.db.models.fields import \
    BigIntegerField, \
    CharField, \
    DateField, \
    FloatField, \
    PositiveIntegerField, PositiveSmallIntegerField, \
    TextField, \
    URLField

from django.db.models.fields.json import JSONField

from django.db.models.fields.related import \
    ForeignKey, ManyToManyField, OneToOneField

from django.db.models.signals import m2m_changed, post_save, pre_delete

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.postgres.constraints import ExclusionConstraint

from django.contrib.postgres.fields.citext import CICharField
from django.contrib.postgres.fields.hstore import HStoreField
from django.contrib.postgres.fields.ranges import BigIntegerRangeField, DecimalRangeField

from django.contrib.postgres.indexes import \
    BrinIndex, \
    BTreeIndex, \
    GinIndex, \
    GistIndex, \
    HashIndex, \
    SpGistIndex
    # TODO (Django 3): BloomIndex

from django_util.models import \
    PGSQL_IDENTIFIER_MAX_LEN, \
    _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC, \
    _ModelWithIntPKMixInABC, _ModelWithBigIntPKMixInABC, \
    _ModelWithCreatedAndUpdatedMixInABC, \
    _ModelWithNullableDateMixInABC, \
    _ModelWithAutoCompleteSearchFieldsMixInABC, \
    _EnvVarABC

from psycopg2.extras import NumericRange

from ..util import MAX_CHAR_FLD_LEN, IterableStrType, coerce_int, format_number_up_to_n_decimal_places, snake_case
from . import \
    DeviceDataStreamTypeChoices, \
    LogicalDataTypeChoices, \
    PhysicalDataTypeMinChoices, PhysicalDataTypeMaxChoices
from .apps import DeviceDataConfig


# logger
LOGGER = logging.getLogger(name=__name__)
LOGGER.setLevel(logging.INFO)

STDOUT_HANDLER = \
    logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setFormatter(
    logging.Formatter(
        fmt='%(levelname)s   %(name)s:   %(message)s\n'))
LOGGER.addHandler(STDOUT_HANDLER)


# M2M actions
M2M_CHANGED_PRE_ADD_ACTION = 'pre_add'   # sent before one or more objects are added to the relation
M2M_CHANGED_POST_ADD_ACTION = 'post_add'   # sent after one or more objects are added to the relation
M2M_CHANGED_PRE_REMOVE_ACTION = 'pre_remove'   # sent before one or more objects are removed from the relation
M2M_CHANGED_POST_REMOVE_ACTION = 'post_remove'   # sent after one or more objects are removed from the relation
M2M_CHANGED_PRE_CLEAR_ACTION = 'pre_clear'   # sent before the relation is cleared
M2M_CHANGED_POST_CLEAR_ACTION = 'post_clear'   # sent after the relation is cleared


# App Label
APP_LABEL = DeviceDataConfig.label


class _ModelWithDeviceSKUsM2MMixInABC(Model):
    machine_skus = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='DeviceSKU',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device SKUs',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device SKUs',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            # related_query_name='%(class)s',
            limit_choices_to=None,
            symmetrical=False,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    class Meta:
        abstract = True


class DeviceComponentBlobData(
        _ModelWithDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_component_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='DeviceComponent_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Device Component Blob Data'


class DeviceComponent(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithDeviceSKUsM2MMixInABC,
        DeviceComponentBlobData,
        _ModelWithDeviceClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_components'
    RELATED_QUERY_NAME = 'machine_component'

    name = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Component Name',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Component',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    machine_families = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='DeviceFamily',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Families',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Families',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through='DeviceFamilyComponent',
            through_fields=('machine_component', 'machine_family'),
            db_table=None,
            db_constraint=True,
            swappable=True)

    # ref: https://stackoverflow.com/questions/19837728/django-manytomany-relation-to-self-without-backward-relations
    directly_interacting_components = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='self',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Directly-Interacting Components',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Directly-Interacting Components',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME + '_directly_interacting',
            related_query_name=RELATED_QUERY_NAME + '_directly_interacting',
            limit_choices_to=None,
            symmetrical=True,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    sub_components = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='self',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Sub-Components',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Sub-Components',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME + '_super',
            related_query_name=RELATED_QUERY_NAME + '_super',
            limit_choices_to=None,
            symmetrical=False,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_data_streams = \
        ManyToManyField(  # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='DeviceDataStream',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Data Streams',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Data Streams',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',
            
            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_components'

        ordering = \
            'machine_class__name', \
            'name'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = f'{_MODEL_OBJECT_NAME}_machine_class_and_name_unique_together'

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_class', 'name'),
                name=_CONSTRAINT_NAME,
                condition=None),
        
        verbose_name = 'Device Component'
        verbose_name_plural = 'Device Components'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} Component {}{}{}{}\n'.format(
                self.machine_class.name.upper(),
                self.name.upper(),

                '\n - Interacts with: {}'.format(
                        [directly_interacting_component.name
                         for directly_interacting_component in self.directly_interacting_components.all()])
                    if self.directly_interacting_components.count()
                    else '',

                '\n- Contains: {}'.format(
                        [sub_component.name
                         for sub_component in self.sub_components.all()])
                    if self.sub_components.count()
                    else '',

                '\n- Data Streams: {}'.format(
                        [machine_data_stream.name
                         for machine_data_stream in self.machine_data_streams.all()])
                    if self.machine_data_streams.count()
                    else '')

    def save(self, *args, **kwargs) -> None:
        self.name = snake_case(self.name)
        assert self.name

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in DeviceClass.search_fields()] + \
               ['name',
                'descriptions']


class DeviceDataStreamBlobData(
        _ModelWithDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_data_stream_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='DeviceDataStream_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Device Data Stream Blob Data'


class DeviceDataStream(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithDeviceSKUsM2MMixInABC,
        DeviceDataStreamBlobData,
        _ModelWithDeviceClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_data_streams'
    RELATED_QUERY_NAME = 'machine_data_stream'

    name = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Data Stream Name',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data Stream',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    machine_data_stream_type = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=DeviceDataStreamTypeChoices.choices,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=DeviceDataStreamTypeChoices.SENSOR,
            editable=True,
            # error_messages={},
            help_text='Device Data Stream Type',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data Stream Type',
            # validators=(),

            max_length=max(len(value)
                           for value in DeviceDataStreamTypeChoices))

    logical_data_type = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=True,
            blank=True,
            choices=LogicalDataTypeChoices.choices,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Logical Data Type',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Logical Data Type',
            # validators=(),

            max_length=max(len(value)
                           for value in LogicalDataTypeChoices))

    physical_data_type = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=PhysicalDataType,
            on_delete=PROTECT,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Physical Data Type',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Physical Data Type',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    measurement_unit = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=MeasurementUnit,
            on_delete=PROTECT,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Measurement Unit',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Measurement Unit',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    neg_invalid = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=PhysicalDataTypeMinChoices.NEG_POW_2_30,
            editable=True,
            # error_messages={},
            help_text='Negative Invalid Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Negative Invalid Numerical Value',
            # validators=()
        )

    pos_invalid = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=PhysicalDataTypeMaxChoices.POW_2_30,
            editable=True,
            # error_messages={},
            help_text='Positive Invalid Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Positive Invalid Numerical Value',
            # validators=()
        )

    default = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Default Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Default Numerical Value',
            # validators=()
        )

    range = \
        DecimalRangeField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.DecimalRangeField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Numerical Value Range',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Numerical Value Range',
            # validators=()
        )

    machine_components = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=DeviceComponent,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Components',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Components',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',
            
            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=DeviceComponent.machine_data_streams.through,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_data_streams'

        ordering = \
            'machine_class__name', \
            'name'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_machine_class_and_name_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_class', 'name'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Device Data Stream'
        verbose_name_plural = 'Device Data Streams'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return u'{} [{}] {} [{}, {}{}, invalid ({:,}, {:,}){}{}]'.format(
                self.machine_class.name.upper(),
                self.machine_data_stream_type,
                self.name,
                self.logical_data_type
                    if self.logical_data_type
                    else 'Logically UNTYPED',
                self.physical_data_type
                    if self.physical_data_type
                    else 'Physically UNTYPED',
                u', unit {}'.format(self.measurement_unit.name.upper())
                    if self.measurement_unit
                    else '',
                coerce_int(self.neg_invalid, return_orig=True),
                coerce_int(self.pos_invalid, return_orig=True),
                '' if self.default is None
                   else ', default {:,}'.format(coerce_int(self.default, return_orig=True)),
                '' if self.range is None
                   else ', {}'.format(self.range))

    def save(self, *args, **kwargs) -> None:
        assert (self.neg_invalid < 0 < self.pos_invalid) \
           and (abs(self.neg_invalid + self.pos_invalid) <= 1)

        self.name = snake_case(self.name)
        assert self.name

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in DeviceClass.search_fields()] + \
               ['name',
                'descriptions',
                'machine_data_stream_type',
                'logical_data_type'] + \
               [f'physical_data_type__{search_field}'
                for search_field in PhysicalDataType.search_fields()] + \
               [f'measurement_unit__{search_field}'
                for search_field in MeasurementUnit.search_fields()]


class DeviceFamilyBlobData(
        _ModelWithDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='DeviceFamily_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Device Family Blob Data'


class DeviceFamily(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithDeviceSKUsM2MMixInABC,
        DeviceFamilyBlobData,
        _ModelWithDeviceClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_families'
    RELATED_QUERY_NAME = 'machine_family'

    name = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Family Unique Name',
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Family',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    filtered_from_machine_family = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to='self',
            on_delete=PROTECT,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Filtered from Device Family',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Filtered from Device Family',
            # validators=(),

            limit_choices_to=None,
            related_name='filtered_' + RELATED_NAME,
            related_query_name='filtered_' + RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    machine_data_filter_condition = \
        TextField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Data Filtering Condition (SQL WHERE Clause Body)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data Filtering Condition',
            # validators=()
        )

    machine_components = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='DeviceComponent',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Components',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Components',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through='DeviceFamilyComponent',
            through_fields=('machine_family', 'machine_component'),
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_data_streams = \
        ManyToManyField(  # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=DeviceDataStream,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Data Streams',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Data Streams',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_families'

        ordering = \
            'machine_class__name', \
            'name'

        verbose_name = 'Device Family'
        verbose_name_plural = 'Device Families'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} Family "{}"{}'.format(
                self.machine_class.name.upper(),
                self.name,
                ' ({}: {})'.format(
                        self.filtered_from_machine_family.name,
                        self.machine_data_filter_condition)
                    if self.filtered_from_machine_family
                    else '')

    def save(self, *args, **kwargs) -> None:
        self.name = snake_case(self.name)
        assert self.name

        if self.filtered_from_machine_family:
            assert self.machine_data_filter_condition, \
                '*** FILTERED MACHINE FAMILY MUST HAVE MACHINE DATA FILTER CONDITION ***'

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in DeviceClass.search_fields()] + \
               ['name',
                'descriptions']

    @property
    def machine_data_full_filter_condition(self):
        if self.filtered_from_machine_family:
            parent_machine_family_machine_data_full_filter_condition = \
                self.filtered_from_machine_family.machine_data_full_filter_condition

            return '({}) AND ({})'.format(
                    parent_machine_family_machine_data_full_filter_condition,
                    self.machine_data_filter_condition) \
                if parent_machine_family_machine_data_full_filter_condition \
              else self.machine_data_filter_condition

        else:
            return self.machine_data_filter_condition


class DeviceSKUBlobData(
        _ModelWithDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_sku_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='DeviceSKU_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Device SKU Blob Data'


class DeviceSKU(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceSKUBlobData,
        _ModelWithDeviceClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_skus'
    RELATED_QUERY_NAME = 'machine_sku'

    name = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device SKU Unique Name',
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device SKU',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    machine_components = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=DeviceComponent,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Components',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Components',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=DeviceComponent.machine_skus.through,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_data_streams = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=DeviceDataStream,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Data Streams',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Data Streams',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=DeviceDataStream.machine_skus.through,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_families = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=DeviceFamily,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Families',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Families',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',
            
            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=DeviceFamily.machine_skus.through,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_skus'

        ordering = \
            'machine_class__name', \
            'name'

        verbose_name = 'Device SKU'
        verbose_name_plural = 'Device SKUs'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} SKU "{}"'.format(
                self.machine_class.name.upper(),
                self.name)

    def save(self, *args, **kwargs) -> None:
        self.name = snake_case(self.name)
        assert self.name

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in DeviceClass.search_fields()] + \
               ['name',
                'descriptions']


def machine_skus_machine_data_streams_m2m_changed(
        sender,
            # The intermediate model class describing the ManyToManyField.
            # This class is automatically created when a many-to-many field is defined;
            # you can access it using the through attribute on the many-to-many field.

        instance,
            # The instance whose many-to-many relation is updated.
            # This can be an instance of the sender, or of the class the ManyToManyField is related to.

        action,
            # A string indicating the type of update that is done on the relation.

        reverse,
            # Indicates which side of the relation is updated
            # (i.e., if it is the forward or reverse relation that is being modified).

        model,
            # The class of the objects that are added to, removed from or cleared from the relation.

        pk_set,
            # For the pre_add, post_add, pre_remove and post_remove actions,
            # this is a set of primary key values that have been added to or removed from the relation.
            # For the pre_clear and post_clear actions, this is None.

        using,
            # The database alias being used.

        *args, **kwargs):
    if action == M2M_CHANGED_PRE_ADD_ACTION:
        # pk_set may be empty if no change
        # assert pk_set, \
        #     '*** {} ***'.format(pk_set)

        invalid_objs_w_diff_machine_class = \
            model.objects \
            .filter(pk__in=pk_set) \
            .exclude(machine_class=instance.machine_class)

        if invalid_objs_w_diff_machine_class:
            LOGGER.warning(
                msg='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT MACHINE CLASS(ES) ***'.format(
                    instance, invalid_objs_w_diff_machine_class))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs_w_diff_machine_class.values('pk'))

    elif (action in (M2M_CHANGED_POST_ADD_ACTION, M2M_CHANGED_POST_REMOVE_ACTION)) and pk_set:
        if (model is DeviceDataStream) and instance.machine_families.count():
            machine_families_to_update = instance.machine_families.all()

            for machine_family_to_update in machine_families_to_update:
                machine_family_to_update.machine_data_streams.set(
                    machine_family_to_update.machine_skus.all()[0].machine_data_streams.union(
                        *(machine_family_machine_sku.machine_data_streams.all()
                          for machine_family_machine_sku in machine_family_to_update.machine_skus.all()[1:]),
                        all=False),
                    # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                    clear=False)

            LOGGER.info(
                msg='{}: CHANGED Device Data Streams: {}: UPDATED Device Data Streams of {}'.format(
                    instance, action.upper(), machine_families_to_update))

        elif model is DeviceSKU:
            changed_machine_skus = model.objects.filter(pk__in=pk_set)

            machine_families_to_update = \
                changed_machine_skus[0].machine_families.union(
                    *(changed_machine_sku.machine_families.all()
                      for changed_machine_sku in changed_machine_skus[1:]),
                    all=False)

            if machine_families_to_update:
                for machine_family_to_update in machine_families_to_update:
                    machine_family_to_update.machine_data_streams.set(
                        machine_family_to_update.machine_skus.all()[0].machine_data_streams.union(
                            *(machine_family_machine_sku.machine_data_streams.all()
                              for machine_family_machine_sku in machine_family_to_update.machine_skus.all()[1:]),
                            all=False),
                        # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                        clear=False)

                LOGGER.info(
                    msg='{}: CHANGED Device SKUs: {}: UPDATED Device Data Streams of {} Related to Added/Removed {}'.format(
                        instance, action.upper(), machine_families_to_update, changed_machine_skus))

    elif action == M2M_CHANGED_PRE_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        if (model is DeviceDataStream) and instance.machine_families.count():
            machine_families_to_update = instance.machine_families.all()

            for machine_family_to_update in machine_families_to_update:
                machine_family_remaining_machine_skus = \
                    machine_family_to_update.machine_skus.exclude(pk=instance.pk)

                if machine_family_remaining_machine_skus.count():
                    machine_family_to_update.machine_data_streams.set(
                        machine_family_remaining_machine_skus[0].machine_data_streams.union(
                            *(machine_family_remaining_machine_sku.machine_data_streams.all()
                              for machine_family_remaining_machine_sku in machine_family_remaining_machine_skus[1:]),
                            all=False),
                        # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                        clear=False)

                else:
                    machine_family_to_update.machine_data_streams.clear()

                    LOGGER.warning(
                        msg='*** {}: CLEARING Device Data Streams: {}: CLEARED Device Data Streams of {} ***'.format(
                            instance, action.upper(), machine_family_to_update))

            LOGGER.warning(
                msg='*** {}: CLEARING Device Data Streams: {}: UPDATED Device Data Streams of {} ***'.format(
                    instance, action.upper(), machine_families_to_update))

        elif (model is DeviceSKU) and instance.machine_skus.count():
            machine_skus_to_clear = instance.machine_skus.all()

            machine_families_to_update = \
                machine_skus_to_clear[0].machine_families.union(
                    *(machine_sku_to_clear.machine_families.all()
                      for machine_sku_to_clear in machine_skus_to_clear[1:]),
                    all=False)

            if machine_families_to_update:
                for machine_family_to_update in machine_families_to_update:
                    machine_family_first_machine_sku = \
                        machine_family_to_update.machine_skus.all()[0]

                    machine_family_to_update.machine_data_streams.set(
                        (machine_family_first_machine_sku.machine_data_streams.exclude(pk=instance.pk)
                         if machine_family_first_machine_sku in machine_skus_to_clear
                         else machine_family_first_machine_sku.machine_data_streams.all()).union(
                            *((machine_family_machine_sku.machine_data_streams.exclude(pk=instance.pk)
                               if machine_family_machine_sku in machine_skus_to_clear
                               else machine_family_machine_sku.machine_data_streams.all())
                              for machine_family_machine_sku in machine_family_to_update.machine_skus.all()[1:]),
                            all=False),
                        # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                        clear=False)

                LOGGER.info(
                    msg='*** {}: CLEARING Device SKUs: {}: UPDATED Device Data Streams of {} Related to {} to Clear'.format(
                        instance, action.upper(), machine_families_to_update, machine_skus_to_clear))

    elif action == M2M_CHANGED_POST_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        if model is DeviceDataStream:
            assert not instance.machine_data_streams.count()

        elif model is DeviceSKU:
            assert not instance.machine_skus.count()


m2m_changed.connect(
    receiver=machine_skus_machine_data_streams_m2m_changed,
    sender=DeviceSKU.machine_data_streams.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


def machine_families_machine_skus_m2m_changed(
        sender,
            # The intermediate model class describing the ManyToManyField.
            # This class is automatically created when a many-to-many field is defined;
            # you can access it using the through attribute on the many-to-many field.

        instance,
            # The instance whose many-to-many relation is updated.
            # This can be an instance of the sender, or of the class the ManyToManyField is related to.

        action,
            # A string indicating the type of update that is done on the relation.

        reverse,
            # Indicates which side of the relation is updated
            # (i.e., if it is the forward or reverse relation that is being modified).

        model,
            # The class of the objects that are added to, removed from or cleared from the relation.

        pk_set,
            # For the pre_add, post_add, pre_remove and post_remove actions,
            # this is a set of primary key values that have been added to or removed from the relation.
            # For the pre_clear and post_clear actions, this is None.

        using,
            # The database alias being used.

        *args, **kwargs):
    if action == M2M_CHANGED_PRE_ADD_ACTION:
        # pk_set may be empty if no change
        # assert pk_set, \
        #     '*** {} ***'.format(pk_set)

        invalid_objs_w_diff_machine_class = \
            model.objects \
            .filter(pk__in=pk_set) \
            .exclude(machine_class=instance.machine_class)

        if invalid_objs_w_diff_machine_class:
            LOGGER.warning(
                msg='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT MACHINE CLASS(ES) ***'.format(
                    instance, invalid_objs_w_diff_machine_class))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs_w_diff_machine_class.values('pk'))

    elif action in (M2M_CHANGED_POST_ADD_ACTION, M2M_CHANGED_POST_REMOVE_ACTION) and pk_set:
        if model is DeviceSKU:
            if instance.machine_skus.count():
                instance.machine_data_streams.set(
                    instance.machine_skus.all()[0].machine_data_streams.union(
                        *(machine_family_machine_sku.machine_data_streams.all()
                          for machine_family_machine_sku in instance.machine_skus.all()[1:]),
                        all=False),
                    # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                    clear=False)

                LOGGER.info(
                    msg='{}: CHANGED Device SKUs: {}: UPDATED Device Data Streams'
                        .format(instance, action.upper()))

            else:
                instance.machine_data_streams.clear()

                LOGGER.warning(
                    msg='*** {}: REMOVED Device SKUs: {}: CLEARED Device Data Streams ***'
                        .format(instance, action.upper()))

        elif model is DeviceFamily:
            machine_families_to_update = \
                model.objects.filter(pk__in=pk_set)

            for machine_family_to_update in machine_families_to_update:
                if machine_family_to_update.machine_skus.count():
                    machine_family_to_update.machine_data_streams.set(
                        machine_family_to_update.machine_skus.all()[0].machine_data_streams.union(
                            *(machine_family_machine_sku.machine_data_streams.all()
                              for machine_family_machine_sku in machine_family_to_update.machine_skus.all()[1:]),
                            all=False),
                        # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                        clear=False)

                else:
                    machine_family_to_update.machine_data_streams.clear()

                    LOGGER.warning(
                        msg='*** {}: REMOVED Device SKUs: {}: CLEARED Device Data Streams ***'
                            .format(machine_family_to_update, action.upper()))

            LOGGER.info(
                msg='{}: CHANGED Device Families: {}: UPDATED Device Data Streams of Added/Removed {}'
                    .format(instance, action.upper(), machine_families_to_update))

    elif action == M2M_CHANGED_PRE_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        if model is DeviceSKU:
            instance.machine_data_streams.clear()

            LOGGER.warning(
                msg='*** {}: CLEARING Device SKUs: {}: CLEARED Device Data Streams ***'.format(
                    instance, action.upper()))

        elif (model is DeviceFamily) and instance.machine_families.count():
            machine_families_to_update = instance.machine_families.all()

            for machine_family_to_update in machine_families_to_update:
                machine_family_remaining_machine_skus = \
                    machine_family_to_update.machine_skus.exclude(pk=instance.pk)

                if machine_family_remaining_machine_skus.count():
                    machine_family_to_update.machine_data_streams.set(
                        machine_family_remaining_machine_skus.all()[0].machine_data_streams.union(
                            *(machine_family_remaining_machine_sku.machine_data_streams.all()
                              for machine_family_remaining_machine_sku in machine_family_remaining_machine_skus[1:]),
                            all=False),
                        # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                        clear=False)

                else:
                    machine_family_to_update.machine_data_streams.clear()

                    LOGGER.warning(
                        msg='*** {}: REMOVING Device SKUs: {}: CLEARED Device Data Streams ***'
                            .format(machine_family_to_update, action.upper()))

            LOGGER.info(
                msg='{}: CLEARING Device Families: {}: UPDATED Device Data Streams of {} to Clear'
                    .format(instance, action.upper(), machine_families_to_update))

    elif action == M2M_CHANGED_POST_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        if model is DeviceSKU:
            assert not instance.machine_skus.count()

        elif model is DeviceFamily:
            assert not instance.machine_families.count()


m2m_changed.connect(
    receiver=machine_families_machine_skus_m2m_changed,
    sender=DeviceFamily.machine_skus.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


def machine_sku_pre_delete(
        sender,   # the model class
        instance,   # the actual instance being deleted
        using,   # the database alias being used
        *args, **kwargs):
    if instance.machine_families.count():
        machine_families_to_update = instance.machine_families.all()

        for machine_family_to_update in machine_families_to_update:
            machine_family_remaining_machine_skus = \
                machine_families_to_update.machine_skus.exclude(pk=instance.pk)

            if machine_family_remaining_machine_skus.count():
                machine_family_to_update.machine_data_streams.set(
                    machine_family_remaining_machine_skus.all()[0].machine_data_streams.union(
                        *(machine_family_remaining_machine_sku.machine_data_streams.all()
                          for machine_family_remaining_machine_sku in machine_family_remaining_machine_skus[1:]),
                        all=False),
                    # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                    clear=False)

            else:
                machine_family_to_update.machine_data_streams.clear()

                LOGGER.warning(
                    msg='*** DELETING {}: CLEARED Device Data Streams of {} ***'
                        .format(instance, machine_family_to_update))

        LOGGER.info(
            msg='*** DELETING {}: UPDATED Device Data Streams of {} ***'
                .format(instance, machine_families_to_update))


pre_delete.connect(
    receiver=machine_sku_pre_delete,
    sender=DeviceSKU,
    weak=True,
    dispatch_uid=None,
    apps=None)


class _ModelWithDeviceFamilyFKMixInABC(Model):
    machine_family = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceFamily,
            on_delete=PROTECT,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Family',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Family',
            # validators=(),

            limit_choices_to=None,
            # related_name='%(class)s_set',
            # related_query_name='%(class)s',
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta:
        abstract = True


class DeviceFamilyComponent(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithDeviceFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_components'
    RELATED_QUERY_NAME = 'machine_family_component'

    machine_component = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceComponent,
            on_delete=PROTECT,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Component',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Component',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    # ref: https://stackoverflow.com/questions/19837728/django-manytomany-relation-to-self-without-backward-relations
    directly_interacting_components = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='self',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Directly-Interacting Components',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Directly-Interacting Components',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME + '_directly_interacting',
            related_query_name=RELATED_QUERY_NAME + '_directly_interacting',
            limit_choices_to=None,
            symmetrical=True,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    sub_components = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='self',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Sub-Components',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Sub-Components',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME + '_super',
            related_query_name=RELATED_QUERY_NAME + '_super',
            limit_choices_to=None,
            symmetrical=False,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_data_streams = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=DeviceDataStream,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Data Streams',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Data Streams',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_components'

        ordering = \
            'machine_family', \
            'machine_component__name'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = f'{_MODEL_OBJECT_NAME}_unique_together'

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'machine_component'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Device Family Component'
        verbose_name_plural = 'Device Family Components'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} Component {}{}{}{}\n'.format(
            self.machine_family,
            self.machine_component.name.upper(),

            '\n- Interacts with: {}'.format(
                [directly_interacting_component.machine_component.name
                 for directly_interacting_component in self.directly_interacting_components.all()])
            if self.directly_interacting_components.count()
            else '',

            '\n- Contains: {}'.format(
                [sub_component.machine_component.name
                 for sub_component in self.sub_components.all()])
            if self.sub_components.count()
            else '',

            '\n- Data Streams: {}'.format(
                [machine_data_stream.name
                 for machine_data_stream in self.machine_data_streams.all()])
            if self.machine_data_streams.count()
            else '')

    def save(self, *args, **kwargs) -> None:
        assert self.machine_family.machine_class \
               == self.machine_component.machine_class, \
            '*** {} AND {} NOT OF SAME MACHINE CLASS ***'.format(
                self.machine_family,
                self.machine_component)

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family__{search_field}'
                for search_field in DeviceFamily.search_fields()] + \
               ['machine_component__name',
                'machine_component__descriptions']


def machine_family_component_directly_interacting_components_m2m_changed(
        sender,
            # The intermediate model class describing the ManyToManyField.
            # This class is automatically created when a many-to-many field is defined;
            # you can access it using the through attribute on the many-to-many field.

        instance,
            # The instance whose many-to-many relation is updated.
            # This can be an instance of the sender, or of the class the ManyToManyField is related to.

        action,
            # A string indicating the type of update that is done on the relation.

        reverse,
            # Indicates which side of the relation is updated
            # (i.e., if it is the forward or reverse relation that is being modified).

        model,
            # The class of the objects that are added to, removed from or cleared from the relation.

        pk_set,
            # For the pre_add, post_add, pre_remove and post_remove actions,
            # this is a set of primary key values that have been added to or removed from the relation.
            # For the pre_clear and post_clear actions, this is None.

        using,
            # The database alias being used.

        *args, **kwargs):
    assert (type(instance) is DeviceFamilyComponent) \
       and (model is DeviceFamilyComponent)

    if action == M2M_CHANGED_PRE_ADD_ACTION:
        # pk_set may be empty if no change
        # assert pk_set, \
        #     '*** {} ***'.format(pk_set)

        invalid_objs_w_diff_machine_family = \
            model.objects \
            .filter(pk__in=pk_set) \
            .exclude(machine_family=instance.machine_family)

        if invalid_objs_w_diff_machine_family:
            LOGGER.warning(
                msg='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT MACHINE FAMILY(IES) ***'
                    .format(instance, invalid_objs_w_diff_machine_family))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs_w_diff_machine_family.values('pk'))

    elif (action in (M2M_CHANGED_POST_ADD_ACTION, M2M_CHANGED_POST_REMOVE_ACTION)) and pk_set:
        machine_component = instance.machine_component

        machine_family_components_of_same_machine_class_and_machine_component = \
            DeviceFamilyComponent.objects \
            .filter(
                machine_family__machine_class=instance.machine_family.machine_class,
                machine_component=machine_component)

        assert machine_family_components_of_same_machine_class_and_machine_component.count()

        machine_component.directly_interacting_components.set(
            {machine_family_component_directly_interacting_component.machine_component
             for machine_family_component_directly_interacting_component in
                (machine_family_components_of_same_machine_class_and_machine_component[0]
                 .directly_interacting_components.union(
                    *(machine_family_component_of_same_machine_class_and_machine_component
                        .directly_interacting_components.all()
                      for machine_family_component_of_same_machine_class_and_machine_component
                        in machine_family_components_of_same_machine_class_and_machine_component[1:]),
                    all=False))},
            # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
            clear=False)

        LOGGER.info(
            msg='{}: CHANGED Directly-Interacting Components: {}: UPDATED Directly-Interacting Components of {}'
                .format(instance, action.upper(), machine_component))

    elif action == M2M_CHANGED_PRE_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        machine_component = instance.machine_component

        remaining_machine_family_components_of_same_machine_class_and_machine_component = \
            DeviceFamilyComponent.objects \
            .filter(
                machine_family__machine_class=instance.machine_family.machine_class,
                machine_component=machine_component) \
            .exclude(
                pk=instance.pk)

        if remaining_machine_family_components_of_same_machine_class_and_machine_component.count():
            machine_component.directly_interacting_components.set(
                {machine_family_component_directly_interacting_component.machine_component
                 for machine_family_component_directly_interacting_component in
                    (remaining_machine_family_components_of_same_machine_class_and_machine_component[0]
                     .directly_interacting_components.union(
                        *(machine_family_component_of_same_machine_class_and_machine_component
                            .directly_interacting_components.all()
                          for machine_family_component_of_same_machine_class_and_machine_component
                            in remaining_machine_family_components_of_same_machine_class_and_machine_component[1:]),
                        all=False))},
                # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                clear=False)

            LOGGER.info(
                msg='{}: CLEARING Directly-Interacting Components: {}: UPDATED Directly-Interacting Components of {}'
                    .format(instance, action.upper(), machine_component))

        else:
            machine_component.directly_interacting_components.clear()

            LOGGER.warning(
                msg='*** {}: CLEARING Directly-Interacting Components: {}: CLEARED Directly-Interacting Components of {} ***'
                    .format(instance, action.upper(), machine_component))

    elif action == M2M_CHANGED_POST_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        assert not instance.directly_interacting_components.count()


m2m_changed.connect(
    receiver=machine_family_component_directly_interacting_components_m2m_changed,
    sender=DeviceFamilyComponent.directly_interacting_components.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


def machine_family_component_sub_components_m2m_changed(
        sender,
            # The intermediate model class describing the ManyToManyField.
            # This class is automatically created when a many-to-many field is defined;
            # you can access it using the through attribute on the many-to-many field.

        instance,
            # The instance whose many-to-many relation is updated.
            # This can be an instance of the sender, or of the class the ManyToManyField is related to.

        action,
            # A string indicating the type of update that is done on the relation.

        reverse,
            # Indicates which side of the relation is updated
            # (i.e., if it is the forward or reverse relation that is being modified).

        model,
            # The class of the objects that are added to, removed from or cleared from the relation.

        pk_set,
            # For the pre_add, post_add, pre_remove and post_remove actions,
            # this is a set of primary key values that have been added to or removed from the relation.
            # For the pre_clear and post_clear actions, this is None.

        using,
            # The database alias being used.

        *args, **kwargs):
    assert (type(instance) is DeviceFamilyComponent) \
       and (model is DeviceFamilyComponent)

    if action == M2M_CHANGED_PRE_ADD_ACTION:
        # pk_set may be empty if no change
        # assert pk_set, \
        #     '*** {} ***'.format(pk_set)

        invalid_objs_w_diff_machine_family = \
            model.objects \
            .filter(pk__in=pk_set) \
            .exclude(machine_family=instance.machine_family)

        if invalid_objs_w_diff_machine_family:
            LOGGER.warning(
                msg='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT MACHINE FAMILY(IES) ***'
                    .format(instance, invalid_objs_w_diff_machine_family))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs_w_diff_machine_family.values('pk'))

    elif (action in (M2M_CHANGED_POST_ADD_ACTION, M2M_CHANGED_POST_REMOVE_ACTION)) and pk_set:
        machine_component = instance.machine_component

        machine_family_components_of_same_machine_class_and_machine_component = \
            DeviceFamilyComponent.objects \
            .filter(
                machine_family__machine_class=instance.machine_family.machine_class,
                machine_component=machine_component)

        assert machine_family_components_of_same_machine_class_and_machine_component.count()

        machine_component.sub_components.set(
            {machine_family_component_sub_component.machine_component
             for machine_family_component_sub_component in
                (machine_family_components_of_same_machine_class_and_machine_component[0]
                 .sub_components.union(
                    *(machine_family_component_of_same_machine_class_and_machine_component
                        .sub_components.all()
                      for machine_family_component_of_same_machine_class_and_machine_component
                        in machine_family_components_of_same_machine_class_and_machine_component[1:]),
                    all=False))},
            # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
            clear=False)

        LOGGER.info(
            msg='{}: CHANGED Sub-Components: {}: UPDATED Sub-Components of {}'
                .format(instance, action.upper(), machine_component))

    elif action == M2M_CHANGED_PRE_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        machine_component = instance.machine_component

        remaining_machine_family_components_of_same_machine_class_and_machine_component = \
            DeviceFamilyComponent.objects \
            .filter(
                machine_family__machine_class=instance.machine_family.machine_class,
                machine_component=machine_component) \
            .exclude(
                pk=instance.pk)

        if remaining_machine_family_components_of_same_machine_class_and_machine_component.count():
            machine_component.sub_components.set(
                {machine_family_component_sub_component.machine_component
                 for machine_family_component_sub_component in
                    (remaining_machine_family_components_of_same_machine_class_and_machine_component[0]
                     .sub_components.union(
                        *(machine_family_component_of_same_machine_class_and_machine_component
                            .sub_components.all()
                          for machine_family_component_of_same_machine_class_and_machine_component
                            in remaining_machine_family_components_of_same_machine_class_and_machine_component[1:]),
                        all=False))},
                # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                clear=False)

            LOGGER.info(
                msg='{}: CLEARING Sub-Components: {}: UPDATED Sub-Components of {}'
                    .format(instance, action.upper(), machine_component))

        else:
            machine_component.sub_components.clear()

            LOGGER.warning(
                msg='*** {}: CLEARING Sub-Components: {}: CLEARED Sub-Components of {} ***'
                    .format(instance, action.upper(), machine_component))

    elif action == M2M_CHANGED_POST_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        assert not instance.sub_components.count()


m2m_changed.connect(
    receiver=machine_family_component_sub_components_m2m_changed,
    sender=DeviceFamilyComponent.sub_components.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


def machine_family_component_machine_data_streams_m2m_changed(
        sender,
            # The intermediate model class describing the ManyToManyField.
            # This class is automatically created when a many-to-many field is defined;
            # you can access it using the through attribute on the many-to-many field.

        instance,
            # The instance whose many-to-many relation is updated.
            # This can be an instance of the sender, or of the class the ManyToManyField is related to.

        action,
            # A string indicating the type of update that is done on the relation.

        reverse,
            # Indicates which side of the relation is updated
            # (i.e., if it is the forward or reverse relation that is being modified).

        model,
            # The class of the objects that are added to, removed from or cleared from the relation.

        pk_set,
            # For the pre_add, post_add, pre_remove and post_remove actions,
            # this is a set of primary key values that have been added to or removed from the relation.
            # For the pre_clear and post_clear actions, this is None.

        using,
            # The database alias being used.

        *args, **kwargs):
    assert (type(instance) is DeviceFamilyComponent) \
       and (model is DeviceDataStream)

    if action == M2M_CHANGED_PRE_ADD_ACTION:
        # pk_set may be empty if no change
        # assert pk_set, \
        #     '*** {} ***'.format(pk_set)

        invalid_objs_w_diff_machine_class = \
            model.objects \
            .filter(pk__in=pk_set) \
            .exclude(machine_class=instance.machine_family.machine_class)

        if invalid_objs_w_diff_machine_class:
            LOGGER.warning(
                msg='*** {}: CANNOT ADD INVALID {} WITH DIFFERENT MACHINE CLASS(ES) ***'
                    .format(instance, invalid_objs_w_diff_machine_class))

            pk_set.difference_update(
                i['pk']
                for i in invalid_objs_w_diff_machine_class.values('pk'))

    elif (action in (M2M_CHANGED_POST_ADD_ACTION, M2M_CHANGED_POST_REMOVE_ACTION)) and pk_set:
        machine_component = instance.machine_component

        machine_family_components_of_same_machine_class_and_machine_component = \
            DeviceFamilyComponent.objects \
            .filter(
                machine_family__machine_class=instance.machine_family.machine_class,
                machine_component=machine_component)

        assert machine_family_components_of_same_machine_class_and_machine_component.count()

        machine_component.machine_data_streams.set(
            machine_family_components_of_same_machine_class_and_machine_component[0]
            .machine_data_streams.union(
                *(machine_family_component_of_same_machine_class_and_machine_component
                    .machine_data_streams.all()
                  for machine_family_component_of_same_machine_class_and_machine_component
                    in machine_family_components_of_same_machine_class_and_machine_component[1:]),
                all=False),
            # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
            clear=False)

        LOGGER.info(
            msg='{}: CHANGED Device Data Streams: {}: UPDATED Device Data Streams of {}'
                .format(instance, action.upper(), machine_component))

    elif action == M2M_CHANGED_PRE_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        machine_component = instance.machine_component

        remaining_machine_family_components_of_same_machine_class_and_machine_component = \
            DeviceFamilyComponent.objects \
            .filter(
                machine_family__machine_class=instance.machine_family.machine_class,
                machine_component=machine_component) \
            .exclude(
                pk=instance.pk)

        if remaining_machine_family_components_of_same_machine_class_and_machine_component.count():
            machine_component.machine_data_streams.set(
                remaining_machine_family_components_of_same_machine_class_and_machine_component[0]
                .machine_data_streams.union(
                    *(machine_family_component_of_same_machine_class_and_machine_component
                        .machine_data_streams.all()
                      for machine_family_component_of_same_machine_class_and_machine_component
                        in remaining_machine_family_components_of_same_machine_class_and_machine_component[1:]),
                    all=False),
                # bulk=True,   # For many-to-many relationships, the bulk keyword argument doesn't exist
                clear=False)

            LOGGER.info(
                msg='{}: CLEARING Device Data Streams: {}: UPDATED Device Data Streams of {}'
                    .format(instance, action.upper(), machine_component))

        else:
            machine_component.machine_data_streams.clear()

            LOGGER.warning(
                msg='*** {}: CLEARING Device Data Streams: {}: CLEARED Device Data Streams of {} ***'
                    .format(instance, action.upper(), machine_component))

    elif action == M2M_CHANGED_POST_CLEAR_ACTION:
        assert pk_set is None, \
            '*** {} ***'.format(pk_set)

        assert not instance.machine_data_streams.count()


m2m_changed.connect(
    receiver=machine_family_component_machine_data_streams_m2m_changed,
    sender=DeviceFamilyComponent.machine_data_streams.through,
    weak=True,
    dispatch_uid=None,
    apps=None)


def filter_machine_family(
        from_machine_family: DeviceFamily,
        to_machine_family: DeviceFamily) -> None:
    # clone Device SKUs
    to_machine_family.machine_skus.set(from_machine_family.machine_skus.all())

    # clone Devices
    to_machine_family.machines.set(from_machine_family.machines.all())

    # clone Device Family Components
    to_machine_family_components = []

    for from_machine_family_component in from_machine_family.machine_family_components.all():
        to_machine_family_component, _ = \
            DeviceFamilyComponent.objects.get_or_create(
                machine_family=to_machine_family,
                machine_component=from_machine_family_component.machine_component)

        to_machine_family_component.directly_interacting_components.set(
            DeviceFamilyComponent.objects.get_or_create(
                machine_family=to_machine_family,
                machine_component=directly_interacting_component.machine_component)[0]
            for directly_interacting_component in from_machine_family_component.directly_interacting_components.all())

        to_machine_family_component.sub_components.set(
            DeviceFamilyComponent.objects.get_or_create(
                machine_family=to_machine_family,
                machine_component=sub_component.machine_component)[0]
            for sub_component in from_machine_family_component.sub_components.all())

        to_machine_family_component.machine_data_streams.set(
            from_machine_family_component.machine_data_streams.all())

        to_machine_family_components.append(to_machine_family_component)

    to_machine_family.machine_family_components.set(to_machine_family_components)


def machine_family_post_save(sender, instance, *args, **kwargs):
    if instance.filtered_from_machine_family:
        filter_machine_family(
            instance.filtered_from_machine_family,
            instance)

    for filtered_machine_family in instance.filtered_machine_families.all():
        filter_machine_family(
            instance,
            filtered_machine_family)


post_save.connect(
    receiver=machine_family_post_save,
    sender=DeviceFamily,
    weak=True,
    dispatch_uid=None,
    apps=None)


class _ModelWithJSONInfoMixInABC(Model):
    info = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Info (JSON)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Info',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta:
        abstract = True

        # *** Django limits index name length to 30 characters ***
        # *** so must explicitly set this in non-abstract sub-classes ***
        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('info',),
                name='%(app_label)s_%(class)s_info',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),


class LocationBlobData(
        _ModelWithJSONInfoMixInABC,
        _ModelWithDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithJSONInfoMixInABC.Meta,
            _ModelWithDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'location_blob_data'

        indexes = \
            GinIndex(
                # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='Location_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None), \
            \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('info',),
                name='Location_info',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None)

        verbose_name = verbose_name_plural = 'Location Blob Data'


class Location(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        LocationBlobData,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'locations'
    RELATED_QUERY_NAME = 'location'

    name = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Location Unique Name',
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Location',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'locations'

        ordering = 'name',

        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return 'Location "{}"'.format(
                self.name)

    def save(self, *args, **kwargs) -> None:
        self.name = snake_case(self.name)
        assert self.name

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return 'name', \
               'descriptions', \
               'info'


class DeviceBlobData(
        _ModelWithJSONInfoMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithJSONInfoMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('info',),
                name='Device_info',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Device Blob Data'


class Device(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceBlobData,
        _ModelWithDeviceClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machines'
    RELATED_QUERY_NAME = 'machine'

    machine_sku = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceSKU,
            on_delete=PROTECT,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device SKU',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device SKU',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    unique_id = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Unique ID',
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Unique ID',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    machine_families = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=DeviceFamily,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Device Families',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Device Families',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    location = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=Location,
            on_delete=PROTECT,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device SKU',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Location',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machines'

        ordering = \
            'machine_class__name', \
            'machine_sku__name', \
            'unique_id'

        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{}{} #{}{}'.format(
                self.machine_class.name.upper(),
                ' SKU "{}"'.format(self.machine_sku.name)
                    if self.machine_sku
                    else '',
                self.unique_id,
                ' @ Location "{}"'.format(self.location.name)
                    if self.location
                    else '')

    def save(self, *args, **kwargs) -> None:
        self.unique_id = snake_case(self.unique_id)
        assert self.unique_id

        if self.machine_sku and (self.machine_sku.machine_class != self.machine_class):
            LOGGER.warning(
                msg='*** MACHINE #{}: MACHINE SKU {} NOT OF MACHINE CLASS {} ***'
                    .format(self.unique_id, self.machine_sku, self.machine_class))

            self.machine_sku = None

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in DeviceClass.search_fields()] + \
               ['machine_sku__name',
                'machine_sku__descriptions',
                'unique_id',
                'info'] + \
               [f'location__{search_field}'
                for search_field in Location.search_fields()]


class _ModelWithDataSchemaMixInABC(_ModelWithIntPKMixInABC):
    schema = \
        HStoreField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.HStoreField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Schema ({"column_name": "column_physical_data_type", ...} Dictionary)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Schema',
            # validators=()
        )

    class Meta:
        abstract = True

        # *** Django limits index name length to 30 characters ***
        # *** so must explicitly set this in non-abstract sub-classes ***
        indexes = \
            GistIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GistIndex
                fields=('schema',),
                name='%(app_label)s_%(class)s_schema',
                db_tablespace=None,
                opclasses=(),
                condition=None,

                buffering=None,
                fillfactor=None),


class DeviceFamilyDataSchema(
        _ModelWithDataSchemaMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithDataSchemaMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data_schema'

        indexes = \
            GistIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GistIndex
                fields=('schema',),
                name='{}_schema'.format(_MODEL_OBJECT_NAME),
                db_tablespace=None,
                opclasses=(),
                condition=None,

                buffering=None,
                fillfactor=None),

        verbose_name = 'Device Family Data Schema'
        verbose_name_plural = 'Device Family Data Schemas'


class _ModelWithDeviceDataInfoMixInABC(Model):
    url = \
        URLField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.URLField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='URL',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='URL',
            # validators=(),

            max_length=10 ** 3)

    n_cols = \
        PositiveSmallIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveSmallIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='No. of Columns',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='No. of Columns',
            # validators=(),
        )

    n_rows = \
        PositiveIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveIntegerField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='No. of Rows',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='No. of Rows',
            # validators=(),
        )

    class Meta:
        abstract = True


class DeviceFamilyData(
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceFamilyDataSchema,
        _ModelWithDeviceDataInfoMixInABC,
        _ModelWithNullableDateMixInABC,
        _ModelWithDeviceFamilyFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = RELATED_QUERY_NAME = 'machine_family_data'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data'

        ordering = \
            'machine_family', \
            'date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_machine_family_and_date_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = verbose_name_plural = 'Device Family Data'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{}{} @ {} ({:,} col(s){})'.format(
                self.machine_family,
                ' on {}'.format(self.date)
                    if self.date
                    else '',
                self.url,
                self.n_cols,
                ' x {:,} row(s)'.format(self.n_rows)
                    if self.n_rows
                    else '')

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family__{search_field}'
                for search_field in DeviceFamily.search_fields()] + \
               ['date',
                'url']


class DeviceFamilyDataStreamsCheckBlobData(
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = RELATED_QUERY_NAME = 'machine_family_data_streams_check_blob_data'

    machine_data_stream_names_not_in_db = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Data Stream Names Not in Database',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data Stream Names Not in Database',
            # validators=(),

            encoder=DjangoJSONEncoder)

    machine_data_stream_names_not_on_disk = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Data Stream Names Not on Disk',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data Stream Names Not on Disk',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data_streams_check_blob_data'

        verbose_name = verbose_name_plural = 'Device Family Data Streams Check Blob Data'


class DeviceFamilyDataStreamsCheck(
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceFamilyDataStreamsCheckBlobData,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_streams_checks'
    RELATED_QUERY_NAME = 'machine_family_data_streams_check'

    machine_family_data = \
        OneToOneField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField
            to=DeviceFamilyData,
            on_delete=PROTECT,
            parent_link=False,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Family Data',
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Family Data',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data_streams_checks'

        ordering = 'machine_family_data__machine_family',

        verbose_name = 'Device Family Data Streams Check'
        verbose_name_plural = 'Device Family Data Streams Checks'

    def __str__(self) -> str:
        return '{}:\n- Not in DB: {}\n- Not on Disk: {}'.format(
                self.machine_family_data.machine_family,
                self.machine_data_stream_names_not_in_db,
                self.machine_data_stream_names_not_on_disk)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family_data__machine_family__{search_field}'
                for search_field in DeviceFamily.search_fields()]


class _ModelWithDeviceFamilyDataFKMixInABC(Model):
    machine_family_data = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceFamilyData,
            on_delete=PROTECT,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Family (Daily) Data',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Family (Daily) Data',
            # validators=(),

            limit_choices_to=None,
            # related_name='%(class)s_set',
            # related_query_name='%(class)s',
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta:
        abstract = True


class _ModelWithDeviceDataStreamFKMixInABC(Model):
    machine_data_stream = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceDataStream,
            on_delete=PROTECT,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Data Stream',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data Stream',
            # validators=(),

            limit_choices_to=None,
            # related_name='%(class)s_set',
            # related_query_name='%(class)s',
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta:
        abstract = True


class _ModelWithNullableDataToDateABC(Model):
    data_to_date = \
        DateField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Data to Date',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Data to Date',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class DeviceFamilyDataStreamValueProportions(
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    distinct_value_proportions = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Distinct Value Proportions',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Distinct Value Proportions',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data_stream_distinct_value_proportions'

        verbose_name = verbose_name_plural = 'Device Family Data Stream Distinct Value Proportions'


class DeviceFamilyDataStreamProfile(
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceFamilyDataStreamValueProportions,
        _ModelWithDeviceDataStreamFKMixInABC,
        _ModelWithNullableDataToDateABC,
        _ModelWithDeviceFamilyDataFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_stream_profiles'
    RELATED_QUERY_NAME = 'machine_family_data_stream_profile'

    n_samples = \
        PositiveIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='No. of Samples',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='No. of Samples',
            # validators=()
        )

    valid_fraction = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Valid Data Fraction',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Valid Data Fraction',
            # validators=()
        )

    n_distinct_values = \
        PositiveIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='No. of Distinct Values',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='No. of Distinct Values',
            # validators=()
        )

    strictly_outlier_robust_proportion = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Strictly Outlier-Robust Data Fraction',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Strictly Outlier-Robust Data Fraction',
            # validators=()
        )

    min = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Min Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Min',
            # validators=()
        )

    robust_min = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Robust Min Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Robust Min',
            # validators=()
        )

    quartile = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Quartile Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Quartile',
            # validators=()
        )

    median = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Median Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Median',
            # validators=()
        )

    _3rd_quartile = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='3rd Quartile Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='3rd Quartile',
            # validators=()
        )

    robust_max = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Robust Max Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Robust Max',
            # validators=()
        )

    max = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Max Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Max',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data_stream_profiles'

        ordering = \
            'machine_family_data', \
            '-data_to_date', \
            '-n_distinct_values'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = f'{_MODEL_OBJECT_NAME}_unique_together'

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family_data', 'data_to_date', 'machine_data_stream'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Device Family Data Stream Profile'
        verbose_name_plural = 'Device Family Data Stream Profiles'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} Profile of {}{}:\n{:,} Rows: {:.1f}% Valid{}\n{:,} Distinct Values{}{}'.format(
                self.machine_family_data.machine_family,
                self.machine_data_stream,
                ' Ending {}'.format(self.data_to_date)
                    if self.data_to_date
                    else '',
                self.n_samples,
                100 * self.valid_fraction,
                '' if self.strictly_outlier_robust_proportion is None
                   else ', {:.1f}% Strictly Outlier-Robust'.format(100 * self.strictly_outlier_robust_proportion),
                self.n_distinct_values,
                ': {}'.format(
                        '; '.join(
                            '{}: {:.1f}%'.format(
                                machine_data_stream_distinct_value,
                                100 * machine_data_stream_distinct_value_proportion)
                            for machine_data_stream_distinct_value,
                                machine_data_stream_distinct_value_proportion in
                                sorted(self.distinct_value_proportions.items(),
                                       key=lambda i: i[1],
                                       reverse=True)))
                    if self.distinct_value_proportions
                    else '',
                u'\nQuartiles ({} ⩽ {}) ⩽ {} ⩽ {} ⩽ {} ⩽ ({} ⩽ {})'.format(
                        format_number_up_to_n_decimal_places(self.min),
                        format_number_up_to_n_decimal_places(self.robust_min),
                        format_number_up_to_n_decimal_places(self.quartile),
                        format_number_up_to_n_decimal_places(self.median),
                        format_number_up_to_n_decimal_places(self._3rd_quartile),
                        format_number_up_to_n_decimal_places(self.robust_max),
                        format_number_up_to_n_decimal_places(self.max))
                    if pandas.notnull(self.median)
                    else '')

    @staticmethod
    def search_fields() -> IterableStrType:
        return ['machine_family_data__machine_family__name',
                'machine_family_data__machine_family__descriptions',
                'data_to_date'] + \
               [f'machine_data_stream__{search_field}'
                for search_field in DeviceDataStream.search_fields()]


class DeviceFamilyDataStreamPairCorr(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithDeviceDataStreamFKMixInABC,
        _ModelWithNullableDataToDateABC,
        _ModelWithDeviceFamilyDataFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_stream_pair_corrs'
    RELATED_QUERY_NAME = 'machine_family_data_stream_pair_corr'

    other_machine_data_stream = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceDataStream,
            on_delete=PROTECT,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Other Device Data Stream',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Other Device Data Stream',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME + '_other',
            related_query_name=RELATED_QUERY_NAME + '_other',
            to_field=None,
            db_constraint=True,
            swappable=True)

    machine_data_stream_range = \
        DecimalRangeField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.DecimalRangeField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Data Stream Numerical Value Range',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data Stream Numerical Value Range',
            # validators=()
        )

    other_machine_data_stream_range = \
        DecimalRangeField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.DecimalRangeField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Other Device Data Stream Numerical Value Range',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Other Device Data Stream Numerical Value Range',
            # validators=()
        )

    n_samples = \
        PositiveIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='No. of Samples',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='No. of Samples',
            # validators=()
        )

    corr = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Correlation',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Correlation',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data_stream_pair_corrs'

        ordering = \
            'machine_family_data', \
            '-data_to_date', \
            '-corr'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = f'{_MODEL_OBJECT_NAME}_unique_together'

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family_data', 'data_to_date', 'machine_data_stream', 'other_machine_data_stream'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Device Family Data Stream Pairwise Correlation'
        verbose_name_plural = 'Device Family Data Stream Pairwise Correlations'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} Correlation between {} {} & {} {}{} = {:,.3f}'.format(
                self.machine_family_data.machine_family,
                self.machine_data_stream, self.machine_data_stream_range,
                self.other_machine_data_stream, self.other_machine_data_stream_range,
                ' Ending {}'.format(self.data_to_date)
                    if self.data_to_date
                    else '',
                self.corr)

    @staticmethod
    def search_fields() -> IterableStrType:
        return DeviceFamilyDataStreamProfile.search_fields()


class DeviceFamilyDataStreamAggBlobData(
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = RELATED_QUERY_NAME = 'machine_family_data_stream_agg_blob_data'

    count_incl_invalid = \
        PositiveIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Count Incl. Invalid Values',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Count Incl. Invalid Values',
            # validators=()
        )

    counts_incl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Counts Incl. Invalid Values (JSON: {"machine_unique_id": count_incl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Counts Incl. Invalid Values',
            # validators=(),

            encoder=DjangoJSONEncoder)

    distinct_value_counts_incl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Distinct Value Counts Incl. Invalid Values (JSON: {"distinct_value": count_incl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Distinct Value Counts Incl. Invalid Values',
            # validators=(),

            encoder=DjangoJSONEncoder)

    distinct_value_proportions_incl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Distinct Value Proportions Incl. Invalid Values (JSON: {"distinct_value": proportion_incl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Distinct Value Proportions Incl. Invalid Values',
            # validators=(),

            encoder=DjangoJSONEncoder)

    count_excl_invalid = \
        PositiveIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Count Excl. Invalid Values',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Count Excl. Invalid Values',
            # validators=()
        )

    counts_excl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Counts Excl. Invalid Values (JSON: {"machine_unique_id": count_excl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Counts Excl. Invalid Values',
            # validators=(),

            encoder=DjangoJSONEncoder)

    distinct_value_proportions_excl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Distinct Value Proportions Excl. Invalid Values (JSON: {"distinct_value": proportion_excl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Distinct Value Proportions Excl. Invalid Values',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_data_stream_agg_blob_data'

        verbose_name = verbose_name_plural = 'Device Family Data Stream Agg Blob Data'
        

class DeviceFamilyDataStreamAgg(
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceFamilyDataStreamAggBlobData,
        _ModelWithDeviceDataStreamFKMixInABC,
        _ModelWithDeviceFamilyDataFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_stream_aggs'
    RELATED_QUERY_NAME = 'machine_family_data_stream_agg'

    weighted_average_min = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average Min Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average Min',
            # validators=()
        )

    weighted_average_robust_min = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average Robust Min Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average Robust Min',
            # validators=()
        )

    weighted_average_quartile = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average Quartile Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average Quartile',
            # validators=()
        )

    weighted_average_median = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average Median Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average Median',
            # validators=()
        )

    weighted_average_mean = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average Mean Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average Mean',
            # validators=()
        )

    weighted_average_3rd_quartile = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average 3rd Quartile Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average 3rd Quartile',
            # validators=()
        )

    weighted_average_robust_max = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average Robust Max Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average Robust Max',
            # validators=()
        )

    weighted_average_max = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Weighted Average Max Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Weighted Average Max',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')
        
        default_related_name = 'machine_family_data_stream_aggs'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = f'{_MODEL_OBJECT_NAME}_unique_together'

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family_data', 'machine_data_stream'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Device Family Data Stream Agg'
        verbose_name_plural = 'Device Family Data Stream Aggs'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} {} Aggs'.format(
                self.machine_family_data,
                self.machine_data_stream)

    @staticmethod
    def search_fields() -> IterableStrType:
        return ['machine_family_data__machine_family__name',
                'machine_family_data__machine_family__descriptions',
                'machine_family_data__date'] + \
               [f'machine_data_stream__{search_field}'
                for search_field in DeviceDataStream.search_fields()]


class DeviceDataSchema(
        _ModelWithDataSchemaMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithDataSchemaMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')
        
        default_related_name = 'machine_data_schema'

        indexes = \
            GistIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GistIndex
                fields=('schema',),
                name='{}_schema'.format(_MODEL_OBJECT_NAME),
                db_tablespace=None,
                opclasses=(),
                condition=None,

                buffering=None,
                fillfactor=None),

        verbose_name = 'Device Data Schema'
        verbose_name_plural = 'Device Data Schemas'


class _ModelWithDeviceFKMixInABC(Model):
    machine = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=Device,
            on_delete=PROTECT,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device',
            # validators=(),

            limit_choices_to=None,
            # related_name='%(class)s_set',
            # related_query_name='%(class)s',
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta:
        abstract = True


class DeviceData(
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceDataSchema,
        _ModelWithDeviceDataInfoMixInABC,
        _ModelWithNullableDateMixInABC,
        _ModelWithDeviceFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = RELATED_QUERY_NAME = 'machine_data'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')
        
        default_related_name = 'machine_data'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_machine_and_date_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine', 'date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = verbose_name_plural = 'Device Data'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{}{} @ {} ({:,} col(s){})'.format(
                self.machine,
                ' on {}'.format(self.date)
                    if self.date
                    else '',
                self.url,
                self.n_cols,
                ' x {:,} row(s)'.format(self.n_rows)
                    if self.n_rows
                    else '')

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine__{search_field}'
                for search_field in Device.search_fields()] + \
               ['date',
                'url']


class DeviceDataStreamAggBlobData(
        _ModelWithBigIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = RELATED_QUERY_NAME = 'machine_data_stream_agg_blob_data'

    count_incl_invalid = \
        PositiveSmallIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveSmallIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Count Incl. Invalid Values',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Count Incl. Invalid Values',
            # validators=()
        )

    distinct_value_counts_incl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Distinct Value Counts Incl. Invalid (JSON: {"distinct_value": count_incl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Distinct Value Counts Incl. Invalid',
            # validators=(),

            encoder=DjangoJSONEncoder)

    distinct_value_proportions_incl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Distinct Value Proportions Incl. Invalid (JSON: {"distinct_value": proportion_incl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Distinct Value Proportions Incl. Invalid',
            # validators=(),

            encoder=DjangoJSONEncoder)
    
    count_excl_invalid = \
        PositiveSmallIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveSmallIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Count Excl. Invalid Values',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Count Excl. Invalid Values',
            # validators=()
        )

    distinct_value_proportions_excl_invalid = \
        JSONField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Distinct Value Proportions Excl. Invalid (JSON: {"distinct_value": proportion_excl_invalid, ...})',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Distinct Value Proportions Excl. Invalid',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_data_stream_agg_blob_data'

        verbose_name = verbose_name_plural = 'Device Data Stream Agg Blob Data'


class _ModelWithDeviceDataFKABC(Model):
    machine_data = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceData,
            on_delete=PROTECT,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Data',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Data',
            # validators=(),

            limit_choices_to=None,
            # related_name='%(class)s_set',
            # related_query_name='%(class)s',
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta:
        abstract = True


class DeviceDataStreamAgg(
        _ModelWithCreatedAndUpdatedMixInABC,
        DeviceDataStreamAggBlobData,
        _ModelWithDeviceDataFKABC,
        _ModelWithDeviceFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_data_stream_aggs'
    RELATED_QUERY_NAME = 'machine_data_stream_agg'

    machine_family_data_stream_agg = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=DeviceFamilyDataStreamAgg,
            on_delete=PROTECT,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Device Family Data Stream Agg',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Device Family Data Stream Agg',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    min = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Min Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Min',
            # validators=()
        )

    robust_min = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Robust Min Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Robust Min',
            # validators=()
        )

    quartile = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Quartile Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Quartile',
            # validators=()
        )

    median = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Median Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Median',
            # validators=()
        )

    mean = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Mean Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Mean',
            # validators=()
        )

    _3rd_quartile = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='3rd Quartile Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='3rd Quartile',
            # validators=()
        )

    robust_max = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Robust Max Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Robust Max',
            # validators=()
        )

    max = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Max Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Max',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')
        
        default_related_name = 'machine_data_stream_aggs'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = f'{_MODEL_OBJECT_NAME}_unique_together'

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family_data_stream_agg', 'machine'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Device Data Stream Agg'
        verbose_name_plural = 'Device Data Stream Aggs'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return f'{self.machine_family_data_stream_agg} Aggs for #{self.machine.unique_id}'

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family_data_stream_agg__{search_field}'
                for search_field in DeviceFamilyDataStreamAgg.search_fields()] + \
               ['machine__machine_sku__name',
                'machine__machine_sku__descriptions',
                'machine__unique_id',
                'machine__info'] + \
               [f'machine__location__{search_field}'
                for search_field in Location.search_fields()]
