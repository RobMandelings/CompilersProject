from enum import Enum, auto


# TODO maybe divide this into subclasses where different AST's may have different types of TokenTypes
class TokenType(Enum):
    PROGRAM = auto()
    INSTRUCTIONS = auto()
    INSTRUCTION = auto()
    PRINTF_INSTRUCTION = auto()

    UNARY_EXPRESSION = auto()
    UNARY_PLUS_OPERATOR = auto()
    UNARY_MINUS_OPERATOR = auto()
    DEREFERENCE_OPERATOR = auto()
    ADDRESS_OPERATOR = auto()

    ADD_EXPRESSION = auto()
    SUB_EXPRESSION = auto()
    MULT_EXPRESSION = auto()
    DIV_EXPRESSION = auto()
    GREATER_THAN_EXPRESSION = auto()
    LESS_THAN_EXPRESSION = auto()
    EQUALS_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()

    IDENTIFIER = auto()

    CHAR_LITERAL = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()

    VARIABLE_DECLARATION = auto()
    VARIABLE_DECLARATION_AND_INIT = auto()
    INT_TYPE = auto()
    FLOAT_TYPE = auto()
    CHAR_TYPE = auto()
    CONST_TYPE = auto()


class ASTToken:
    """
    Token that is used in an AST To identify the specific type of a node
    """

    def __init__(self, token_type, content=None):

        self.token_type = token_type
        if content is not None:
            if not isinstance(content, str):
                self.content = str(content)
            else:
                self.content = content
        else:
            self.content = self.token_type.name.lower().replace("_", " ")

    @staticmethod
    def is_binary_expression(token_type: TokenType):
        """
        Checks whether a given token type is a binary expression or not
        """
        if (
                token_type == TokenType.ADD_EXPRESSION or
                token_type == TokenType.SUB_EXPRESSION or
                token_type == TokenType.DIV_EXPRESSION or
                token_type == TokenType.MULT_EXPRESSION or
                token_type == TokenType.GREATER_THAN_EXPRESSION or
                token_type == TokenType.LESS_THAN_EXPRESSION or
                token_type == TokenType.EQUALS_EXPRESSION or
                token_type == TokenType.ASSIGNMENT_EXPRESSION
        ):
            return True

        return False
