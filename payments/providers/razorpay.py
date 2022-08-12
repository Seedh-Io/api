import logging
from typing import Tuple

import razorpay

from backend_api.constants.messages import Messages
from backend_api.helpers.custom_exception_helper import PGOrderCreationFailed, PGInvalidVerificationResponse
from payments.dto import PaymentProviderResponseDTO
from payments.providers import BaseProvider

from payments.models.razorpay_models import RazorpayModel
from payments.enum import RazorpayStatusEnum, PaymentStatusEnum, PaymentProvidersEnum, SupportedPaymentCurrenciesEnum


class Razorpay(BaseProvider):

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

    def verify_payment(self, pg_id: str, payment_id: str, signature: str, success: bool) -> PaymentStatusEnum:
        logging.info("rzp_verification_initiated", extra={
            "pg_id": pg_id,
            "payment_id": payment_id,
            "signature": signature,
            "success": success
        })
        raz_obj = RazorpayModel.objects.get(id=pg_id)
        status = None
        if success:
            logging.info("rzp_payment_success_initiated")
            try:
                self.client.utility.verify_payment_signature({
                    'razorpay_order_id': raz_obj.pg_order_id,
                    'razorpay_payment_id': payment_id,
                    'signature': signature
                })
                status = RazorpayStatusEnum.CREATED
            except Exception as e:
                logging.error("rzp_verification_failed", extra={"exception_raised": e})
                status = RazorpayStatusEnum.VERIFICATION_FAILED
        else:
            logging.info("rzp_payment_success_failed")
            status = RazorpayStatusEnum.FAILED
        payment_status = status.payment_state
        return payment_status

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
            status = RazorpayStatusEnum.search_by_razorpay_status(response["status"]).val
            response_amount = response["amount_due"]
            rzp_obj.status = status
            rzp_obj.pg_order_id = pg_order_id
            rzp_obj.save()
            return PaymentProviderResponseDTO(amount_in_cents=response_amount, provider_order_id=pg_order_id,
                                              provider_id=rzp_obj.pk)
        except Exception as e:
            logging.error("rzp_order_create_failed", extra={"request_data": data, "error": e})
            raise PGOrderCreationFailed(Messages.error_in_initiating_payment())
