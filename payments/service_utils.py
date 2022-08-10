from orders.repository import OrdersRepository


class OrderServiceUtils:

    @staticmethod
    def get_order_by_id(order_id):
        return OrdersRepository.get_order_by_id(order_id)
