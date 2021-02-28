from AST import AST


class ASTInternal(AST):

    def __init__(self, node_category):
        super().__init__(node_category)
        self.children = list()

    def add_child(self, ast):
        ast.parent = self
        self.children.append(ast)

    def createDot(self, current_dot):
        raise NotImplementedError("Not implemented yet")

    def createAST(self, concrete_syntax_tree):


        pass

