from enum import Enum, auto
from .ASTVisitors import ASTVisitor


class TokenType(Enum):
    PROGRAM = auto()
    INSTRUCTIONS = auto()
    INSTRUCTION = auto()

    UNARY_EXPRESSION = auto()
    UNARY_PLUS_OPERATOR = auto()
    UNARY_MINUS_OPERATOR = auto()
    DEREFERENCE_OPERATOR = auto()
    ADDRESS_OPERATOR = auto()

    ADD_OPERATOR = auto()
    SUB_OPERATOR = auto()
    MULT_OPERATOR = auto()
    DIV_OPERATOR = auto()
    GREATER_THAN_OPERATOR = auto()
    LESS_THAN_OPERATOR = auto()
    EQUALS_OPERATOR = auto()
    ASSIGNMENT_OPERATOR = auto()

    IDENTIFIER = auto()

    DOUBLE_LITERAL = auto()
    INT_LITERAL = auto()

    TYPE_DECLARATION = auto()
    VARIABLE_DECLARATION = auto()
    INT_TYPE = auto()
    FLOAT_TYPE = auto()
    CHAR_TYPE = auto()
    CONST_TYPE = auto()


class ASTToken:

    def __init__(self, token_type, content=None):

        self.tokenType = token_type
        if content is not None:
            self.content = content
        else:
            self.content = self.tokenType.name.lower().replace("_", " ")


class AST:

    def __init__(self, token: ASTToken):
        self.parent = None
        self.token = token

    def isRoot(self):
        return self.parent is None

    def accept(self, visitor):
        raise NotImplementedError('Generic method')


class ASTInternal(AST):

    def __init__(self, token: ASTToken):
        super().__init__(token)
        self.children = list()

    def accept(self, visitor: ASTVisitor):
        for child in self.children:
            assert isinstance(child, AST)
            child.accept(visitor)
        visitor.visitASTInternal(self)

    def addChild(self, child: AST):
        assert child is not None
        child.parent = self
        self.children.append(child)


class ASTLeaf(AST):

    def __init__(self, token: ASTToken):
        super().__init__(token)

    def accept(self, visitor: ASTVisitor):
        assert isinstance(visitor, ASTVisitor)
        visitor.visitASTLeaf(self)
