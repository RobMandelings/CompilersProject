from graphviz import Digraph


class ASTVisitor:

    def visitASTLeaf(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visitASTInternal(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')


class ASTVisitorDot(ASTVisitor):

    def __init__(self):
        super().__init__()
        self.graph = Digraph('Abstract Syntax Tree')

    def addToDotNode(self, ast):
        self.graph.node(str(id(ast)), ast.token.content)
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visitASTLeaf(self, ast):
        self.addToDotNode(ast)

    def visitASTInternal(self, ast):
        self.addToDotNode(ast)
