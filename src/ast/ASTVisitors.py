from graphviz import Digraph
import abc


# TODO import asts to get some 'expected' types as parameters

class ASTVisitor:

    @abc.abstractmethod
    def visit_ast_leaf(self, ast):
        pass

    @abc.abstractmethod
    def visit_ast_internal(self, ast):
        pass

    @abc.abstractmethod
    def visitor_ast_binary_expression(self, ast):
        pass

    @abc.abstractmethod
    def visit_ast_variable_declaration(self, ast):
        pass

    @abc.abstractmethod
    def visit_ast_variable_declaration_and_init(self, ast):
        pass


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

    def visitor_ast_binary_expression(self, ast):
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration(self, ast):
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration_and_init(self, ast):
        self.add_to_dot_node(ast)
