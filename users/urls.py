from django.urls import path
from knox import views as knox_views

from users.views import RegisterUserView, LoginView, VerifyEmailView, RequestVerificationEmailView, AdminLoginView

adminUrls = [
    path("login", AdminLoginView.as_view(), name="login"),
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
]

businessUrls = [
    path("register", RegisterUserView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
    path("<uuid:user_id>/verify", VerifyEmailView.as_view(), name="verify"),
    path("resend-verification-mail", RequestVerificationEmailView.as_view(), name="resent_verification_email"),
]
