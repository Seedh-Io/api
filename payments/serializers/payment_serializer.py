from rest_framework import serializers

from payments.models import PaymentsModel
from payments.enum import PaymentProvidersEnum, SupportedPaymentCurrenciesEnum
from payments.service_utils import OrderServiceUtils
from payments.providers import BaseProvider


class PaymentSerializer(serializers.ModelSerializer):
    provider_order_id = serializers.CharField(read_only=True)
    order = None

    class Meta:
        model = PaymentsModel
        fields = "__all__"
        read_only_fields = ('provider_id', 'status')

    def validate(self, attrs):
        order_id = self.instance.order_id if self.instance else attrs["order_id"]
        self.order = OrderServiceUtils.get_order_by_id(order_id)
        return attrs

    def create(self, validated_data):
        provider = PaymentProvidersEnum.search_by_value(validated_data["provider_id"])
        currency = SupportedPaymentCurrenciesEnum.search_by_value(validated_data["currency"])
        data = {
            "amount_in_cents": validated_data["amount_in_cents"],
            "currency": currency.val,
            "order_reference_id": self.order.order_id
        }
        provider_obj: BaseProvider = provider.obj(**data)
        provider_data_obj = provider_obj.create_payment_order()
        validated_data["provider_order_id"] = provider_data_obj.provider_order_id
        return super(PaymentSerializer, self).create(validated_data)
