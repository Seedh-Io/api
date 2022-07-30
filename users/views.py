from django.contrib.auth import login, authenticate, logout

# Create your views here.
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView

from users.models import UserModel
from users.serializers.user_serializer import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
