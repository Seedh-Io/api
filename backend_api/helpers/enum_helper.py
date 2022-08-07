from enum import Enum, unique


@unique
class BaseEnum(Enum):
    def __init__(self, display_name, data):
        self._display_name = display_name
        self._data = data

    @classmethod
    def get_choices(cls):
        choice = []
        for key in cls:
            choice.append((key.val, key.display_name))
        return choice

    @classmethod
    def search_by_value(cls, value) -> 'BaseEnum':
        for key in cls:
            if key.val == value:
                return key

    @property
    def display_name(self):
        return self._display_name

    @property
    def val(self):
        return self._data

    @property
    def data(self):
        return self._data
