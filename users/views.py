from django.contrib.auth import login

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from backend_api.authentication.business_authentication import BusinessAuthentication
from users.models import UserModel
from users.serializers.user_serializer import RegisterUserSerializer, VerifyEmailSerializer


class RegisterUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: UserModel = serializer.validated_data['user']
        if user.is_staff_user():
            raise PermissionDenied("Not allowed to log in for business")
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class AdminLoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: UserModel = serializer.validated_data['user']
        if not (user.is_staff_user()):
            raise PermissionDenied("Not a admin user.")
        login(request, user)
        return super(AdminLoginView, self).post(request, format=None)


class VerifyEmailView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = UserModel.objects
    serializer_class = VerifyEmailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data={
            "token": self.request.query_params.get("token", ""),
        }, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.headers)


class RequestVerificationEmailView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BusinessAuthentication,)

    def get(self, *args, **kwargs):
        self.request.user.send_email_for_verification()
        from backend_api.constants.messages import Messages
        return Response({
            "message": Messages.verification_email_sent()
        }, status=status.HTTP_200_OK, headers=self.headers)

