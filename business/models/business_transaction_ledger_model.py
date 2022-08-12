from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend_api.fields.base_model_fields import BaseModelFields
from backend_api.validators import Validators
from business.enum import BusinessReferenceTypeEnum
from business.models import BusinessModel
from business.apps import BusinessConfig as AppConfig


class BusinessTransactionLedgerModel(BaseModelFields, models.Model):
    business = models.ForeignKey(BusinessModel, null=False, blank=False, on_delete=models.DO_NOTHING)
    credits = models.IntegerField(null=False, blank=False, validators=[Validators.min_0_validator])
    is_credit = models.BooleanField(null=False, blank=False)
    created_by = models.UUIDField(null=True, blank=False)
    reference_id = models.UUIDField(null=False, blank=False)
    reference_type = models.IntegerField(choices=BusinessReferenceTypeEnum.get_choices(), null=False, blank=False)
    expiry_date_time = models.DateTimeField(null=True, blank=False)
    credits_used = models.IntegerField(null=False, blank=False, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "transaction_ledger"
        unique_together = (('reference_type', 'reference_id', 'is_credit'),)
        index_together = (('business', 'is_active', 'is_deleted'), )


@receiver(post_save, sender=BusinessTransactionLedgerModel)
def update_business_credits(sender, instance: BusinessTransactionLedgerModel, created: bool, **kwargs):
    if created:
        business = instance.business
        business.available_credits += (instance.credits * (1 if instance.is_credit else -1))
        business.save()




