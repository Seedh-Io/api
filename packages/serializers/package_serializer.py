from rest_framework import serializers

from backend_api.fields.base_serializer_fields import BaseSerializer
from packages.models import PackagesModel


class PackageConfigurationSerializer(serializers.Serializer):
    default_credits = serializers.JSONField(allow_null=False, default=0)
    credit_multiplier = serializers.FloatField(allow_null=False, default=1.0, min_value=1.0)
    duration_in_seconds = serializers.IntegerField(allow_null=False)


class PackageSerializer(serializers.ModelSerializer):
    configuration = BaseSerializer.get_serializer("package_configuration", PackageConfigurationSerializer)

    class Meta:
        model = PackagesModel
        fields = '__all__'
