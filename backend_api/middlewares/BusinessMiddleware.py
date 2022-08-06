import re

from django.contrib.auth.models import AnonymousUser


class BusinessMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if re.search("/api/business/*", path) and request.user and type(request.user) != AnonymousUser:
            from business.repository import BusinessRepository
            business = BusinessRepository.get_active_business_for_user(request.user.id)
            if not business:
                from backend_api.helpers.custom_exception_helper import UserBusinessNotFoundException
                raise UserBusinessNotFoundException("")
        return response
