import logging
from abc import ABC, abstractmethod
from typing import Tuple

from backend_api.helpers.custom_exception_helper import CustomApiException
from payments.dto import PaymentProviderResponseDTO
from payments.enum import PaymentStatusEnum, PGStateEnumBase
from payments.enum import PaymentProvidersEnum, SupportedPaymentCurrenciesEnum
from payments.models import PaymentsModel


class BaseProvider(ABC):

    @abstractmethod
    def create_payment_order(self, amount_in_cents: int, order_reference_id: str, payment_id: str,
                             currency: SupportedPaymentCurrenciesEnum = SupportedPaymentCurrenciesEnum.INR) -> PaymentProviderResponseDTO: pass

    @abstractmethod
    def _verify_payment(self, payment_id: str, success: bool, response: dict) -> PGStateEnumBase: pass

    @abstractmethod
    def _update_status(self, pg_id: str, status: PGStateEnumBase): pass

    @abstractmethod
    def get_provider(self) -> PaymentProvidersEnum: pass

    def verify(self, payment: PaymentsModel, success: bool, response: dict) -> PaymentStatusEnum:
        logging.info("payment_verification_initiated",
                     extra={"payment": payment.pk, "success": success, "response": response})
        pg_status = self._verify_payment(payment.pk, success, response)
        payment_state = pg_status.payment_state
        _ = self._update_status(payment.provider_id, pg_status)
        return payment_state

    @staticmethod
    def provider(provider=None) -> PaymentProvidersEnum:
        if provider is not None and type(provider) != PaymentProvidersEnum:
            raise CustomApiException("Invalid Provider Type")
        return provider or PaymentProvidersEnum.RAZORPAY

    @staticmethod
    @abstractmethod
    def extract_payment_id_signature_from_response(response: dict) -> Tuple[str, str]: pass
