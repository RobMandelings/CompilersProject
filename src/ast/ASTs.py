from enum import Enum, auto
from antlr4.tree.Tree import TerminalNodeImpl
from . import ASTVisitors
from ..antlr4_gen.CLexer import CLexer


class TokenType(Enum):
    PROGRAM = auto()
    STATEMENT = auto()

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

    def __init__(self, cst, lexer, token_type: TokenType = None):

        if token_type is None:
            self.tokenType = self.get_token_type_from_cst(cst, lexer)
            self.content = cst.symbol.text
        else:
            self.tokenType = token_type
            self.content = self.tokenType.name

    @staticmethod
    def get_token_type_from_cst(cst, lexer):
        assert isinstance(cst, TerminalNodeImpl)
        assert isinstance(lexer, CLexer)
        symbol_text = cst.getSymbol().text
        # Literals are easy to check
        if symbol_text == '*':
            return TokenType.MULT_OPERATOR
        elif symbol_text == '/':
            return TokenType.DIV_OPERATOR
        elif symbol_text == '+':
            return TokenType.ADD_OPERATOR
        elif symbol_text == '-':
            return TokenType.SUB_OPERATOR
        elif symbol_text == '>':
            return TokenType.GREATER_THAN_OPERATOR
        elif symbol_text == '<':
            return TokenType.LESS_THAN_OPERATOR
        elif symbol_text == '==':
            return TokenType.EQUALS_OPERATOR
        elif symbol_text == '=':
            return TokenType.ASSIGNMENT_OPERATOR
        elif symbol_text == 'int':
            return TokenType.INT_TYPE
        elif symbol_text == 'float':
            return TokenType.FLOAT_TYPE
        elif symbol_text == 'char':
            return TokenType.CHAR_TYPE
        elif symbol_text == 'const':
            return TokenType.CONST_TYPE
        # These 'symbolic' tokens are recognized by a regular expression so we can check if the ID corresponds to one
        # of the parsers' token IDs
        elif cst.getSymbol().type == lexer.INTEGER:
            return TokenType.INT_LITERAL
        elif cst.getSymbol().type == lexer.DOUBLE:
            return TokenType.DOUBLE_LITERAL
        elif cst.getSymbol().type == lexer.ID:
            return TokenType.IDENTIFIER
        else:
            raise NotImplementedError("The token type could not be deduced from the symbol '" + symbol_text + "'.")


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

    def accept(self, visitor: ASTVisitors.ASTVisitor):
        for child in self.children:
            assert isinstance(child, AST)
            child.accept(visitor)

    def addChild(self, child: AST):
        child.parent = self
        self.children.append(child)


class ASTProgram(ASTInternal):

    def accept(self, visitor: ASTVisitors.ASTVisitor):
        super().accept(visitor)
        visitor.visitASTProgram(self)


class ASTStatement(ASTInternal):

    def accept(self, visitor: ASTVisitors.ASTVisitor):
        super().accept(visitor)
        visitor.visitASTStatement(self)


"""
Structure to keep track of binary operations such as +, -, *, / and >, <, ==
"""


class ASTBinaryOperation(AST):

    def __init__(self, token, left, right):
        super().__init__(token)
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def accept(self, visitor: ASTVisitors.ASTVisitor):
        self.left.accept(visitor)
        self.right.accept(visitor)
        visitor.visitASTBinaryOp(self)


class ASTUnaryExpression(AST):
    def __init__(self, left, right):
        super().__init__(ASTToken(None, None, TokenType.UNARY_EXPRESSION))
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def accept(self, visitor: ASTVisitors.ASTVisitor):
        self.left.accept(visitor)
        self.right.accept(visitor)
        visitor.visitASTUnaryExpression(self)


class ASTLeaf(AST):

    def __init__(self, token: ASTToken):
        super().__init__(token)

    def accept(self, visitor: ASTVisitors.ASTVisitor):
        assert isinstance(visitor, ASTVisitors.ASTVisitor)
        visitor.visitASTLeaf(self)


class ASTType(ASTInternal):

    def __init__(self, token: ASTToken):
        super().__init__(token)

    def accept(self, visitor: ASTVisitors.ASTVisitor):
        super().accept(visitor)
        visitor.visitASTType(self)


class ASTVariableDeclaration(AST):

    def __init__(self, variable_type: ASTType, variable: AST, token):
        super().__init__(token)
        self.variable_type = variable_type
        self.variable = variable
        self.variable_type.parent = self
        self.variable.parent = self

    def accept(self, visitor):
        assert isinstance(visitor, ASTVisitors.ASTVisitor)
        visitor.visitASTBinaryOp(self)
        self.variable_type.accept(visitor)
        self.variable.accept(visitor)
