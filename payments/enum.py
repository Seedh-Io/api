from backend_api.helpers.enum_helper import BaseEnum
from payments.providers.razorpay import RazorpayProvider


class SupportedPaymentCurrenciesEnum(BaseEnum):
    INR = ("INR", "INR")


class PaymentProvidersEnum(BaseEnum):
    RAZORPAY = ("Razorpay", (1, RazorpayProvider))

    @property
    def val(self):
        return self.data[0]

    @property
    def obj(self):
        return self.data[1]


class PaymentStatusEnum(BaseEnum):
    INITIATED = ("Initiated", 10)
    PROCESSING = ("Processing", 20)
    SUCCESS = ("Success", 30)
    REFUNDED = ("Refunded", 40)
    FAILED = ("Failed", 50)
    FLAGGED = ("Flagged", 60)
