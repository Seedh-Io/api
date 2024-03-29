import logging

from backend_api.helpers.service_helper import BaseService
from orders.models import OrderModel
from rest_framework.exceptions import NotFound


class OrdersRepository(BaseService):

    @staticmethod
    def get_order_by_id(order_id):
        try:
            return OrderModel.objects.get(id=order_id)
        except Exception as e:
            logging.info("order_not_found", extra={"order_id": order_id, "exception": str(e)})
            raise NotFound("Order Not found")
