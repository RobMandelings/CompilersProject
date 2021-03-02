from enum import Enum, auto
from antlr4.tree.Tree import TerminalNodeImpl
from . import ASTVisitors


class AST:

    def __init__(self, token):
        self.parent = None
        self.token = token

    def isRoot(self):
        return self.parent is None

    def accept(self, visitor):
        raise NotImplementedError('Generic method')


class ASTBinaryOperation(AST):

    def __init__(self, token, left, right):
        super().__init__(token)
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def accept(self, visitor):
        assert isinstance(visitor, ASTVisitors.ASTVisitor)
        visitor.visitASTBinaryOp(self)
        self.left.accept(visitor)
        self.right.accept(visitor)


class ASTLeaf(AST):

    def accept(self, visitor):
        assert isinstance(visitor, ASTVisitors.ASTVisitor)
        visitor.visitASTLeaf(self)

    def __init__(self, token):
        super().__init__(token)

    def createDot(self, current_dot, counter):
        counter.value += 1
        current_dot.node('node' + str(counter.value), self.token.content)


class Token:

    def __init__(self, cst):
        assert isinstance(cst, TerminalNodeImpl)
        self.tokenType = self.get_token_type_from_cst(cst)
        self.content = cst.symbol.text

    @staticmethod
    def get_token_type_from_cst(cst):
        assert isinstance(cst, TerminalNodeImpl)
        symbol = cst.symbol.text
        if symbol == '*':
            return NodeCategory.MULT_OPERATOR
        elif symbol == '/':
            return NodeCategory.DIV_OPERATOR
        elif symbol == '+':
            return NodeCategory.ADD_OPERATOR
        elif symbol == '-':
            return NodeCategory.SUB_OPERATOR


class NodeCategory(Enum):
    ADD_OPERATOR = auto()
    SUB_OPERATOR = auto()
    MULT_OPERATOR = auto()
    DIV_OPERATOR = auto()
    ID = auto()
    DOUBLE = auto()
    INT = auto()