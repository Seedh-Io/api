from django.urls import path

from payments.views import VerifyPaymentView

PaymentBusinessUrls = [
    path("verify/<uuid:payment_id>", VerifyPaymentView.as_view(), name="verify"),
]


PaymentAdminUrls = [

]
