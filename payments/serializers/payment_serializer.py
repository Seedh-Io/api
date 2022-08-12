from rest_framework import serializers

from payments.enum import PaymentProvidersEnum, SupportedPaymentCurrenciesEnum
from payments.models import PaymentsModel


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentsModel
        fields = "__all__"


class InitiatePaymentSerializer(serializers.Serializer):
    # Write only fields
    order_id = serializers.UUIDField(write_only=True, required=True, allow_null=False)
    amount_in_cents = serializers.IntegerField(write_only=True, required=True, allow_null=False)
    provider = serializers.ChoiceField(choices=PaymentProvidersEnum.get_choices(), allow_null=False, allow_blank=False,
                                       required=True)
    currency = serializers.ChoiceField(choices=SupportedPaymentCurrenciesEnum.get_choices(), allow_null=False,
                                       allow_blank=False, required=True)

    # Read only fields
    pg_response = serializers.JSONField(read_only=True)
    payment = PaymentSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from orders.models import OrderModel
        self.order: OrderModel | None = None

    def validate_order_id(self, order_id):
        from payments.service_utils import OrderUtils
        order = OrderUtils(context=self.context).get_order_by_id(order_id)
        self.order = order
        return order_id

    def create(self, validated_data):
        provider = PaymentProvidersEnum.search_by_value(validated_data["provider"])
        if not self.order:
            raise serializers.ValidationError("Order not found")
        currency = SupportedPaymentCurrenciesEnum.search_by_value(validated_data["currency"])
        payment_obj = PaymentSerializer(data=validated_data, context=self.context)
        payment_obj.is_valid(raise_exception=True)
        payment_obj.save()
        gateway_response = provider.obj.create_payment_order(validated_data["amount_in_cents"], self.order.order_id,
                                                             payment_obj.instance.pk, currency,)

        # Updating Gateway id
        payment_obj = PaymentSerializer(instance=payment_obj.instance, data={
            "provider_id": gateway_response.provider_id
        }, context=self.context, partial=True)
        payment_obj.is_valid(raise_exception=True)
        payment_obj.save()

        validated_data["payment"] = payment_obj.instance
        validated_data["pg_response"] = gateway_response.to_dict()
        return validated_data

    def update(self, instance, validated_data):
        from backend_api.helpers.custom_exception_helper import CustomApiException
        raise CustomApiException("Method not allowed")
