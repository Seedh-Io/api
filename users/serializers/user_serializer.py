from rest_framework import serializers

from backend_api.validators import Validators
from users.models import UserModel
from users.service_utils import BusinessServiceUtils


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[Validators.password_validator])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ('password', 'password2', 'email_id', 'first_name', 'last_name', 'mobile')

    def validate_password2(self, password2):
        if password2 != self.initial_data["password"]:
            raise serializers.ValidationError("Passwords do not match")
        return password2

    def validate(self, attrs):
        if "password2" in attrs:
            del attrs["password2"]
        return attrs

    def create(self, validated_data):
        password = validated_data["password"]
        del validated_data["password"]
        user: UserModel = super(RegisterUserSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        BusinessServiceUtils(context=self.context).register_business(user)
        return user
