from orders.models import OrderModel


class OrdersRepository:

    @staticmethod
    def get_order_by_id(order_id):
        return OrderModel.objects.get(id=order_id)
