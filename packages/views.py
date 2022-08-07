from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from backend_api.authentication.business_authentication import BusinessAuthentication
from backend_api.permission import IsSupportUserPermission
from .models import PackagesModel
from .serializers import PackageSerializer


# Create your views here.

class PackageLCView(ListCreateAPIView):
    queryset = PackagesModel.objects
    serializer_class = PackageSerializer
    permission_classes = (IsAuthenticated, IsSupportUserPermission)
    authentication_classes = (BusinessAuthentication,)


class PackageRUDView(RetrieveUpdateDestroyAPIView):
    queryset = PackagesModel.objects
    serializer_class = PackageSerializer
    permission_classes = (IsAuthenticated, IsSupportUserPermission)
    authentication_classes = (BusinessAuthentication, )
    lookup_field = 'id'
