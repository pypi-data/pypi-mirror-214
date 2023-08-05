from datetime import timedelta

from django.core.serializers.json import DjangoJSONEncoder

from django.db.models.base import Model

from django.db.models.constraints import UniqueConstraint

from django.db.models.deletion import CASCADE, PROTECT, SET_NULL

from django.db.models.fields import \
    BooleanField, \
    DateField, DateTimeField, DurationField, \
    FloatField, \
    BigIntegerField, PositiveSmallIntegerField, \
    TextField

from django.db.models.fields.json import JSONField

from django.db.models.fields.related import \
    ForeignKey, ManyToManyField, OneToOneField

from django.contrib.postgres.fields.citext import CICharField
from django.contrib.postgres.fields.ranges import DateRangeField

from django.contrib.postgres.indexes import GinIndex

from django.db.models.signals import post_save

from django_util.models import \
    PGSQL_IDENTIFIER_MAX_LEN, \
    _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC, \
    _ModelWithIntPKMixInABC, _ModelWithBigIntPKMixInABC, \
    _ModelWithCreatedAndUpdatedMixInABC, \
    _EnvVarABC

from psycopg2.extras import DateRange

from ..data.models import \
    _ModelWithMultilingualDescriptionsMixInABC, \
    _ModelWithJSONInfoMixInABC, \
    _ModelWithMachineClassFKMixInABC, \
    _ModelWithMachineFamilyFKMixInABC, \
    _ModelWithMachineFamilyDataFKMixInABC, \
    _ModelWithMachineDataStreamFKMixInABC, \
    _ModelWithMachineFKMixInABC, \
    MachineClass, \
    MachineFamily, \
    MachineDataStream, \
    Location, \
    Machine, \
    MachineFamilyData, \
    MachineFamilyDataStreamProfile

from ..util import MAX_CHAR_FLD_LEN, IterableStrType, snake_case

from .apps import MachineHealthConfig


# App Label
APP_LABEL = MachineHealthConfig.label


_ONE_DAY_TIME_DELTA = timedelta(days=1)


class EnvVar(_EnvVarABC):
    class Meta(_EnvVarABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"


EnvironmentVariable = EnvVar


class _ModelWithOpenDateRangeMixInABC(Model):
    from_date = \
        DateField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='From Date',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='From Date',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    to_date = \
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
            help_text='To Date',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='To Date',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class _ModelWithActiveMixInABC(Model):
    active = \
        BooleanField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BooleanField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=False,
            editable=True,
            # error_messages={},
            help_text='Active?',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Active?',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithCommentsMixInABC(Model):
    comments = \
        TextField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.TextField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Comments',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Comments',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithExclInputMachineDataStreamsM2MMixInABC(Model):
    excl_input_machine_data_streams = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineDataStream,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Excluded Input Machine Data Streams',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Excluded Input Machine Data Streams',
            # validators=(),   # ManyToManyField does not support validators

            # not necessary to create reverse accessor
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


class MachineFamilyHealthServiceConfigBlob(
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    configs = \
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
            help_text='Machine Family Health Service Config Settings (JSON)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Family Health Service Config Settings',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_health_service_config_settings'

        verbose_name = verbose_name_plural = 'Machine Family Health Service Config Settings'


class MachineFamilyHealthServiceConfig(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithCommentsMixInABC,
        _ModelWithActiveMixInABC,
        MachineFamilyHealthServiceConfigBlob,
        _ModelWithExclInputMachineDataStreamsM2MMixInABC,
        _ModelWithOpenDateRangeMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_health_service_configs'
    RELATED_QUERY_NAME = 'machine_family_health_service_config'

    machine_family = \
        OneToOneField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField
            to=MachineFamily,
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
            help_text='Machine Family',
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Family',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    incl_cat_input_machine_data_streams = \
        BooleanField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BooleanField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=True,
            editable=True,
            # error_messages={},
            help_text='Include Input Categorical Machine Data Streams?',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Include Input Categorical Machine Data Streams?',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_health_service_configs'

        ordering = \
            '-active', \
            'machine_family'

        verbose_name = 'Machine Family Health Service Config'
        verbose_name_plural = 'Machine Family Health Service Configs'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    @property
    def vital_and_incl_excl_machine_data_stream_names(self):
        return '{}{}'.format(
                '; '.join(
                    str(machine_family_vital_data_stream_config)
                    for machine_family_vital_data_stream_config in self.machine_family_vital_data_stream_configs.all()
                    if machine_family_vital_data_stream_config.active
                    # ^^^ USE ABOVE "IF" STATEMENT INSTEAD OF .filter(active=True) TO AVOID VOIDING THE CACHED PREFETCHED DATA ^^^
                ),

                ' | excl: {}'.format(
                    ', '.join(excluded_input_machine_data_stream.name
                              for excluded_input_machine_data_stream in self.excl_input_machine_data_streams.all()))
                if self.excl_input_machine_data_streams.count()
                else '')

    def __str__(self) -> str:
        return '{}Health Service Config for {}: {}'.format(
                '' if self.active
                   else '(INACTIVE) ',
                self.machine_family,
                self.vital_and_incl_excl_machine_data_stream_names)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family__{search_field}'
                for search_field in MachineFamily.search_fields()]


class MachineFamilyVitalDataStreamConfigBlob(
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    high_corr_num_machine_data_streams = \
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
            help_text='Highly-Correlated Numerical Machine Data Streams (JSON)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Highly-Correlated Numerical Machine Data Streams',
            # validators=(),

            encoder=DjangoJSONEncoder)

    auto_incl_input_machine_data_streams = \
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
            help_text='Automatically-Included Input Machine Data Streams (JSON)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Automatically-Included Input Machine Data Streams',
            # validators=(),

            encoder=DjangoJSONEncoder)

    low_corr_num_machine_data_streams = \
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
            help_text='Lowly-Correlated Numerical Machine Data Streams (JSON)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Lowly-Correlated Numerical Machine Data Streams',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_family_vital_data_stream_config_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('high_corr_num_machine_data_streams',),
                name='MFVital_high_corr_data_streams',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None), \
            \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('auto_incl_input_machine_data_streams',),
                name='MFVital_auto_incl_data_streams',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None), \
            \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('low_corr_num_machine_data_streams',),
                name='MFVital_low_corr_data_streams',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None)

        verbose_name = verbose_name_plural = 'Machine Family Vital Data Stream Config Blob Data'


class MachineFamilyVitalDataStreamConfig(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithCommentsMixInABC,
        _ModelWithActiveMixInABC,
        _ModelWithExclInputMachineDataStreamsM2MMixInABC,
        MachineFamilyVitalDataStreamConfigBlob,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_vital_data_stream_configs'
    RELATED_QUERY_NAME = 'machine_family_vital_data_stream_config'

    machine_family_health_service_config = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=MachineFamilyHealthServiceConfig,
            on_delete=CASCADE,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Machine Family Health Service Config',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Family Health Service Config',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    vital_machine_data_stream = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=MachineDataStream,
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
            help_text='Vital Machine Data Stream',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Vital Machine Data Stream',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    vital_machine_data_stream_profile = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=MachineFamilyDataStreamProfile,
            on_delete=SET_NULL,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Machine Family Vital Data Stream Profile',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Family Vital Data Stream Profile',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    incl_input_machine_data_streams = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineDataStream,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Included Input Machine Data Streams',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Included Input Machine Data Streams',
            # validators=(),   # ManyToManyField does not support validators

            # not necessary to create reverse accessor
            related_name='+',

            # related_query_name=RELATED_QUERY_NAME + '_incl',
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

        default_related_name = 'machine_family_vital_data_stream_configs'

        ordering = \
            '-active', \
            'vital_machine_data_stream__name'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family_health_service_config', 'vital_machine_data_stream'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Vital Data Stream Config'
        verbose_name_plural = 'Machine Family Vital Data Stream Configs'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{}{}{}{}'.format(
                '' if self.active
                   else '(inactive) ',

                self.vital_machine_data_stream.name.upper(),

                ' (incl: {})'.format(
                    ', '.join(incl_input_machine_data_stream.name
                              for incl_input_machine_data_stream in self.incl_input_machine_data_streams.all()))
                    if self.incl_input_machine_data_streams.count()
                    else '',

                ' (excl: {})'.format(
                    ', '.join(excl_input_machine_data_stream.name
                              for excl_input_machine_data_stream in self.excl_input_machine_data_streams.all()))
                    if self.excl_input_machine_data_streams.count()
                    else '')

    def save(self, *args, **kwargs) -> None:
        if not self.vital_machine_data_stream_profile:
            self.vital_machine_data_stream_profile = \
                MachineFamilyDataStreamProfile.objects \
                .filter(
                    machine_family_data__machine_family=self.machine_family_health_service_config.machine_family,
                    data_to_date=None,
                    machine_data_stream=self.vital_machine_data_stream) \
                .first()

        super().save(*args, **kwargs)


class _ModelWithRefDataToDateABC(Model):
    ref_data_to_date = \
        DateField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Reference Data to Date',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Reference Data to Date',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class AIBlobData(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
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
            help_text='AI Unique ID',
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='AI Unique ID',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    ref_eval_metrics = \
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
            help_text='Reference Evaluation Metrics (JSON)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Reference Evaluation Metrics',
            # validators=(),

            encoder=DjangoJSONEncoder)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'ai_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('ref_eval_metrics',),
                name='AI_ref_eval_metrics',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'AI Blob Data'


class AI(_ModelWithCreatedAndUpdatedMixInABC,
         _ModelWithActiveMixInABC,
         AIBlobData,
         _ModelWithRefDataToDateABC,
         _ModelWithMachineFamilyFKMixInABC,
         _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'ais'
    RELATED_QUERY_NAME = 'ai'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'ais'

        ordering = \
            'machine_family', \
            '-ref_data_to_date', \
            '-created'

        verbose_name = 'AI'
        verbose_name_plural = 'AIs'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{}"{}" AI (Created at {})'.format(
                '' if self.active
                   else '(INACTIVE) ',
                self.unique_id,
                self.created)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family__{search_field}'
                for search_field in MachineFamily.search_fields()]


class AIModel(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'ai_models'
    RELATED_QUERY_NAME = 'ai_model'

    ai = ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=AI,
            on_delete=CASCADE,

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='AI',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='AI',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    input_machine_data_streams = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineDataStream,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Input Machine Data Streams',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Input Machine Data Streams',
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

    target_machine_data_stream = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=MachineDataStream,
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
            help_text='Target Machine Data Stream',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Target Machine Data Stream',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'ai_models'

        ordering = \
            'ai', \
            'target_machine_data_stream__name'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_ai_and_target_machine_data_stream_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(
                # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('ai', 'target_machine_data_stream'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'AI Model'
        verbose_name_plural = 'AI Models'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return self.target_machine_data_stream.name \
            if self.target_machine_data_stream \
          else ''


class MachineFamilyVitalAIEvalMetricProfile(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithRefDataToDateABC,
        _ModelWithMachineDataStreamFKMixInABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_vital_data_stream_ai_eval_metric_profiles'
    RELATED_QUERY_NAME = 'machine_family_vital_data_stream_ai_eval_metric_profile'

    N = BigIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BigIntegerField
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
            # validators=(),
        )

    MAE = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,   # TODO: may need to relax to accommodate Inf & NaN
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Mean Absolute Error (MAE)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Mean Absolute Error (MAE)',
            # validators=()
        )

    MedAE = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,  # TODO: may need to relax to accommodate Inf & NaN
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Median Absolute Error (MedAE)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Median Absolute Error (MedAE)',
            # validators=()
        )

    RMSE = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,  # TODO: may need to relax to accommodate Inf & NaN
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Root Mean Square Error (RMSE)',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Root Mean Square Error (RMSE)',
            # validators=()
        )

    R2 = \
        FloatField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FloatField
            null=False,  # TODO: may need to relax to accommodate Inf & NaN
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='R2',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='R2',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        # ^^^ leaving out APP_LABEL to make table name length <= PostgreSQL's 63-character limit ^^^

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_vital_data_stream_ai_eval_metric_profiles'

        ordering = \
            'machine_family', \
            'machine_data_stream__name', \
            '-ref_data_to_date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'machine_data_stream', 'ref_data_to_date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Vital Data Stream AI Eval Metric Profile'
        verbose_name_plural = 'Machine Family Vital Data Stream AI Eval Metric Profiles'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} AI Eval Metric Profile for {} Ending {}'.format(
                self.machine_family,
                self.machine_data_stream,
                self.ref_data_to_date)

    @staticmethod
    def search_fields() -> IterableStrType:
        return ['machine_family_data__machine_family__unique_name',
                'machine_family_data__machine_family__descriptions',
                'ref_data_to_date'] + \
               [f'machine_data_stream__{search_field}'
                for search_field in MachineDataStream.search_fields()]


class MachineHealthRiskScoreMethodBlobData(
        _ModelWithJSONInfoMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithJSONInfoMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_health_risk_score_method_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('info',),
                name='MachineHealthRiskMethod_info',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Machine Health Risk Score Method Blob Data'


class MachineHealthRiskScoreMethod(
        _ModelWithCreatedAndUpdatedMixInABC,
        MachineHealthRiskScoreMethodBlobData,
        _ModelWithMachineClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_health_risk_score_methods'
    RELATED_QUERY_NAME = 'machine_health_risk_score_method'

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
            help_text='Machine Health Risk Score Method Name',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Health Risk Score Method',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_health_risk_score_methods'

        ordering = \
            'machine_class__unique_name', \
            'name'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_class', 'name'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Health Risk Score Method'
        verbose_name_plural = 'Machine Health Risk Score Methods'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} Machine Health Risk Score Method "{}"'.format(
                self.machine_class.unique_name.upper(),
                self.name)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in MachineClass.search_fields()] + \
               ['name',
                'info']


class _ModelWithMachineHealthRiskScoreMethodFKMixInABC(Model):
    machine_health_risk_score_method = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=MachineHealthRiskScoreMethod,
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
            help_text='Machine Health Risk Score Method',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Health Risk Score Method',
            # validators=(),

            limit_choices_to=None,
            # related_name='%(class)s_set',
            # related_query_name='%(class)s',
            to_field=None,
            db_constraint=True,
            swappable=True)

    class Meta:
        abstract = True


class MachineHealthRiskScore(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithMachineHealthRiskScoreMethodFKMixInABC,
        _ModelWithMachineFKMixInABC,
        _ModelWithMachineFamilyDataFKMixInABC,
        _ModelWithBigIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_health_risk_scores'
    RELATED_QUERY_NAME = 'machine_health_risk_score'

    machine_health_risk_score_value = \
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
            help_text='Machine Health Risk Score Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Health Risk Score Value',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_health_risk_scores'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family_data', 'machine', 'machine_health_risk_score_method'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Health Risk Score'
        verbose_name_plural = 'Machine Health Risk Scores'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} {} #{} on {}: {} = {:.3g}'.format(
                self.machine_family_data.machine_family.machine_class.unique_name,
                self.machine_family_data.machine_family.unique_name,
                self.machine.unique_id,
                self.machine_family_data.date,
                self.machine_health_risk_score_method.name,
                self.machine_health_risk_score_value)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family_data__{search_field}'
                for search_field in MachineFamilyData.search_fields()] + \
               ['machine_health_risk_score_method__name',
                'machine__machine_sku__unique_name',
                'machine__machine_sku__descriptions',
                'machine__unique_id',
                'machine__info'] + \
               [f'machine__location__{search_field}'
                for search_field in Location.search_fields()]


class _ModelWithDateRangeAndDurationMixInABC(Model):
    date_range = \
        DateRangeField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.DateRangeField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Date Range',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Date Range',
            # validators=()
        )

    duration = \
        DurationField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DurationField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Duration',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Duration',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithOpenDateRangeAndDurationAndOngoingMixInABC(
        _ModelWithDateRangeAndDurationMixInABC,
        _ModelWithOpenDateRangeMixInABC):
    ongoing = \
        BooleanField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BooleanField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=False,
            editable=True,
            # error_messages={},
            help_text='Ongoing?',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Ongoing?',
            # validators=()
        )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        self.date_range = \
            DateRange(
                lower=self.from_date,
                upper=self.to_date,
                bounds='[]',
                empty=False)

        if self.to_date:
            self.duration = \
                self.to_date - self.from_date + _ONE_DAY_TIME_DELTA

            self.ongoing = True

        else:
            self.duration = None

            self.ongoing = False

        super().save(*args, **kwargs)


class _ModelWithHasMachineHealthRiskAlertsMixInABC(Model):
    has_machine_health_risk_alerts = \
        BooleanField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BooleanField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=False,
            editable=True,
            # error_messages={},
            help_text='Has Machine Health Risk Alerts?',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Has Machine Health Risk Alerts?',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithMachineHealthProblemDiagnosesM2MMixInABC(Model):
    machine_health_problem_diagnoses = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='MachineHealthProblemDiagnosis',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Health Problem Diagnoses',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Health Problem Diagnoses',
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


class _ModelWithHasMachineHealthProblemDiagnosesMixInABC(Model):
    has_machine_health_problem_diagnoses = \
        BooleanField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BooleanField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=False,
            editable=True,
            # error_messages={},
            help_text='Has Machine Health Problem Diagnoses?',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Has Machine Health Problem Diagnoses?',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithMachineMaintenanceRepairActionsM2MMixInABC(Model):
    machine_maintenance_repair_actions = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='MachineMaintenanceRepairAction',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Maintenance Repair Actions',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Maintenance Repair Actions',
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


class _ModelWithHasMachineMaintenanceRepairActionsMixInABC(Model):
    has_machine_maintenance_repair_actions = \
        BooleanField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BooleanField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=False,
            editable=True,
            # error_messages={},
            help_text='Has Machine Maintenance Repair Actions?',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Has Machine Maintenance Repair Actions?',
            # validators=()
        )

    class Meta:
        abstract = True


class _ModelWithMachineErrorsM2MMixInABC(Model):
    machine_errors = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='MachineError',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Errors',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Errors',
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


class _ModelWithHasMachineErrorsABC(Model):
    has_machine_errors = \
        BooleanField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BooleanField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=False,
            editable=True,
            # error_messages={},
            help_text='Has Machine Errors?',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Has Machine Errors?',
            # validators=()
        )

    class Meta:
        abstract = True


class MachineHealthRiskAlertBlobData(
        _ModelWithJSONInfoMixInABC,
        _ModelWithBigIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithJSONInfoMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_health_risk_alert_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('info',),
                name='MachineHealthRiskAlert_info',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Machine Health Risk Alert Blob Data'


class MachineHealthRiskAlert(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithMachineErrorsM2MMixInABC, _ModelWithHasMachineErrorsABC,
        _ModelWithMachineMaintenanceRepairActionsM2MMixInABC, _ModelWithHasMachineMaintenanceRepairActionsMixInABC,
        _ModelWithMachineHealthProblemDiagnosesM2MMixInABC, _ModelWithHasMachineHealthProblemDiagnosesMixInABC,
        MachineHealthRiskAlertBlobData,
        _ModelWithOpenDateRangeAndDurationAndOngoingMixInABC,
        _ModelWithMachineHealthRiskScoreMethodFKMixInABC,
        _ModelWithMachineFKMixInABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_health_risk_alerts'
    RELATED_QUERY_NAME = 'machine_health_risk_alert'

    machine_health_risk_score_value_alert_threshold = \
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
            help_text='Machine Health Risk Score Value Alert Threshold',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Health Risk Score Value Alert Threshold',
            # validators=()
        )

    last_machine_health_risk_score_value = \
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
            help_text='Last Machine Health Risk Score Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Last Machine Health Risk Score Value',
            # validators=()
        )

    cum_excess_machine_health_risk_score_value = \
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
            help_text='Cumulative Excess Machine Health Risk Score Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Cumulative Excess Machine Health Risk Score Value',
            # validators=()
        )

    approx_average_machine_health_risk_score_value = \
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
            help_text='(Approximate) Average Machine Health Risk Score Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='(Approximate) Average Machine Health Risk Score Value',
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_health_risk_alerts'

        ordering = \
            '-ongoing', \
            'machine_health_risk_score_method__name', \
            '-machine_health_risk_score_value_alert_threshold', \
            '-cum_excess_machine_health_risk_score_value'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME_1 = '{}_unique_together_from_date'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME_1) <= PGSQL_IDENTIFIER_MAX_LEN, \
            '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME_1)

        _CONSTRAINT_NAME_2 = '{}_unique_together_to_date'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME_2) <= PGSQL_IDENTIFIER_MAX_LEN, \
            '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME_2)

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family',
                        'machine',
                        'machine_health_risk_score_method',
                        'machine_health_risk_score_value_alert_threshold',
                        'from_date'),
                name=_CONSTRAINT_NAME_1,
                condition=None), \
            \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family',
                        'machine',
                        'machine_health_risk_score_method',
                        'machine_health_risk_score_value_alert_threshold',
                        'to_date'),
                name=_CONSTRAINT_NAME_2,
                condition=None)

        verbose_name = 'Machine Health Risk Alert'
        verbose_name_plural = 'Machine Health Risk Alerts'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{}Risk Alert on {} {} #{} from {} to {} w Approx Avg Risk Score {:,.1f} (Last: {:,.1f}) (based on {} > {}) for {:,} Day(s)'.format(
                'ONGOING '
                    if self.ongoing
                    else '',
                self.machine_family.machine_class.unique_name.upper(),
                self.machine_family.unique_name,
                self.machine.unique_id,
                self.from_date,
                self.to_date,
                self.approx_average_machine_health_risk_score_value,
                self.last_machine_health_risk_score_value,
                self.machine_health_risk_score_method.name,
                self.machine_health_risk_score_value_alert_threshold,
                self.duration.days)

    def save(self, *args, **kwargs) -> None:
        assert self.to_date

        self.date_range = \
            DateRange(
                lower=self.from_date,
                upper=self.to_date,
                bounds='[]',
                empty=False)

        self.duration = duration = \
            self.to_date - self.from_date + _ONE_DAY_TIME_DELTA

        self.approx_average_machine_health_risk_score_value = \
            self.machine_health_risk_score_value_alert_threshold + \
            (self.cum_excess_machine_health_risk_score_value / duration.days)

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_family__{search_field}'
                for search_field in MachineFamily.search_fields()] + \
               ['machine_health_risk_score_method__name',
                'machine__machine_sku__unique_name',
                'machine__machine_sku__descriptions',
                'machine__unique_id',
                'machine__info'] + \
               [f'machine__location__{search_field}'
                for search_field in Location.search_fields()]


class MachineHealthProblemBlobData(
        _ModelWithMultilingualDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithMultilingualDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_health_problem_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='MachineProblem_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Machine Health Problem Blob Data'


class MachineHealthProblem(
        _ModelWithCreatedAndUpdatedMixInABC,
        MachineHealthProblemBlobData,
        _ModelWithMachineClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_health_problems'
    RELATED_QUERY_NAME = 'machine_health_problem'

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
            help_text='Machine Health Problem Name',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Health Problem',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_health_problems'

        ordering = \
            'machine_class__unique_name', \
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

        verbose_name = 'Machine Health Problem'
        verbose_name_plural = 'Machine Health Problems'

    def __str__(self) -> str:
        return '{} Health Problem "{}"'.format(
                self.machine_class.unique_name.upper(),
                self.name)

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def save(self, *args, **kwargs) -> None:
        self.name = snake_case(self.name)
        assert self.name

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in MachineClass.search_fields()] + \
               ['name',
                'descriptions']


class MachineHealthProblemDiagnosis(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithMachineErrorsM2MMixInABC, _ModelWithHasMachineErrorsABC,
        _ModelWithMachineMaintenanceRepairActionsM2MMixInABC, _ModelWithHasMachineMaintenanceRepairActionsMixInABC,
        _ModelWithHasMachineHealthRiskAlertsMixInABC,
        _ModelWithCommentsMixInABC,
        _ModelWithOpenDateRangeAndDurationAndOngoingMixInABC,
        _ModelWithMachineFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_health_problem_diagnoses'
    RELATED_QUERY_NAME = 'machine_health_problem_diagnosis'

    machine_health_problems = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineHealthProblem,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Diagnosed Machine Health Problems',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Diagnosed Machine Health Problems',
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

    machine_health_risk_alerts = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineHealthRiskAlert,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Health Risk Alerts',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Health Risk Alerts',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=MachineHealthRiskAlert.machine_health_problem_diagnoses.through,
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

        default_related_name = 'machine_health_problem_diagnoses'

        ordering = \
            '-to_date', \
            'from_date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(
                # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine', 'from_date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Health Problem Diagnosis'
        verbose_name_plural = 'Machine Health Problem Diagnoses'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{} from {}{}{}'.format(
                self.machine,
                self.from_date,
                ' to {} ({:,} Day(s))'.format(self.to_date, self.duration.days)
                    if self.to_date
                    else ' (ONGOING)',
                ': {}'.format(
                    ', '.join(machine_health_problem.name
                              for machine_health_problem in self.machine_health_problems.all()))
                    if self.machine_health_problems.count()
                    else '')

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine__{search_field}'
                for search_field in Machine.search_fields()] + \
               ['machine_health_problem__name',
                'machine_health_problem__descriptions']


class MachineMaintenanceRepairAction(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithMachineErrorsM2MMixInABC, _ModelWithHasMachineErrorsABC,
        _ModelWithHasMachineHealthProblemDiagnosesMixInABC,
        _ModelWithHasMachineHealthRiskAlertsMixInABC,
        _ModelWithCommentsMixInABC,
        _ModelWithOpenDateRangeAndDurationAndOngoingMixInABC,
        _ModelWithMachineFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_maintenance_repair_actions'
    RELATED_QUERY_NAME = 'machine_maintenance_repair_action'

    machine_health_risk_alerts = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineHealthRiskAlert,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Health Risk Alerts',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Health Risk Alerts',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=MachineHealthRiskAlert.machine_maintenance_repair_actions.through,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_health_problem_diagnoses = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineHealthProblemDiagnosis,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Health Problem Diagnoses',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Health Problem Diagnoses',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=MachineHealthProblemDiagnosis.machine_maintenance_repair_actions.through,
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

        default_related_name = 'machine_maintenance_repair_actions'

        ordering = \
            '-to_date', \
            'from_date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine', 'from_date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Maintenance/Repair Action'
        verbose_name_plural = 'Machine Maintenance/Repair Actions'

    def __str__(self) -> str:
        return '{} Maintained/Repaired from {}{}'.format(
                self.machine,
                self.from_date,
                ' to {} ({:,} Day(s))'.format(self.to_date, self.duration.days)
                    if self.to_date
                    else ' (ONGOING)')

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine__{search_field}'
                for search_field in Machine.search_fields()]


class MachineErrorCodeBlobData(
        _ModelWithMultilingualDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithMultilingualDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{ __qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_error_code_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='MachineErrorCode_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Machine Error Code Blob Data'


class MachineErrorCode(
        _ModelWithCreatedAndUpdatedMixInABC,
        MachineErrorCodeBlobData,
        _ModelWithMachineClassFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_error_codes'
    RELATED_QUERY_NAME = 'machine_error_code'

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
            help_text='Machine Error Code Name',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Error Code',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    excl_n_days_of_machine_data_before = \
        PositiveSmallIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.PositiveSmallIntegerField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=0,
            editable=True,
            # error_messages={},
            help_text='No. of Days of Machine Data Before Error to Exclude for AI Training & Evaluation',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Exclude No. of Days of Machine Data Before',
            # validators=(),
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f'{APP_LABEL}_{_MODEL_OBJECT_NAME}'

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'machine_error_codes'

        ordering = \
            'machine_class__unique_name', \
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

        verbose_name = 'Machine Error Code'
        verbose_name_plural = 'Machine Error Codes'

    def __str__(self) -> str:
        return '{} Error Code "{}"'.format(
                self.machine_class.unique_name.upper(),
                self.name)

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def save(self, *args, **kwargs) -> None:
        self.name = snake_case(self.name)
        assert self.name

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine_class__{search_field}'
                for search_field in MachineClass.search_fields()] + \
               ['name',
                'descriptions']


class MachineError(
        _ModelWithCreatedAndUpdatedMixInABC,
        _ModelWithHasMachineMaintenanceRepairActionsMixInABC,
        _ModelWithHasMachineHealthProblemDiagnosesMixInABC,
        _ModelWithHasMachineHealthRiskAlertsMixInABC,
        _ModelWithDateRangeAndDurationMixInABC,
        _ModelWithMachineFKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_errors'
    RELATED_QUERY_NAME = 'machine_error'

    machine_error_code = \
        ForeignKey(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey
            to=MachineErrorCode,
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
            help_text='Machine Error Code',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Machine Error Code',
            # validators=(),

            limit_choices_to=None,
            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            to_field=None,
            db_constraint=True,
            swappable=True)

    from_utc_date_time = \
        DateTimeField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='From UTC Date-Time',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='From UTC Date-Time',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    to_utc_date_time = \
        DateTimeField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='To UTC Date-Time',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='To UTC Date-Time',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    machine_health_risk_alerts = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineHealthRiskAlert,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Health Risk Alerts',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Health Risk Alerts',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=MachineHealthRiskAlert.machine_errors.through,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_health_problem_diagnoses = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineHealthProblemDiagnosis,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Health Problem Diagnoses',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Health Problem Diagnoses',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=MachineHealthProblemDiagnosis.machine_errors.through,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    machine_maintenance_repair_actions = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to=MachineMaintenanceRepairAction,

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Related Machine Maintenance/Repair Actions',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Related Machine Maintenance/Repair Actions',
            # validators=(),   # ManyToManyField does not support validators

            # *** do not create backwards relation to avoid reverse accessor name clashing ***
            related_name='+',

            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,
            through=MachineMaintenanceRepairAction.machine_errors.through,
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
        
        default_related_name = 'machine_errors'

        ordering = \
            '-to_utc_date_time', \
            'from_utc_date_time'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)

        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{_CONSTRAINT_NAME}" TOO LONG ***')

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine', 'machine_error_code', 'from_utc_date_time'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Error'
        verbose_name_plural = 'Machine Errors'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return '{}: {} from {}{}'.format(
                self.machine,
                self.machine_error_code.name.upper(),
                self.from_utc_date_time,
                ' to {} ({:.3f} Day(s))'.format(self.to_utc_date_time, self.duration / _ONE_DAY_TIME_DELTA)
                    if self.to_utc_date_time
                    else ' (ONGOING)')

    def save(self, *args, **kwargs) -> None:
        if self.to_utc_date_time:
            self.duration = self.to_utc_date_time - self.from_utc_date_time

            _to_date = (self.to_utc_date_time + _ONE_DAY_TIME_DELTA).date()

        else:
            self.duration = _to_date = None

        self.date_range = \
            DateRange(
                lower=(self.from_utc_date_time - _ONE_DAY_TIME_DELTA).date(),
                upper=_to_date,
                bounds='[]',
                empty=False)

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return [f'machine__{search_field}'
                for search_field in Machine.search_fields()] + \
               ['machine_error_code__name',
                'machine_error_code__descriptions']


def machine_health_risk_alert_post_save(sender, instance, *args, **kwargs):
    machine_health_problem_diagnoses = \
        MachineHealthProblemDiagnosis.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_health_problem_diagnoses.set(
        machine_health_problem_diagnoses,
        clear=False)

    machine_health_problem_diagnoses.update(
        has_machine_health_risk_alerts=True)

    machine_maintenance_repair_actions = \
        MachineMaintenanceRepairAction.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_maintenance_repair_actions.set(
        machine_maintenance_repair_actions,
        clear=False)

    machine_maintenance_repair_actions.update(
        has_machine_health_risk_alerts=True)

    machine_errors = \
        MachineError.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_errors.set(
        machine_errors,
        clear=False)

    machine_errors.update(
        has_machine_health_risk_alerts=True)

    MachineHealthRiskAlert.objects.filter(pk=instance.pk).update(
        has_machine_health_problem_diagnoses=bool(machine_health_problem_diagnoses.count()),
        has_machine_maintenance_repair_actions=bool(machine_maintenance_repair_actions.count()),
        has_machine_errors=bool(machine_errors.count()))


post_save.connect(
    receiver=machine_health_risk_alert_post_save,
    sender=MachineHealthRiskAlert,
    weak=True,
    dispatch_uid=None,
    apps=None)


def machine_health_problem_diagnosis_post_save(sender, instance, *args, **kwargs):
    machine_health_risk_alerts = \
        MachineHealthRiskAlert.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_health_risk_alerts.set(
        machine_health_risk_alerts,
        clear=False)

    machine_health_risk_alerts.update(
        has_machine_health_problem_diagnoses=True)

    machine_maintenance_repair_actions = \
        MachineMaintenanceRepairAction.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_maintenance_repair_actions.set(
        machine_maintenance_repair_actions,
        clear=False)

    machine_maintenance_repair_actions.update(
        has_machine_health_problem_diagnoses=True)

    machine_errors = \
        MachineError.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_errors.set(
        machine_errors,
        clear=False)

    machine_errors.update(
        has_machine_health_problem_diagnoses=True)

    MachineHealthProblemDiagnosis.objects.filter(pk=instance.pk).update(
        has_machine_health_risk_alerts=bool(machine_health_risk_alerts.count()),
        has_machine_maintenance_repair_actions=bool(machine_maintenance_repair_actions.count()),
        has_machine_errors=bool(machine_errors.count()))


post_save.connect(
    receiver=machine_health_problem_diagnosis_post_save,
    sender=MachineHealthProblemDiagnosis,
    weak=True,
    dispatch_uid=None,
    apps=None)


def machine_maintenance_repair_action_post_save(sender, instance, *args, **kwargs):
    machine_health_risk_alerts = \
        MachineHealthRiskAlert.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_health_risk_alerts.set(
        machine_health_risk_alerts,
        clear=False)

    machine_health_risk_alerts.update(
        has_machine_maintenance_repair_actions=True)

    machine_health_problem_diagnoses = \
        MachineHealthProblemDiagnosis.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_health_problem_diagnoses.set(
        machine_health_problem_diagnoses,
        clear=False)

    machine_health_problem_diagnoses.update(
        has_machine_maintenance_repair_actions=True)

    machine_errors = \
        MachineError.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_errors.set(
        machine_errors,
        clear=False)

    machine_errors.update(
        has_machine_maintenance_repair_actions=True)

    MachineMaintenanceRepairAction.objects.filter(pk=instance.pk).update(
        has_machine_health_risk_alerts=bool(machine_health_risk_alerts.count()),
        has_machine_health_problem_diagnoses=bool(machine_health_problem_diagnoses.count()),
        has_machine_errors=bool(machine_errors.count()))


post_save.connect(
    receiver=machine_maintenance_repair_action_post_save,
    sender=MachineMaintenanceRepairAction,
    weak=True,
    dispatch_uid=None,
    apps=None)


def machine_error_post_save(sender, instance, *args, **kwargs):
    machine_health_risk_alerts = \
        MachineHealthRiskAlert.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_health_risk_alerts.set(
        machine_health_risk_alerts,
        clear=False)

    machine_health_risk_alerts.update(
        has_machine_errors=True)

    machine_health_problem_diagnoses = \
        MachineHealthProblemDiagnosis.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_health_problem_diagnoses.set(
        machine_health_problem_diagnoses,
        clear=False)

    machine_health_problem_diagnoses.update(
        has_machine_errors=True)

    machine_maintenance_repair_actions = \
        MachineMaintenanceRepairAction.objects.filter(
            machine=instance.machine,
            date_range__overlap=instance.date_range)

    instance.machine_maintenance_repair_actions.set(
        machine_maintenance_repair_actions,
        clear=False)

    machine_maintenance_repair_actions.update(
        has_machine_errors=True)

    MachineError.objects.filter(pk=instance.pk).update(
        has_machine_health_risk_alerts=bool(machine_health_risk_alerts.count()),
        has_machine_health_problem_diagnoses=bool(machine_health_problem_diagnoses.count()),
        has_machine_maintenance_repair_actions=bool(machine_maintenance_repair_actions.count()))


post_save.connect(
    receiver=machine_error_post_save,
    sender=MachineError,
    weak=True,
    dispatch_uid=None,
    apps=None)
