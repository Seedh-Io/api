from knox.auth import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import PackagesModel
from .serializers import PackageSerializer


# Create your views here.

class PackageLCView(ListCreateAPIView):
    queryset = PackagesModel.objects
    serializer_class = PackageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class PackageRUDView(RetrieveUpdateDestroyAPIView):
    queryset = PackagesModel.objects
    serializer_class = PackageSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    lookup_field = 'id'
