import logging

from rest_framework import serializers

from backend_api.constants.messages import Messages
from payments.enum import PaymentProvidersEnum, PaymentStatusEnum
from payments.service_utils import OrderUtils
from payments.models import PaymentsModel


class UserPaymentVerificationSerializer(serializers.Serializer):
    success = serializers.BooleanField(required=True, allow_null=False, write_only=True)
    response = serializers.JSONField(required=True, allow_null=False, write_only=True)

    payment_verified = serializers.BooleanField(read_only=True)

    def update(self, instance: PaymentsModel, validated_data):
        if instance.status not in [PaymentStatusEnum.INITIATED.val, PaymentStatusEnum.PROCESSING.val]:
            raise serializers.ValidationError(Messages.payment_already_verified())
        provider = PaymentProvidersEnum.search_by_value(instance.provider)
        provider_obj = provider.obj
        success = validated_data["success"]
        pg_response = validated_data["response"]
        payment_verified = False
        if success:
            try:
                logging.info("payment_verification_initiated", extra={"payment_id": instance.pk, "success": success})
                _, _ = provider_obj.extract_payment_id_signature_from_response(pg_response)
                payment_status = provider.obj.verify(instance, validated_data['success'], pg_response)
            except Exception as e:
                logging.error("payment_verification_failed",
                              extra={"error_msg": str(e), "payment_id": instance.pk, "success": success})
                payment_status = PaymentStatusEnum.FLAGGED
        else:
            payment_status = PaymentStatusEnum.FAILED
        try:
            logging.info("order_update_initiated", extra={"payment_id": instance.pk, "success": success})
            OrderUtils(context=self.context).update_order_state(instance.order_id, payment_status)
            payment_verified = True
        except Exception as e:
            logging.error("order_update_failed",
                          extra={"payment_id": instance.pk, "success": success, "error_message": str(e)})

        return {"payment_verified": payment_verified}

    def create(self, validated_data):
        from backend_api.helpers.custom_exception_helper import CustomApiException
        raise CustomApiException("Method not allowed")
