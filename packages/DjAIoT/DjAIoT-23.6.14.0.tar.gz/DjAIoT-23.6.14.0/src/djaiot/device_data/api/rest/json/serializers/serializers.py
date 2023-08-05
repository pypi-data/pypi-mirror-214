from rest_framework_json_api.relations import \
    HyperlinkedRelatedField as JSONAPIHyperlinkedRelatedField, \
    ResourceRelatedField, PolymorphicResourceRelatedField

from rest_framework_json_api.serializers import \
    HyperlinkedModelSerializer as JSONAPIHyperlinkedModelSerializer, \
    ModelSerializer as JSONAPIModelSerializer, \
    PolymorphicModelSerializer

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
    PHYSICAL_DATA_TYPE_API_FIELD_NAMES, PHYSICAL_DATA_TYPE_NESTED_API_FIELD_NAMES, \
    MEASUREMENT_UNIT_API_FIELD_NAMES, \
    MACHINE_CLASS_API_FIELD_NAMES, \
    MACHINE_COMPONENT_API_FIELD_NAMES, MACHINE_COMPONENT_NESTED_API_FIELD_NAMES, \
    MACHINE_DATA_STREAM_API_FIELD_NAMES, MACHINE_DATA_STREAM_NESTED_API_FIELD_NAMES, \
    MACHINE_FAMILY_API_FIELD_NAMES, MACHINE_FAMILY_NESTED_API_FIELD_NAMES, \
    MACHINE_SKU_API_FIELD_NAMES, MACHINE_SKU_NESTED_API_FIELD_NAMES, \
    LOCATION_API_FIELD_NAMES, \
    MACHINE_API_FIELD_NAMES, \
    MACHINE_DAILY_DATA_SCHEMA_API_FIELD_NAMES, \
    MACHINE_DAILY_DATA_API_FIELD_NAMES, \
    MACHINE_FAMILY_DATA_STREAM_PROFILE_API_FIELD_NAMES, \
    MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_API_FIELD_NAMES


class EnvironmentVariableJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = EnvironmentVariable

        fields = \
            ENVIRONMENT_VARIABLE_API_FIELD_NAMES   # + \
            # ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = EnvironmentVariable.JSONAPIMeta.resource_name

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class PhysicalDataTypeJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = PhysicalDataType

        fields = \
            PHYSICAL_DATA_TYPE_API_FIELD_NAMES   # + \
            # ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = PhysicalDataType.JSONAPIMeta.resource_name

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class PhysicalDataTypeNameOnlyJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = PhysicalDataType

        fields = 'unique_name',

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = PhysicalDataType.JSONAPIMeta.resource_name

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class PhysicalDataTypeNestedJSONAPISerializer(JSONAPIModelSerializer):
    same = \
        ResourceRelatedField(
            queryset=PhysicalDataType.objects, read_only=False,
            many=True,
            required=False)

    included_serializers = related_serializers = \
        dict(same=PhysicalDataTypeNameOnlyJSONAPISerializer)

    class Meta:
        model = PhysicalDataType

        fields = \
            PHYSICAL_DATA_TYPE_NESTED_API_FIELD_NAMES   # + \
            # ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = PhysicalDataType.JSONAPIMeta.resource_name

        included_resources = 'same',

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MeasurementUnitJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = MeasurementUnit

        fields = \
            MEASUREMENT_UNIT_API_FIELD_NAMES   # + \
            # ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MeasurementUnit.JSONAPIMeta.resource_name

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineClassJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = MachineClass

        fields = \
            MACHINE_CLASS_API_FIELD_NAMES   # + \
            # ('url',)   # TODO: fix

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineClass.JSONAPIMeta.resource_name

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineComponentJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer)

    class Meta:
        model = MachineComponent

        fields = MACHINE_COMPONENT_API_FIELD_NAMES

    class JSONAPIMeta:
        resource_name = MachineSKU.JSONAPIMeta.resource_name

        included_resources = 'machine_class',


class MachineDataStreamJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    physical_data_type = \
        ResourceRelatedField(
            queryset=PhysicalDataType.objects, read_only=False,
            many=False,
            required=True)

    measurement_unit = \
        ResourceRelatedField(
            queryset=MeasurementUnit.objects, read_only=False,
            many=False,
            required=False)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer,
             physical_data_type=PhysicalDataTypeJSONAPISerializer,
             measurement_unit=MeasurementUnitJSONAPISerializer)

    class Meta:
        model = MachineDataStream

        fields = MACHINE_DATA_STREAM_API_FIELD_NAMES

    class JSONAPIMeta:
        resource_name = MachineDataStream.JSONAPIMeta.resource_name

        included_resources = \
            'machine_class', \
            'physical_data_type', \
            'measurement_unit'


class MachineFamilyJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer)

    class Meta:
        model = MachineFamily

        fields = MACHINE_FAMILY_API_FIELD_NAMES

    class JSONAPIMeta:
        resource_name = MachineFamily.JSONAPIMeta.resource_name

        included_resources = 'machine_class',


class MachineSKUJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer)

    class Meta:
        model = MachineSKU

        fields = MACHINE_SKU_API_FIELD_NAMES

    class JSONAPIMeta:
        resource_name = MachineSKU.JSONAPIMeta.resource_name

        included_resources = 'machine_class',


class MachineComponentNestedJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    directly_interacting_components = \
        ResourceRelatedField(
            queryset=MachineComponent.objects, read_only=False,
            many=True,
            required=False)

    sub_components = \
        ResourceRelatedField(
            queryset=MachineComponent.objects, read_only=False,
            many=True,
            required=False)

    machine_data_streams = \
        ResourceRelatedField(
            queryset=MachineDataStream.objects, read_only=False,
            many=True,
            required=False)

    machine_skus = \
        ResourceRelatedField(
            queryset=MachineSKU.objects, read_only=False,
            many=True,
            required=False)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer,
             directly_interacting_components=MachineComponentJSONAPISerializer,
             sub_components=MachineComponentJSONAPISerializer,
             machine_data_streams=MachineDataStreamJSONAPISerializer,
             machine_skus=MachineSKUJSONAPISerializer)

    class Meta:
        model = MachineComponent

        fields = \
            MACHINE_COMPONENT_NESTED_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineComponent.JSONAPIMeta.resource_name

        included_resources = \
            'machine_class', \
            'directly_interacting_components', \
            'sub_components', \
            'machine_data_streams', \
            'machine_skus'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineDataStreamNestedJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    machine_components = \
        ResourceRelatedField(
            queryset=MachineComponent.objects, read_only=False,
            many=True,
            required=False)

    physical_data_type = \
        ResourceRelatedField(
            queryset=PhysicalDataType.objects, read_only=False,
            many=False,
            required=False)

    measurement_unit = \
        ResourceRelatedField(
            queryset=MeasurementUnit.objects, read_only=False,
            many=False,
            required=False)

    machine_skus = \
        ResourceRelatedField(
            queryset=MachineSKU.objects, read_only=False,
            many=True,
            required=False)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer,
             machine_components=MachineComponentJSONAPISerializer,
             physical_data_type=PhysicalDataTypeNestedJSONAPISerializer,
             measurement_unit=MeasurementUnitJSONAPISerializer,
             machine_skus=MachineSKUJSONAPISerializer)

    class Meta:
        model = MachineDataStream

        fields = \
            MACHINE_DATA_STREAM_NESTED_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineDataStream.JSONAPIMeta.resource_name

        included_resources = \
            'machine_class', \
            'machine_components', \
            'physical_data_type', \
            'measurement_unit', \
            'machine_skus'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineFamilyNestedJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True,
            self_link_view_name=None,
            related_link_view_name=None,
            related_link_lookup_field='pk',
            related_link_url_kwarg='pk')

    machine_skus = \
        ResourceRelatedField(
            queryset=MachineSKU.objects, read_only=False,
            many=True,
            required=False)

    machine_components = \
        ResourceRelatedField(
            read_only=True,
            many=True,
            required=False)

    machine_data_streams = \
        ResourceRelatedField(
            read_only=True,
            many=True,
            required=False)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer,
             machine_skus=MachineSKUJSONAPISerializer,
             machine_components=MachineComponentJSONAPISerializer,
             machine_data_streams=MachineDataStreamJSONAPISerializer)

    class Meta:
        model = MachineFamily

        fields = \
            MACHINE_FAMILY_NESTED_API_FIELD_NAMES   # + \
            # ('url',)   # TODO: fix

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineFamily.JSONAPIMeta.resource_name

        included_resources = \
            'machine_class', \
            'machine_skus', \
            'machine_components', \
            'machine_data_streams'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineSKUNestedJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    machine_components = \
        ResourceRelatedField(
            queryset=MachineComponent.objects, read_only=False,
            many=True,
            required=False)

    machine_data_streams = \
        ResourceRelatedField(
            queryset=MachineDataStream.objects, read_only=False,
            many=True,
            required=False)

    machine_families = \
        ResourceRelatedField(
            queryset=MachineFamily.objects, read_only=False,
            many=True,
            required=False)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer,
             machine_components=MachineComponentJSONAPISerializer,
             machine_data_streams=MachineDataStreamJSONAPISerializer,
             machine_families=MachineFamilyJSONAPISerializer)

    class Meta:
        model = MachineSKU

        fields = \
            MACHINE_SKU_NESTED_API_FIELD_NAMES   # + \
            # ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineSKU.JSONAPIMeta.resource_name

        included_resources = \
            'machine', \
            'machine_component', \
            'machine_data_stream', \
            'machine_families'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class LocationJSONAPISerializer(JSONAPIModelSerializer):
    class Meta:
        model = Location

        fields = \
            'unique_name', \
            'info'

    class JSONAPIMeta:
        resource_name = Location.JSONAPIMeta.resource_name


class MachineJSONAPISerializer(JSONAPIModelSerializer):
    machine_class = \
        ResourceRelatedField(
            queryset=MachineClass.objects, read_only=False,
            many=False,
            required=True)

    machine_sku = \
        ResourceRelatedField(
            queryset=MachineSKU.objects, read_only=False,
            many=False,
            required=False)

    location = \
        ResourceRelatedField(
            queryset=Location.objects, read_only=False,
            many=False,
            required=False)

    machine_families = \
        ResourceRelatedField(
            queryset=MachineFamily.objects, read_only=False,
            many=True,
            required=False)

    included_serializers = related_serializers = \
        dict(machine_class=MachineClassJSONAPISerializer,
             machine_sku=MachineSKUJSONAPISerializer,
             location=LocationJSONAPISerializer,
             machine_families=MachineFamilyJSONAPISerializer)

    class Meta:
        model = Machine

        fields = \
            MACHINE_API_FIELD_NAMES   # + \
            # ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = Machine.JSONAPIMeta.resource_name

        included_resources = \
            'machine_class', \
            'machine_sku', \
            'location'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class LocationNestedJSONAPISerializer(JSONAPIModelSerializer):
    # machines = \
    #     ResourceRelatedField(
    #         queryset=Machine.objects, read_only=False,
    #         many=True,
    #         required=False)

    # included_serializers = related_serializers = \
    #     dict(machine=MachineJSONAPISerializer)

    class Meta:
        model = Location

        fields = \
            'unique_name', \
            'info', # \
            # 'machines' #, \
            # 'url'

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = Location.JSONAPIMeta.resource_name

        # included_resources = 'machines',

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineDailyDataJSONAPISerializer(JSONAPIModelSerializer):
    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    schema = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(machine=MachineJSONAPISerializer)

    class Meta:
        model = MachineData

        fields = MACHINE_DAILY_DATA_API_FIELD_NAMES

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineData.JSONAPIMeta.resource_name

        included_resources = 'machine',

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineDataStreamDailyAggJSONAPISerializer(JSONAPIModelSerializer):
    machine = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_data_stream = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(machine=MachineJSONAPISerializer,
             machine_data_stream=MachineDataStreamJSONAPISerializer)

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

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineDataStreamAgg.JSONAPIMeta.resource_name

        included_resources = \
            'machine', \
            'machine_data_stream'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineFamilyDataStreamProfileJSONAPISerializer(JSONAPIModelSerializer):
    machine_family_data = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_data_stream = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(#machine_family_data=MachineFamilyJSONAPISerializer,
             machine_data_stream=MachineDataStreamJSONAPISerializer)

    class Meta:
        model = MachineFamilyDataStreamProfile

        fields = \
            MACHINE_FAMILY_DATA_STREAM_PROFILE_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineFamilyDataStreamProfile.JSONAPIMeta.resource_name

        included_resources = \
            'machine_family_data', \
            'machine_data_stream'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}


class MachineFamilyDataStreamPairCorrJSONAPISerializer(JSONAPIModelSerializer):
    machine_family_data = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    machine_data_stream = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    other_machine_data_stream = \
        ResourceRelatedField(
            read_only=True,
            many=False)

    included_serializers = related_serializers = \
        dict(# machine_family=MachineFamilyJSONAPISerializer,
             machine_data_stream=MachineDataStreamJSONAPISerializer,
             other_machine_data_stream=MachineDataStreamJSONAPISerializer)

    class Meta:
        model = MachineFamilyDataStreamPairCorr

        fields = \
            MACHINE_FAMILY_DATA_STREAM_PAIR_CORR_API_FIELD_NAMES + \
            ('url',)

        meta_fields = ()

    class JSONAPIMeta:
        resource_name = MachineFamilyDataStreamPairCorr.JSONAPIMeta.resource_name

        included_resources = \
            'machine_family_data', \
            'machine_data_stream', \
            'other_machine_data_stream'

    def get_root_meta(self, resource, many):
        return dict(n=len(resource)) \
            if many \
          else {}
