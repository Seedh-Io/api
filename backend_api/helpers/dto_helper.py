import uuid
from datetime import datetime

from backend_api.helpers.json_helper import JSONHelper


class DataObject(type):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)


class BaseDataObject(metaclass=DataObject):

    def to_dict(self):
        return self.__to_dict(convert_json=False)

    def to_json(self):
        return self.__to_dict(convert_json=True)

    def __to_dict(self, convert_json=False) -> dict:
        attributes = dir(self)
        final_dict = {}
        for attr in attributes:
            if not attr.startswith("_") and attr not in ["to_dict", "to_json"]:
                value = getattr(self, attr)
                type_value = type(value)
                if type_value == datetime:
                    value = str(value)
                elif type_value == uuid.UUID:
                    value = str(value)
                elif isinstance(value, BaseDataObject):
                    value = value.to_json()
                elif isinstance(value, list):
                    """
                    Make Sure Every object is of BaseDataObject type or else app will crash
                    """
                    if len(value) > 0:
                        if isinstance(value[0], BaseDataObject):
                            value = list(map(lambda x: x.to_dict(), value))
                    else:
                        value = value

                final_dict[attr] = value
        return final_dict if not convert_json else JSONHelper.dict_to_json(final_dict)
