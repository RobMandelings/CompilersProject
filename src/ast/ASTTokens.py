from enum import Enum, auto


class DataTypeToken(Enum):
    """
    Ordered from lowest precedence to highest precedence
    """
    CHAR = auto()
    INT = auto()
    FLOAT = auto()

    @staticmethod
    def get_data_type_from_name(name: str):
        if name == 'int':
            return DataTypeToken.INT
        elif name == 'float':
            return DataTypeToken.FLOAT
        elif name == 'char':
            return DataTypeToken.CHAR
        else:
            return None

    @staticmethod
    def get_data_type_for_token_type(token_type):
        assert isinstance(token_type, DataTypeToken) or isinstance(token_type, LiteralToken)
        if token_type == DataTypeToken.CHAR or token_type == LiteralToken.CHAR_LITERAL:
            return DataTypeToken.CHAR
        elif token_type == DataTypeToken.INT or token_type == LiteralToken.INT_LITERAL:
            return DataTypeToken.INT
        elif token_type == DataTypeToken.FLOAT or token_type == LiteralToken.FLOAT_LITERAL:
            return DataTypeToken.FLOAT
        else:
            raise NotImplementedError(f"Cannot convert the given tokentype '{token_type.name}' to a datatype token")

    @staticmethod
    def is_richer_than(datatype1, datatype2):
        """
        Must be placed outside the DataType class because it would not be fully 'defined' when setting the expected parameter types, weird stuff
        """
        if not isinstance(datatype1, DataTypeToken):
            datatype1 = DataTypeToken.get_data_type_for_token_type(datatype1)
        if not isinstance(datatype2, DataTypeToken):
            datatype2 = DataTypeToken.get_data_type_for_token_type(datatype2)
        return datatype1.value > datatype2.value


class TypeAttributeToken(Enum):
    CONST = auto()


class LiteralToken(Enum):
    CHAR_LITERAL = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()


class UnaryExprToken(Enum):
    UNARY_PLUS_EXPRESSION = auto()
    UNARY_MINUS_EXPRESSION = auto()
    DEREFERENCE_EXPRESSION = auto()
    ADDRESS_EXPRESSION = auto()


class BinaryArithmeticExprToken(Enum):
    ADD_EXPRESSION = auto()
    SUB_EXPRESSION = auto()
    MUL_EXPRESSION = auto()
    DIV_EXPRESSION = auto()


class BinaryCompareExprToken(Enum):
    GREATER_THAN_EXPRESSION = auto()
    LESS_THAN_EXPRESSION = auto()
    EQUALS_EXPRESSION = auto()
