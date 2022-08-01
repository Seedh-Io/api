import json

from rest_framework.renderers import JSONRenderer


class JSONResponseFormatter(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'data': data,
        } if "error" not in data else data
        return json.dumps(response_dict)
