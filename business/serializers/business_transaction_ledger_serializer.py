from rest_framework import serializers

from business.models import BusinessTransactionLedgerModel
from business.enum import BusinessReferenceTypeEnum
from business.service_utils import OrderUtils


class AddCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessTransactionLedgerModel
        fields = ('credits', 'reference_type', 'reference_id', 'expiry_date_time', 'business')

    def validate_reference_id(self, reference_id):
        reference_type = BusinessReferenceTypeEnum.search_by_value(self.initial_data['reference_type'])
        match reference_type:
            case BusinessReferenceTypeEnum.ORDER:
                OrderUtils(context=self.context).get_order_by_id(reference_id)
            case _:
                raise serializers.ValidationError("Not supported reference")
        return reference_id

    def validate(self, attrs):
        attrs['is_credit'] = True
        return attrs

