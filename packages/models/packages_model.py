from django.db import models

from backend_api.fields.base_model_fields import BaseModelFields
from backend_api.validators import Validators
from packages.enum import PackageStatusEnum

from packages.apps import PackagesConfig as AppConfig


class PackagesModel(BaseModelFields, models.Model):
    name = models.CharField(null=False, blank=False, max_length=30)
    display_name = models.CharField(null=False, blank=False, max_length=40)
    status = models.IntegerField(null=False, blank=False, choices=PackageStatusEnum.get_choices(),
                                 default=PackageStatusEnum.ACTIVE.val)
    list_price_in_cents = models.IntegerField(null=False, blank=False, validators=[Validators.min_0_validator])
    selling_price_in_cents = models.IntegerField(null=False, blank=False, validators=[Validators.min_0_validator])
    configuration = models.JSONField(null=False, blank=False, default=dict)

    class Meta:
        managed = True
        db_table = str(AppConfig.name)
