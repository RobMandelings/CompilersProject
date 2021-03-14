from graphviz import Digraph

from src.ast.ASTToken import TokenType
from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import ASTPrintfInstruction


class ASTVisitorDot(ASTBaseVisitor):

    def __init__(self):
        super().__init__()
        self.graph = Digraph('Abstract Syntax Tree')

    def add_to_dot_node(self, ast, content=None):
        if content is not None:
            self.graph.node(str(id(ast)), content)
        else:
            self.graph.node(str(id(ast)), ast.token.content)

        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visit_ast_leaf(self, ast):
        super().visit_ast_leaf(ast)

        content = None
        if ast.get_token_type() == TokenType.CHAR_LITERAL:
            content = "'" + str(chr(int(ast.get_token_content()))) + "'"

        self.add_to_dot_node(ast, content)

    def visit_ast_internal(self, ast):
        super().visit_ast_internal(ast)
        self.add_to_dot_node(ast)

    def visit_ast_binary_expression(self, ast):
        super().visit_ast_binary_expression(ast)
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration(self, ast):
        super().visit_ast_variable_declaration(ast)
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration_and_init(self, ast):
        super().visit_ast_variable_declaration_and_init(ast)
        self.add_to_dot_node(ast)

    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        super().visit_ast_printf_instruction(ast)
        self.add_to_dot_node(ast, f"printf({ast.get_token_content()})")
