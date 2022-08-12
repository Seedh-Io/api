from django.db import models

from backend_api.fields.base_model_fields import BaseModelFields, BaseModelManager
from payments.apps import PaymentsConfig as AppConfig
from payments.enum import PaymentProvidersEnum, PaymentStatusEnum, SupportedPaymentCurrenciesEnum


class PaymentsManager(BaseModelManager):

    def get_payment_by_pg(self, pg: PaymentStatusEnum, pg_id: str):
        return self.get(provider=pg.val, provider_id=pg_id)


class PaymentsModel(BaseModelFields, models.Model):
    order_id = models.UUIDField(null=False, blank=False)
    amount_in_cents = models.BigIntegerField(null=False, blank=False)
    provider = models.IntegerField(choices=PaymentProvidersEnum.get_choices(), null=False, blank=False)
    provider_id = models.UUIDField(null=True, blank=False)
    status = models.IntegerField(null=False, choices=PaymentStatusEnum.get_choices(),
                                 default=PaymentStatusEnum.INITIATED.val)
    currency = models.CharField(choices=SupportedPaymentCurrenciesEnum.get_choices(), max_length=5, null=False,
                                blank=False)

    objects = PaymentsManager()

    class Meta:
        managed = True
        db_table = str(AppConfig.name)
