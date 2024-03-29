from rest_framework.exceptions import NotFound

from backend_api.helpers.service_helper import BaseService


class PackagesRepository(BaseService):

    @staticmethod
    def get_package_by_id(package_id):
        from packages.models import PackagesModel
        try:
            return PackagesModel.objects.get(id=package_id)
        except Exception as e:
            raise NotFound("Package not found")
