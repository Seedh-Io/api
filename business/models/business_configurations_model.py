from django.db import models

from backend_api.fields.base_model_fields import BaseModelFields
from business.apps import BusinessConfig as AppConfig
from business.models import BusinessModel


class BusinessConfigurationsModel(BaseModelFields, models.Model):
    business = models.ForeignKey(BusinessModel, null=False, blank=False, on_delete=models.CASCADE)
    facebook_ads_config = models.JSONField(null=False, blank=False, default=dict)
    google_ads_config = models.JSONField(null=False, blank=False, default=dict)
    active_plan = models.UUIDField(null=True, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "configurations"
