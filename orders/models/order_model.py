import logging
import random

from django.db import models
from django_fsm import transition, FSMIntegerField

from backend_api.fields.base_model_fields import BaseModelFields, BaseModelManager
from orders.apps import OrdersConfig as AppConfig
from orders.enum import OrderStateEnum, OrderTypeEnum


class OrderManager(BaseModelManager):

    @staticmethod
    def get_order_id(order_type: OrderTypeEnum):
        import string
        return order_type.initial + "_" + ''.join(random.choices(string.ascii_lowercase, k=8))


class OrderModel(BaseModelFields, models.Model):
    user_id = models.UUIDField(null=False, blank=False)
    business_id = models.UUIDField(null=False, blank=False)
    order_id = models.CharField(null=False, blank=False, max_length=15, unique=True)
    list_price_in_cents = models.BigIntegerField(null=False, blank=False)
    offer_discount_in_cents = models.BigIntegerField(null=False, blank=False)
    coupon_discount_in_cents = models.BigIntegerField(null=False, blank=False, default=0)
    sale_price_in_cents = models.BigIntegerField(null=False, blank=False)
    status = FSMIntegerField(default=OrderStateEnum.CREATED.val, null=False, blank=False,
                             choices=OrderStateEnum.get_choices())
    package_id = models.UUIDField(null=True, blank=False)
    order_type = models.IntegerField(null=False, blank=False, choices=OrderTypeEnum.get_choices())

    objects = OrderManager()

    class Meta:
        managed = True
        db_table = str(AppConfig.name)

    @transition(field=status, source=OrderStateEnum.CREATED.val, target=OrderStateEnum.PROCESSING.val)
    def mark_as_processing(self):
        logging.info("mark_order_as_processing", extra={"order_id": self.pk})

    @transition(field=status, source=OrderStateEnum.PROCESSING.val, target=OrderStateEnum.ISSUE.val)
    def mark_as_issue(self, msg=""):
        logging.info("mark_order_as_processing", extra={"order_id": self.pk, "msg": msg})

    @transition(field=status,
                source=[OrderStateEnum.PROCESSING.val, OrderStateEnum.ISSUE.val, OrderStateEnum.FAILED.val],
                target=OrderStateEnum.COMPLETED.val)
    def mark_as_completed(self):
        logging.info("mark_order_as_completed", extra={"order_id": self.pk, })


    @transition(field=status, source=OrderStateEnum.COMPLETED.val, target=OrderStateEnum.)
