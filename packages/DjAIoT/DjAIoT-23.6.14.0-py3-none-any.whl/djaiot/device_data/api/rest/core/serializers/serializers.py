from rest_framework.serializers import \
    Serializer, CharField, ListField, \
    ModelSerializer, RelatedField, ManyRelatedField, PrimaryKeyRelatedField, SlugRelatedField, StringRelatedField, \
    HyperlinkedModelSerializer, HyperlinkedIdentityField, HyperlinkedRelatedField

from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from drf_writable_nested.serializers import WritableNestedModelSerializer

from ....models import \
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

from ...field_names import \
    ENVIRONMENT_VARIABLE_API_FIELD_NAMES, \
    PHYSICAL_DATA_TYPE_NESTED_API_FIELD_NAMES, \
    MEASUREMENT_UNIT_API_FIELD_NAMES, \
    MACHINE_CLASS_API_FIELD_NAMES, \
    MACHINE_COMPONENT_API_FIELD_NAMES, MACHINE_COMPONENT_NESTED_API_FIELD_NAMES, \
    MACHINE_DATA_STREAM_API_FIELD_NAMES, MACHINE_DATA_STREAM_NESTED_API_FIELD_NAMES, \
    MACHINE_FAMILY_API_FIELD_NAMES, MACHINE_FAMILY_NESTED_API_FIELD_NAMES, \
    MACHINE_SKU_API_FIELD_NAMES, MACHINE_SKU_NESTED_API_FIELD_NAMES, \
    LOCATION_API_FIELD_NAMES, LOCATION_NESTED_API_FIELD_NAMES, \
    MACHINE_API_FIELD_NAMES, \
    MACHINE_DAILY_DATA_API_FIELD_NAMES, \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_API_FIELD_NAMES, \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_API_FIELD_NAMES


class EnvironmentVariableSerializer(ModelSerializer):
    class Meta:
        model = EnvironmentVariable

        fields = ENVIRONMENT_VARIABLE_API_FIELD_NAMES


class PhysicalDataTypeNestedSerializer(WritableNestedModelSerializer):
    same = \
        SlugRelatedField(
            queryset=PhysicalDataType.objects, read_only=False,
            slug_field='unique_name',
            many=True,
            required=False)

    class Meta:
        model = PhysicalDataType

        fields = PHYSICAL_DATA_TYPE_NESTED_API_FIELD_NAMES


PHYSICAL_DATA_TYPE_RELATED_FIELD = \
    PhysicalDataTypeNestedSerializer(
        read_only=False,
        many=False,
        required=False)


class MeasurementUnitSerializer(ModelSerializer):
    class Meta:
        model = MeasurementUnit

        fields = MEASUREMENT_UNIT_API_FIELD_NAMES


MEASUREMENT_UNIT_RELATED_FIELD = \
    MeasurementUnitSerializer(
        read_only=False,
        many=False,
        required=False)


class MachineClassSerializer(ModelSerializer):
    class Meta:
        model = MachineClass

        fields = MACHINE_CLASS_API_FIELD_NAMES


MACHINE_CLASS_SLUG_RELATED_FIELD = \
    SlugRelatedField(
        queryset=MachineClass.objects, read_only=False,
        slug_field='unique_name',
        many=False,
        required=True)


class MachineComponentSerializer(ModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    class Meta:
        model = MachineComponent

        fields = MACHINE_COMPONENT_API_FIELD_NAMES


MACHINE_COMPONENTS_RELATED_FIELD = \
    MachineComponentSerializer(
        read_only=False,
        many=True,
        required=False)


class MachineDataStreamSerializer(ModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    physical_data_type = PHYSICAL_DATA_TYPE_RELATED_FIELD

    measurement_unit = MEASUREMENT_UNIT_RELATED_FIELD

    class Meta:
        model = MachineDataStream

        fields = MACHINE_DATA_STREAM_API_FIELD_NAMES


MACHINE_DATA_STREAM_RELATED_FIELD = \
    MachineDataStreamSerializer(
        read_only=False,
        many=False,
        required=True)

MACHINE_DATA_STREAMS_RELATED_FIELD = \
    MachineDataStreamSerializer(
        read_only=False,
        many=True,
        required=False)


class MachineFamilySerializer(ModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    class Meta:
        model = MachineFamily

        fields = MACHINE_FAMILY_API_FIELD_NAMES


MACHINE_FAMILY_RELATED_FIELD = \
    MachineFamilySerializer(
        read_only=False,
        many=False,
        required=True)

MACHINE_FAMILIES_RELATED_FIELD = \
    MachineFamilySerializer(
        read_only=False,
        many=True,
        required=False)


class MachineSKUSerializer(ModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    class Meta:
        model = MachineSKU

        fields = MACHINE_SKU_API_FIELD_NAMES


MACHINE_SKU_RELATED_FIELD = \
    MachineSKUSerializer(
        read_only=False,
        many=False,
        required=False)

MACHINE_SKUS_RELATED_FIELD = \
    MachineSKUSerializer(
        read_only=False,
        many=True,
        required=False)


class MachineComponentNestedSerializer(WritableNestedModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    directly_interacting_components = MACHINE_COMPONENTS_RELATED_FIELD

    sub_components = MACHINE_COMPONENTS_RELATED_FIELD

    machine_data_streams = MACHINE_DATA_STREAMS_RELATED_FIELD

    machine_skus = MACHINE_SKUS_RELATED_FIELD

    class Meta:
        model = MachineComponent

        fields = MACHINE_COMPONENT_NESTED_API_FIELD_NAMES


class MachineDataStreamNestedSerializer(WritableNestedModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    machine_components = MACHINE_COMPONENTS_RELATED_FIELD

    physical_data_type = PHYSICAL_DATA_TYPE_RELATED_FIELD

    measurement_unit = MEASUREMENT_UNIT_RELATED_FIELD

    machine_skus = MACHINE_SKUS_RELATED_FIELD

    class Meta:
        model = MachineDataStream

        fields = MACHINE_DATA_STREAM_NESTED_API_FIELD_NAMES


class MachineFamilyNestedSerializer(WritableNestedModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    machine_skus = MACHINE_SKUS_RELATED_FIELD

    machine_components = MACHINE_COMPONENTS_RELATED_FIELD

    machine_data_streams = MACHINE_DATA_STREAMS_RELATED_FIELD

    class Meta:
        model = MachineFamily

        fields = MACHINE_FAMILY_NESTED_API_FIELD_NAMES


class MachineSKUNestedSerializer(WritableNestedModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    machine_components = MACHINE_COMPONENTS_RELATED_FIELD

    machine_data_streams = MACHINE_DATA_STREAMS_RELATED_FIELD

    machine_families = MACHINE_FAMILIES_RELATED_FIELD

    class Meta:
        model = MachineSKU

        fields = MACHINE_SKU_NESTED_API_FIELD_NAMES


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location

        fields = LOCATION_API_FIELD_NAMES


LOCATION_RELATED_FIELD = \
    LocationSerializer(
        read_only=False,
        many=False,
        required=False)


class MachineSerializer(WritableNestedModelSerializer):
    machine_class = MACHINE_CLASS_SLUG_RELATED_FIELD

    machine_sku = MACHINE_SKU_RELATED_FIELD

    location = LOCATION_RELATED_FIELD

    machine_families = MACHINE_FAMILIES_RELATED_FIELD

    class Meta:
        model = Machine

        fields = MACHINE_API_FIELD_NAMES


MACHINE_RELATED_FIELD = \
    MachineSerializer(
        read_only=False,
        many=False,
        required=True)

MACHINES_RELATED_FIELD = \
    MachineSerializer(
        read_only=False,
        many=True,
        required=False)


class LocationNestedSerializer(WritableNestedModelSerializer):
    machines = MACHINES_RELATED_FIELD

    class Meta:
        model = Location

        fields = LOCATION_NESTED_API_FIELD_NAMES


class MachineDailyDataSerializer(ModelSerializer):
    machine = MACHINE_RELATED_FIELD

    schema = \
        SlugRelatedField(
            read_only=True,
            slug_field='schema',
            many=False)

    class Meta:
        model = MachineData

        fields = MACHINE_DAILY_DATA_API_FIELD_NAMES


class MachineDataStreamDailyAggSerializer(ModelSerializer):
    machine = MACHINE_RELATED_FIELD

    machine_data_stream = MACHINE_DATA_STREAM_RELATED_FIELD

    class Meta:
        model = MachineDataStreamAgg

        fields = \
            'id', \
            'machine', \
            'machine_data_stream', \
            'date', \
            'count', \
            'distinct_value_counts', \
            'min', \
            'robust_min', \
            'quartile', \
            'median', \
            'mean', \
            '_3rd_quartile', \
            'robust_max', \
            'max'


class MachineFamilyDataStreamProfileSerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    machine_data_stream = MACHINE_DATA_STREAM_RELATED_FIELD

    class Meta:
        model = MachineFamilyDataStreamProfile

        fields = MACHINE_FAMILY_DATA_STREAM_PROFILE_API_FIELD_NAMES


class MachineFamilyDataStreamPairCorrSerializer(ModelSerializer):
    machine_family = MACHINE_FAMILY_RELATED_FIELD

    machine_data_stream = MACHINE_DATA_STREAM_RELATED_FIELD

    other_machine_data_stream = MACHINE_DATA_STREAM_RELATED_FIELD

    class Meta:
        model = MachineFamilyDataStreamPairCorr

        fields = MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_API_FIELD_NAMES


# serializer(obj)
# serializer(data=data)
# serializer(objs, many=True): serializer.data will be OrderedDict
# serializer.data; JSONRenderer().render(serializer.data)
# stream = io.BytesIO(content); data = JSONParser().parse(stream)
# serializer.errors
# serializer.save()
# serializer.create(validated_data): return Instance saved
# serializer.update(instance, validated_data): return Instance updated and saved
