from backend_api.helpers.service_helper import BaseService
from business.service import BusinessService
from orders.repository import OrdersRepository
from orders.service import OrderService
from business.repository import BusinessRepository
from payments.enum import PaymentStatusEnum


class OrderUtils(BaseService):

    def __init__(self, *args, **kwargs):
        super(OrderUtils, self).__init__(*args, **kwargs)
        self.order_service = OrderService(context=self.context)
        self.order_repository = OrdersRepository(context=self.context)

    def get_order_by_id(self, order_id):
        return self.order_repository.get_order_by_id(order_id)

    def update_order_state(self, order_id, payment_state: PaymentStatusEnum):
        return self.order_service.update_order_status(order_id, payment_state.val)


class BusinessUtils(BaseService):

    @staticmethod
    def get_business_by_id(business_id):
        return BusinessRepository.get_business_by_id(business_id)

    def activate_package_for_business(self, business_id, package_id, expiry_date_time):
        return BusinessService(context=self.context).activate_package_for_business(business_id, package_id,
                                                                                   expiry_date_time)
