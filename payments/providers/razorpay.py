import logging
from typing import Tuple

import razorpay

from backend_api.constants.messages import Messages
from backend_api.helpers.custom_exception_helper import PGOrderCreationFailed, PGInvalidVerificationResponse
from payments.dto import PaymentProviderResponseDTO
from payments.providers import BaseProvider

from payments.models.razorpay_models import RazorpayModel
from payments.enum import RazorpayStatusEnum, PaymentProvidersEnum, SupportedPaymentCurrenciesEnum, \
    PGStateEnumBase


class Razorpay(BaseProvider):

    def _update_status(self, pg_id: str, status: PGStateEnumBase):
        rzp = RazorpayModel.objects.get(id=pg_id)
        rzp.status = status.val
        rzp.save()
        return rzp

    @staticmethod
    def extract_payment_id_signature_from_response(response: dict) -> Tuple[str, str]:
        payment_id = response.get('razorpay_payment_id')
        signature = response.get('razorpay_signature')
        if not payment_id or not signature:
            raise PGInvalidVerificationResponse("Invalid Payment Response")
        return payment_id, signature

    def get_provider(self) -> PaymentProvidersEnum:
        return PaymentProvidersEnum.RAZORPAY

    def __init__(self, *args, **kwargs):
        super(Razorpay, self).__init__(*args, **kwargs)
        self.client = razorpay.Client(auth=("rzp_test_VWCiOk5dOLy47F", "sz0jeUOYrfuwAEWgw1YKeX0x"))

    def _verify_payment(self, payment_id: str, success: bool, response: dict) -> PGStateEnumBase:
        logging.info("rzp_verification_initiated", extra={
            "payment_id": payment_id,
            "response": response,
            "success": success
        })
        status = None
        if success:
            logging.info("rzp_payment_success_initiated")
            try:
                self.client.utility.verify_payment_signature(response)
                status = RazorpayStatusEnum.PAID
            except Exception as e:
                logging.error("rzp_verification_failed", extra={"exception_raised": e})
                status = RazorpayStatusEnum.VERIFICATION_FAILED
        else:
            logging.info("rzp_payment_success_failed")
            status = RazorpayStatusEnum.FAILED
        return status

    def create_payment_order(self, amount_in_cents: int, order_reference_id: str, payment_id: str,
                             currency: SupportedPaymentCurrenciesEnum = SupportedPaymentCurrenciesEnum.INR) -> PaymentProviderResponseDTO | None:
        data = {
            "amount": amount_in_cents,
            "currency": currency.val,
            "receipt": order_reference_id,
        }
        logging.info("rzp_payment_initiated", extra={**data})
        rzp_obj = RazorpayModel.objects.create(user_order_id=order_reference_id, amount_in_cents=amount_in_cents,
                                               payment_id=payment_id)
        try:
            response = self.client.order.create(data=data)
            logging.info("rzp_order_create_success", extra={"response": response, "request_data": data})
            pg_order_id = response["id"]
            status = RazorpayStatusEnum.search_by_pg_state(response["status"]).val
            response_amount = response["amount_due"]
            rzp_obj.status = status
            rzp_obj.pg_order_id = pg_order_id
            rzp_obj.save()
            return PaymentProviderResponseDTO(amount_in_cents=response_amount, provider_order_id=pg_order_id,
                                              provider_id=rzp_obj.pk)
        except Exception as e:
            logging.error("rzp_order_create_failed", extra={"request_data": data, "error": e})
            raise PGOrderCreationFailed(Messages.error_in_initiating_payment())
