import re

from knox.auth import TokenAuthentication


class BusinessAuthentication(TokenAuthentication):

    def authenticate(self, request):
        user, auth_token = super(BusinessAuthentication, self).authenticate(request)
        path = request.path
        from users.models import UserModel
        if re.search("/api/business/*", path) and user and type(user) == UserModel:
            from business.repository import BusinessRepository
            business = BusinessRepository.get_active_business_for_user(user.id)
            if not business:
                from backend_api.helpers.custom_exception_helper import UserBusinessNotFoundException
                raise UserBusinessNotFoundException("")
            request.business = business
        return user, auth_token
