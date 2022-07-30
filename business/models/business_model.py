from django.db import models

# Create your models here.
from django.db.models import JSONField

from backend_api.fields.base_fields import BaseFields
from business.apps import BusinessConfig as AppConfig
from business.enum import BusinessStatusEnum


class BusinessModel(models.Model, BaseFields):
    name = models.CharField(null=False, blank=False, max_length=30)
    gst_details = JSONField(null=False, blank=False, default=dict)
    business_owner = models.UUIDField(null=False, blank=False)
    image_id = models.UUIDField(null=True, blank=False)
    status = models.IntegerField(null=False, blank=False, choices=BusinessStatusEnum.get_choices(),
                                 default=BusinessStatusEnum.ACTIVE.val)
    business_verified = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name)
