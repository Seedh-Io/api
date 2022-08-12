from django.db import models

from backend_api.fields.base_model_fields import BaseModelFields
from business.enum import BusinessRolesEnum, BusinessUserStatusEnum
from business.models import BusinessModel
from business.apps import BusinessConfig as AppConfig


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=BusinessUserStatusEnum.ACTIVE.val)

    def get_active_business_for_user(self, user_id: str) -> 'BusinessUserModel':
        return self.get_queryset().filter(user_id=user_id).first().business


class BusinessUserModel(BaseModelFields, models.Model):
    user_id = models.UUIDField(null=False, blank=False)
    business = models.ForeignKey(BusinessModel, null=False, blank=False, on_delete=models.DO_NOTHING)
    role = models.IntegerField(choices=BusinessRolesEnum.get_choices(), null=False, blank=False)
    status = models.IntegerField(null=False, blank=False, choices=BusinessUserStatusEnum.get_choices(),
                                 default=BusinessUserStatusEnum.ACTIVE.val)

    active_objects = ActiveUserManager()
    objects = models.Manager()

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "user"
