from backend_api.helpers.service_helper import BaseService
from business.service import BusinessService
from orders.repository import OrdersRepository
from business.repository import BusinessRepository


class OrderServiceUtils(BaseService):

    @staticmethod
    def get_order_by_id(order_id):
        return OrdersRepository.get_order_by_id(order_id)


class BusinessUtils(BaseService):

    @staticmethod
    def get_business_by_id(business_id):
        return BusinessRepository.get_business_by_id(business_id)

    def activate_package_for_business(self, business_id, package_id, expiry_date_time):
        return BusinessService(context=self.context).activate_package_for_business(business_id, package_id,
                                                                                   expiry_date_time)
