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
            request.business = BusinessRepository.get_active_business_for_user(request.user.id)
        return response
