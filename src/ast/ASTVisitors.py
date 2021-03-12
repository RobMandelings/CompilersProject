from graphviz import Digraph


class ASTVisitor:

    def visit_ast_leaf(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visit_ast_internal(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visit_ast_variable_declaration(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')

    def visit_ast_variable_declaration_and_init(self, ast):
        raise NotImplementedError('This method is meant to be generic and thus cannot be called')


class ASTVisitorDot(ASTVisitor):

    def __init__(self):
        super().__init__()
        self.graph = Digraph('Abstract Syntax Tree')

    def add_to_dot_node(self, ast):
        self.graph.node(str(id(ast)), ast.token.content)
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visit_ast_leaf(self, ast):
        self.add_to_dot_node(ast)

    def visit_ast_internal(self, ast):
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration(self, ast):
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration_and_init(self, ast):
        self.add_to_dot_node(ast)


class ASTVisitorSemanticAnalysis(ASTVisitor):

    def __init__(self):
        super().__init__()
        # Todo
        self.symbol_table = None

    def visit_ast_leaf(self, ast):
        pass

    def visit_ast_internal(self, ast):
        pass