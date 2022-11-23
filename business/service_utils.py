from backend_api.helpers.service_helper import BaseService

from orders.repository import OrdersRepository


class OrderUtils(BaseService):

    def __init__(self, *args, **kwargs):
        super(OrderUtils, self).__init__(*args, **kwargs)
        self.order_repository = OrdersRepository(context=self.context)

    def get_order_by_id(self, order_id):
        return self.order_repository.get_order_by_id(order_id)
