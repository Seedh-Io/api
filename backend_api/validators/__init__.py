from django.core.exceptions import ValidationError


class Validators:

    @staticmethod
    def email_validator(email_id: str):
        return email_id

    @staticmethod
    def mobile_validator(mobile: str):
        return mobile

    @staticmethod
    def password_validator(password: str):
        return password

    @staticmethod
    def min_0_validator(amount: int):
        if amount < 0:
            raise ValidationError('Amount cannot be less than 0')
