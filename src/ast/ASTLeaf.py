from src.ast.AST import AST
from graphviz import Digraph

class ASTLeaf(AST):

    def __init__(self, token):
        super().__init__(token)

    def createDot(self, current_dot, counter):
        counter.value += 1
        current_dot.node('node' + str(counter.value), self.token.content)
