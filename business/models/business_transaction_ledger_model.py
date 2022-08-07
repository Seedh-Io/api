from django.db import models

from backend_api.fields.base_model_fields import BaseModelFields
from backend_api.validators import Validators
from business.enum import BusinessReferenceTypeEnum
from business.models import BusinessModel
from business.apps import BusinessConfig as AppConfig


class BusinessTransactionLedgerModel(BaseModelFields, models.Model):
    business = models.ForeignKey(BusinessModel, null=False, blank=False, on_delete=models.DO_NOTHING)
    amount_in_cents = models.IntegerField(null=False, blank=False, validators=[Validators.min_0_validator])
    is_credit = models.BooleanField(null=False, blank=False)
    created_by = models.UUIDField(null=False, blank=False)
    reference_id = models.UUIDField(null=False, blank=False)
    reference_type = models.IntegerField(choices=BusinessReferenceTypeEnum.get_choices(), null=False, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "transaction_ledger"
