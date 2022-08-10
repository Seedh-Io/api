from abc import ABC, abstractmethod

from rest_framework import serializers

from business.models import BusinessModel
from orders.enum import OrderTypeEnum
from orders.models import OrderModel
from payments.enum import PaymentProvidersEnum, SupportedPaymentCurrenciesEnum
from users.models import UserModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"
        read_only_fields = ('order_id',)

    def validate_order_type(self, order_type):
        package_id = self.initial_data['package_id']
        from orders.enum import OrderTypeEnum
        if package_id is None and order_type == OrderTypeEnum.PACKAGE.val:
            raise serializers.ValidationError({"package_id": "Package id is required"})
        if order_type == OrderTypeEnum.RECHARGE.val and package_id is not None:
            raise serializers.ValidationError({"package_id": "Package Id is not required"})
        return order_type

    def validate(self, attrs):
        from orders.enum import OrderTypeEnum
        attrs['order_id'] = OrderModel.objects.get_order_id(OrderTypeEnum.search_by_value(attrs['order_type']))
        return attrs


class BaseOrderSerializerMixin(serializers.Serializer):
    payment_gateway_id = serializers.ChoiceField(choices=PaymentProvidersEnum.get_choices(),
                                                 default=PaymentProvidersEnum.RAZORPAY.val)
    payment_gateway_order_id = serializers.CharField(read_only=True)
    payment_gateway_amount_in_cents = serializers.IntegerField(read_only=True)
    payment_gateway_currency = serializers.ChoiceField(choices=SupportedPaymentCurrenciesEnum.get_choices(),
                                                       read_only=True)
    order = OrderSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        self.order_data: dict | None = None
        super(BaseOrderSerializerMixin, self).__init__(*args, **kwargs)

    @staticmethod
    def generate_payment(order, payment_gateway, amount_in_cents):
        pass

    def create_order(self) -> OrderModel:
        order = OrderSerializer(data=self.order_data)
        order.is_valid(raise_exception=True)
        order.save()
        return order.instance

    @property
    def business(self) -> BusinessModel:
        return self.context['request'].business

    @property
    def user(self) -> UserModel:
        return self.context['request'].user

    @staticmethod
    @abstractmethod
    def get_order_type() -> OrderTypeEnum: pass

    def get_base_order_data(self) -> dict:
        return {
            "business_id": self.business.pk,
            "user_id": self.user.pk,
            "order_type": self.get_order_type().val,
        }

    def set_order_data(self, order_data):
        self.order_data = order_data

    def create(self, validated_data):
        from payments.providers import BaseProvider
        order = self.create_order()
        amount_in_cents = order.sale_price_in_cents
        payment_obj = BaseProvider.provider().obj.create_payment_order(amount_in_cents, order.order_id)
        validated_data["order"] = order
        validated_data['payment_gateway_id'] = payment_obj.provider_id
        validated_data['payment_gateway_order_id'] = payment_obj.provider_order_id
        validated_data['payment_gateway_amount_in_cents'] = amount_in_cents
        validated_data['payment_gateway_currency'] = SupportedPaymentCurrenciesEnum.INR.val
        return validated_data

    def update(self, instance, validated_data):
        from backend_api.helpers.custom_exception_helper import CustomApiException
        raise CustomApiException("Method not allowed")


class PackageOrderSerializer(BaseOrderSerializerMixin):
    package_id = serializers.UUIDField(allow_null=False, write_only=True)

    @staticmethod
    def get_order_type() -> OrderTypeEnum:
        return OrderTypeEnum.PACKAGE

    def validate(self, attrs):
        from orders.service_utils import PackagesUtils
        package = PackagesUtils.get_package_by_id(attrs['package_id'])
        self.set_order_data({
            "package_id": package.pk,
            "list_price_in_cents": package.list_price_in_cents,
            "sale_price_in_cents": package.selling_price_in_cents,
            "offer_discount_in_cents": package.list_price_in_cents - package.selling_price_in_cents,
            **self.get_base_order_data()
        })
        return attrs


class RechargeOrderSerializer(BaseOrderSerializerMixin):
    recharge_amount = serializers.IntegerField(allow_null=False, min_value=1)

    @staticmethod
    def get_order_type() -> OrderTypeEnum:
        return OrderTypeEnum.RECHARGE

    def validate(self, attrs):
        recharge_amount = attrs['recharge_amount']

        self.set_order_data({
            "list_price_in_cents": recharge_amount,
            "sale_price_in_cents": recharge_amount,
            "offer_discount_in_cents": 0,
        })
        return attrs
