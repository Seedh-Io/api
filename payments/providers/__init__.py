from abc import ABC, abstractmethod
from typing import Tuple

from backend_api.helpers.custom_exception_helper import CustomApiException
from payments.dto import PaymentProviderResponseDTO
from payments.enum import PaymentStatusEnum
from payments.enum import PaymentProvidersEnum, SupportedPaymentCurrenciesEnum


class BaseProvider(ABC):

    @abstractmethod
    def create_payment_order(self, amount_in_cents: int, order_reference_id: str, payment_id:str,
                             currency: SupportedPaymentCurrenciesEnum = SupportedPaymentCurrenciesEnum.INR) -> PaymentProviderResponseDTO: pass

    @abstractmethod
    def verify_payment(self, pg_id: str, payment_id: str, signature: str, success: bool) -> PaymentStatusEnum: pass

    @abstractmethod
    def get_provider(self) -> PaymentProvidersEnum: pass

    def verify(self, pg_id: str, payment_id: str, signature: str, success: bool) -> PaymentStatusEnum:
        payment_status = self.verify_payment(pg_id, payment_id, signature, success)
        from payments.models import PaymentsModel
        payment_obj = PaymentsModel.objects.get_payment_by_pg(payment_status, pg_id)
        payment_obj.status = payment_status.val
        payment_obj.save()
        return payment_status

    @staticmethod
    def provider(provider=None) -> PaymentProvidersEnum:
        if provider is not None and type(provider) != PaymentProvidersEnum:
            raise CustomApiException("Invalid Provider Type")
        return provider or PaymentProvidersEnum.RAZORPAY

    @staticmethod
    @abstractmethod
    def extract_payment_id_signature_from_response(response: dict) -> Tuple[str, str]: pass
