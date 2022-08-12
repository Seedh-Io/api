from abc import abstractmethod

from rest_framework import serializers

from business.models import BusinessModel
from orders.enum import OrderTypeEnum
from orders.models import OrderModel
from orders.service_utils import PaymentUtils
from payments.enum import PaymentProvidersEnum, SupportedPaymentCurrenciesEnum
from users.models import UserModel
from payments.enum import PaymentStatusEnum


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
    payment_id = serializers.UUIDField(read_only=True)
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
    def get_order_type() -> OrderTypeEnum:
        pass

    @staticmethod
    @abstractmethod
    def get_collection_amount(order: OrderModel):
        pass

    def get_base_order_data(self) -> dict:
        return {
            "business_id": self.business.pk,
            "user_id": self.user.pk,
            "order_type": self.get_order_type().val,
        }

    def set_order_data(self, order_data):
        self.order_data = order_data

    def create(self, validated_data):
        order = self.create_order()
        amount_in_cents = self.get_collection_amount(order)
        try:
            payment_obj = PaymentUtils(context=self.context).initiate_payment(order.pk, amount_in_cents)
            order.mark_as_processing()
            order.save()
        except Exception as e:
            order.mark_as_issue()
            order.save()
            raise e
        validated_data["order"] = order
        validated_data['payment_gateway_id'] = payment_obj.payment.provider
        validated_data['payment_gateway_order_id'] = payment_obj.pg_response.provider_order_id
        validated_data['payment_gateway_amount_in_cents'] = payment_obj.pg_response.amount_in_cents
        validated_data['payment_gateway_currency'] = payment_obj.payment.currency
        validated_data["payment_id"] = payment_obj.payment.id
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
        package = PackagesUtils().get_package_by_id(attrs['package_id'])
        self.set_order_data({
            "package_id": package.pk,
            "list_price_in_cents": package.list_price_in_cents,
            "sale_price_in_cents": package.selling_price_in_cents,
            "offer_discount_in_cents": package.list_price_in_cents - package.selling_price_in_cents,
            **self.get_base_order_data()
        })
        return attrs

    @staticmethod
    def get_collection_amount(order: OrderModel):
        return order.sale_price_in_cents


class RechargeOrderSerializer(BaseOrderSerializerMixin):
    recharge_amount = serializers.IntegerField(allow_null=False, min_value=1)

    @staticmethod
    def get_order_type() -> OrderTypeEnum:
        return OrderTypeEnum.RECHARGE

    @staticmethod
    def get_collection_amount(order: OrderModel):
        return order.list_price_in_cents

    def validate(self, attrs):
        recharge_amount = attrs['recharge_amount']

        self.set_order_data({
            "list_price_in_cents": recharge_amount,
            "sale_price_in_cents": recharge_amount,
            "offer_discount_in_cents": 0,
        })
        return attrs


class UpdateOrderStatusSerializer(serializers.Serializer):
    payment_status = serializers.ChoiceField(choices=PaymentStatusEnum.get_choices(), allow_null=False, required=True,
                                             allow_blank=False, write_only=True)
    order = OrderSerializer(read_only=True)

    def update(self, instance: OrderModel, validated_data):
        payment_state = PaymentStatusEnum.search_by_value(validated_data['payment_status'])
        match payment_state:
            case PaymentStatusEnum.FAILED:
                instance.mark_as_failed()
            case PaymentStatusEnum.PROCESSING:
                pass
            case PaymentStatusEnum.REFUNDED:
                instance.refund_order()
            case PaymentStatusEnum.SUCCESS:
                instance.mark_as_completed(self.context)
            case PaymentStatusEnum.FLAGGED:
                instance.mark_as_issue()
            case PaymentStatusEnum.INITIATED:
                pass
        instance.save()
        return {"order": instance}

    def create(self, validated_data):
        from backend_api.helpers.custom_exception_helper import CustomApiException
        raise CustomApiException("Method not allowed")
