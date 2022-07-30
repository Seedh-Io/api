from django.db import models

from backend_api.fields.base_fields import BaseFields
from business.enum import BusinessRolesEnum, BusinessUserStatusEnum
from business.models import BusinessModel
from business.apps import BusinessConfig as AppConfig


class BusinessUserModel(models.Model, BaseFields):
    user_id = models.UUIDField(null=False, blank=False)
    business = models.ForeignKey(BusinessModel, null=False, blank=False, on_delete=models.DO_NOTHING)
    role = models.IntegerField(choices=BusinessRolesEnum.get_choices(), null=False, blank=False)
    status = models.IntegerField(null=False, blank=False, choices=BusinessUserStatusEnum.get_choices(),
                                 default=BusinessUserStatusEnum.ACTIVE.val)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "user"
