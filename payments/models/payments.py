from django.db import models

from backend_api.fields.base_model_fields import BaseModelFields
from payments.apps import PaymentsConfig as AppConfig
from payments.enum import PaymentProvidersEnum, PaymentStatusEnum


class PaymentsModel(BaseModelFields, models.Model):
    order_id = models.UUIDField(null=False, blank=False)
    amount_in_cents = models.BigIntegerField(null=False, blank=False)
    provider = models.IntegerField(choices=PaymentProvidersEnum.get_choices(), null=False, blank=False)
    provider_id = models.UUIDField(null=False, blank=False)
    status = models.IntegerField(null=False, choices=PaymentStatusEnum.get_choices(),
                                 default=PaymentStatusEnum.INITIATED.val)

    class Meta:
        managed = True
        db_table = str(AppConfig.name)
