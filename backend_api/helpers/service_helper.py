from rest_framework.serializers import Serializer


class BaseService:

    def __init__(self, context=None):
        self.__context = context

    @property
    def context(self):
        return self.__context
