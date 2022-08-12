from rest_framework.exceptions import NotFound

from backend_api.helpers.service_helper import BaseService
from business.models import BusinessModel
from business.serializers.business_serializers import CreateBusinessSerializers, ActivatePackageForBusiness
from users.models import UserModel


class BusinessService(BaseService):

    def create_business_when_user_register(self, user: UserModel) -> 'BusinessModel':
        business = CreateBusinessSerializers(data={"name": user.first_name, "business_owner": user.pk},
                                             context=self.context)
        business.is_valid(raise_exception=True)
        business.save()
        return business.instance

    def activate_package_for_business(self, business_id, package_id, expiry_date_time):
        try:
            business = BusinessModel.objects.get(id=business_id)
        except Exception as e:
            raise NotFound("Business Not found")
        business_obj = ActivatePackageForBusiness(
            data={"active_package_id": package_id, "active_package_expiry_date_time": expiry_date_time},
            context=self.context, instance=business)
        business_obj.is_valid(raise_exception=True)
        business_obj.save()
        return business_obj.data
