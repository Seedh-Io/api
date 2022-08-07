import re

from users.models import UserModel


class BusinessMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if re.search("/api/business/*", path) and request.user and type(request.user) == UserModel:
            from business.repository import BusinessRepository
            business = BusinessRepository.get_active_business_for_user(request.user.id)
            if not business:
                from backend_api.helpers.custom_exception_helper import UserBusinessNotFoundException
                raise UserBusinessNotFoundException("")
        response = self.get_response(request)
        return response
