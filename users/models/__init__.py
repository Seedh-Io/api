from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager

from backend_api.fields.base_fields import BaseFields
from backend_api.validators import Validators
from users.apps import UsersConfig as AppConfig


# Create your models here.
class UserModel(BaseFields, AbstractBaseUser):
    USERNAME_FIELD = 'email_id'

    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=False)
    email_id = models.EmailField(max_length=100, null=False, blank=False, unique=True,
                                 validators=[Validators.email_validator])
    mobile = models.CharField(max_length=10, null=False, blank=False, unique=True,
                              validators=[Validators.mobile_validator])
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=False)
    email_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING)

    objects = UserManager()

    class Meta:
        managed = True
        db_table = str(AppConfig.name)
