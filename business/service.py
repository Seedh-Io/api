from backend_api.helpers.service_helper import BaseService
from business.models import BusinessModel
from business.serializers.business_serializers import CreateBusinessSerializers
from users.models import UserModel


class BusinessService(BaseService):

    def create_business_when_user_register(self, user: UserModel) -> 'BusinessModel':
        business = CreateBusinessSerializers(data={"name": user.first_name, "business_owner": user.pk},
                                             context=self.context)
        business.is_valid(raise_exception=True)
        business.save()
        return business.instance
