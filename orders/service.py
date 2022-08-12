from backend_api.helpers.service_helper import BaseService
from orders.models import OrderModel
from orders.serializers.order_serializer import UpdateOrderStatusSerializer


class OrderService(BaseService):

    def update_order_status(self, order_id, payment_status: int):
        order = OrderModel.objects.get(id=order_id)
        obj = UpdateOrderStatusSerializer(instance=order, data={
            "payment_status": payment_status
        }, context=self.context)
        obj.is_valid(raise_exception=True)
        obj.save()
        return obj.data
