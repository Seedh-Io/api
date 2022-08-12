from backend_api.helpers.service_helper import BaseService

from business.service import BusinessService
from packages.repository import PackagesRepository
from payments.enum import SupportedPaymentCurrenciesEnum, PaymentProvidersEnum
from payments.service import PaymentService


class PackagesUtils(BaseService):

    def __init__(self, *args, **kwargs):
        super(PackagesUtils, self).__init__(*args, **kwargs)
        self.package_repository = PackagesRepository(context=self.context)

    def get_package_by_id(self, package_id):
        return self.package_repository.get_package_by_id(package_id)


class BusinessUtils(BaseService):

    def __init__(self, *args, **kwargs):
        super(BusinessUtils, self).__init__(*args, **kwargs)
        self.business_service = BusinessService(context=self.context)

    def active_package_for_business(self, business_id, package_id, package_expiry_date_time):
        return self.business_service.activate_package_for_business(business_id, package_id, package_expiry_date_time)


class PaymentUtils(BaseService):

    def __init__(self, *args, **kwargs):
        super(PaymentUtils, self).__init__(*args, **kwargs)
        self.payment_service = PaymentService(context=self.context)

    def initiate_payment(self, order_id: str, amount_in_cents: int,
                         provider: PaymentProvidersEnum = PaymentProvidersEnum.RAZORPAY,
                         currency: SupportedPaymentCurrenciesEnum = SupportedPaymentCurrenciesEnum.INR):
        return self.payment_service.initiate_payment(order_id, amount_in_cents, provider, currency)
