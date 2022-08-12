from backend_api.helpers.service_helper import BaseService
from payments.dto import CreatePaymentResponseDTO

from payments.enum import PaymentProvidersEnum, SupportedPaymentCurrenciesEnum
from payments.serializers.payment_serializer import InitiatePaymentSerializer


class PaymentService(BaseService):

    def initiate_payment(self, order_id: str, amount_in_cents: int, provider: PaymentProvidersEnum,
                         currency: SupportedPaymentCurrenciesEnum) -> CreatePaymentResponseDTO:
        payment_obj = InitiatePaymentSerializer(context=self.context, data={
            "order_id": order_id,
            "amount_in_cents": amount_in_cents,
            "provider": provider.val,
            "currency": currency.val
        })
        payment_obj.is_valid(raise_exception=True)
        payment_obj.save()
        return CreatePaymentResponseDTO(**payment_obj.data)
