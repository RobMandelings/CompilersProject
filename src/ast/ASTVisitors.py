from graphviz import Digraph


class ASTVisitor:

    def visitASTBinaryOp(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visitASTLeaf(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visitASTType(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visitASTProgram(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visitASTStatement(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visitASTUnaryExpression(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')


class ASTVisitorDot(ASTVisitor):

    def __init__(self):
        super().__init__()
        self.graph = Digraph('Abstract Syntax Tree')

    def visitASTBinaryOp(self, ast):
        self.graph.node(str(id(ast)), ast.token.content)
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visitASTUnaryExpression(self, ast):
        self.graph.node(str(id(ast)), ast.token.content)
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visitASTLeaf(self, ast):
        self.graph.node(str(id(ast)), ast.token.content)
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visitASTType(self, ast):
        self.graph.node(str(id(ast)), ast.token.content)
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visitASTProgram(self, ast):
        assert ast.parent is None
        self.graph.node(str(id(ast)), "Program")

    def visitASTStatement(self, ast):
        self.graph.node(str(id(ast)), "Statement")
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))
