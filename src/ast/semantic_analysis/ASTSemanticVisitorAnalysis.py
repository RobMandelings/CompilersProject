from src.ast.ASTVisitors import ASTVisitor


class ASTVisitorSemanticAnalysis(ASTVisitor):

    def __init__(self):
        super().__init__()
        self.symbol_table_stack = list()

    def visitASTLeaf(self, ast):
        pass

    def visitASTInternal(self, ast):
        pass
