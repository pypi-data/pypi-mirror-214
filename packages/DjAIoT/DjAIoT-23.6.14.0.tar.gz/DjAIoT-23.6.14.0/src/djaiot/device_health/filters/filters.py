from django.db.models.fields.json import JSONField

from rest_framework_filters import CharFilter, FilterSet, OrderingFilter, RelatedFilter

from .models import \
    EnvironmentVariable, \
    MachineFamilyHealthServiceConfig, \
    AI, \
    MachineFamilyVitalAIEvalMetricProfile, \
    MachineHealthRiskScore, \
    MachineHealthProblemDiagnosis, \
    MachineHealthRiskAlert, \
    MachineErrorCode, MachineError

from ..data.filters import \
    MachineFamilyFilter, \
    MachineDataStreamFilter, \
    MachineFilter

from ..data.models import \
    MachineFamily, \
    MachineDataStream, \
    Machine


class EnvironmentVariableFilter(FilterSet):
    class Meta:
        model = EnvironmentVariable

        fields = dict(
            key=(
                'exact', 'iexact',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                'regex', 'iregex'
            ),

            value='__all__'
        )

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }

    order_by = \
        OrderingFilter(
            fields=(
                'key',
            )
        )


class MachineFamilyHealthServiceConfigFilter(FilterSet):
    machine_family = \
        RelatedFilter(
            queryset=MachineFamily.objects.all(),
            filterset=MachineFamilyFilter)

    class Meta:
        model = MachineFamilyHealthServiceConfig

        fields = dict(
            active=['exact']
        )


class AIFilter(FilterSet):
    machine_family = \
        RelatedFilter(
            queryset=MachineFamily.objects.all(),
            filterset=MachineFamilyFilter)

    class Meta:
        model = AI

        fields = dict(
            ref_data_to_date=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'to_date__contained_by'
            ],

            created=[
                # 'exact', 'iexact',
                'gt', 'gte', 'lt', 'lte',
                # 'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                # 'endswith',   'iendswith',
                'range',
                # 'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'contained_by'
            ],

            unique_id=[
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ],

            active=['exact'])


class MachineFamilyVitalDataStreamAIEvalMetricProfileFilter(FilterSet):
    machine_family = \
        RelatedFilter(
            queryset=MachineFamily.objects.all(),
            filterset=MachineFamilyFilter)

    machine_data_stream = \
        RelatedFilter(
            queryset=MachineDataStream.objects.all(),
            filterset=MachineDataStreamFilter)

    class Meta:
        model = MachineFamilyVitalAIEvalMetricProfile

        fields = dict(
            ref_data_to_date=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'contained_by'
            ],

            R2=[
                # 'exact', 'iexact',
                'gt', 'gte', 'lt', 'lte',
                # 'in',
                # 'contains', 'icontains',
                'startswith', 'istartswith',
                # 'endswith', 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ])


class MachineDailyRiskScoreFilter(FilterSet):
    # machine_family = \
    #     RelatedFilter(
    #         queryset=MachineFamily.objects.all(),
    #         filterset=MachineFamilyFilter)

    machine = \
        RelatedFilter(
            queryset=Machine.objects.all(),
            filterset=MachineFilter)

    class Meta:
        model = MachineHealthRiskScore

        fields = dict(
            machine_health_risk_score_value=[
                # 'exact', 'iexact',
                'gt', 'gte', 'lt', 'lte',
                # 'in',
                # 'contains', 'icontains',
                'startswith', 'istartswith',
                # 'endswith', 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ])


class MachineProblemDiagnosisFilter(FilterSet):
    machine = \
        RelatedFilter(
            queryset=Machine.objects.all(),
            filterset=MachineFilter)

    class Meta:
        model = MachineHealthProblemDiagnosis

        fields = dict(
            from_date=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'to_date__contained_by'
            ),

            to_date=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'to_date__contained_by'
            ),

            duration=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            has_machine_health_risk_alerts=(
                'exact',
            ),

            has_machine_errors=(
                'exact',
            )
        )


class AlertFilter(FilterSet):
    machine_family = \
        RelatedFilter(
            queryset=MachineFamily.objects.all(),
            filterset=MachineFamilyFilter)

    machine = \
        RelatedFilter(
            queryset=Machine.objects.all(),
            filterset=MachineFilter)

    class Meta:
        model = MachineHealthRiskAlert

        fields = dict(
            machine_health_risk_score_value_alert_threshold=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            from_date=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'to_date__contained_by'
            ),

            to_date=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'to_date__contained_by'
            ),

            duration=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            cum_excess_machine_health_risk_score_value=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            approx_average_machine_health_risk_score_value=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            last_machine_health_risk_score_value=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            ongoing=(
                'exact',
            ),

            has_machine_health_problem_diagnoses=(
                'exact',
            ),

            has_machine_errors=(
                'exact',
            )
        )


class MachineErrorCodeFilter(FilterSet):
    class Meta:
        model = MachineErrorCode

        fields = dict(
            name=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            descriptions='__all__')

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


class MachineErrorFilter(FilterSet):
    machine = \
        RelatedFilter(
            queryset=Machine.objects.all(),
            filterset=MachineFilter)

    machine_error_code = \
        RelatedFilter(
            queryset=MachineErrorCode.objects.all(),
            filterset=MachineErrorCodeFilter)

    class Meta:
        model = MachineError

        fields = dict(
            from_utc_date_time=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'to_date__contained_by'
            ),

            to_utc_date_time=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains'
                'startswith',   # 'istartswith'
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                # 'regex', 'iregex',
                'year',   # 'year__iexact'
                'year__gt', 'year__gte', 'year__lt', 'year__lte',
                'year__in',
                # 'year__contains', 'year__icontains',
                # 'year__startswith', 'year__istartswith', 'year__endswith', year__iendswith',
                'year__range',
                # 'year__isnull',
                # 'year__regex', 'year__iregex',
                # 'year__contained_by',
                'month',   # 'month__iexact',
                'month__gt', 'month__gte', 'month__lt', 'month__lte',
                'month__in',
                # 'month__contains', 'month__icontains',
                # 'month__startswith', 'month__istartswith', 'month__endswith', 'month__iendswith'
                'month__range',
                # 'month__isnull',
                # 'month__regex', 'month__iregex',
                # 'month__contained_by',
                # 'day', 'day__iexact',
                # 'day__gt', 'day__gte', 'day__lt', 'day__lte',
                # 'day__in',
                # 'day__contains', 'day__icontains',
                # 'day__startswith', 'day__istartswith', 'day__endswith', 'day__iendswith',
                # 'day__range',
                # 'day__isnull'
                # 'day__regex', 'day__iregex'
                # 'day__contained_by'
                # 'week_day', 'week_day__iexact',
                # 'week_day__gt', 'week_day__gte', 'week_day__lt', 'week_day__lte',
                # 'week_day__in',
                # 'week_day__contains', 'week_day__icontains',
                # 'week_day__startswith', 'week_day__istartswith', 'week_day__endswith', 'week_day__iendswith',
                # 'week_day__range',
                # 'week_day__isnull',
                # 'week_day__regex', 'week_day__iregex'
                # 'week_day__contained_by',
                # 'week', 'week__iexact',
                # 'week__gt', 'week__gte', 'week__lt', 'week__lte',
                # 'week__in',
                # 'week__contains', 'week__icontains',
                # 'week__startswith', 'week__istartswith', 'week__endswith', 'week__iendswith',
                # 'week__range',
                # 'week__isnull',
                # 'week__regex', 'week__iregex',
                # 'week__contained_by',

                # django_filters.exceptions.FieldLookupError: Unsupported lookup 'quarter'
                # 'quarter',   # 'quarter__iexact',
                # 'quarter__gt', 'quarter__gte', 'quarter__lt', 'quarter__lte',
                # 'quarter__in',
                # 'quarter__contains', 'quarter__icontains',
                # 'quarter__startswith', 'quarter__istartswith', 'quarter__endswith', 'quarter__iendswith',
                # 'quarter__range'
                # 'quarter__isnull',
                # 'quarter__regex', 'quarter__iregex',
                # 'quarter__contained_by'

                # 'to_date__contained_by'
            ),

            duration=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range'
                # 'isnull',
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            has_machine_health_problem_diagnoses=(
                'exact',
            ),

            has_machine_health_risk_alerts=(
                'exact',
            )
        )
