import matplotlib
matplotlib.use('Agg')

from plotnine import \
    ggplot, aes, geom_line, geom_vline, \
    scale_x_datetime, scale_y_continuous, ylim, \
    ggtitle, element_text, theme

import datetime
from dateutil.relativedelta import relativedelta
from django.db.models.aggregates import Min
from django.db.models.query_utils import Q
from django.utils.timezone import make_aware
import numpy
import os
import pandas
from psycopg2.extras import DateRange
import pytz
import re
import tempfile
import time
from tqdm import tqdm
from uuid import uuid4

from pyspark.sql import functions

import arimo.util.data_backend
from infx.ai import _MRegrAIABC, load as load_ai
from infx.ai.cs import m_regr as cs_m_regr, regr as cs_regr
from infx.ai.ts import m_regr as ts_m_regr, regr as ts_regr
from infx.df._abc import _XDFABC
from infx.df.from_files import ArrowXDF
from infx.df.spark import SparkXDF
from infx.df.spark_from_files import ArrowSparkXDF
from arimo.util import fs, Namespace
from arimo.util.date_time import \
    DATE_COL, MONTH_COL, \
    _PRED_VARS_INCL_T_AUX_COLS, _T_WoM_COL, _T_DoW_COL, _T_DELTA_COL, _T_PoM_COL, _T_PoW_COL, _T_PoD_COL, \
    month_end, month_str
from arimo.util.iterables import to_iterable

from arimo.util.aws import s3

from ....data.api.python import Client as MachineDataClient
from ....util import _PARQUET_EXT, snake_case, format_number_up_to_n_decimal_places, NonOverlappingClosedIntervals


TODAY = datetime.date.today()


class Client(MachineDataClient):
    VITAL_MACHINE_DATA_STREAM_MIN_STRICTLY_OUTLIER_ROBUST_PROPORTION = .32
    
    REF_N_MONTHS = 24

    EVAL_REF_DATA_FRACTION = .32

    _LOADED_AIS = {}

    MIN_FRACTION_OF_GOOD_COMPONENT_AIS = .01   # previously .32, too strict

    MAX_INDIV_OVER_GLOBAL_REF_EVAL_METRIC_RATIO = 1.68

    _M_REGR_AI_UNIQUE_ID_COL = 'ai_unique_id'

    _OVERALL_M_REGR_RISK_SCORE_NAME_PREFIX = 'rowHigh__'

    DEFAULT_EMA_ALPHA = .168

    _DEFAULT_EMA_ALPHA_PREFIX = 'ema' + '{:.3f}'.format(DEFAULT_EMA_ALPHA)[-3:] + '__'

    _ALERT_RECURRENCE_GROUPING_INTERVAL = 30

    _DEFAULT_PARAMS = Namespace(**MachineDataClient._DEFAULT_PARAMS)

    _DEFAULT_PARAMS.update(
        s3=Namespace(
            machine_data=Namespace(
                train_val_eval_machine_family_conso_dir_prefix='.arimo/PredMaint/EquipmentData/TrainValBenchmark',   # TODO: 'tmp/TrainValEvalMachineFamilyConsoData'
            ),

            ais_dir_prefix='.arimo/PredMaint/PPP/Blueprints',   # TODO: 'tmp/AIs'
            err_mults_dir_prefix='.arimo/PredMaint/PPP/ErrMults',   # TODO: 'tmp/ErrMults'
            day_err_mults_dir_prefix='.arimo/PredMaint/PPP/DailyErrMults',   # TODO: 'tmp/DayErrMults'

            risk_scores=Namespace(
                dir_prefix='.arimo/PredMaint/AnomScores',   # TODO: 'tmp/RiskScores'
                file_name='PPPAnomScores{}'.format(_PARQUET_EXT)   # TODO: 'MRegrAIbased-RiskScores'
                )),

        health_monitoring=Namespace(
            risk_score_names_and_thresholds=dict(
                # dayMean__rowHigh__abs__MAEx=(2.5, 3, 3.5, 4, 4.5, 5),
                rowHigh__dayMean__abs__MAEx=(2.5, 3, 3.5, 4, 4.5, 5))))

    def __init__(self, name='test', *, params={}, **kwargs):
        super().__init__(
            name=name,
            params=params,
            **kwargs)

        from ...models import \
            MachineFamilyHealthServiceConfig, \
            AI, AIModel, \
            MachineFamilyVitalAIEvalMetricProfile, \
            MachineHealthRiskScoreMethod, MachineHealthRiskScore, \
            MachineHealthRiskAlert, \
            MachineHealthProblem, MachineHealthProblemDiagnosis, \
            MachineMaintenanceRepairAction, \
            MachineErrorCode, MachineError

        from ....jobs.models import \
            MachineFamilyAITrainingJob, MachineFamilyAIEvaluationJob, \
            MachineFamilyHealthRiskScoringJob, MachineFamilyHealthRiskScoresToDBJob

        self.db.update(dict(
            MachineFamilyHealthServiceConfigs=MachineFamilyHealthServiceConfig.objects,
            AIs=AI.objects,
            AIModels=AIModel.objects,
            MachineFamilyVitalDataStreamAIEvalMetricProfiles=MachineFamilyVitalAIEvalMetricProfile.objects,

            MachineHealthRiskScoreMethods=MachineHealthRiskScoreMethod.objects,
            MachineHealthRiskScores=MachineHealthRiskScore.objects,

            MachineHealthRiskAlerts=MachineHealthRiskAlert.objects,

            MachineHealthProblems=MachineHealthProblem.objects,
            MachineHealthProblemDiagnoses=MachineHealthProblemDiagnosis.objects,

            MachineMaintenanceRepairActions=MachineMaintenanceRepairAction.objects,

            MachineErrorCodes=MachineErrorCode.objects,
            MachineErrors=MachineError.objects,

            MachineFamilyAITrainingJobs=MachineFamilyAITrainingJob.objects,
            MachineFamilyAIEvaluationJobs=MachineFamilyAIEvaluationJob.objects,
            
            MachineFamilyRiskScoringJobs=MachineFamilyHealthRiskScoringJob.objects,
            MachineFamilyRiskScoresToDBJobs=MachineFamilyHealthRiskScoresToDBJob.objects))

        self.refresh_machine_families_vital_and_incl_excl_input_data_streams()

        # Machine Data
        self.params.s3.machine_data.train_val_eval_machine_family_conso_dir_path = \
            's3://{}/{}'.format(
                self.params.s3.bucket,
                self.params.s3.machine_data.train_val_eval_machine_family_conso_dir_prefix)

        # AI
        self.params.s3.ais_dir_path = \
            's3://{}/{}'.format(
                self.params.s3.bucket,
                self.params.s3.ais_dir_prefix)

    def refresh_machine_families_vital_and_incl_excl_input_data_streams(self):
        # Machine Families' Vital & Included/Excluded Input Data Streams
        self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams = Namespace()

        for machine_family_health_service_config in self.db.MachineFamilyHealthServiceConfigs.all():
            machine_class_name = machine_family_health_service_config.machine_family.machine_class.unique_name

            if machine_class_name not in self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams:
                self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[machine_class_name] = Namespace()

            machine_family_name = machine_family_health_service_config.machine_family.unique_name

            if machine_family_name not in self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[machine_class_name]:
                self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[machine_class_name][machine_family_name] = Namespace()

            incl_cat_input_machine_data_stream_names = \
                {incl_input_machine_data_stream.name
                 for incl_input_machine_data_stream in
                    machine_family_health_service_config.machine_family.machine_data_streams.exclude(
                        logical_data_type__in=self.NUM_LOGICAL_DATA_TYPES)} \
                if machine_family_health_service_config.incl_cat_input_machine_data_streams \
                else set()

            for machine_family_vital_data_stream_config in \
                    machine_family_health_service_config.machine_family_vital_data_stream_configs.filter(active=True):
                excl_input_machine_data_stream_names = \
                    {excl_input_machine_data_stream.name
                     for excl_input_machine_data_stream in
                        machine_family_health_service_config.excl_input_machine_data_streams.all().union(
                            machine_family_vital_data_stream_config.excl_input_machine_data_streams.all(),
                            all=False)}

                self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[machine_class_name][machine_family_name][machine_family_vital_data_stream_config.vital_machine_data_stream.name] = \
                    Namespace(
                        incl=incl_cat_input_machine_data_stream_names.union(
                                incl_input_machine_data_stream.name
                                for incl_input_machine_data_stream in
                                    machine_family_health_service_config.machine_family.machine_data_streams.filter(
                                        name__in={i[0] for i in machine_family_vital_data_stream_config.auto_incl_input_machine_data_streams})
                                    .union(
                                        machine_family_vital_data_stream_config.incl_input_machine_data_streams.all(),
                                        all=False))
                            .difference(excl_input_machine_data_stream_names),
                        excl=excl_input_machine_data_stream_names)

    def recommend_m_regr_ai_vital_and_input_machine_data_streams(
            self,
            machine_class_name, machine_family_name,   # TODO: /
            *,
            abs_corr_lower_threshold=.168, abs_corr_upper_threshold=.888) -> None:
        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        from_date = \
            self.db.MachineFamilyData \
            .filter(machine_family=machine_family) \
            .aggregate(Min(DATE_COL)) \
            ['{}__min'.format(DATE_COL)]

        assert pandas.notnull(from_date)

        machine_family_health_service_config, _ = \
            self.db.MachineFamilyHealthServiceConfigs.get_or_create(
                machine_family=machine_family,
                defaults=dict(
                            from_date=from_date,
                            active=True))

        machine_family_candidate_vital_data_streams = \
            machine_family.machine_data_streams \
            .filter(
                machine_data_stream_type__in=
                    (self.SENSOR_MACHINE_DATA_STREAM_TYPE,
                     self.CALC_MACHINE_DATA_STREAM_TYPE),
                logical_data_type__in=self.NUM_LOGICAL_DATA_TYPES) \
            .difference(
                machine_family_health_service_config.excl_input_machine_data_streams.all())

        machine_family_data_field_pair_corrs = \
            self.db.MachineFamilyDataStreamPairCorrs.filter(
                machine_family_data__machine_family=machine_family,
                data_to_date=None)

        assert machine_family_data_field_pair_corrs.count()

        from ...models import MachineFamilyVitalDataStreamConfig

        for machine_family_candidate_vital_data_stream in tqdm(machine_family_candidate_vital_data_streams):
            machine_family_candidate_vital_data_stream_config, _ = \
                MachineFamilyVitalDataStreamConfig.objects.get_or_create(
                    machine_family_health_service_config=machine_family_health_service_config,
                    vital_machine_data_stream=machine_family_candidate_vital_data_stream)

            machine_family_candidate_vital_data_stream_profile = \
                machine_family_candidate_vital_data_stream_config.vital_machine_data_stream_profile

            if machine_family_candidate_vital_data_stream_profile:
                if machine_family_candidate_vital_data_stream_profile.strictly_outlier_robust_proportion \
                        >= self.VITAL_MACHINE_DATA_STREAM_MIN_STRICTLY_OUTLIER_ROBUST_PROPORTION:
                    if machine_family_candidate_vital_data_stream_profile.n_distinct_values >= self._MAX_N_DISTINCT_VALUES_TO_PROFILE:
                        if machine_family_candidate_vital_data_stream_profile.min == \
                                machine_family_candidate_vital_data_stream_profile._3rd_quartile:
                            machine_family_candidate_vital_data_stream_config.active = False

                            machine_family_candidate_vital_data_stream_config.comments = \
                                '*** TOO SKEWED: MIN = 3RD QUARTILE = {} ***'.format(
                                    format_number_up_to_n_decimal_places(
                                        machine_family_candidate_vital_data_stream_profile.min))

                        elif machine_family_candidate_vital_data_stream_profile.robust_min == \
                                machine_family_candidate_vital_data_stream_profile._3rd_quartile:
                            machine_family_candidate_vital_data_stream_config.active = False

                            machine_family_candidate_vital_data_stream_config.comments = \
                                '*** TOO SKEWED: ROBUST MIN = 3RD QUARTILE = {} ***'.format(
                                    format_number_up_to_n_decimal_places(
                                        machine_family_candidate_vital_data_stream_profile.robust_min))

                        elif machine_family_candidate_vital_data_stream_profile.robust_max == \
                                machine_family_candidate_vital_data_stream_profile.quartile:
                            machine_family_candidate_vital_data_stream_config.active = False

                            machine_family_candidate_vital_data_stream_config.comments = \
                                '*** TOO SKEWED: ROBUST MAX = QUARTILE = {} ***'.format(
                                    format_number_up_to_n_decimal_places(
                                        machine_family_candidate_vital_data_stream_profile.robust_max))

                        elif machine_family_candidate_vital_data_stream_profile.max == \
                                machine_family_candidate_vital_data_stream_profile.quartile:
                            machine_family_candidate_vital_data_stream_config.active = False

                            machine_family_candidate_vital_data_stream_config.comments = \
                                '*** TOO SKEWED: MAX = QUARTILE = {} ***'.format(
                                    format_number_up_to_n_decimal_places(
                                        machine_family_candidate_vital_data_stream_profile.max))

                        else:
                            machine_family_candidate_vital_data_stream_config.active = True

                            if machine_family_candidate_vital_data_stream_profile.median == \
                                    machine_family_candidate_vital_data_stream_profile.min:
                                machine_family_candidate_vital_data_stream_config.comments = \
                                    '*** SKEWED: MEDIAN = MIN = {} ***'.format(
                                        format_number_up_to_n_decimal_places(
                                            machine_family_candidate_vital_data_stream_profile.median))

                            elif machine_family_candidate_vital_data_stream_profile.median == \
                                     machine_family_candidate_vital_data_stream_profile.max:
                                machine_family_candidate_vital_data_stream_config.comments = \
                                    '*** SKEWED: MEDIAN = MAX = {} ***'.format(
                                        format_number_up_to_n_decimal_places(
                                            machine_family_candidate_vital_data_stream_profile.max))

                    else:
                        machine_family_candidate_vital_data_stream_config.active = False

                        machine_family_candidate_vital_data_stream_config.comments = \
                            '*** INSUFFICIENT NUMBER OF ({}) DISTINCT DATA VALUES ***'.format(
                                machine_family_candidate_vital_data_stream_profile.n_distinct_values)

                else:
                    machine_family_candidate_vital_data_stream_config.active = False

                    machine_family_candidate_vital_data_stream_config.comments = \
                        '*** STRICTLY OUTLIER-ROBUST DATA PROPORTION {:.3f} < {:.3f} ***'.format(
                            machine_family_candidate_vital_data_stream_profile.strictly_outlier_robust_proportion,
                            self.VITAL_MACHINE_DATA_STREAM_MIN_STRICTLY_OUTLIER_ROBUST_PROPORTION)

            else:
                machine_family_candidate_vital_data_stream_config.active = False

                machine_family_candidate_vital_data_stream_config.comments = \
                    '*** NO DATA PROFILE ***'

            _machine_family_data_field_pair_corrs = \
                machine_family_data_field_pair_corrs.filter(
                    machine_data_stream=machine_family_candidate_vital_data_stream)

            # *** using ordered lists below because PostgreSQL JSONB does not preserve dictionary key ordering ***
            machine_family_candidate_vital_data_stream_config.high_corr_num_machine_data_streams = \
                [(i['other_machine_data_stream__name'], i['corr'])
                 for i in
                    sorted(
                        _machine_family_data_field_pair_corrs
                            .exclude(corr__range=(-abs_corr_upper_threshold, abs_corr_upper_threshold))
                            .values('other_machine_data_stream__name', 'corr'),
                        key=lambda i: abs(i['corr']),
                        reverse=True)]

            machine_family_candidate_vital_data_stream_config.auto_incl_input_machine_data_streams = \
                [(i['other_machine_data_stream__name'], i['corr'])
                 for i in
                    sorted(
                        _machine_family_data_field_pair_corrs
                            .filter(corr__gte=-abs_corr_upper_threshold)
                            .filter(corr__lte=abs_corr_upper_threshold)
                            .exclude(corr__range=(-abs_corr_lower_threshold, abs_corr_lower_threshold))
                            .values('other_machine_data_stream__name', 'corr'),
                        key=lambda i: abs(i['corr']),
                        reverse=True)]

            machine_family_candidate_vital_data_stream_config.low_corr_num_machine_data_streams = \
                [(i['other_machine_data_stream__name'], i['corr'])
                 for i in
                    sorted(
                        _machine_family_data_field_pair_corrs
                            .filter(corr__range=(-abs_corr_lower_threshold, abs_corr_lower_threshold))
                            .values('other_machine_data_stream__name', 'corr'),
                        key=lambda i: abs(i['corr']),
                        reverse=True)]

            machine_family_candidate_vital_data_stream_config.save()

        machine_family_health_service_config \
        .machine_family_vital_data_stream_configs \
        .exclude(
            vital_machine_data_stream__in=
                set(machine_family_candidate_vital_data_streams)
                # using set(...) ^ to avoid django.db.utils.ProgrammingError: subquery has too many columns
        ).update(
            active=False)

    def setup_machine_family_health_service(self, machine_class_name, machine_family_name):
        # 0. MANUALLY:
        # - create Machine Class beforehand
        # - create Machine Family beforehand
        # - associate Machine Family with Machine SKUs, Machine Data Streams & Machines

        # 1. MANUALLY run chk-data-streams to check whether data has been correctly organized on S3 vs. DB
        self.stdout_logger.info(
            msg=self.check_machine_family_data_streams(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name))

        # 2. MANUALLY run profile-data to profile Machine Data Streams' statistics
        self.profile_machine_family_data_streams(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name,
            to_month=None)

        # 3. MANUALLY update Machine Data Streams' attributes

        # 4. Automatically profile numerical Machine Data Streams' pair-wise correlations
        self.profile_machine_family_num_data_stream_pair_corrs(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name,
            to_month=None)

        # 5. Set Up Candidate Vital Machine Data Streams &
        # automatically recommend Input Machine Data Streams
        self.recommend_m_regr_ai_vital_and_input_machine_data_streams(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name)
        
        # 6. MANUALLY refine Health Service Configs
        # - check mechanical definitions of candidate vitals
        #   to exclude those too exposed to exogenous environmental factors or with inconsistent definitions/designs

    def _machine_family_train_val_data_set_name(
            self,
            machine_class_name, machine_family_name,
            to_month):
        return '{}---from-{}---to-{}---TrainVal'.format(
                self.machine_family_conventional_full_name(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name),
                str((datetime.datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                     relativedelta(months=self.REF_N_MONTHS - 1)).date())[:7],
                to_month)

    def _machine_family_train_val_data_set_path(
            self,
            machine_class_name, machine_family_name,
            to_month,
            s3_dir_path=None):
        if s3_dir_path:
            assert s3_dir_path.startswith('s3://')
        else:
            s3_dir_path = self.params.s3.machine_data.train_val_eval_machine_family_conso_dir_path

        return os.path.join(
                s3_dir_path,
                self._machine_family_train_val_data_set_name(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name,
                    to_month=to_month)
                + _PARQUET_EXT)

    def _machine_family_eval_data_set_name(
            self,
            machine_class_name, machine_family_name,
            to_month):
        return '{}---from-{}---to-{}---Eval'.format(
                self.machine_family_conventional_full_name(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name),
                str((datetime.datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                    relativedelta(months=self.REF_N_MONTHS - 1)).date())[:7],
                to_month)

    def _machine_family_eval_data_set_path(
            self,
            machine_class_name, machine_family_name,
            to_month,
            s3_dir_path=None):
        if s3_dir_path:
            assert s3_dir_path.startswith('s3://')
        else:
            s3_dir_path = self.params.s3.machine_data.train_val_eval_machine_family_conso_dir_path

        return os.path.join(
                s3_dir_path,
                self._machine_family_eval_data_set_name(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name,
                    to_month=to_month)
                + _PARQUET_EXT)

    def create_train_val_eval_data_sets(
            self,
            machine_class_name, machine_family_name,
            to_month,
            s3_dir_path=None):
        machine_family_arrow_spark_xdf = \
            self.load_machine_family_data(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name,
                _from_files=True,
                _spark=True,
                set_i_col=True,
                set_t_col=False,
                verbose=True) \
            .filterPartitions(
                (DATE_COL,
                 str((datetime.datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                      relativedelta(months=self.REF_N_MONTHS - 1)).date()),
                 '{}-31'.format(to_month)))

        sql_exclude_conditions = []

        TODAY = datetime.date.today()

        for machine_unique_id in \
                tqdm(machine_family_arrow_spark_xdf(
                        'SELECT DISTINCT {} FROM this'
                        .format(self._MACHINE_UNIQUE_ID_COL_NAME))
                     .toPandas()
                     [self._MACHINE_UNIQUE_ID_COL_NAME]):
            machine = \
                self.update_or_create_machine(
                    machine_class_name=machine_class_name,
                    machine_unique_id=machine_unique_id,
                    create=False)

            excl_machine_data_date_ranges = NonOverlappingClosedIntervals()

            for machine_health_problem_diagnosis_date_range in \
                    self.db.MachineHealthProblemDiagnoses \
                    .filter(
                        machine=machine) \
                    .exclude(
                        machine_health_problems=None)\
                    .values(
                        'from_date',
                        'to_date'):
                excl_machine_data_date_ranges.add(
                    interval=
                        [machine_health_problem_diagnosis_date_range['from_date'],
                         machine_health_problem_diagnosis_date_range['to_date']
                            if machine_health_problem_diagnosis_date_range['to_date']
                            else TODAY])

            for machine_maintenance_repair_action_date_range in \
                    self.db.MachineMaintenanceRepairActions \
                    .filter(
                        machine=machine) \
                    .values(
                        'from_date',
                        'to_date'):
                excl_machine_data_date_ranges.add(
                    interval=
                        [machine_maintenance_repair_action_date_range['from_date'],
                         machine_maintenance_repair_action_date_range['to_date']
                            if machine_maintenance_repair_action_date_range['to_date']
                            else TODAY])

            for machine_error_date_range_and_n_days_of_prior_machine_data_to_exclude in \
                    self.db.MachineErrors \
                    .filter(
                        machine=machine,
                        machine_error_code__excl_n_days_of_machine_data_before__gt=0) \
                    .values(
                        'date_range',
                        'machine_error_code__excl_n_days_of_machine_data_before'):
                machine_error_date_range = \
                    machine_error_date_range_and_n_days_of_prior_machine_data_to_exclude['date_range']

                machine_error_n_days_of_prior_machine_data_to_exclude = \
                    machine_error_date_range_and_n_days_of_prior_machine_data_to_exclude[
                        'machine_error_code__excl_n_days_of_machine_data_before']
                assert machine_error_n_days_of_prior_machine_data_to_exclude > 0

                excl_machine_data_date_ranges.add(
                    interval=
                        [machine_error_date_range.lower
                            - datetime.timedelta(
                                days=machine_error_n_days_of_prior_machine_data_to_exclude - 1),
                         machine_error_date_range.upper
                            if machine_error_date_range.upper
                            else TODAY])

            if excl_machine_data_date_ranges:
                sql_exclude_conditions += \
                    ["(({} = {}) AND ({} BETWEEN '{}' AND '{}'))".format(
                        self._MACHINE_UNIQUE_ID_COL_NAME,
                        "'{}'".format(machine_unique_id)
                            if isinstance(machine_unique_id, str)
                            else machine_unique_id,
                        DATE_COL,
                        excl_machine_data_from_date,
                        excl_machine_data_to_date)
                     for excl_machine_data_from_date, excl_machine_data_to_date in
                        excl_machine_data_date_ranges.intervals]

        if sql_exclude_conditions:
            self.stdout_logger.info(
                msg='Excluding Machine Data Date Ranges: {}...'
                    .format(sql_exclude_conditions))

            machine_family_arrow_spark_xdf.filter(
                condition='NOT({})'.format(
                            ' OR '.join(sql_exclude_conditions)),
                inplace=True)

            machine_family_arrow_spark_xdf.tCol = self._LOCAL_DATE_TIME_COL_NAME

            _tmp_s3_dir_path = \
                os.path.join(
                    self.params.s3.bucket_path,
                    machine_family_arrow_spark_xdf.tmpDirS3Key,
                    str(uuid4()))

            machine_family_arrow_spark_xdf.save(
                path=_tmp_s3_dir_path,
                format='parquet',
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                mode='overwrite',
                partitionBy=DATE_COL,
                verbose=True,
                switch=False)

            # free up Spark resources for other tasks
            arimo.util.data_backend.spark.stop()

            machine_family_arrow_xdf = \
                ArrowXDF(
                    path=_tmp_s3_dir_path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=self._MACHINE_UNIQUE_ID_COL_NAME,
                    tCol=self._LOCAL_DATE_TIME_COL_NAME,
                    verbose=True)

        else:
            machine_family_arrow_xdf = \
                ArrowXDF(
                    path=machine_family_arrow_spark_xdf.path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    iCol=self._MACHINE_UNIQUE_ID_COL_NAME,
                    tCol=self._LOCAL_DATE_TIME_COL_NAME,
                    verbose=True)

        train_val_arrow_xdf, eval_arrow_xdf = \
            machine_family_arrow_xdf.split(
                1 - self.EVAL_REF_DATA_FRACTION,
                self.EVAL_REF_DATA_FRACTION)

        train_val_arrow_xdf.copyToPath(
            path=self._machine_family_train_val_data_set_path(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name,
                    to_month=to_month,
                    s3_dir_path=s3_dir_path))

        eval_arrow_xdf.copyToPath(
            path=self._machine_family_eval_data_set_path(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name,
                    to_month=to_month,
                    s3_dir_path=s3_dir_path))

    def _train_val_arrow_xdf(
            self,
            machine_class_name,
            machine_family_name,
            to_month,
            set_i_col=True,
            verbose=True):
        train_val_arrow_xdf = \
            ArrowXDF(
                path=self._machine_family_train_val_data_set_path(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name,
                        to_month=to_month),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=self._MACHINE_UNIQUE_ID_COL_NAME
                    if set_i_col
                    else None,
                tCol=self._LOCAL_DATE_TIME_COL_NAME,
                verbose=verbose)

        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name,
                create=False,
                machine_class_name=machine_class_name)

        for col in train_val_arrow_xdf.possibleNumContentCols:
            machine_data_stream = \
                machine_family.machine_class.machine_data_streams.filter(
                    name=snake_case(col)) \
                .first()

            if machine_data_stream:
                train_val_arrow_xdf._nulls[col] = \
                    machine_data_stream.neg_invalid, \
                    machine_data_stream.pos_invalid

        return train_val_arrow_xdf

    def _eval_arrow_spark_xdf(
            self,
            machine_class_name,
            machine_family_name,
            to_month,
            set_i_col=True,
            verbose=True):
        return ArrowSparkXDF(
                path=self._machine_family_eval_data_set_path(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name,
                        to_month=to_month),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                iCol=self._MACHINE_UNIQUE_ID_COL_NAME
                    if set_i_col
                    else None,
                tCol=self._LOCAL_DATE_TIME_COL_NAME,
                verbose=verbose)

    def _m_regr_ai(
            self, unique_id=None, set_unique_id=None,
            machine_class_name=None, machine_family_name=None,
            timeser_input_len=1, incl_time_features=True, excl_mth_time_features=False,
            __model_params__=
                {'train.n_samples': 10 ** 8,
                 'train.n_train_samples_per_epoch': 10 ** 6,
                 'train.min_n_val_samples_per_epoch': 10 ** 5,
                 'train.batch_size': 500,
                 'train.val_batch_size': 10 ** 4},
            params={}, **kwargs):
        if unique_id:
            if unique_id not in self._LOADED_AIS:
                self._LOADED_AIS[unique_id] = \
                    load_ai(
                        dir_path=
                            os.path.join(
                                self.params.s3.ais_dir_path,
                                unique_id),
                        s3_bucket=self.params.s3.bucket,
                        s3_dir_prefix=
                            os.path.join(
                                self.params.s3.ais_dir_prefix,
                                unique_id),
                        aws_access_key_id=self.params.s3.access_key_id,
                        aws_secret_access_key=self.params.s3.secret_access_key,
                        s3_client=self.s3_client,
                        verbose=False)

            return self._LOADED_AIS[unique_id]

        else:
            assert machine_class_name \
               and machine_family_name

            machine_data_streams = \
                self.machine_family(
                    machine_family_name=machine_family_name) \
                .machine_data_streams.all()

            cat_machine_data_stream_names = []
            num_machine_data_stream_names = []

            for machine_data_stream in machine_data_streams:
                if machine_data_stream.logical_data_type == self.CAT_LOGICAL_DATA_TYPE:
                    cat_machine_data_stream_names.append(machine_data_stream.name)

                elif machine_data_stream.logical_data_type in self.NUM_LOGICAL_DATA_TYPES:
                    num_machine_data_stream_names.append(machine_data_stream.name)

            _pred_vars_incl = \
                ([_T_WoM_COL, _T_DoW_COL,
                  _T_DELTA_COL,
                  _T_PoM_COL, _T_PoW_COL, _T_PoD_COL]
                 if excl_mth_time_features
                 else list(_PRED_VARS_INCL_T_AUX_COLS)) \
                if incl_time_features \
                else []

            _pred_vars_excl = \
                list(set(SparkXDF._T_COMPONENT_AUX_COLS)
                     .difference(_pred_vars_incl))

            component_ais = {}

            for vital_num_machine_data_stream_name, incl_excl_input_machine_data_stream_names in \
                    self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[machine_class_name][machine_family_name].items():
                # verify uniqueness of vital data stream
                _vital_num_machine_data_stream = \
                    machine_data_streams.get(
                        name=vital_num_machine_data_stream_name,
                        logical_data_type__in=self.NUM_LOGICAL_DATA_TYPES)

                component_ais[vital_num_machine_data_stream_name] = \
                    ts_regr.DLAI(
                        params=Namespace(
                                data=Namespace(
                                        label=Namespace(
                                                var=vital_num_machine_data_stream_name),

                                        pred_vars=
                                            _pred_vars_incl +
                                            to_iterable(incl_excl_input_machine_data_stream_names.incl, iterable_type=list),

                                        pred_vars_excl=
                                            _pred_vars_excl +
                                            [vital_num_machine_data_stream_name] +
                                            to_iterable(incl_excl_input_machine_data_stream_names.excl, iterable_type=list),

                                        force_cat=cat_machine_data_stream_names,
                                        force_num=num_machine_data_stream_names),

                                min_input_ser_len=timeser_input_len,
                                max_input_ser_len=timeser_input_len),

                        verbose=False) \
                    if timeser_input_len > 1 \
                    else cs_regr.DLAI(
                        params=Namespace(
                                data=Namespace(
                                        label=Namespace(
                                                var=vital_num_machine_data_stream_name),

                                        pred_vars=
                                            _pred_vars_incl +
                                            to_iterable(incl_excl_input_machine_data_stream_names.incl, iterable_type=list),

                                        pred_vars_excl=
                                            _pred_vars_excl +
                                            [vital_num_machine_data_stream_name] +
                                            to_iterable(incl_excl_input_machine_data_stream_names.excl, iterable_type=list),

                                        force_cat=cat_machine_data_stream_names,
                                        force_num=num_machine_data_stream_names)),

                        verbose=False)

            ai_params = \
                Namespace(
                    data=Namespace(
                            id_col=self._MACHINE_UNIQUE_ID_COL_NAME,
                            time_col=self._LOCAL_DATE_TIME_COL_NAME,

                            force_cat=cat_machine_data_stream_names,
                            force_num=num_machine_data_stream_names,

                            nulls={machine_data_stream.name:
                                    (machine_data_stream.neg_invalid, machine_data_stream.pos_invalid)
                                   for machine_data_stream in machine_data_streams}),

                    model=Namespace(
                            component_ais=component_ais),

                    persist=Namespace(
                                s3=Namespace(
                                    bucket=self.params.s3.bucket,
                                    dir_prefix=self.params.s3.ais_dir_prefix)))

            ai_params.update(params)

            return (ts_m_regr.DLMRegrAI
                    if timeser_input_len > 1
                    else cs_m_regr.DLMRegrAI)(
                            uuid=set_unique_id,
                            params=ai_params, __model_params__=__model_params__,
                            aws_access_key_id=self.params.s3.access_key_id,
                            aws_secret_access_key=self.params.s3.secret_access_key,
                            verbose=False,
                            **kwargs)

    def train_m_regr_ai(
            self,
            machine_class_name, machine_family_name,
            to_month,
            timeser_input_len=1, incl_time_features=True,
            __model_params__=
                {'train.n_samples': 248 * 10 ** 6,
                 'train.n_train_samples_per_epoch': 10 ** 6,
                 'train.min_n_val_samples_per_epoch': 10 ** 5,
                 'train.batch_size': 500,
                 'train.val_batch_size': 10 ** 4},
            params={},
            verbose=True,
            _spark=False,
            **kwargs):
        self.profile_machine_family_data_streams(
            machine_class_name=machine_class_name,
            machine_family_name=machine_family_name,
            to_month=to_month)

        machine_family_ai_training_job = \
            self.db.MachineFamilyAITrainingJobs.create(
                machine_family=self.machine_family(machine_family_name=machine_family_name),
                ref_data_to_date=month_end(to_month),
                started=make_aware(
                            value=datetime.datetime.utcnow(),
                            timezone=pytz.UTC,
                            is_dst=None))

        m_regr_ai_unique_id = \
            '{}---{}---to-{}---{}'.format(
                machine_class_name.upper(),
                machine_family_name,
                to_month,
                machine_family_ai_training_job.uuid)

        m_regr_ai = \
            self._m_regr_ai(
                set_unique_id=m_regr_ai_unique_id,
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name,
                timeser_input_len=timeser_input_len,
                incl_time_features=incl_time_features, excl_mth_time_features=False,
                __model_params__=__model_params__, params=params)

        m_regr_ai.train(
            df=self._train_val_arrow_xdf(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name,
                to_month=to_month,
                set_i_col=timeser_input_len > 1,
                verbose=verbose),
            verbose=verbose,
            **kwargs)

        self.save_m_regr_ai(
            m_regr_ai=m_regr_ai,
            unique_id=m_regr_ai_unique_id,
            machine_family_name=machine_family_name,
            to_month=to_month)

        machine_family_ai_training_job.finished = \
            make_aware(
                value=datetime.datetime.utcnow(),
                timezone=pytz.UTC,
                is_dst=None)
        
        machine_family_ai_training_job.save()

        return m_regr_ai

    def save_m_regr_ai(
            self, m_regr_ai=None, unique_id=None,
            machine_family_name=None, to_month=None):
        if m_regr_ai:
            if unique_id:
                assert m_regr_ai.params.uuid == unique_id

            else:
                unique_id = m_regr_ai.params.uuid

        else:
            assert unique_id
            m_regr_ai = self._m_regr_ai(unique_id=unique_id)

        component_ais = \
            {vital_machine_data_stream_name: component_ai_params
             for vital_machine_data_stream_name, component_ai_params in m_regr_ai.params.model.component_ais.items()
             if component_ai_params.model.ver}

        if component_ais:
            if machine_family_name and to_month:
                ref_data_to_date = month_end(to_month)

            else:
                _MACHINE_CLASS_NAME, machine_family_name, year, month, _uuid = \
                    re.search('(.+)---(.+)---to-(.+)-(.+)---(.+)', unique_id).groups()

                ref_data_to_date = month_end('{}-{}'.format(year, month))

            try:
                ai, _ = \
                    self.db.AIs.get_or_create(
                        machine_family=self.machine_family(machine_family_name=machine_family_name),
                        unique_id=unique_id,
                        ref_data_to_date=ref_data_to_date)

            except Exception as err:
                self.stdout_logger.warn(msg='*** {} ***'.format(err))

                # force reconnect with db to overcome django.db.utils.OperationalError: SSL SYSCALL error: EOF detected
                # ref: https://stackoverflow.com/questions/48329685/how-can-i-force-django-to-restart-a-database-connection-from-the-shell
                from django.db import connection
                connection.connect()

                ai, _ = \
                    self.db.AIs.get_or_create(
                        machine_family=self.machine_family(machine_family_name=machine_family_name),
                        unique_id=unique_id,
                        ref_data_to_date=ref_data_to_date)

            machine_class_name = ai.machine_family.machine_class.unique_name

            for vital_machine_data_stream_name, component_ai_params in component_ais.items():
                assert (component_ai_params.data.pred_vars_incl is None) \
                   and (component_ai_params.data.pred_vars_excl is None)

                ai_model, _ = \
                    self.db.AIModels.get_or_create(
                        ai=ai,
                        target_machine_data_stream=
                            self.machine_data_stream(
                                machine_class_name,
                                vital_machine_data_stream_name,
                                create=False))

                ai_model.input_machine_data_streams.set(
                    self.machine_data_stream(
                        machine_class_name,
                        input_machine_data_stream_name,
                        create=False)
                    for input_machine_data_stream_name in
                        set(component_ai_params.data.pred_vars).difference(_PRED_VARS_INCL_T_AUX_COLS))

            self.db.MachineFamilyAIEvaluationJobs.get_or_create(ai=ai)

        else:
            self.stdout_logger.warn(
                msg='*** {} DOES NOT HAVE SUFFICIENT NO. OF TRAINED COMPONENT AIs ***'
                    .format(unique_id))

    def _good_m_regr_label_var_names(self, m_regr_ai_obj, ref_eval_metrics=None):
        if not ref_eval_metrics:
            ref_eval_metrics = m_regr_ai_obj.ref_eval_metrics

        label_var_names = []

        for label_var_name in \
                self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[m_regr_ai_obj.machine_family.machine_class.unique_name][m_regr_ai_obj.machine_family.unique_name]:
            ref_eval_metrics_for_label_var_name = ref_eval_metrics.get(label_var_name)

            if ref_eval_metrics_for_label_var_name:
                if _MRegrAIABC._is_good_component_ai(
                        label_var_name=label_var_name,
                        ref_eval_metrics_for_label_var_name=ref_eval_metrics_for_label_var_name,
                        ai_obj=m_regr_ai_obj):
                    label_var_names.append(label_var_name)

            else:
                self.stdout_logger.warn(
                    msg='*** {}: {}: NO COMPONENT AI ***'
                        .format(m_regr_ai_obj.unique_id, label_var_name))

        return label_var_names

    def _good_m_regr_ai(self, m_regr_ai_obj=None, ref_eval_metrics=None):
        if isinstance(m_regr_ai_obj, str):
            m_regr_ai_obj = self.db.AIs.get(unique_id=m_regr_ai_obj)

        if not ref_eval_metrics:
            ref_eval_metrics = m_regr_ai_obj.ref_eval_metrics

        if ref_eval_metrics:
            return len(self._good_m_regr_label_var_names(
                        m_regr_ai_obj=m_regr_ai_obj,
                        ref_eval_metrics=ref_eval_metrics)) \
                >= (self.MIN_FRACTION_OF_GOOD_COMPONENT_AIS *
                    len(self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[m_regr_ai_obj.machine_family.machine_class.unique_name][m_regr_ai_obj.machine_family.unique_name]))

    def eval_m_regr_ai(
            self, unique_id,
            sql_filter=None,
            save=True, _force_re_eval=False,
            verbose=True):
        self.stdout_logger.info(msg='Evaluating Reference Metrics for "{}"...'.format(unique_id))

        m_regr_ai = \
            self._m_regr_ai(
                unique_id=unique_id,
                verbose=False)

        _m_regr_ai_obj = self.db.AIs.get(unique_id=m_regr_ai.params.uuid)

        machine_class_name = _m_regr_ai_obj.machine_family.machine_class.unique_name
        machine_family_name = _m_regr_ai_obj.machine_family.unique_name

        if save:
            machine_family_ai_evaluation_job, _ = \
                self.db.MachineFamilyAIEvaluationJobs.update_or_create(
                    ai=_m_regr_ai_obj,
                    defaults=dict(
                        started=make_aware(
                                    value=datetime.datetime.utcnow(),
                                    timezone=pytz.UTC,
                                    is_dst=None),
                        finished=None))

            ref_eval_metrics_exist = 'ref_eval_metrics' in m_regr_ai.params

            if _force_re_eval or (not ref_eval_metrics_exist):
                eval_arrow_spark_xdf = \
                    self._eval_arrow_spark_xdf(
                        machine_class_name=machine_class_name,
                        machine_family_name=machine_family_name,
                        to_month=str(_m_regr_ai_obj.ref_data_to_date)[:7],
                        set_i_col=isinstance(m_regr_ai, ts_m_regr.DLMRegrAI),
                        verbose=verbose)

                if sql_filter:
                    try:
                        eval_arrow_spark_xdf.filter(
                            condition=sql_filter,
                            inplace=True)

                    except Exception as err:
                        self.stdout_logger.warn(msg='*** {} ***'.format(err))

                m_regr_ai.eval(
                    df=eval_arrow_spark_xdf,
                    save=True)

            ref_eval_metrics = m_regr_ai.params.ref_eval_metrics.to_dict()

            # treat cases in which N = 1 leading to R2 = NaN
            for vital_machine_data_stream_name, global_and_indiv_ref_eval_metrics in ref_eval_metrics.items():
                machines_indiv_ref_eval_metrics = \
                    global_and_indiv_ref_eval_metrics[_MRegrAIABC._INDIV_EVAL_KEY]

                for machine_unique_id, machine_indiv_ref_eval_metrics in machines_indiv_ref_eval_metrics.items():
                    n = machine_indiv_ref_eval_metrics['n']
                    r2 = machine_indiv_ref_eval_metrics['R2']

                    if n == 1:
                        assert numpy.isnan(r2)
                        machine_indiv_ref_eval_metrics['R2'] = None

            _m_regr_ai_obj.ref_eval_metrics = ref_eval_metrics

            _m_regr_ai_obj.active = active = \
                bool(self._good_m_regr_ai(
                        m_regr_ai_obj=_m_regr_ai_obj,
                        ref_eval_metrics=ref_eval_metrics))

            _m_regr_ai_obj.save()

            machine_family_ai_evaluation_job.finished = \
                make_aware(
                    value=datetime.datetime.utcnow(),
                    timezone=pytz.UTC,
                    is_dst=None)

            machine_family_ai_evaluation_job.save()

            self.profile_m_regr_ais(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name)

        else:
            eval_arrow_spark_xdf = \
                self._eval_arrow_spark_xdf(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name,
                    to_month=str(_m_regr_ai_obj.ref_data_to_date)[:7],
                    set_i_col=isinstance(m_regr_ai, ts_m_regr.DLMRegrAI),
                    verbose=verbose)

            if sql_filter:
                try:
                    eval_arrow_spark_xdf.filter(
                        condition=sql_filter,
                        inplace=True)

                except Exception as err:
                    self.stdout_logger.warn(msg='*** {} ***'.format(err))

            m_regr_ai.eval(
                df=eval_arrow_spark_xdf,
                save=False)

            active = False

        self.stdout_logger.info(
            msg='{}{} ({})\n{}'.format(
                unique_id,
                '' if active else ' (*** INACTIVATED ***)',
                'SAVED' if save else '*** NOT SAVED ***',
                '\n'.join(
                    '{}: {}'.format(
                        label_var_name,
                        m_regr_ai.params.ref_eval_metrics[label_var_name][m_regr_ai._GLOBAL_EVAL_KEY])
                    for label_var_name, component_ai_params in m_regr_ai.params.model.component_ais.items()
                    if component_ai_params.model.ver)))

        return m_regr_ai

    def profile_m_regr_ais(self, machine_class_name, machine_family_name):
        machine_class_name = snake_case(machine_class_name)
        machine_family_name = snake_case(machine_family_name)

        _active_m_regr_ai_objs = \
            self.db.AIs.filter(
                machine_family__unique_name=machine_family_name,
                active=True)

        records = []
        label_var_names = set()
        col_names = set()

        for _active_m_regr_ai_obj in _active_m_regr_ai_objs:
            if _active_m_regr_ai_obj.created == \
                    max(_m_regr_ai_obj.created
                        for _m_regr_ai_obj in _active_m_regr_ai_objs.filter(
                            ref_data_to_date=_active_m_regr_ai_obj.ref_data_to_date)):
                d = dict(ref_data_to_date=_active_m_regr_ai_obj.ref_data_to_date)

                for label_var_name, ref_eval_metrics in tqdm(_active_m_regr_ai_obj.ref_eval_metrics.items()):
                    label_var_names.add(label_var_name)

                    global_ref_eval_metrics = ref_eval_metrics[_MRegrAIABC._GLOBAL_EVAL_KEY]

                    machine_family_data_stream_ai_ref_eval_metric_profile, _ = \
                        self.db.MachineFamilyVitalDataStreamAIEvalMetricProfiles.update_or_create(
                            machine_family=
                                self.machine_family(
                                    machine_family_name=machine_family_name),
                            machine_data_stream=
                                self.machine_data_stream(
                                    machine_class_name=machine_class_name,
                                    machine_data_stream_name=label_var_name),
                            ref_data_to_date=_active_m_regr_ai_obj.ref_data_to_date,
                            defaults=dict(
                                        N=global_ref_eval_metrics['n'],
                                        MAE=global_ref_eval_metrics['MAE'],
                                        MedAE=global_ref_eval_metrics['MedAE'],
                                        RMSE=global_ref_eval_metrics['RMSE'],
                                        R2=global_ref_eval_metrics['R2']))

                    _MAE_col_name = '{}___MAE'.format(label_var_name)
                    d[_MAE_col_name] = global_ref_eval_metrics['MAE']

                    _MedAE_col_name = '{}___MedAE'.format(label_var_name)
                    d[_MedAE_col_name] = global_ref_eval_metrics['MedAE']

                    _RMSE_col_name = '{}___RMSE'.format(label_var_name)
                    d[_RMSE_col_name] = global_ref_eval_metrics['RMSE']

                    _R2_col_name = '{}___R2'.format(label_var_name)
                    d[_R2_col_name] = global_ref_eval_metrics['R2']

            #        col_names.update((_R2_col_name, _MedAE_col_name, _MAE_col_name, _RMSE_col_name))

            #    records.append(d)
            # df = pandas.DataFrame.from_records(
            #             data=records,
            #             index=None,
            #             columns=['trained_to_date'] + sorted(col_names),
            #             exclude=None,
            #             coerce_float=False) \
            #             .sort_values(
            #             by='trained_to_date',
            #             axis='index',
            #             ascending=True,
            #             inplace=False,
            #             kind='quicksort',
            #             na_position='last')

            # r2_melt_df = \
            #     pandas.melt(
            #         frame=df[['trained_to_date'] +
            #                  ['{}___R2'.format(label_var_name)
            #                   for label_var_name in label_var_names]]
            #             .rename(
            #             columns={'{}___R2'.format(label_var_name):  label_var_name
            #                      for label_var_name in label_var_names},
            #             copy=False,
            #             inplace=False,
            #             level=None),
            #         id_vars=['trained_to_date'],
            #         value_vars=None,
            #         var_name='label',
            #         value_name='R2',
            #         col_level=None)

            # r2_plot = \
            #     ggplot(
            #         aes(x='trained_to_date',
            #             y='R2',
            #             color='label',
            #             group='label'),
            #         data=r2_melt_df) + \
            #     geom_line() + \
            #     scale_x_datetime(
            #         date_breaks='1 month',
            #         date_labels='%Y-%m') + \
            #     ylim(.68, 1) + \
            #     ggtitle('{}: {}: R2'.format(
            #         equipment_general_type_name,
            #         equipment_unique_type_group_name)) + \
            #     theme(axis_text_x=element_text(rotation=90))

            # err_plots = Namespace()

            # for label_var_name in label_var_names:
            #     errors_melt_df = \
            #         pandas.melt(
            #             frame=df[['trained_to_date',
            #                       '{}___MedAE'.format(label_var_name),
            #                       '{}___MAE'.format(label_var_name),
            #                       '{}___RMSE'.format(label_var_name)]]
            #                 .rename(
            #                 columns={'{}___MedAE'.format(label_var_name): 'MedAE',
            #                          '{}___MAE'.format(label_var_name): 'MAE',
            #                          '{}___RMSE'.format(label_var_name): 'RMSE'},
            #                 copy=False,
            #                 inplace=False,
            #                 level=None),
            #             id_vars=['trained_to_date'],
            #             value_vars=None,
            #             var_name='metric',
            #             value_name='err',
            #             col_level=None)

            #     err_plots[label_var_name] = \
            #         ggplot(
            #             aes(x='trained_to_date',
            #                 y='err',
            #                 color='metric',
            #                 group='metric'),
            #             data=errors_melt_df) + \
            #         geom_line() + \
            #         scale_x_datetime(
            #             date_breaks='1 month',
            #             date_labels='%Y-%m') + \
            #         ylim(0, None) + \
            #         ggtitle('{}: {}:\n{}: Error Metrics'.format(
            #             equipment_general_type_name,
            #             equipment_unique_type_group_name,
            #             label_var_name)) + \
            #         theme(axis_text_x=element_text(rotation=90))

            # return Namespace(
            #     r2_plot=r2_plot,
            #     err_plots=err_plots)

    def _reactivate_m_regr_ais(self):
        for m_regr_ai_obj in tqdm(self.db.AIs.all()):
            good = self._good_m_regr_ai(m_regr_ai_obj=m_regr_ai_obj)

            if good is None:
                assert not (m_regr_ai_obj.ref_eval_metrics or m_regr_ai_obj.active), \
                    '*** {} ***'.format(m_regr_ai_obj.unique_id)

            elif m_regr_ai_obj.active != good:
                self.stdout_logger.info(
                    msg='{}ACTIVATING {}... '
                        .format(
                        '' if good else '*** IN',
                        m_regr_ai_obj.unique_id))

                m_regr_ai_obj.active = good
                m_regr_ai_obj.save()
    
    def risk_score(
            self,
            machine_class_name, machine_family_name,   # TODO: / ,
            date, *, to_date=None, monthly=False, _max_n_dates_at_one_time=9,
            _force_calc=False, re_calc_daily=False,
            __batch_size__=10 ** 3,
            sql_filter=None) -> None:
        machine_family_data_set_name = \
            self.machine_family_conventional_full_name(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name)

        active_m_regr_ais = \
            self.db.AIs.filter(
                machine_family__machine_class__unique_name=machine_class_name,
                machine_family__unique_name=machine_family_name,
                active=True)

        _ref_data_to_dates = \
            sorted(active_ai.ref_data_to_date
                   for active_ai in active_m_regr_ais)

        if _force_calc:
            re_calc_daily = True

        calc_daily_for_dates = set()

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
                    msg='Risk Scoring {} for {}...'
                        .format(machine_family_data_set_name, _mth_str))

                for i, _ref_data_to_date in enumerate(_ref_data_to_dates):
                    if str(_ref_data_to_date) > _mth_str:
                        if i:
                            _ref_data_to_date = _ref_data_to_dates[i - 1]

                        break

                active_m_regr_ais_ref_data_to_date = \
                    active_m_regr_ais.filter(
                        ref_data_to_date=_ref_data_to_date)

                active_m_regr_ai_ref_data_to_date = \
                    active_m_regr_ais_ref_data_to_date.get(
                        created=max(bp.created
                                    for bp in active_m_regr_ais_ref_data_to_date))

                m_regr_ai_unique_id = active_m_regr_ai_ref_data_to_date.unique_id

                if 'Contents' in \
                       self.s3_client.list_objects_v2(
                           Bucket=self.params.s3.bucket,
                           Prefix=os.path.join(
                                   self.params.s3.err_mults_dir_prefix,
                                   'monthly',
                                   machine_family_data_set_name + _PARQUET_EXT,
                                   '{}={}'.format(MONTH_COL, _mth_str),
                                   '{}={}'.format(self._M_REGR_AI_UNIQUE_ID_COL, m_regr_ai_unique_id))):
                    # TODO: test load to make sure

                    if re_calc_daily:
                        calc_daily_for_dates.update(
                            (_mth_str + '-{:02d}'.format(d))
                            for d in range(1, 32))

                        if _force_calc:
                            _to_calc = True

                            machine_family_arrow_spark_xdf_for_month = \
                                self.load_machine_family_data(
                                    machine_class_name=machine_class_name,
                                    machine_family_name=machine_family_name,
                                    _from_files=True, _spark=True,
                                    set_i_col=False, set_t_col=True) \
                                .filterPartitions(
                                    (DATE_COL,
                                     _mth_str + '-01',
                                     _mth_str + '-31'))

                        else:
                            _to_calc = False

                    else:
                        _to_calc = False
                        
                else:
                    machine_family_arrow_spark_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=True,
                            set_i_col=False, set_t_col=True)

                    try:
                        machine_family_arrow_spark_xdf_for_month = \
                            machine_family_arrow_spark_xdf \
                            .filterPartitions(
                                (DATE_COL,
                                 _mth_str + '-01',
                                 _mth_str + '-31'))

                        _to_calc = True

                    except Exception as err:
                        self.stdout_logger.warn(
                            msg='*** CANNOT LOAD DATA FOR "{}" IN {}: {} ***'
                                .format(machine_family_data_set_name, _mth_str, err))

                        _to_calc = False

                if _to_calc:
                    m_regr_ai = \
                        self._m_regr_ai(
                            unique_id=m_regr_ai_unique_id,
                            verbose=False)

                    if isinstance(m_regr_ai, ts_m_regr.DLMRegrAI):
                        machine_family_arrow_spark_xdf_for_month.iCol = self._MACHINE_UNIQUE_ID_COL_NAME

                    if sql_filter:
                        try:
                            machine_family_arrow_spark_xdf_for_month.filter(
                                condition=sql_filter,
                                inplace=True)

                        except Exception as err:
                            self.stdout_logger.warn(
                                msg='*** {} ***'.format(err))

                    m_regr_ai.err_mults(
                        m_regr_ai.score(
                            df=machine_family_arrow_spark_xdf_for_month,
                            __batch_size__=__batch_size__),
                        *self._good_m_regr_label_var_names(m_regr_ai_obj=active_m_regr_ai_ref_data_to_date),
                        max_indiv_over_global_ref_eval_metric_ratio=self.MAX_INDIV_OVER_GLOBAL_REF_EVAL_METRIC_RATIO
                        ).withColumn(
                            colName=self._M_REGR_AI_UNIQUE_ID_COL,
                            col=functions.lit(m_regr_ai_unique_id)
                        ).save(
                            path=os.path.join(
                                's3://{}/{}/monthly'.format(
                                    self.params.s3.bucket,
                                    self.params.s3.err_mults_dir_prefix),
                                machine_family_data_set_name + _PARQUET_EXT,
                                '{}={}'.format(MONTH_COL, _mth_str)),
                            format='parquet',
                            partitionBy=(self._M_REGR_AI_UNIQUE_ID_COL, DATE_COL),
                            aws_access_key_id=self.params.s3.access_key_id,
                            aws_secret_access_key=self.params.s3.secret_access_key,
                            verbose=True)

                    calc_daily_for_dates.update(
                        (_mth_str + '-{:02d}'.format(d))
                        for d in range(1, 32))

                _mth_str = month_str(_mth_str, n_months_offset=1)

        else:
            if to_date:
                assert (len(to_date) == 10) and (to_date > date)

            else:
                to_date = date

            m_regr_ais_to_calc_for_dates = {}

            for _date in tqdm(pandas.date_range(start=date, end=to_date).date):
                for i, _ref_data_to_date in enumerate(_ref_data_to_dates):
                    if _ref_data_to_date >= _date:
                        if i:
                            _ref_data_to_date = _ref_data_to_dates[i - 1]

                        break

                active_m_regr_ais_ref_data_to_date = \
                    active_m_regr_ais.filter(
                        ref_data_to_date=_ref_data_to_date)

                active_m_regr_ai_ref_data_to_date = \
                    active_m_regr_ais_ref_data_to_date.get(
                        created=max(bp.created
                                    for bp in active_m_regr_ais_ref_data_to_date))

                m_regr_ai_unique_id = active_m_regr_ai_ref_data_to_date.unique_id

                if 'Contents' in \
                       self.s3_client.list_objects_v2(
                           Bucket=self.params.s3.bucket,
                           Prefix=os.path.join(
                                   self.params.s3.err_mults_dir_prefix,
                                   'daily',
                                   machine_family_data_set_name + _PARQUET_EXT,
                                   '{}={}'.format(DATE_COL, _date),
                                   '{}={}'.format(self._M_REGR_AI_UNIQUE_ID_COL, m_regr_ai_unique_id))):
                    # TODO: test load to make sure

                    if re_calc_daily:
                        calc_daily_for_dates.add(_date)

                        if _force_calc:
                            if active_m_regr_ai_ref_data_to_date in m_regr_ais_to_calc_for_dates:
                                m_regr_ais_to_calc_for_dates[active_m_regr_ai_ref_data_to_date].append(_date)
                            else:
                                m_regr_ais_to_calc_for_dates[active_m_regr_ai_ref_data_to_date] = [_date]

                else:
                    machine_family_arrow_spark_xdf = \
                        self.load_machine_family_data(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name,
                            _from_files=True, _spark=True,
                            set_i_col=False, set_t_col=True)

                    try:
                        machine_family_arrow_spark_xdf_for_date = \
                            machine_family_arrow_spark_xdf \
                            .filterPartitions(
                                (DATE_COL,
                                 _date))

                        if active_m_regr_ai_ref_data_to_date in m_regr_ais_to_calc_for_dates:
                            m_regr_ais_to_calc_for_dates[active_m_regr_ai_ref_data_to_date].append(_date)
                        else:
                            m_regr_ais_to_calc_for_dates[active_m_regr_ai_ref_data_to_date] = [_date]

                    except Exception as err:
                        self.stdout_logger.warn(
                            msg='*** CANNOT LOAD DATA FOR "{}" ON {}: {} ***'
                                .format(machine_family_data_set_name, _date, err))

            if m_regr_ais_to_calc_for_dates:
                self.stdout_logger.info(
                    msg='Risk Scoring {}: {}...'
                      .format(machine_family_data_set_name, m_regr_ais_to_calc_for_dates))

                err_mults_s3_dir_path = \
                    os.path.join(
                        's3://{}/{}/daily'.format(
                            self.params.s3.bucket,
                            self.params.s3.err_mults_dir_prefix),
                        machine_family_data_set_name + _PARQUET_EXT)

                for m_regr_ai_obj, dates in m_regr_ais_to_calc_for_dates.items():
                    m_regr_ai_unique_id = m_regr_ai_obj.unique_id

                    m_regr_ai = self._m_regr_ai(unique_id=m_regr_ai_unique_id)

                    for i in tqdm(range(0, len(dates), _max_n_dates_at_one_time)):
                        _dates = dates[i:(i + _max_n_dates_at_one_time)]

                        machine_family_arrow_spark_xdf_for_dates = \
                            self.load_machine_family_data(
                                machine_class_name=machine_class_name,
                                machine_family_name=machine_family_name,
                                _from_files=True, _spark=True,
                                set_i_col=False, set_t_col=True) \
                            .filterPartitions(
                                (DATE_COL,
                                 _dates))

                        if isinstance(m_regr_ai, ts_m_regr.DLMRegrAI):
                            machine_family_arrow_spark_xdf_for_dates.iCol = self._MACHINE_UNIQUE_ID_COL_NAME

                        if sql_filter:
                            try:
                                machine_family_arrow_spark_xdf_for_dates.filter(
                                    condition=sql_filter,
                                    inplace=True)

                            except Exception as err:
                                self.stdout_logger.warn(
                                    msg='*** {} ***'.format(err))

                        _tmp_dir_path = tempfile.mkdtemp()

                        m_regr_ai.err_mults(
                            m_regr_ai.score(
                                df=machine_family_arrow_spark_xdf_for_dates,
                                __batch_size__=__batch_size__),
                            *self._good_m_regr_label_var_names(m_regr_ai_obj=m_regr_ai_obj),
                            max_indiv_over_global_ref_eval_metric_ratio=self.MAX_INDIV_OVER_GLOBAL_REF_EVAL_METRIC_RATIO
                            ).withColumn(
                                colName=self._M_REGR_AI_UNIQUE_ID_COL,
                                col=functions.lit(m_regr_ai_unique_id)
                            ).save(
                                path=_tmp_dir_path,
                                format='parquet',
                                partitionBy=(DATE_COL, self._M_REGR_AI_UNIQUE_ID_COL),
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
                                to_dir_path=os.path.join(err_mults_s3_dir_path, partition_key),
                                delete=True, quiet=True,
                                access_key_id=self.params.s3.access_key_id,
                                secret_access_key=self.params.s3.secret_access_key,
                                verbose=False)

                        fs.rm(path=_tmp_dir_path,
                              is_dir=True,
                              hdfs=False)

                        calc_daily_for_dates.update(_dates)

        if calc_daily_for_dates:
            copy_risk_scores_from_date = min(calc_daily_for_dates)

            self.stdout_logger.info(
                msg='Aggregating Daily Error Multiples for {} on ~{:,} Dates from {} to {} ***'
                    .format(machine_family_data_set_name,
                            len(calc_daily_for_dates), min(calc_daily_for_dates), max(calc_daily_for_dates)))

            err_mults_arrow_xdf = \
                ArrowSparkXDF(
                    path=os.path.join(
                        's3://{}/{}/{}'.format(
                            self.params.s3.bucket,
                            self.params.s3.err_mults_dir_prefix,
                            'monthly' if monthly else 'daily'),
                        machine_family_data_set_name + _PARQUET_EXT),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    reCache=True,
                    verbose=True) \
                .filterPartitions(
                    (DATE_COL,
                     calc_daily_for_dates))

            label_var_names = []
            n_label_var_names = 0

            for label_var_name in \
                    self.params.health_monitoring.machine_families_vital_and_incl_excl_input_data_streams[machine_class_name][machine_family_name]:
                if 'MAE__{}'.format(label_var_name) in err_mults_arrow_xdf.columns:
                    label_var_names.append(label_var_name)
                    n_label_var_names += 1

            _day_err_mults_arrow_xdf = \
                _MRegrAIABC.day_err_mults(
                    err_mults_arrow_xdf,
                    *label_var_names,
                    id_col=self._MACHINE_UNIQUE_ID_COL_NAME,
                    time_col=self._LOCAL_DATE_TIME_COL_NAME)

            s3_dir_path = \
                os.path.join(
                    's3://{}/{}'.format(
                        self.params.s3.bucket,
                        self.params.s3.day_err_mults_dir_prefix),
                    machine_family_data_set_name + _PARQUET_EXT)

            _tmp_dir_path = tempfile.mkdtemp()

            if len(calc_daily_for_dates) > 1:
                _day_err_mults_arrow_xdf \
                .repartition(DATE_COL) \
                .save(
                    path=_tmp_dir_path,
                    format='parquet',
                    partitionBy=DATE_COL,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    verbose=True)

                # free up Spark resources for other tasks
                arimo.util.data_backend.spark.stop()

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
                        from_dir_path=
                            os.path.join(
                                _tmp_dir_path,
                                partition_key),
                        to_dir_path=
                            os.path.join(
                                s3_dir_path,
                                partition_key),
                        delete=True, quiet=True,
                        access_key_id=self.params.s3.access_key_id,
                        secret_access_key=self.params.s3.secret_access_key,
                        verbose=False)

            else:
                _day_err_mults_arrow_xdf \
                .repartition(1) \
                .save(
                    path=os.path.join(
                            s3_dir_path,
                            '{}={}'.format(
                                DATE_COL,
                                calc_daily_for_dates.pop())),
                    format='parquet',
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    verbose=True)

                # free up Spark resources for other tasks
                arimo.util.data_backend.spark.stop()

            day_mean_abs_mae_mult_prefix = \
                _MRegrAIABC._dayMean_PREFIX + \
                _MRegrAIABC._ABS_PREFIX + \
                _MRegrAIABC._ERR_MULT_PREFIXES['MAE']

            day_mean_abs_mae_mult_col_names = \
                [(day_mean_abs_mae_mult_prefix +
                  label_var_name)
                 for label_var_name in label_var_names]

            err_mults_df = \
                ArrowXDF(
                    path=s3_dir_path,
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    verbose=True) \
                .collect(
                    self._MACHINE_UNIQUE_ID_COL_NAME,
                    DATE_COL,
                    *day_mean_abs_mae_mult_col_names)

            overall_m_regr_risk_score_col_name = \
                self._OVERALL_M_REGR_RISK_SCORE_NAME_PREFIX + \
                _MRegrAIABC._dayMean_PREFIX + \
                _MRegrAIABC._ABS_PREFIX + \
                _MRegrAIABC._ERR_MULT_NAMES['MAE']

            err_mults_df[overall_m_regr_risk_score_col_name] = \
                err_mults_df[day_mean_abs_mae_mult_col_names].max(
                    axis='columns',
                    skipna=True,
                    level=None,
                    numeric_only=True) \
                if n_label_var_names > 1 \
                else err_mults_df[day_mean_abs_mae_mult_col_names[0]]

            risk_scores_df = \
                _MRegrAIABC.ema_day_err_mults(
                    err_mults_df,
                    overall_m_regr_risk_score_col_name,
                    *day_mean_abs_mae_mult_col_names,
                    id_col=self._MACHINE_UNIQUE_ID_COL_NAME)

            _tmp_m_regr_ai_based_risk_scores_parquet_file_path = \
                os.path.join(
                    _tmp_dir_path,
                    self.params.s3.risk_scores.file_name)

            risk_scores_df.columns = \
                risk_scores_df.columns.map(str)   # Arrow Parquet columns cannot be Unicode

            n_rows = len(risk_scores_df)

            message = \
                'Writing {:,} Rows of Risk Scores to Parquet Files with Columns {}...'.format(
                    n_rows, risk_scores_df.columns.tolist())

            self.stdout_logger.info(msg=message)
            tic = time.time()

            risk_scores_df.to_parquet(
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_parquet.html
                path=_tmp_m_regr_ai_based_risk_scores_parquet_file_path,
                    # File path or Root Directory path.
                    # Will be used as Root Directory path while writing a partitioned dataset.

                engine='pyarrow',
                    # {'auto', 'pyarrow', 'fastparquet'}, default ‘auto’
                    # Parquet library to use.
                    # If 'auto', then the option io.parquet.engine is used.
                    # The default io.parquet.engine behavior is to try 'pyarrow',
                    # falling back to 'fastparquet' if 'pyarrow' is unavailable.

                compression='snappy',
                    # {'snappy', 'gzip', 'brotli', None}, default 'snappy'
                    # Name of the compression to use. Use None for no compression.

                index=False,
                    # If True, include the dataframe's index(es) in the file output.
                    # If False, they will not be written to the file.
                    # If None, the behavior depends on the chosen engine.

                partition_cols=None,
                    # Column names by which to partition the dataset Columns are partitioned in the order they are given

                # https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table.from_pandas
                # schema=None,   # __cinit__() got an unexpected keyword argument 'schema'
                    # The expected schema of the Arrow Table.
                    # This can be used to indicate the type of columns if we cannot infer it automatically.

                # preserve_index=False,   # __cinit__() got an unexpected keyword argument 'preserve_index'
                    # Whether to store the index as an additional column in the resulting Table.

                # nthreads=psutil.cpu_count(logical=True),   # __cinit__() got an unexpected keyword argument 'nthreads'
                    # default None (may use up to system CPU count threads))
                    # If greater than 1, convert columns to Arrow in parallel using indicated number of threads

                # columns=None,   # __cinit__() got an unexpected keyword argument 'columns'
                    # List of column to be converted.
                    # If None, use all columns.

                # safe=True,   # __cinit__() got an unexpected keyword argument 'safe'
                    # Check for overflows or other unsafe conversions

                # https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html#pyarrow.parquet.write_table
                row_group_size=None,

                version='2.0',
                    # The Parquet format version, defaults to 1.0

                use_dictionary=True,
                    # Specify if we should use dictionary encoding in general or only for some columns

                # compression='snappy',
                    # Specify the compression codec, either on a general basis or per-column.
                    # Valid values: {'NONE', 'SNAPPY', 'GZIP', 'LZO', 'BROTLI', 'LZ4', 'ZSTD'}

                use_deprecated_int96_timestamps=False,
                    # Write timestamps to INT96 Parquet format.
                    # Defaults to False unless enabled by flavor argument.
                    # This take priority over the coerce_timestamps option.

                coerce_timestamps=None,
                    # Cast timestamps a particular resolution.
                    # Valid values: {None, 'ms', 'us'}

                allow_truncated_timestamps=False,
                    # Allow loss of data when coercing timestamps to a particular resolution.
                    # E.g. if microsecond or nanosecond data is lost when coercing to 'ms', do not raise an exception

                flavor='spark',   # https://arrow.apache.org/docs/python/parquet.html#using-with-spark
                    # Sanitize schema or set other compatibility options for compatibility

                filesystem=None
                    # If nothing passed, will be inferred from where if path-like,
                    # else where is already a file-like object so no filesystem is needed.
            )

            toc = time.time()
            self.stdout_logger.info(msg=message + ' done!   <{:,.1f} m>'.format((toc - tic) / 60))

            message = 'Uploading Risk Scores Parquet File...'
            self.stdout_logger.info(msg=message)
            tic = time.time()

            self.s3_client.upload_file(
                Filename=_tmp_m_regr_ai_based_risk_scores_parquet_file_path,
                Bucket=self.params.s3.bucket,
                Key=os.path.join(
                        self.params.s3.risk_scores.dir_prefix,
                        machine_family_data_set_name,
                        self.params.s3.risk_scores.file_name))

            toc = time.time()
            self.stdout_logger.info(msg=message + ' done!   <{:,.1f} m>'.format((toc - tic) / 60))

            fs.rm(path=_tmp_dir_path,
                  is_dir=True,
                  hdfs=False)

            self.risk_scores_to_db(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name,
                from_date=copy_risk_scores_from_date,
                _risk_scores_pandas_df=risk_scores_df)

            machine_family = \
                self.machine_family(
                    machine_family_name=machine_family_name)

            date_time = \
                make_aware(
                    value=datetime.datetime.utcnow(),
                    timezone=pytz.UTC,
                    is_dst=None)

            for date in tqdm(risk_scores_df[DATE_COL].unique()):
                self.db.MachineFamilyRiskScoringJobs.update_or_create(
                    machine_family=machine_family,
                    date=date,
                    defaults=dict(
                                started=date_time,
                                finished=date_time))

    def risk_scores_to_db(
            self,
            machine_class_name, machine_family_name,
            from_date, monthly=False,
            _risk_scores_pandas_df=None):
        if monthly:
            assert len(from_date) == 7
            from_date = datetime.datetime.strptime(from_date + '-01', '%Y-%m-%d').date()

        elif isinstance(from_date, str):
            assert len(from_date) == 10
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()

        machine_class = \
            self.machine_class(
                machine_class_name=machine_class_name)

        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        self.stdout_logger.info(
            msg='*** DELETED EXISTING Machine Health Risk Scores TO RE-INSERT: {} ***'
                .format(
                    self.db.MachineHealthRiskScores.filter(
                        machine_family_data__machine_family=machine_family,
                        machine_family_data__date__gte=from_date)
                    .delete()))

        machine_family_data_set_name = \
            self.machine_family_conventional_full_name(
                machine_class_name=machine_class_name,
                machine_family_name=machine_family_name)

        if _risk_scores_pandas_df is None:
            risk_scores_df = \
                ArrowXDF(
                    path=os.path.join(
                            's3://{}'.format(self.params.s3.bucket),
                            self.params.s3.risk_scores.dir_prefix,
                            machine_family_data_set_name,
                            self.params.s3.risk_scores.file_name),
                    aws_access_key_id=self.params.s3.access_key_id,
                    aws_secret_access_key=self.params.s3.secret_access_key,
                    reCache=True,
                    verbose=True) \
                .collect()

        else:
            risk_scores_df = _risk_scores_pandas_df

        risk_scores_df = risk_scores_df.loc[risk_scores_df[DATE_COL] >= from_date]

        risk_scores_df.loc[:, self._MACHINE_UNIQUE_ID_COL_NAME] = \
            risk_scores_df[self._MACHINE_UNIQUE_ID_COL_NAME].map(
                lambda machine_unique_id: snake_case(str(machine_unique_id)))

        _n_risk_scores_rows_before_dedup = len(risk_scores_df)

        risk_scores_df.drop_duplicates(
            subset=(self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL),
            keep='first',
            inplace=True)

        _n_risk_scores_rows_after_dedup = len(risk_scores_df)

        _n_dup_risk_scores_rows_dropped = _n_risk_scores_rows_before_dedup - _n_risk_scores_rows_after_dedup
        if _n_dup_risk_scores_rows_dropped:
            self.stdout_logger.warning(
                msg='*** DROPPED {:,} DUPLICATE ROW(S) OF {} ***'
                    .format(_n_dup_risk_scores_rows_dropped, risk_scores_df.columns))

        machine_family_data = {}

        for date in tqdm(risk_scores_df[DATE_COL].unique()):
            machine_family_data_for_date = \
                self.db.MachineFamilyData \
                .filter(
                    machine_family=machine_family,
                    date=date) \
                .first()

            if machine_family_data_for_date:
                machine_family_data[date] = machine_family_data_for_date

            else:
                self.register_machine_family_data(
                    machine_class_name=machine_class_name,
                    machine_family_name=machine_family_name,
                    date=date, to_date=None)

                machine_family_data[date] = \
                    self.db.MachineFamilyData.get(
                        machine_family=machine_family,
                        date=date)

        machines = \
            {machine_unique_id:
                self.update_or_create_machine(
                    machine_class_name=machine_class_name,
                    machine_unique_id=machine_unique_id)
             for machine_unique_id in tqdm(risk_scores_df[self._MACHINE_UNIQUE_ID_COL_NAME].unique())}

        from infx.machine_intel.health.models import MachineHealthRiskScore

        message = 'Writing {:,} Rows of {} Risk Scores for {} to DB...'.format(
                    _n_risk_scores_rows_after_dedup, risk_scores_df.columns, machine_family_data_set_name)
        self.stdout_logger.info(msg=message)
        tic = time.time()

        for i in tqdm(range(0, _n_risk_scores_rows_after_dedup, self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)):
            _risk_scores_df = \
                risk_scores_df.iloc[i:(i + self._MAX_N_ROWS_TO_COPY_TO_DB_AT_ONE_TIME)]

            self.db.MachineHealthRiskScores.bulk_create(
                [MachineHealthRiskScore(
                    machine_family_data=machine_family_data[row[DATE_COL]],
                    machine=machines[row[self._MACHINE_UNIQUE_ID_COL_NAME]],
                    machine_health_risk_score_method=
                        self.db.MachineHealthRiskScoreMethods.get_or_create(
                            machine_class=machine_class,
                            name=risk_score_name)[0],
                    machine_health_risk_score_value=row[risk_score_name])
                 for _, row in tqdm(_risk_scores_df.iterrows(), total=len(_risk_scores_df))
                    for risk_score_name in set(row.index).difference((self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL))
                        if pandas.notnull(row[risk_score_name])],
                batch_size=self._DB_BULK_CREATE_OR_UPDATE_BATCH_SIZE,
                ignore_conflicts=False)

        toc = time.time()
        self.stdout_logger.info(msg=message + ' done!   <{:,.1f} m>'.format((toc - tic) / 60))

        date_time = \
            make_aware(
                value=datetime.datetime.utcnow(),
                timezone=pytz.UTC,
                is_dst=None)

        for date in tqdm(risk_scores_df[DATE_COL].unique()):
            self.db.MachineFamilyRiskScoresToDBJobs.update_or_create(
                machine_family=machine_family,
                date=date,
                defaults=dict(
                            started=date_time,
                            finished=date_time))

    def risk_alert(
            self,
            machine_class_name, machine_family_name,
            from_date=None, to_date=None,
            _redo=False):
        machine_class = \
            self.machine_class(
                machine_class_name=machine_class_name)

        machine_family = \
            self.machine_family(
                machine_family_name=machine_family_name)

        if from_date:
            from_date = \
                datetime.datetime.strptime(
                    (from_date + '-01')
                        if len(from_date) == 7
                        else from_date,
                    '%Y-%m-%d') \
                .date()

        if to_date:
            to_date = \
                month_end(to_date) \
                if len(to_date) == 7 \
                else datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

        def update_or_create_risk_alert(
                machine_id,
                risk_score_name, threshold,
                start_date, end_date, cum_excess_risk_score, last_risk_score,
                m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores,
                ongoing=False):
            m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores = \
                sorted(
                    m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores.items(),
                    key=lambda i: -i[1])

            alerts = \
                self.db.MachineHealthRiskAlerts.filter(
                    machine_family=machine_family,
                    machine__unique_id=machine_id,

                    machine_health_risk_score_method=
                        self.db.MachineHealthRiskScoreMethods.get_or_create(
                            machine_class=machine_class,
                            name=risk_score_name)[0],
                    machine_health_risk_score_value_alert_threshold=threshold,

                    date_range__overlap=
                        DateRange(
                            lower=start_date,
                            upper=end_date,
                            bounds='[]',
                            empty=False))
    
            n_alerts = alerts.count()
    
            if n_alerts:
                assert n_alerts == 1, \
                    (f"*** {start_date} to {end_date} CONFLICTS: {n_alerts} ALERTS: ***"
                     + '\n'
                     + '\n'.join(str(alert) for alert in alerts))

                alert = alerts.first()

                if (not from_date) or (alert.from_date >= from_date):
                    alert.from_date = start_date

                if (not to_date) or (alert.to_date <= to_date):
                    alert.to_date = end_date

                alert.ongoing = ongoing

                alert.cum_excess_machine_health_risk_score_value = cum_excess_risk_score
                alert.last_machine_health_risk_score_value = last_risk_score

                if m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores:
                    alert.info = \
                        dict(m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores=
                                m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores)

                else:
                    alert.info = None
    
                alert.save()
    
            else:
                self.db.MachineHealthRiskAlerts.create(
                    machine_family=machine_family,

                    machine=self.update_or_create_machine(
                                machine_class_name=machine_family.machine_class.unique_name,
                                machine_unique_id=machine_id),

                    machine_health_risk_score_method=
                        self.db.MachineHealthRiskScoreMethods.get_or_create(
                            machine_class=machine_class,
                            name=risk_score_name)[0],
                    machine_health_risk_score_value_alert_threshold=threshold,

                    from_date=start_date,
                    to_date=end_date,
                    ongoing=ongoing,

                    cum_excess_machine_health_risk_score_value=cum_excess_risk_score,
                    last_machine_health_risk_score_value=last_risk_score,

                    info=dict(m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores=
                                m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores)
                        if m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores
                        else None)

        if _redo:
            self.stdout_logger.info(
                msg='*** DELETING EXISTING ANOM ALERTS FOR {}: {} ***'
                    .format(
                        self.machine_family_conventional_full_name(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name),
                        self.db.MachineHealthRiskAlerts.filter(
                            machine_family=machine_family).delete()))

        m_regr_ai_risk_scores_arrow_xdf = \
            ArrowXDF(
                path=os.path.join(
                        's3://{}/{}'.format(
                            self.params.s3.bucket,
                            self.params.s3.risk_scores.dir_prefix),
                        self.machine_family_conventional_full_name(
                            machine_class_name=machine_class_name,
                            machine_family_name=machine_family_name),
                        self.params.s3.risk_scores.file_name),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=True)

        m_regr_ai_risk_scores_df = m_regr_ai_risk_scores_arrow_xdf.collect()

        if from_date or to_date:
            m_regr_ai_risk_scores_df = \
                m_regr_ai_risk_scores_df.loc[
                    ((m_regr_ai_risk_scores_df[DATE_COL] >= from_date) if from_date else True) &
                    ((m_regr_ai_risk_scores_df[DATE_COL] <= to_date) if to_date else True)]

        m_regr_ai_risk_scores_df = \
            m_regr_ai_risk_scores_df.sort_values(
                by=[self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL],
                axis='index',
                ascending=True,
                inplace=False,
                kind='quicksort',
                na_position='last') \
            .reset_index(
                level=None,
                drop=True,
                inplace=False,
                col_level=0,
                col_fill='')

        m_regr_ai_risk_scores_df.loc[:, self._MACHINE_UNIQUE_ID_COL_NAME] = \
            m_regr_ai_risk_scores_df[self._MACHINE_UNIQUE_ID_COL_NAME].map(
                lambda machine_unique_id: snake_case(str(machine_unique_id)))

        _n_risk_scores_rows_before_dedup = len(m_regr_ai_risk_scores_df)

        m_regr_ai_risk_scores_df.drop_duplicates(
            subset=(self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL),
            keep='first',
            inplace=True)

        _n_risk_scores_rows_after_dedup = len(m_regr_ai_risk_scores_df)

        _n_dup_risk_scores_rows_dropped = _n_risk_scores_rows_before_dedup - _n_risk_scores_rows_after_dedup
        if _n_dup_risk_scores_rows_dropped:
            self.stdout_logger.warning(
                msg='*** DROPPED {:,} DUPLICATE ROW(S) OF {} ***'
                    .format(_n_dup_risk_scores_rows_dropped, m_regr_ai_risk_scores_df.columns))

        _n_risk_scores_rows_after_dedup = len(m_regr_ai_risk_scores_df)

        risk_score_names_and_thresholds = {}

        for risk_score_name, thresholds in self.params.health_monitoring.risk_score_names_and_thresholds.items():
            if thresholds:
                risk_score_names_and_thresholds[self._DEFAULT_EMA_ALPHA_PREFIX + risk_score_name] = \
                    risk_score_names_and_thresholds[risk_score_name] = thresholds

        current_machine_id = None

        m_regr_ai_machine_data_stream_risk_score_name_prefixes_and_prefix_lengths = {}

        for i, row in tqdm(m_regr_ai_risk_scores_df.iterrows(), total=_n_risk_scores_rows_after_dedup):
            machine_id = row[self._MACHINE_UNIQUE_ID_COL_NAME]
            date = row[DATE_COL]

            if machine_id != current_machine_id:
                if i:
                    for risk_score_name in unfinished_anomalies:
                        for threshold, unfinished_anomaly in unfinished_anomalies[risk_score_name].items():
                            if unfinished_anomaly.start_date and unfinished_anomaly.end_date and unfinished_anomaly.cum_excess_risk_score:
                                update_or_create_risk_alert(
                                    machine_id=current_machine_id,

                                    risk_score_name=risk_score_name,
                                    threshold=threshold,

                                    start_date=unfinished_anomaly.start_date,
                                    end_date=unfinished_anomaly.end_date,
                                    ongoing=True,

                                    cum_excess_risk_score=unfinished_anomaly.cum_excess_risk_score,
                                    last_risk_score=unfinished_anomaly.last_risk_score,

                                    m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores=
                                        unfinished_anomaly.m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores)

                unfinished_anomalies = \
                    {risk_score_name:
                        {threshold:
                            Namespace(
                                start_date=None,
                                end_date=None,
                                cum_excess_risk_score=0,
                                last_risk_score=0,
                                m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores={})
                         for threshold in thresholds}
                     for risk_score_name, thresholds in risk_score_names_and_thresholds.items()}

                current_machine_id = machine_id

            for risk_score_name, thresholds in risk_score_names_and_thresholds.items():
                if risk_score_name in m_regr_ai_machine_data_stream_risk_score_name_prefixes_and_prefix_lengths:
                    m_regr_ai_vital_machine_data_stream_risk_score_name_prefix, \
                    m_regr_ai_vital_machine_data_stream_risk_score_name_prefix_len = \
                        m_regr_ai_machine_data_stream_risk_score_name_prefixes_and_prefix_lengths[risk_score_name]

                else:
                    m_regr_ai_vital_machine_data_stream_risk_score_name_prefix = \
                        (self._DEFAULT_EMA_ALPHA_PREFIX +
                         risk_score_name[(len(self._DEFAULT_EMA_ALPHA_PREFIX) + len(self._OVERALL_M_REGR_RISK_SCORE_NAME_PREFIX)):] + '__') \
                        if risk_score_name.startswith(self._DEFAULT_EMA_ALPHA_PREFIX) \
                        else (risk_score_name[len(self._OVERALL_M_REGR_RISK_SCORE_NAME_PREFIX):] + '__')

                    m_regr_ai_vital_machine_data_stream_risk_score_name_prefix_len = \
                        len(m_regr_ai_vital_machine_data_stream_risk_score_name_prefix)

                    m_regr_ai_machine_data_stream_risk_score_name_prefixes_and_prefix_lengths[risk_score_name] = \
                        m_regr_ai_vital_machine_data_stream_risk_score_name_prefix, \
                        m_regr_ai_vital_machine_data_stream_risk_score_name_prefix_len

                risk_score = row[risk_score_name]

                for threshold in thresholds:
                    unfinished_anomaly = unfinished_anomalies[risk_score_name][threshold]

                    if risk_score > threshold:
                        if unfinished_anomaly.start_date is None:
                            unfinished_anomaly.start_date = date

                        unfinished_anomaly.end_date = date

                        unfinished_anomaly.cum_excess_risk_score += (risk_score - threshold)

                        unfinished_anomaly.last_risk_score = risk_score

                        for k, v in row.items():
                            if k.startswith(m_regr_ai_vital_machine_data_stream_risk_score_name_prefix) \
                                    and (v > threshold):
                                m_regr_ai_vital_machine_data_stream_name = \
                                    k[m_regr_ai_vital_machine_data_stream_risk_score_name_prefix_len:]

                                if m_regr_ai_vital_machine_data_stream_name in unfinished_anomaly.m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores:
                                    unfinished_anomaly.m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores[m_regr_ai_vital_machine_data_stream_name] += (v - threshold)

                                else:
                                    unfinished_anomaly.m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores[m_regr_ai_vital_machine_data_stream_name] = (v - threshold)

                    elif pandas.notnull(risk_score) and \
                            unfinished_anomaly.start_date and unfinished_anomaly.end_date and \
                            unfinished_anomaly.cum_excess_risk_score and \
                            ((date - unfinished_anomaly.end_date).days > self._ALERT_RECURRENCE_GROUPING_INTERVAL):
                        update_or_create_risk_alert(
                            machine_id=current_machine_id,

                            risk_score_name=risk_score_name,
                            threshold=threshold,

                            start_date=unfinished_anomaly.start_date,
                            end_date=unfinished_anomaly.end_date,
                            ongoing=False,
                                
                            cum_excess_risk_score=unfinished_anomaly.cum_excess_risk_score,
                            last_risk_score=unfinished_anomaly.last_risk_score,

                            m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores=
                                unfinished_anomaly.m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores)

                        unfinished_anomaly.start_date = unfinished_anomaly.end_date = None
                        unfinished_anomaly.cum_excess_risk_score = unfinished_anomaly.last_risk_score = 0
                        unfinished_anomaly.m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores = {}

            if i == (_n_risk_scores_rows_after_dedup - 1):
                for risk_score_name in unfinished_anomalies:
                    for threshold, unfinished_anomaly in unfinished_anomalies[risk_score_name].items():
                        if unfinished_anomaly.start_date and unfinished_anomaly.end_date and unfinished_anomaly.cum_excess_risk_score:
                            update_or_create_risk_alert(
                                machine_id=current_machine_id,

                                risk_score_name=risk_score_name,
                                threshold=threshold,

                                start_date=unfinished_anomaly.start_date,
                                end_date=unfinished_anomaly.end_date,
                                ongoing=True,

                                cum_excess_risk_score=unfinished_anomaly.cum_excess_risk_score,
                                last_risk_score=unfinished_anomaly.last_risk_score,

                                m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores=
                                    unfinished_anomaly.m_regr_ai_vital_machine_data_stream_cum_excess_risk_scores)

    def _run_combo(
            self,
            machine_class_name: str, machine_family_name: str,
            date: str, *, to_date: str = None, monthly=False) -> None:
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


    def _precision_recall(
            self, risk_score_name='ewma168__rowHigh__dailyMean__abs__MAE_Mult', anom_alert_threshold=3,
            from_date=None, to_date=None,
            return_query_sets=False):
        kwargs = {}

        if from_date:
            kwargs['to_date__gte'] = from_date

        if to_date:
            kwargs['from_date__lte'] = to_date

        equipment_problem_periods = \
            self.data.EquipmentProblemPeriods.filter(
                dismissed=False,
                **kwargs)

        n_equipment_problem_periods = \
            equipment_problem_periods.count()

        recall = \
            (# TODO: enhance this with advanced Django queries
                    sum(bool(equipment_problem_period.alerts.filter(
                        risk_score_name=risk_score_name,
                        threshold=anom_alert_threshold))
                        for equipment_problem_period in tqdm(equipment_problem_periods))
                    / n_equipment_problem_periods) \
                if n_equipment_problem_periods \
                else None

        alerts = \
            self.data.PredMaintAlerts.filter(
                risk_score_name=risk_score_name,
                threshold=anom_alert_threshold,
                **kwargs) \
                .filter(
                Q(diagnosis_status__name__icontains='concluded') |
                ~Q(equipment_problem_periods=None))

        n_alerts = alerts.count()

        precision = \
            (alerts.exclude(equipment_problem_periods=None).count()
             / n_alerts) \
                if n_alerts \
                else None

        results = Namespace(
            n_equipment_problem_periods=n_equipment_problem_periods, recall=recall,
            n_alerts=n_alerts, precision=precision)

        if return_query_sets:
            results.equipment_problem_periods = equipment_problem_periods
            results.alerts = alerts

        return results

    def _n_alerts_per_equipment_instance_per_year(
            self, from_date, to_date,
            risk_score_name='ewma168__rowHigh__dailyMean__abs__MAE_Mult', anom_alert_threshold=3):
        n_yrs = ((datetime.datetime.strptime(to_date, '%Y-%m-%d') -
                  datetime.datetime.strptime(from_date, '%Y-%m-%d')).days + 1) / 365

        alerts = \
            self.data.PredMaintAlerts.filter(
                risk_score_name=risk_score_name,
                threshold=anom_alert_threshold,
                from_date__lte=to_date,
                to_date__gte=from_date)

        results = {}

        for r in alerts.values('equipment_general_type__name', 'equipment_unique_type_group__name') \
                .distinct() \
                .order_by():   # *** DBUG: https://stackoverflow.com/questions/9017706/django-comment-framework-distinct-does-not-work ***
            equipment_general_type_name = r['equipment_general_type__name']
            equipment_unique_type_group_name = r['equipment_unique_type_group__name']

            n_alerts = alerts.filter(
                equipment_unique_type_group__name=equipment_unique_type_group_name)

            n_equipment_instances = \
                len(self.load_equipment_data(
                    '{}---{}'.format(
                        equipment_general_type_name.upper(),
                        equipment_unique_type_group_name),
                    _from_files=True, _spark=False,
                    set_i_col=False, set_t_col=False,
                    verbose=True)
                    .filterByPartitionKeys(
                    (DATE_COL, from_date, to_date))
                    [self._MACHINE_UNIQUE_ID_COL_NAME]
                    .collect(self._MACHINE_UNIQUE_ID_COL_NAME)
                    .unique())

            results[(equipment_general_type_name, equipment_unique_type_group_name)] = \
                Namespace(
                    n_alerts=n_alerts,
                    n_equipment_instances=n_equipment_instances,
                    n_alerts_per_equipment_instance_per_year=n_alerts / (n_equipment_instances * n_yrs))

        return results

    def _viz(self,
             machine_unique_id, dir_path,
             from_month=None, to_month=None, dates_of_interest=(),
             detail=False):
        SCORE_STR = 'score'
        risk_score_STR = 'Anomaly Score'
        SENSOR_NAME_STR = 'sensor'

        print('*** VISUALIZING {}{}{} WITH DATES OF INTEREST {} ***'.format(
            machine_unique_id,
            ' FROM {}'.format(from_month)
            if from_month
            else '',
            ' TO {}'.format(to_month)
            if to_month
            else '',
            dates_of_interest))

        dir_path = \
            os.path.join(
                dir_path,
                '{}{}{}'.format(
                    machine_unique_id,
                    '---from-{}'.format(from_month)
                    if from_month
                    else '',
                    '---to-{}'.format(to_month)
                    if to_month
                    else ''))

        if from_month:
            from_month_start_date_str = '{}-01'.format(from_month)
            from_month_start_date = datetime.datetime.strptime(from_month_start_date_str, '%Y-%m-%d').date()
            from_month_start_timestamp = pandas.Timestamp(from_month_start_date_str)

        if to_month:
            to_month_end_date = month_end(to_month)
            to_month_end_date_str = str(to_month_end_date)
            to_month_end_timestamp = pandas.Timestamp(to_month_end_date)

        daily_risk_scores_dfs = {}
        daily_err_mults_arrow_adfs = {}

        associated_equipment_instances = \
            self.associated_equipment_instances(
                equipment_instance_name=machine_unique_id,
                from_date=from_month_start_date_str if from_month else None,
                to_date=to_month_end_date_str if to_month else None)

        for equipment_instance in tqdm(associated_equipment_instances, total=associated_equipment_instances.count()):
            equipment_general_type_name = \
                equipment_instance.equipment_general_type.name

            for equipment_unique_type_group in equipment_instance.equipment_unique_type.equipment_unique_type_groups.all():
                if self.data.PredMaintBlueprints.filter(
                        equipment_unique_type_group=equipment_unique_type_group,
                        active=True):
                    equipment_unique_type_group_name = equipment_unique_type_group.name

                    _dir_path = \
                        os.path.join(
                            dir_path,
                            equipment_instance.name,
                            equipment_unique_type_group_name)

                    tup = (equipment_general_type_name, equipment_unique_type_group_name)

                    equipment_unique_type_group_data_set_name = \
                        '{}---{}'.format(
                            equipment_general_type_name.upper(),
                            equipment_unique_type_group_name)

                    if tup not in daily_risk_scores_dfs:
                        daily_risk_scores_s3_parquet_df = \
                            S3ParquetDataFeeder(
                                path=os.path.join(
                                    's3://{}/{}'.format(
                                        self.params.s3.bucket,
                                        self.params.s3.risk_scores.dir_prefix),
                                    equipment_unique_type_group_data_set_name + _PARQUET_EXT),
                                aws_access_key_id=self.params.s3.access_key_id,
                                aws_secret_access_key=self.params.s3.secret_access_key,
                                verbose=True)

                        daily_risk_scores_dfs[tup] = \
                            daily_risk_scores_s3_parquet_df.collect()

                        daily_risk_scores_dfs[tup].loc[:, self._MACHINE_UNIQUE_ID_COL_NAME] = \
                            daily_risk_scores_dfs[tup][self._MACHINE_UNIQUE_ID_COL_NAME].map(str)

                    daily_risk_scores_df = daily_risk_scores_dfs[tup]

                    daily_risk_scores_df = \
                        daily_risk_scores_df.loc[
                            (daily_risk_scores_df[self._MACHINE_UNIQUE_ID_COL_NAME].map(snake_case) == equipment_instance.name) &
                            ((daily_risk_scores_df[DATE_COL] >= from_month_start_timestamp) if from_month else True) &
                            ((daily_risk_scores_df[DATE_COL] <= to_month_end_timestamp) if to_month else True)]

                    _alpha_str = '{:.3f}'.format(self.DEFAULT_EWMA_ALPHA)[-3:]

                    _ewma_prefix = AbstractPPPBlueprint._EWMA_PREFIX + _alpha_str + '__'

                    plot_title_prefix = \
                        '{} {} #{}\n'.format(
                            equipment_general_type_name.upper(),
                            equipment_unique_type_group_name,
                            equipment_instance.name)

                    # plot Anom Scores
                    dailyMean_AnomScores_df = \
                        daily_risk_scores_df[
                            [self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL,
                             self._OVERALL_PPP_risk_score_NAME_PREFIX + AbstractPPPBlueprint._dailyMean_PREFIX +
                             AbstractPPPBlueprint._ABS_PREFIX + 'MAE_Mult']
                        ].rename(
                            index=None,
                            columns={(self._OVERALL_PPP_risk_score_NAME_PREFIX + AbstractPPPBlueprint._dailyMean_PREFIX +
                                      AbstractPPPBlueprint._ABS_PREFIX + 'MAE_Mult'):
                                         'high dayMean MAE x'},
                            copy=False,
                            inplace=False,
                            level=None)

                    if len(dailyMean_AnomScores_df) and dailyMean_AnomScores_df.iloc[:, 2:].notnull().any().any():
                        risk_scores_plot = \
                            ggplot(
                                aes(x=DATE_COL,
                                    y=risk_score_STR,
                                    color=SCORE_STR,
                                    group=SCORE_STR),
                                data=pandas.melt(
                                    frame=dailyMean_AnomScores_df,
                                    id_vars=[self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL],
                                    value_vars=None,
                                    var_name=SCORE_STR,
                                    value_name=risk_score_STR,
                                    col_level=None)) + \
                            geom_line() + \
                            geom_vline(
                                xintercept=dates_of_interest,
                                color='red',
                                linetype='dotted',   # 'solid', 'dashed', 'dashdot'
                                size=.3) + \
                            scale_x_datetime(
                                date_breaks='1 month',
                                date_labels='%Y-%m') + \
                            scale_y_continuous(
                                limits=(0, 9),
                                breaks=(0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 9)) + \
                            ggtitle(plot_title_prefix + risk_score_STR) + \
                            theme(axis_text_x=element_text(rotation=90))

                        file_name = \
                            '{}---ANOM-SCORES.png'.format(
                                equipment_instance.name)

                        fs.mkdir(
                            dir=_dir_path,
                            hdfs=False)

                        try:
                            risk_scores_plot.save(
                                filename=file_name,
                                path=_dir_path,
                                width=None, height=None, dpi=300,
                                verbose=False)

                        except Exception as err:
                            print('*** {}: {} ***'.format(file_name, err))

                    # plot EWMA Anom Scores
                    ewma_dailyMean_AnomScores_df = \
                        daily_risk_scores_df[
                            [self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL,

                             _ewma_prefix + self._OVERALL_PPP_risk_score_NAME_PREFIX + AbstractPPPBlueprint._dailyMean_PREFIX +
                             AbstractPPPBlueprint._ABS_PREFIX + 'MAE_Mult']
                        ].rename(
                            index=None,
                            columns={(_ewma_prefix + self._OVERALL_PPP_risk_score_NAME_PREFIX + AbstractPPPBlueprint._dailyMean_PREFIX +
                                      AbstractPPPBlueprint._ABS_PREFIX + 'MAE_Mult'):
                                         'ewma high dailyMean MAE x'},
                            copy=False,
                            inplace=False,
                            level=None)

                    if len(ewma_dailyMean_AnomScores_df) and \
                            ewma_dailyMean_AnomScores_df.iloc[:, 2:].notnull().any().any():
                        ewma_risk_scores_plot = \
                            ggplot(
                                aes(x=DATE_COL,
                                    y=risk_score_STR,
                                    color=SCORE_STR,
                                    group=SCORE_STR),
                                data=pandas.melt(
                                    frame=ewma_dailyMean_AnomScores_df,
                                    id_vars=[self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL],
                                    value_vars=None,
                                    var_name=SCORE_STR,
                                    value_name=risk_score_STR,
                                    col_level=None)) + \
                            geom_line() + \
                            geom_vline(
                                xintercept=dates_of_interest,
                                color='red',
                                linetype='dotted',   # 'solid', 'dashed', 'dashdot'
                                size=.3) + \
                            scale_x_datetime(
                                date_breaks='1 month',
                                date_labels='%Y-%m') + \
                            scale_y_continuous(
                                limits=(0, 9),
                                breaks=(0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 9)) + \
                            ggtitle(plot_title_prefix + risk_score_STR + ' (EWMA alpha={})'.format(self.DEFAULT_EWMA_ALPHA)) + \
                            theme(axis_text_x=element_text(rotation=90))

                        file_name = \
                            '{}---EWMA-ANOM-SCORES.png'.format(
                                equipment_instance.name)

                        try:
                            ewma_risk_scores_plot.save(
                                filename=file_name,
                                path=_dir_path,
                                width=None, height=None, dpi=300,
                                verbose=False)

                        except Exception as err:
                            print('*** {}: {} ***'.format(file_name, err))

                    if detail:
                        # plot (non-EWMA) Abs MAE Mults
                        if tup not in daily_err_mults_arrow_adfs:
                            daily_err_mults_arrow_adf = \
                                S3ParquetDataFeeder(
                                    path=os.path.join(
                                        's3://{}/{}'.format(
                                            self.params.s3.bucket,
                                            self.params.s3.ppp.daily_err_mults_dir_prefix),
                                        equipment_unique_type_group_data_set_name + _PARQUET_EXT),
                                    aws_access_key_id=self.params.s3.access_key_id,
                                    aws_secret_access_key=self.params.s3.secret_access_key,
                                    verbose=True)

                            daily_err_mults_arrow_adfs[tup] = \
                                daily_err_mults_arrow_adf.collect()

                            daily_err_mults_arrow_adfs[tup].loc[:, self._MACHINE_UNIQUE_ID_COL_NAME] = \
                                daily_err_mults_arrow_adfs[tup][self._MACHINE_UNIQUE_ID_COL_NAME].map(str)

                        daily_err_mults_df = daily_err_mults_arrow_adfs[tup]

                        daily_err_mults_df = \
                            daily_err_mults_df.loc[
                                (daily_err_mults_df[self._MACHINE_UNIQUE_ID_COL_NAME].map(snake_case) == equipment_instance.name) &
                                ((daily_err_mults_df[DATE_COL] >= from_month_start_date) if from_month else True) &
                                ((daily_err_mults_df[DATE_COL] <= to_month_end_date) if to_month else True)]

                        abs_mults_plots = {}
                        mults_plots = dict(MAE={})

                        for metric in ('MAE',):
                            MEAN_MULT_STR = 'Mean {} Multiple'.format(metric)
                            MEAN_ABS_MULT_STR = 'Mean Abs {} Multiple'.format(metric)

                            _dailyMean_abs_mult_prefix = \
                                AbstractPPPBlueprint._dailyMean_PREFIX + \
                                AbstractPPPBlueprint._ABS_PREFIX + \
                                '{}_Mult__'.format(metric)

                            _dailyMean_abs_mult_prefix_len = \
                                len(_dailyMean_abs_mult_prefix)

                            _dailyMean_abs_mult_cols = \
                                [col for col in daily_err_mults_df.columns
                                 if col.startswith(_dailyMean_abs_mult_prefix)]

                            assert _dailyMean_abs_mult_cols, \
                                '*** {} ***'.format(_dailyMean_abs_mult_prefix)

                            _dailyMean_abs_mult_cols_rename_dict = \
                                {col: col[_dailyMean_abs_mult_prefix_len:]
                                 for col in _dailyMean_abs_mult_cols}

                            dailyMean_abs_mults_df = \
                                daily_err_mults_df[
                                    [self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL] +
                                    _dailyMean_abs_mult_cols] \
                                    .rename(
                                    index=None,
                                    columns=_dailyMean_abs_mult_cols_rename_dict,
                                    copy=False,
                                    inplace=False,
                                    level=None)

                            if len(dailyMean_abs_mults_df) and dailyMean_abs_mults_df.iloc[:, 2:].notnull().any().any():
                                abs_mults_plots[metric] = \
                                    abs_mults_plot = \
                                    ggplot(
                                        aes(x=DATE_COL,
                                            y=MEAN_ABS_MULT_STR,
                                            color=SENSOR_NAME_STR,
                                            group=SENSOR_NAME_STR),
                                        data=pandas.melt(
                                            frame=dailyMean_abs_mults_df,
                                            id_vars=[self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL],
                                            value_vars=None,
                                            var_name=SENSOR_NAME_STR,
                                            value_name=MEAN_ABS_MULT_STR,
                                            col_level=None)) + \
                                    geom_line() + \
                                    geom_vline(
                                        xintercept=dates_of_interest,
                                        color='red',
                                        linetype='dotted',   # 'solid', 'dashed', 'dashdot'
                                        size=.3) + \
                                    scale_x_datetime(
                                        date_breaks='1 month',
                                        date_labels='%Y-%m') + \
                                    scale_y_continuous(
                                        limits=(0, 9),
                                        breaks=(0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 9)) + \
                                    ggtitle(plot_title_prefix + MEAN_ABS_MULT_STR) + \
                                    theme(axis_text_x=element_text(rotation=90))

                                file_name = \
                                    '{}---ABS-{}-MULTS.png'.format(
                                        equipment_instance.name,
                                        metric)

                                try:
                                    abs_mults_plot.save(
                                        filename=file_name,
                                        path=_dir_path,
                                        width=None, height=None, dpi=300,
                                        verbose=False)

                                except Exception as err:
                                    print('*** {}: {} ***'.format(file_name, err))

                            # plot Indiv Target Sensor non-EWMA MAE Mults
                            for label_var_name in \
                                    self.params.equipment_monitoring.equipment_unique_type_groups_monitored_and_included_excluded_data_fields[equipment_general_type_name][equipment_unique_type_group_name]:
                                if ('{}__'.format(metric) + label_var_name) in daily_err_mults_df.columns:
                                    err_mults_df = \
                                        daily_err_mults_df[
                                            [self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL,
                                             AbstractPPPBlueprint._dailyMean_PREFIX + AbstractPPPBlueprint._SGN_PREFIX + '{}_Mult__'.format(metric) + label_var_name,
                                             AbstractPPPBlueprint._dailyMean_PREFIX + AbstractPPPBlueprint._NEG_PREFIX + '{}_Mult__'.format(metric) + label_var_name,
                                             AbstractPPPBlueprint._dailyMean_PREFIX + AbstractPPPBlueprint._POS_PREFIX + '{}_Mult__'.format(metric) + label_var_name]] \
                                            .rename(
                                            index=None,
                                            columns={(AbstractPPPBlueprint._dailyMean_PREFIX + AbstractPPPBlueprint._SGN_PREFIX + '{}_Mult__'.format(metric) + label_var_name):
                                                         'Act - Pred',
                                                     (AbstractPPPBlueprint._dailyMean_PREFIX + AbstractPPPBlueprint._NEG_PREFIX + '{}_Mult__'.format(metric) + label_var_name):
                                                         'under',
                                                     (AbstractPPPBlueprint._dailyMean_PREFIX + AbstractPPPBlueprint._POS_PREFIX + '{}_Mult__'.format(metric) + label_var_name):
                                                         'over'},
                                            copy=False,
                                            inplace=False,
                                            level=None)

                                    if len(err_mults_df) and err_mults_df.iloc[:, 2:].notnull().any().any():
                                        mults_plots[metric][label_var_name] = \
                                            mults_plot = \
                                            ggplot(
                                                aes(x=DATE_COL,
                                                    y=MEAN_MULT_STR,
                                                    color=label_var_name,
                                                    group=label_var_name),
                                                data=pandas.melt(
                                                    frame=err_mults_df,
                                                    id_vars=[self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL],
                                                    value_vars=None,
                                                    var_name=label_var_name,
                                                    value_name=MEAN_MULT_STR,
                                                    col_level=None)) + \
                                            geom_line() + \
                                            geom_vline(
                                                xintercept=dates_of_interest,
                                                color='red',
                                                linetype='dotted',   # 'solid', 'dashed', 'dashdot'
                                                size=.3) + \
                                            scale_x_datetime(
                                                date_breaks='1 month',
                                                date_labels='%Y-%m') + \
                                            scale_y_continuous(
                                                limits=(-9, 9),
                                                breaks=(-9, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -.5,
                                                        0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 9)) + \
                                            ggtitle(plot_title_prefix + MEAN_MULT_STR + ': ' + label_var_name) + \
                                            theme(axis_text_x=element_text(rotation=90))

                                        file_name = \
                                            '{}---SIGNED-{}-MULTS.{}.png'.format(
                                                equipment_instance.name,
                                                metric,
                                                label_var_name)

                                        try:
                                            mults_plot.save(
                                                filename=file_name,
                                                path=_dir_path,
                                                width=None, height=None, dpi=300,
                                                verbose=False)

                                        except Exception as err:
                                            print('*** {}: {} ***'.format(file_name, err))

    def _export_risk_scores_csv(
            self,
            equipment_general_type_name, equipment_unique_type_group_name,
            from_month=None, to_month=None):
        equipment_unique_type_group_data_set_name = \
            '{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name)

        index_cols = [self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL]

        daily_err_mults_df = \
            S3ParquetDataFeeder(
                path=os.path.join(
                    's3://{}/{}'.format(
                        self.params.s3.bucket,
                        self.params.s3.ppp.daily_err_mults_dir_prefix),
                    equipment_unique_type_group_data_set_name + _PARQUET_EXT),
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=True) \
                .filterByPartitionKeys(
                (DATE_COL,
                 '{}-01'.format(from_month)
                 if from_month
                 else None,
                 '{}-31'.format(to_month)
                 if to_month
                 else None)) \
                .collect() \
                .sort_values(
                by=index_cols,
                axis='index',
                ascending=True,
                inplace=False,
                kind='quicksort',
                na_position='last') \
                .reset_index(
                level=None,
                drop=True,
                inplace=False,
                col_level=0,
                col_fill='')

        risk_scores_s3_dir_path = \
            os.path.join(
                's3://{}/{}'.format(
                    self.params.s3.bucket,
                    self.params.s3.risk_scores.dir_prefix),
                equipment_unique_type_group_data_set_name + _PARQUET_EXT)

        risk_scores_df = \
            S3ParquetDataFeeder(
                path=risk_scores_s3_dir_path,
                aws_access_key_id=self.params.s3.access_key_id,
                aws_secret_access_key=self.params.s3.secret_access_key,
                verbose=True) \
                .collect()

        if from_month or to_month:
            risk_scores_df = \
                risk_scores_df.loc[
                    ((risk_scores_df[DATE_COL].dt.date.map(str) > from_month) if from_month else True) &
                    ((risk_scores_df[DATE_COL].dt.date.map(str) <= '{}-31'.format(to_month)) if to_month else True)]

        risk_scores_df = \
            risk_scores_df.sort_values(
                by=index_cols,
                axis='index',
                ascending=True,
                inplace=False,
                kind='quicksort',
                na_position='last') \
                .reset_index(
                level=None,
                drop=True,
                inplace=False,
                col_level=0,
                col_fill='')

        assert (risk_scores_df[self._MACHINE_UNIQUE_ID_COL_NAME]
                == daily_err_mults_df[self._MACHINE_UNIQUE_ID_COL_NAME]).all()

        risk_scores_df = \
            pandas.concat(
                [risk_scores_df,
                 daily_err_mults_df[[col for col in daily_err_mults_df.columns
                                     if not (col in {self._MACHINE_UNIQUE_ID_COL_NAME, DATE_COL, 'blueprint_uuid'}
                                             or col.startswith('dailyMean__neg__MAE_Mult__')
                                             or col.startswith('dailyMean__pos__MAE_Mult__')
                                             or col.startswith('dailyMean__sgn__MAE_Mult__'))]]],
                axis='columns',
                join='outer',
                ignore_index=False,
                keys=None,
                levels=None,
                names=None,
                verify_integrity=False,
                sort=False,
                copy=False)

        _tmp_csv_file_path = \
            '/tmp/{}---AnomScores.csv.bz2'.format(
                equipment_unique_type_group_data_set_name)

        print('Writing {:,} Rows to {}... '.format(len(risk_scores_df), _tmp_csv_file_path), end='')
        tic = time.time()

        risk_scores_df.to_csv(
            _tmp_csv_file_path,
            sep=',',
            na_rep='',
            float_format=None,
            columns=None,
            header=True,
            index=False,
            index_label=None,
            mode='w',
            encoding='utf-8',
            compression='bz2',   # smaller files than Zlib/Gzip (XZ not installed by default)
            quoting=None,
            quotechar='"',
            line_terminator='\n',
            chunksize=None,
            tupleize_cols=None,
            date_format=None,
            doublequote=True,
            escapechar=None,
            decimal='.')

        toc = time.time()
        print('done!   <{:,.1f} m>'.format((toc - tic) / 60))

        print('Uploading {}... '.format(_tmp_csv_file_path), end='')
        tic = time.time()

        self.s3_client.upload_file(
            Filename=_tmp_csv_file_path,
            Bucket=self.params.s3.bucket,
            Key=os.path.join(
                self.params.s3.risk_scores.dir_prefix,
                equipment_unique_type_group_data_set_name + '.csv.bz2'))

        toc = time.time()
        print('done!   <{:,.1f} m>'.format((toc - tic) / 60))

    def _move_train_val_benchmark_files(
            self,
            equipment_general_type_name, equipment_unique_type_group_name,
            *to_months,
            **kwargs):
        equipment_unique_type_group_data_set_name = \
            '{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name)

        archive = kwargs.get('archive')

        for to_month in to_months:
            from_date = \
                str((datetime.datetime.strptime('{}-01'.format(to_month), '%Y-%m-%d') -
                     relativedelta(months=self.REF_N_MONTHS - 1)).date())

            from_month = from_date[:7]

            equipment_unique_type_group_train_val_data_set_path = \
                os.path.join(
                    self.params.s3.equipment_data.train_val_benchmark_dir_path,
                    '{}---from-{}---to-{}---TrainVal{}'.format(
                        equipment_unique_type_group_data_set_name,
                        from_month, to_month, _PARQUET_EXT))

            equipment_unique_type_group_benchmark_data_set_path = \
                os.path.join(
                    self.params.s3.equipment_data.train_val_benchmark_dir_path,
                    '{}---from-{}---to-{}---Benchmark{}'.format(
                        equipment_unique_type_group_data_set_name,
                        from_month, to_month, _PARQUET_EXT))

            if archive:
                s3.mv(
                    from_path=equipment_unique_type_group_train_val_data_set_path,
                    to_path='{}.ARCHIVE-{}'.format(equipment_unique_type_group_train_val_data_set_path, datetime.date.today()),
                    is_dir=True,
                    access_key_id=self.params.s3.access_key_id,
                    secret_access_key=self.params.s3.secret_access_key,
                    quiet=True,
                    verbose=True)

                s3.mv(
                    from_path=equipment_unique_type_group_benchmark_data_set_path,
                    to_path='{}.ARCHIVE-{}'.format(equipment_unique_type_group_benchmark_data_set_path, datetime.date.today()),
                    is_dir=True,
                    access_key_id=self.params.s3.access_key_id,
                    secret_access_key=self.params.s3.secret_access_key,
                    quiet=True,
                    verbose=True)

            else:
                s3.rm(
                    path=equipment_unique_type_group_train_val_data_set_path,
                    dir=True,
                    access_key_id=self.params.s3.access_key_id,
                    secret_access_key=self.params.s3.secret_access_key,
                    quiet=True,
                    verbose=True)

                s3.rm(
                    path=equipment_unique_type_group_benchmark_data_set_path,
                    dir=True,
                    access_key_id=self.params.s3.access_key_id,
                    secret_access_key=self.params.s3.secret_access_key,
                    quiet=True,
                    verbose=True)

    def _equipment_proportion_w_ongoing_alerts(
            self,
            equipment_general_type_name=None, equipment_unique_type_group_name=None,
            risk_score_name='ewma168__rowHigh__dailyMean__abs__MAE_Mult', anom_alert_threshold=3):
        results = self.count_equipment(
            equipment_general_type_name=equipment_general_type_name,
            equipment_unique_type_group_name=equipment_unique_type_group_name)

        for equipment_general_type_name, equipment_unique_type_group_names_and_counts in results.items():
            for equipment_unique_type_group_name, count in equipment_unique_type_group_names_and_counts.items():
                n_ongoing_alerts = \
                    self.data.PredMaintAlerts.filter(
                        equipment_unique_type_group__name=equipment_unique_type_group_name,
                        risk_score_name=risk_score_name,
                        threshold=anom_alert_threshold,
                        ongoing=True) \
                        .count()

                results[equipment_general_type_name][equipment_unique_type_group_name] = \
                    count, n_ongoing_alerts, n_ongoing_alerts / count

        return results
    
    def _api_vs_s3_risk_scores(self, equipment_general_type_name, equipment_unique_type_group_name):
        import requests

        risk_score_NAME = 'ewma168__rowHigh__dailyMean__abs__MAE_Mult'
        N_risk_scoreS_TO_LOAD = 10 ** 7

        risk_scores_api_url = \
            'http://{}/api/pred-maint/equipment-instance-daily-risk-scores/?equipment_unique_type_group__name={}&risk_score_name={}'.format(
                self.params.api.endpoint,
                equipment_unique_type_group_name,
                risk_score_NAME)

        api_risk_scores_query = \
            requests.get(
                url=risk_scores_api_url + '&limit={}'.format(N_risk_scoreS_TO_LOAD),
                auth=(self.params.api.user, self.params.api.password))

        n_api_risk_scores = api_risk_scores_query.json()['count']

        if n_api_risk_scores > N_risk_scoreS_TO_LOAD:
            api_risk_scores_query = \
                requests.get(
                    url=risk_scores_api_url + '&limit={}'.format(n_api_risk_scores),
                    auth=(self.params.api.user, self.params.api.password))



        equipment_unique_type_group_data_set_name = \
            '{}---{}'.format(
                equipment_general_type_name.upper(),
                equipment_unique_type_group_name)

        s3_risk_scores_df = \
            S3ParquetDataFeeder(
                path=os.path.join(
                    's3://{}'.format(self.params.s3.bucket),
                    self.params.s3.risk_scores.dir_prefix,
                    equipment_unique_type_group_data_set_name,
                    'PPPAnomScores' + _PARQUET_EXT)) \
                .collect()
