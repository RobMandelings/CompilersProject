from abc import abstractmethod
from enum import Enum


class NamedEnum(Enum):
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


class DataTypeToken(NamedEnum):
    """
    Ordered from lowest precedence to highest precedence
    """
    # Indicates the richness of the datatype, from low to high
    _order_ = 'BOOL CHAR INT FLOAT'
    BOOL = 'bool'
    CHAR = 'char'
    INT = 'int'
    FLOAT = 'float'

    @staticmethod
    def from_str(name: str):
        if name == 'int':
            return DataTypeToken.INT
        elif name == 'float':
            return DataTypeToken.FLOAT
        elif name == 'char':
            return DataTypeToken.CHAR
        elif name == 'bool':
            return DataTypeToken.BOOL
        else:
            return None

    @staticmethod
    def is_richer_than(datatype1, datatype2):
        """
        Must be placed outside the DataType class because it would not be fully 'defined' when setting the expected parameter types, weird stuff
        """
        return datatype1.value > datatype2.value


class TypeAttributeToken(NamedEnum):
    CONST = 'const'

    @staticmethod
    def from_str(name: str):

        if name == 'const':
            return TypeAttributeToken.CONST
        else:
            return None


class IfStatementToken(NamedEnum):
    IF = 'if'
    ELSE_IF = 'else if'
    ELSE = 'else'

    @staticmethod
    def from_str(name: str):

        if name == 'if':
            return IfStatementToken.IF
        elif name == 'else if':
            return IfStatementToken.ELSE_IF
        elif name == 'else if':
            return IfStatementToken.ELSE
        else:
            return None


class UnaryArithmeticExprToken(NamedEnum):
    PLUS = '+'
    MINUS = '-'

    @staticmethod
    def from_str(name: str):

        if name == '+':
            return UnaryArithmeticExprToken.PLUS
        elif name == '-':
            return UnaryArithmeticExprToken.MINUS
        else:
            return None


class PointerExprToken(NamedEnum):
    DEREFERENCE = '*'
    ADDRESS = '&'

    @staticmethod
    def from_str(name: str):

        if name == '*':
            return PointerExprToken.PLUS
        elif name == '&':
            return PointerExprToken.MINUS
        else:
            return None


class BinaryArithmeticExprToken(NamedEnum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'

    @staticmethod
    def from_str(name: str):

        if name == '+':
            return BinaryArithmeticExprToken.ADD
        elif name == '-':
            return BinaryArithmeticExprToken.SUB
        elif name == '*':
            return BinaryArithmeticExprToken.MUL
        elif name == '/':
            return BinaryArithmeticExprToken.DIV
        elif name == '%':
            return BinaryArithmeticExprToken.MOD
        else:
            return None


class LogicalExprToken(NamedEnum):
    OR = '||'
    AND = '&&'
    NOT = '!'

    @staticmethod
    def from_str(name: str):
        if name == '||':
            return LogicalExprToken.OR
        elif name == '&&':
            return LogicalExprToken.AND
        elif name == '!':
            return LogicalExprToken.NOT
        else:
            return None


class BitwiseExprToken(NamedEnum):
    OR = '|'
    AND = '&'

    @staticmethod
    def from_str(name: str):
        if name == '|':
            return BitwiseExprToken.OR
        elif name == '&':
            return BitwiseExprToken.AND
        else:
            return None


class RelationalExprToken(NamedEnum):
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUALS = '>='
    LESS_THAN = '<'
    LESS_THAN_OR_EQUALS = '<='
    EQUALS = '=='
    NOT_EQUALS = '!='

    @staticmethod
    def from_str(name: str):
        if name == '>':
            return RelationalExprToken.GREATER_THAN
        elif name == '>=':
            return RelationalExprToken.GREATER_THAN_OR_EQUALS
        elif name == '<':
            return RelationalExprToken.LESS_THAN
        elif name == '<=':
            return RelationalExprToken.LESS_THAN_OR_EQUALS
        elif name == '==':
            return RelationalExprToken.EQUALS
        elif name == '!=':
            return RelationalExprToken.NOT_EQUALS
        else:
            return None
