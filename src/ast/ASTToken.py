from enum import Enum, auto


class ASTTypeToken(Enum):
    INT_TYPE = auto()
    FLOAT_TYPE = auto()
    CHAR_TYPE = auto()
    CONST_TYPE = auto()


class ASTLiteralToken(Enum):
    CHAR_LITERAL = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()


class ASTUnaryExpressionToken(Enum):
    UNARY_PLUS_EXPRESSION = auto()
    UNARY_MINUS_EXPRESSION = auto()
    DEREFERENCE_EXPRESSION = auto()
    ADDRESS_EXPRESSION = auto()


class ASTBinaryArithmeticExprToken(Enum):
    ADD_EXPRESSION = auto()
    SUB_EXPRESSION = auto()
    MUL_EXPRESSION = auto()
    DIV_EXPRESSION = auto()


class ASTBinaryCompareExprToken(Enum):
    GREATER_THAN_EXPRESSION = auto()
    LESS_THAN_EXPRESSION = auto()
    EQUALS_EXPRESSION = auto()
