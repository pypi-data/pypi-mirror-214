from django.db.models.base import Model

from django.db.models.constraints import UniqueConstraint

from django.db.models.deletion import PROTECT

from django.db.models.fields import DateTimeField

from django.db.models.fields.related import OneToOneField

from django_util.models import \
    PGSQL_IDENTIFIER_MAX_LEN, \
    _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC, \
    _ModelWithIntPKMixInABC, _ModelWithUUIDPKMixInABC, \
    _EnvVarABC, \
    _ModelWithNonNullableDateMixInABC

from .apps import MachineIntelJobsConfig

from ..data.models import \
    _ModelWithMachineFamilyFKMixInABC, \
    _ModelWithNullableDataToDateABC, \
    MachineClass, MachineFamily

from ..health.models import \
    _ModelWithRefDataToDateABC, \
    AI


# App Label
APP_LABEL = MachineIntelJobsConfig.label


class EnvVar(_EnvVarABC):
    class Meta(_EnvVarABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate '%(app_label)', etc. ***
        db_table = '{}_{}'.format(APP_LABEL, __qualname__.split('.')[0])

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            '*** "{}" TOO LONG ***'.format(db_table)

    class JSONAPIMeta:
        resource_name = \
            '{}.{}'.format(
                __module__,
                __qualname__.split('.')[0])


EnvironmentVariable = EnvVar


class _ModelWithNullableStartDateTimeABC(Model):
    started = \
        DateTimeField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Started at',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Started at',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class _ModelWithNonNullableStartDateTimeABC(Model):
    started = \
        DateTimeField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Started at',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Started at',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class _ModelWithFinishDateTimeABC(Model):
    finished = \
        DateTimeField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateTimeField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Finished at',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Finished at',
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta:
        abstract = True


class MachineFamilyDataStreamsCheckingJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_streams_checking_jobs'
    RELATED_QUERY_NAME = 'machine_family_data_streams_checking_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_data_streams_checking_jobs'

        ordering = 'machine_family',

        verbose_name = 'Machine Family Data Streams Checking Job'
        verbose_name_plural = 'Machine Family Data Streams Checking Jobs'

    def __str__(self) -> str:
        return '{} Machine Data Streams Checking Job'.format(
                self.machine_family)


class MachineFamilyDataStreamsProfilingJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithNullableDataToDateABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_streams_profiling_jobs'
    RELATED_QUERY_NAME = 'machine_family_data_streams_profiling_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_data_streams_profiling_jobs'

        ordering = \
            'machine_family', \
            '-data_to_date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)
        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME)

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'data_to_date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Data Streams Profiling Job'
        verbose_name_plural = 'Machine Family Data Streams Profiling Jobs'

    def __str__(self) -> str:
        return '{} Machine Data Streams Profiling Job{}'.format(
                self.machine_family,
                ' (Data Ending {})'.format(self.data_to_date)
                    if self.data_to_date
                    else '')


class MachineFamilyDataStreamCorrsProfilingJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithNullableDataToDateABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_stream_corrs_profiling_jobs'
    RELATED_QUERY_NAME = 'machine_family_data_stream_corrs_profiling_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_data_stream_corrs_profiling_jobs'

        ordering = \
            'machine_family', \
            '-data_to_date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)
        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME)

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'data_to_date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Data Stream Pairwise Correlations Profiling Job'
        verbose_name_plural = 'Machine Family Data Stream Pairwise Correlations Profiling Jobs'

    def __str__(self) -> str:
        return '{} Machine Data Stream Pairwise Correlations Profiling Job{}'.format(
                self.machine_family,
                ' (Data Ending {})'.format(self.data_to_date)
                    if self.data_to_date
                    else '')


class MachineFamilyDataAggJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithNonNullableDateMixInABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_agg_jobs'
    RELATED_QUERY_NAME = 'machine_family_data_agg_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_data_agg_jobs'

        ordering = \
            'machine_family', \
            '-date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_machine_family_and_date_unique_together'.format(_MODEL_OBJECT_NAME)
        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME)

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Data Agg Job'
        verbose_name_plural = 'Machine Family Data Agg Jobs'

    def __str__(self) -> str:
        return '{} Data Agg Job for {}'.format(
                self.machine_family,
                self.date)


class MachineFamilyDataAggsToDBJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithNonNullableDateMixInABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_data_aggs_to_db_jobs'
    RELATED_QUERY_NAME = 'machine_family_data_aggs_to_db_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_data_aggs_to_db_jobs'

        ordering = \
            'machine_family', \
            '-date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)
        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME)

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Data-Aggs-to-DB Job'
        verbose_name_plural = 'Machine Family Data-Aggs-to-DB Jobs'

    def __str__(self) -> str:
        return '{} Data-Aggs-to-DB Job for {}'.format(
                self.machine_family,
                self.date)


class MachineFamilyAITrainingJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithRefDataToDateABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithUUIDPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_ai_training_jobs'
    RELATED_QUERY_NAME = 'machine_family_ai_training_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, __qualname__.split('.')[0])
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_ai_training_jobs'

        ordering = \
            'machine_family', \
            '-ref_data_to_date', \
            '-started'

        verbose_name = 'Machine Family AI Training Job'
        verbose_name_plural = 'Machine Family AI Training Jobs'

    def __str__(self) -> str:
        return '{} AI Training Job with Ref Data Ending {}'.format(
                self.machine_family,
                self.ref_data_to_date)


class MachineFamilyAIEvaluationJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNullableStartDateTimeABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_ai_evaluation_jobs'
    RELATED_QUERY_NAME = 'machine_family_ai_evaluation_job'

    ai = OneToOneField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField
            to=AI,
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
            help_text='AI',
            primary_key=False,
            unique=True,
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

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, __qualname__.split('.')[0])
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_ai_evaluation_jobs'

        ordering = 'ai',

        verbose_name = 'Machine Family AI Evaluation Job'
        verbose_name_plural = 'Machine Family AI Evaluation Jobs'

    def __str__(self) -> str:
        return '{} Evaluation Job'.format(
                self.ai)


class MachineFamilyHealthRiskScoringJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithNonNullableDateMixInABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_health_risk_scoring_jobs'
    RELATED_QUERY_NAME = 'machine_family_health_risk_scoring_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_health_risk_scoring_jobs'

        ordering = \
            'machine_family', \
            '-date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)
        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME)

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Health Risk Scoring Job'
        verbose_name_plural = 'Machine Family Health Risk Scoring Jobs'

    def __str__(self) -> str:
        return '{} Risk Scoring Job for {}'.format(
                self.machine_family,
                self.date)


class MachineFamilyHealthRiskScoresToDBJob(
        _ModelWithFinishDateTimeABC,
        _ModelWithNonNullableStartDateTimeABC,
        _ModelWithNonNullableDateMixInABC,
        _ModelWithMachineFamilyFKMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'machine_family_health_risk_scores_to_db_jobs'
    RELATED_QUERY_NAME = 'machine_family_health_risk_scores_to_db_job'

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        _MODEL_OBJECT_NAME = __qualname__.split('.')[0]

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = '{}_{}'.format(APP_LABEL, _MODEL_OBJECT_NAME)
        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(db_table)

        default_related_name = 'machine_family_health_risk_scores_to_db_jobs'

        ordering = \
            'machine_family', \
            '-date'

        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        _CONSTRAINT_NAME = '{}_unique_together'.format(_MODEL_OBJECT_NAME)
        assert len(_CONSTRAINT_NAME) <= PGSQL_IDENTIFIER_MAX_LEN, '*** "{}" TOO LONG ***'.format(_CONSTRAINT_NAME)

        constraints = \
            UniqueConstraint(   # https://docs.djangoproject.com/en/dev/ref/models/constraints/#django.db.models.UniqueConstraint
                fields=('machine_family', 'date'),
                name=_CONSTRAINT_NAME,
                condition=None),

        verbose_name = 'Machine Family Risk-Scores-to-DB Job'
        verbose_name_plural = 'Machine Family Risk-Scores-to-DB Jobs'

    def __str__(self) -> str:
        return '{} Risk-Scores-to-DB Job for {}'.format(
                self.machine_family,
                self.date)
