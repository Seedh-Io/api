import logging
import random

from django.db import models
from django_fsm import transition, FSMIntegerField

from backend_api.fields.base_model_fields import BaseModelFields, BaseModelManager
from backend_api.helpers.datetime_helper import DateTimeHelper
from orders.apps import OrdersConfig as AppConfig
from orders.enum import OrderStateEnum, OrderTypeEnum
from users.models import UserModel


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

    @transition(field=status, source=OrderStateEnum.CREATED.val, target=OrderStateEnum.ISSUE.val)
    def mark_as_issue(self, msg=""):
        logging.info("mark_order_as_processing", extra={"order_id": self.pk, "response": msg})

    @transition(field=status,
                source=[OrderStateEnum.PROCESSING.val, OrderStateEnum.ISSUE.val, OrderStateEnum.FAILED.val],
                target=OrderStateEnum.COMPLETED.val, on_error=OrderStateEnum.FAILED.val)
    def mark_as_completed(self, context):
        logging.info("mark_order_as_completed", extra={"order_id": self.pk, })

        def add_credit_for_business(credit):
            pass

        from orders.service_utils import PackagesUtils
        package = PackagesUtils().get_package_by_id(self.package_id) if self.package_id else None
        if self.order_type == OrderTypeEnum.PACKAGE.val:
            expiry_time = DateTimeHelper.add_seconds_to_date(package.duration_in_seconds)
            if package.default_credits > 0:
                add_credit_for_business(package.default_credits)
            from orders.service_utils import BusinessUtils
            BusinessUtils(context=context).active_package_for_business(self.business_id, self.package_id, expiry_time)
        else:
            credit = package.get_credits_when_recharge(
                self.list_price_in_cents) if package else self.list_price_in_cents
            add_credit_for_business(credit)

    @transition(field=status, source=OrderStateEnum.COMPLETED.val, target=OrderStateEnum.REFUNDED.val)
    def refund_order(self, user: UserModel):
        # todo implement code for refund
        logging.info("refund_order", extra={"order_id": self.pk, "user": user.pk})

    @transition(field=status, source=OrderStateEnum.PROCESSING.val, target=OrderStateEnum.FAILED.val)
    def mark_as_failed(self):
        logging.info("order_failed", extra={"order_id": self.pk})
