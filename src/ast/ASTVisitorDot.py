from graphviz import Digraph

from src.ast.ASTVisitor import ASTVisitor


class ASTVisitorDot(ASTVisitor):

    def __init__(self):
        super().__init__()
        self.graph = Digraph('Abstract Syntax Tree')

    def add_to_dot_node(self, ast):
        self.graph.node(str(id(ast)), ast.token.content)
        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visit_ast_leaf(self, ast):
        super().visit_ast_leaf(ast)
        self.add_to_dot_node(ast)

    def visit_ast_internal(self, ast):
        super().visit_ast_internal(ast)
        self.add_to_dot_node(ast)

    def visitor_ast_binary_expression(self, ast):
        super().visitor_ast_binary_expression(ast)
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration(self, ast):
        super().visit_ast_variable_declaration(ast)
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration_and_init(self, ast):
        super().visit_ast_variable_declaration_and_init(ast)
        self.add_to_dot_node(ast)
