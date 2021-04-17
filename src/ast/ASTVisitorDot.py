from graphviz import Digraph

import src.DataType as DataType
from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import ASTPrintfInstruction, ASTUnaryExpression, ASTLiteral, ASTControlFlowStatement, \
    ASTFunctionDeclaration, ASTArrayDeclaration, ASTArrayInit, ASTReturnStatement, ASTFunctionCall


class ASTVisitorDot(ASTBaseVisitor):

    def __init__(self):
        super().__init__()
        self.graph = Digraph('Abstract Syntax Tree')

    def add_to_dot_node(self, ast, content=None):
        if content is not None:
            self.graph.node(str(id(ast)), content)
        else:
            self.graph.node(str(id(ast)), ast.get_content())

        if ast.parent is not None:
            self.graph.edge(str(id(ast.parent)), str(id(ast)))

    def visit_ast_leaf(self, ast):
        self.add_to_dot_node(ast)

    def visit_ast_literal(self, ast: ASTLiteral):
        content = None
        if ast.get_data_type_token() == DataType.DataTypeToken.CHAR:
            content = "'" + str(chr(int(ast.get_content()))) + "'"

        self.add_to_dot_node(ast, content)

    def visit_ast_internal(self, ast):
        super().visit_ast_internal(ast)
        self.add_to_dot_node(ast)

    def visit_ast_unary_expression(self, ast: ASTUnaryExpression):
        super().visit_ast_unary_expression(ast)
        self.add_to_dot_node(ast)

    def visit_ast_binary_expression(self, ast):
        super().visit_ast_binary_expression(ast)
        self.add_to_dot_node(ast)

    def visit_ast_array_init(self, ast: ASTArrayInit):
        super().visit_ast_array_init(ast)
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration(self, ast):
        super().visit_ast_variable_declaration(ast)
        self.add_to_dot_node(ast)

    def visit_ast_array_declaration(self, ast: ASTArrayDeclaration):
        super().visit_ast_array_declaration(ast)
        self.add_to_dot_node(ast)

    def visit_ast_variable_declaration_and_init(self, ast):
        super().visit_ast_variable_declaration_and_init(ast)
        self.add_to_dot_node(ast)

    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        super().visit_ast_printf_instruction(ast)
        self.add_to_dot_node(ast, f"printf({ast.get_content()})")

    def visit_ast_scope(self, ast):
        super().visit_ast_scope(ast)
        self.add_to_dot_node(ast)

    def visit_ast_control_flow_statement(self, ast: ASTControlFlowStatement):
        super().visit_ast_control_flow_statement(ast)
        self.add_to_dot_node(ast)

    def visit_ast_if_statement(self, ast):
        super().visit_ast_if_statement(ast)
        self.add_to_dot_node(ast)

    def visit_ast_while_loop(self, ast):
        super().visit_ast_while_loop(ast)
        self.add_to_dot_node(ast)

    def visit_ast_function_call(self, ast: ASTFunctionCall):
        super().visit_ast_function_call(ast)
        self.add_to_dot_node(ast)

    def visit_ast_function_declaration(self, ast: ASTFunctionDeclaration):
        super().visit_ast_function_declaration(ast)
        self.add_to_dot_node(ast)

    def visit_ast_return_statement(self, ast: ASTReturnStatement):
        super().visit_ast_return_statement(ast)
        self.add_to_dot_node(ast)
