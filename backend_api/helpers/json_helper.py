from backend_api.encoders.JSONEncoder import JSONEncoder


class JSONHelper:

    @staticmethod
    def dict_to_json(dict_data):
        import json
        return json.loads(json.dumps(dict_data, cls=JSONEncoder))
