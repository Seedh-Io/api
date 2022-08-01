import logging
from datetime import timedelta

import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.template.loader import get_template
from jwt import InvalidTokenError

from backend_api.constants.messages import Messages
from backend_api.fields.base_fields import BaseFields
from backend_api.helpers.custom_exception_helper import VerificationMailSentException, AccountAlreadyVerifiedException, \
    VerificationTokenException
from backend_api.helpers.datetime_helper import DateTimeHelper
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
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING)
    verified_on = models.DateTimeField(null=True, blank=False, default=None)
    last_verification_request = models.DateTimeField(null=True, blank=False)
    verification_count = models.IntegerField(default=0, null=False, blank=False)

    objects = UserManager()

    class Meta:
        managed = True
        db_table = str(AppConfig.name)

    @staticmethod
    def get_token_expiry_time():
        return DateTimeHelper.get_current_datetime() + timedelta(hours=1)

    def get_jwt_details(self):
        return settings.SECRET_KEY, "HS256", f"usr:{str(self.pk)}"

    def generate_verification_token(self):
        if self.is_verified:
            raise AccountAlreadyVerifiedException(Messages.verification_mail_already_sent())
        if self.last_verification_request and (
                DateTimeHelper.get_current_datetime() - self.last_verification_request) <= timedelta(seconds=1):
            raise VerificationMailSentException(Messages.account_already_verified())
        code, algorithm, audience = self.get_jwt_details()
        token = jwt.encode({"user_id": str(self.pk), "exp": self.get_token_expiry_time(), "aud": audience},
                           code, algorithm=algorithm)
        self.verification_count += 1
        self.last_verification_request = DateTimeHelper.get_current_datetime()
        self.save()
        logging.info("verification_token_requested", {})
        return token

    def verify_token(self, token):
        from jwt import ExpiredSignatureError
        if self.is_verified:
            raise VerificationTokenException("Account already verified...")
        try:
            code, algorithm, audience = self.get_jwt_details()
            data = jwt.decode(token, code, algorithms=[algorithm], audience=audience)
            self.verified_on = DateTimeHelper.get_current_datetime()
            self.is_verified = True
            self.save()
        except ExpiredSignatureError as e:
            raise VerificationTokenException(Messages.verification_link_expired())
        except InvalidTokenError as e:
            raise VerificationTokenException(Messages.invalid_verification_token())
        except Exception as e:
            from rest_framework.exceptions import APIException
            logging.error("token_verification_failed", extra={"msg": str(e), "exception": e})
            raise (e if type(e) == APIException else VerificationTokenException(
                Messages.some_error_occurred_contact_support()))

    def send_email_for_token(self):
        from django.core.mail import EmailMultiAlternatives
        from backend_api.helpers.url_helper import UrlHelper
        token = self.generate_verification_token()
        url = UrlHelper.get_website_url(f"/{str(self.id)}/verify?token={token}")
        body = get_template("email_verification.jinja2").render({'url': url})
        msg = EmailMultiAlternatives(Messages.verification_email_subject(), body, settings.EMAIL_HOST_USER,
                                     [self.email_id])
        msg.attach_alternative(body, "text/html")
        msg.send()
