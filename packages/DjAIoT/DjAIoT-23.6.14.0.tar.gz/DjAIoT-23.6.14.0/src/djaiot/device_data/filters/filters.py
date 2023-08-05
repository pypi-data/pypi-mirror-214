from django.db.models.fields.json import JSONField

from rest_framework_filters import CharFilter, FilterSet, OrderingFilter, RelatedFilter, AllLookupsFilter

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
    MachineData, \
    MachineDataStreamAgg, \
    MachineFamilyDataStreamProfile, \
    MachineFamilyDataStreamPairCorr


class EnvironmentVariableFilter(FilterSet):
    class Meta:
        model = EnvironmentVariable

        fields = dict(
            key=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
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


class PhysicalDataTypeFilter(FilterSet):
    class Meta:
        model = PhysicalDataType

        fields = dict(
            unique_name=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            min=(
                'exact',  # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',  # 'icontains',
                'startswith',  # 'istartswith',
                'endswith',  # 'iendswith',
                'range',
                # 'isnull',
                'regex', 'iregex',
                # 'contained_by'
            ),

            max=(
                'exact',  # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',  # 'icontains',
                'startswith',  # 'istartswith',
                'endswith',  # 'iendswith',
                'range',
                # 'isnull',
                'regex', 'iregex',
                # 'contained_by'
            )
        )

    order_by = \
        OrderingFilter(
            fields=(
                'unique_name',
            )
        )


class MeasurementUnitFilter(FilterSet):
    class Meta:
        model = MeasurementUnit

        fields = dict(
            unique_name=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                # 'regex', 'iregex'
            ),

            descriptions='__all__',
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
                'unique_name',
            )
        )


class MachineClassFilter(FilterSet):
    class Meta:
        model = MachineClass

        fields = dict(
            unique_name=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            descriptions='__all__',
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
                'unique_name',
            )
        )


class MachineComponentFilter(FilterSet):
    machine_class = \
        RelatedFilter(
            queryset=MachineClass.objects.all(),
            filterset=MachineClassFilter)

    directly_interacting_components = \
        RelatedFilter(
            queryset=MachineComponent.objects.all(),
            filterset='MachineComponentFilter')

    sub_components = \
        RelatedFilter(
            queryset=MachineComponent.objects.all(),
            filterset='MachineComponentFilter')

    machine_data_streams = \
        RelatedFilter(
            queryset=MachineDataStream.objects.all(),
            filterset='MachineDataStreamFilter')

    machine_skus = \
        RelatedFilter(
            queryset=MachineSKU.objects.all(),
            filterset='MachineSKUFilter')

    class Meta:
        model = MachineComponent

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

    order_by = \
        OrderingFilter(
            fields=(
                'machine_class__unique_name',
                'name'
            )
        )


class MachineDataStreamFilter(FilterSet):
    machine_class = \
        RelatedFilter(
            queryset=MachineClass.objects.all(),
            filterset=MachineClassFilter)

    machine_components = \
        RelatedFilter(
            queryset=MachineComponent.objects.all(),
            filterset=MachineComponentFilter)

    physical_data_type = \
        RelatedFilter(
            queryset=PhysicalDataType.objects.all(),
            filterset=PhysicalDataTypeFilter)

    measurement_unit = \
        RelatedFilter(
            queryset=MeasurementUnit.objects.all(),
            filterset=MeasurementUnitFilter)

    machine_skus = \
        RelatedFilter(
            queryset=MachineSKU.objects.all(),
            filterset='MachineSKUFilter')

    class Meta:
        model = MachineDataStream

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

            descriptions='__all__',

            machine_data_stream_type=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                # 'isnull',
                'regex', 'iregex',
                # 'contained_by'
            ),

            logical_data_type=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                # 'isnull',
                'regex', 'iregex',
                # 'contained_by'
            ),

            pos_invalid=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                # 'isnull',
                'regex', 'iregex',
                # 'contained_by'
            ),

            default=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull',
                'regex', 'iregex',
                # 'contained_by'
            ))

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }

    order_by = \
        OrderingFilter(
            fields=(
                'machine_class__unique_name',
                'name'
            )
        )


class MachineFamilyFilter(FilterSet):
    machine_class = \
        RelatedFilter(
            queryset=MachineClass.objects.all(),
            filterset=MachineClassFilter)

    machine_skus = \
        RelatedFilter(
            queryset=MachineSKU.objects.all(),
            filterset='MachineSKUFilter')

    machine_components = \
        RelatedFilter(
            queryset=MachineComponent.objects.all(),
            filterset=MachineComponentFilter)

    machine_data_streams = \
        RelatedFilter(
            queryset=MachineDataStream.objects.all(),
            filterset=MachineDataStreamFilter)

    class Meta:
        model = MachineFamily

        fields = dict(
            unique_name=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            descriptions='__all__',
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
                'machine_class__unique_name',
                'unique_name'
            )
        )


class MachineSKUFilter(FilterSet):
    machine_class = \
        RelatedFilter(
            queryset=MachineClass.objects.all(),
            filterset=MachineClassFilter)

    machine_components = \
        RelatedFilter(
            queryset=MachineComponent.objects.all(),
            filterset=MachineComponentFilter)

    machine_data_streams = \
        RelatedFilter(
            queryset=MachineDataStream.objects.all(),
            filterset=MachineDataStreamFilter)

    machine_families = \
        RelatedFilter(
            queryset=MachineFamily.objects.all(),
            filterset=MachineFamilyFilter)

    class Meta:
        model = MachineSKU

        fields = dict(
            unique_name=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            descriptions='__all__',
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
                'machine_class__unique_name',
                'unique_name'
            )
        )


class LocationFilter(FilterSet):
    # machines = \
    #     RelatedFilter(
    #         queryset=Machine.objects.all(),
    #         filterset='MachineFilter')

    class Meta:
        model = Location

        fields = dict(
            unique_name=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            descriptions='__all__',

            info='__all__'
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
                'unique_name',
            )
        )


class MachineFilter(FilterSet):
    machine_class = \
        RelatedFilter(
            queryset=MachineClass.objects.all(),
            filterset=MachineClassFilter)

    machine_sku = \
        RelatedFilter(
            queryset=MachineSKU.objects.all(),
            filterset=MachineSKUFilter)

    location = \
        RelatedFilter(
            queryset=Location.objects.all(),
            filterset=LocationFilter)

    class Meta:
        model = Machine

        fields = dict(
            unique_id=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            info='__all__',
        )

        filter_overrides = {
            JSONField: dict(
                filter_class=CharFilter
                # 'extra': lambda f: {'lookup_expr': 'icontains'}
            )
        }


class MachineDailyDataFilter(FilterSet):
    machine = \
        RelatedFilter(
            queryset=Machine.objects.all(),
            filterset=MachineFilter)

    class Meta:
        model = MachineData

        fields = dict(
            date=(
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
            ),

            url=(
                'exact', 'iexact',
                # 'gt', 'gte', 'lt', 'lte',
                'in',
                'contains', 'icontains',
                'startswith', 'istartswith', 'endswith', 'iendswith',
                # 'range',
                # 'isnull',
                'regex', 'iregex'
            ),

            n_cols=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ),

            n_rows=(
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            )
        )


class MachineDataStreamDailyAggFilter(FilterSet):
    machine = \
        RelatedFilter(
            queryset=Machine.objects.all(),
            filterset=MachineFilter)

    # machine_data_stream = \
    #     RelatedFilter(
    #         queryset=MachineDataStream.objects.all(),
    #         filterset=MachineDataStreamFilter)

    class Meta:
        model = MachineDataStreamAgg

        fields = dict(
            min=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            robust_min=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            quartile=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            median=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            mean=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            _3rd_quartile=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            robust_max=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ],

            max=[
                'exact',   # 'iexact',
                'gt', 'gte', 'lt', 'lte',
                'in',
                'contains',   # 'icontains',
                'startswith',   # 'istartswith',
                'endswith',   # 'iendswith',
                'range',
                'isnull'
                # 'regex', 'iregex',
                # 'contained_by'
            ])


class MachineFamilyDataStreamProfileFilter(FilterSet):
    # machine_family = \
    #     RelatedFilter(
    #         queryset=MachineFamily.objects.all(),
    #         filterset=MachineFamilyFilter)

    machine_data_stream = \
        RelatedFilter(
            queryset=MachineDataStream.objects.all(),
            filterset=MachineDataStreamFilter)

    class Meta:
        model = MachineFamilyDataStreamProfile

        fields = dict(
            data_to_date=(
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
            ),

            valid_fraction=(
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
            ),

            n_distinct_values=(
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
            ))


class MachineFamilyDataStreamPairCorrFilter(FilterSet):
    # machine_family = \
    #     RelatedFilter(
    #         queryset=MachineFamily.objects.all(),
    #         filterset=MachineFamilyFilter)

    machine_data_stream = \
        RelatedFilter(
            queryset=MachineDataStream.objects.all(),
            filterset=MachineDataStreamFilter)

    other_machine_data_stream = \
        RelatedFilter(
            queryset=MachineDataStream.objects.all(),
            filterset=MachineDataStreamFilter)

    class Meta:
        model = MachineFamilyDataStreamPairCorr

        fields = dict(
            data_to_date=(
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
            ),

            n_samples=(
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
            ),

            corr=(
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
            ))
