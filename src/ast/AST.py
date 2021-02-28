from enum import Enum, auto
from antlr4.tree.Tree import TerminalNodeImpl
from graphviz import Digraph


class AST:

    def __init__(self, token):
        self.parent = None
        self.token = token

    def isRoot(self):
        return self.parent is None

    """
    Generic method to create the dot string
    """

    def createDot(self, current_dot, counter):
        raise NotImplementedError("This is an abstract method")


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


class BinaryOp(AST):

    def __init__(self, token, left, right):
        super().__init__(token)
        self.left = left
        self.right = right

    def createDot(self, current_dot, counter):
        counter.value += 1
        old_counter_value = counter.value
        current_dot.node('node' + str(counter.value), self.token.content)
        current_dot.edge('node' + str(old_counter_value), 'node' + str(counter.value + 1))
        self.left.createDot(current_dot, counter)
        current_dot.edge('node' + str(old_counter_value), 'node' + str(counter.value + 1))
        self.right.createDot(current_dot, counter)


class NodeCategory(Enum):
    ADD_OPERATOR = auto()
    SUB_OPERATOR = auto()
    MULT_OPERATOR = auto()
    DIV_OPERATOR = auto()
    ID = auto()
    DOUBLE = auto()
    INT = auto()


class Counter:

    def __init__(self):
        self.value = 0
