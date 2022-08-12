from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from backend_api.authentication.business_authentication import BusinessAuthentication
from payments.models import PaymentsModel
# Create your views here.
from payments.serializers.payment_verification_serializer import UserPaymentVerificationSerializer


class VerifyPaymentView(GenericAPIView, UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BusinessAuthentication,)
    queryset = PaymentsModel.objects
    serializer_class = UserPaymentVerificationSerializer
    lookup_field = "id"
    lookup_url_kwarg = "payment_id"

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
