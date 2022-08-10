from django.db import models

from backend_api.fields.base_model_fields import BaseModelFields
from payments.enum import RazorpayStatusEnum


class RazorpayModel(BaseModelFields, models.Model):

    pg_order_id = models.CharField(null=True, blank=False, max_length=20, default=None)
    user_order_id = models.CharField(null=False, blank=False, max_length=20)
    request_response = models.JSONField(null=False, blank=False, default=dict)
    status = models.IntegerField(null=True, blank=False, choices=RazorpayStatusEnum.get_choices())
    payment_id = models.CharField(null=True, blank=False, max_length=40)
    signature = models.CharField(null=True, blank=False, max_length=64)
    amount_in_cents = models.BigIntegerField(null=False, blank=False)


