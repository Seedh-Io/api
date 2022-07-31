from rest_framework import serializers

from business.models import BusinessModel


class CreateBusinessSerializers(serializers.ModelSerializer):

    class Meta:
        model = BusinessModel
        fields = ('name', 'business_owner')
