from rest_framework import serializers

from backend_api.helpers.datetime_helper import DateTimeHelper
from business.models import BusinessModel


class CreateBusinessSerializers(serializers.ModelSerializer):
    class Meta:
        model = BusinessModel
        fields = ('name', 'business_owner')


class ActivatePackageForBusiness(serializers.ModelSerializer):
    active_package_id = serializers.UUIDField(allow_null=False, required=True, write_only=True)
    active_package_expiry_date_time = serializers.DateTimeField(allow_null=False, required=True, write_only=True)

    class Meta:
        model = BusinessModel
        fields = ('active_package_expiry_date_time', 'active_package_id')

    def validate_active_package_expiry_date_time(self, active_package_expiry_date_time):
        if active_package_expiry_date_time < DateTimeHelper.get_current_datetime():
            raise serializers.ValidationError("Expiry time cannot be less than current time")
        return active_package_expiry_date_time
