import logging

from django.db import models
from django.db.models.signals import post_save
# Create your models here.
from django.db.models import JSONField
from django.dispatch import receiver

from backend_api.fields.base_fields import BaseFields
from backend_api.validators import Validators
from business.apps import BusinessConfig as AppConfig
from business.enum import BusinessStatusEnum, BusinessRolesEnum


class BusinessModel(BaseFields, models.Model):
    name = models.CharField(null=False, blank=False, max_length=30)
    gst_details = JSONField(null=False, blank=False, default=dict)
    business_owner = models.UUIDField(null=False, blank=False)
    image_id = models.UUIDField(null=True, blank=False)
    status = models.IntegerField(null=False, blank=False, choices=BusinessStatusEnum.get_choices(),
                                 default=BusinessStatusEnum.ACTIVE.val)
    available_credits = models.IntegerField(null=False, blank=False, default=0, validators=[Validators.min_0_validator])
    business_verified = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        managed = True
        db_table = str(AppConfig.name)


@receiver(post_save, sender=BusinessModel)
def create_business_user(sender, instance: BusinessModel, created: bool, **kwargs):
    if created:
        from business.models import BusinessUserModel

        logging.info("create_business_user",
                     extra={"business_id": str(instance.pk), "user_id": str(instance.business_owner)})
        BusinessUserModel.objects.create(user_id=instance.business_owner, business=instance,
                                         role=BusinessRolesEnum.OWNER.val)
