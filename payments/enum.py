from backend_api.helpers.enum_helper import BaseEnum


class SupportedPaymentCurrenciesEnum(BaseEnum):
    INR = ("INR", "INR")


class PaymentProvidersEnum(BaseEnum):
    # Class Reff is given to avoid circular import issue
    RAZORPAY = ("Razorpay", (1, 'payments.providers.razorpay.Razorpay'))

    @property
    def val(self) -> int:
        return self.data[0]

    @property
    def obj(self):
        from pydoc import locate
        from payments.providers import BaseProvider
        data: BaseProvider = locate(self.data[1])()
        return data


class PaymentStatusEnum(BaseEnum):
    INITIATED = ("Initiated", 10)
    PROCESSING = ("Processing", 20)
    SUCCESS = ("Success", 30)
    REFUNDED = ("Refunded", 40)
    FAILED = ("Failed", 50)
    FLAGGED = ("Flagged", 60)


class RazorpayStatusEnum(BaseEnum):
    CREATED = ("Created", (1, "created", PaymentStatusEnum.INITIATED))
    ATTEMPTED = ("Attempted", (2, "attempted", PaymentStatusEnum.PROCESSING))
    FAILED = ("Failed", (3, "failed", PaymentStatusEnum.FAILED))
    PAID = ("Paid", (4, "paid", PaymentStatusEnum.SUCCESS))
    REFUNDED = ("Refunded", (5, "refunded", PaymentStatusEnum.REFUNDED))
    VERIFICATION_FAILED = ("Verification Failed", (6, "verification_failed", PaymentStatusEnum.FLAGGED))

    @property
    def val(self):
        return self.data[0]

    @property
    def razorpay_status(self):
        return self.data[1]

    @classmethod
    def search_by_razorpay_status(cls, value) -> 'RazorpayStatusEnum':
        for key in cls:
            if key.data[1] == value:
                return key

    @property
    def payment_state(self) -> PaymentStatusEnum:
        return self.data[2]
