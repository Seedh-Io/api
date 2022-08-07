from rest_framework import serializers


def create(*args, **kwargs):
    return {}


class BaseSerializer:

    @staticmethod
    def get_serializer(name: str, serializer: serializers.Serializer.__class__, version=1.0, **kwargs):
        return type('VersionSerializer', (serializers.Serializer,), {
            "version": serializers.FloatField(default=version),
            "name": serializers.CharField(default=name),
            "value": serializer(required=True, **kwargs),
            "required": True,
            "create": create,
        })()
