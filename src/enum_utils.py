import enum


class NamedEnum(enum.Enum):
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, token_name: str):
        assert isinstance(token_name, str)
        self.token_name = token_name

    def __str__(self):
        return self.token_name
