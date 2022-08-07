from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from backend_api.authentication.business_authentication import BusinessAuthentication
from orders.serializers import PackageOrderSerializer, RechargeOrderSerializer


# Create your views here.


class PackageOrderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BusinessAuthentication,)
    serializer_class = PackageOrderSerializer


class RechargeOrderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BusinessAuthentication,)
    serializer_class = RechargeOrderSerializer
