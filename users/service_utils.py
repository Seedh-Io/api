from backend_api.helpers.service_helper import BaseService
from users.models import UserModel


class BusinessServiceUtils(BaseService):

    def register_business(self, user: UserModel):
        from business.service import BusinessService
        return BusinessService(context=self.context).create_business_when_user_register(user=user)

