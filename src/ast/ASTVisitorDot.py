from graphviz import Digraph

import src.DataType as DataType
from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import ASTPrintfInstruction, ASTUnaryExpression, ASTLiteral, ASTControlFlowStatement, \
    ASTFunctionDeclaration, ASTArrayVarDeclaration, ASTArrayInit, ASTReturnStatement, ASTFunctionCall, \
    ASTVarDeclaration, ASTIdentifier, ASTFunctionDefinition, ASTArrayVarDeclarationAndInit, ASTDereference, \
    ASTAccessArrayVarExpression


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

    def visit_ast_identifier(self, ast: ASTIdentifier):
        self.add_to_dot_node(ast, ast.get_name())

    def visit_ast_literal(self, ast: ASTLiteral):
        content = None
        if ast.get_data_type_token() == DataType.DataTypeToken.CHAR:
            test = ast.get_content()
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

    def visit_ast_var_declaration(self, ast: ASTVarDeclaration):
        super().visit_ast_var_declaration(ast)
        self.add_to_dot_node(ast)

    def visit_ast_array_declaration(self, ast: ASTArrayVarDeclaration):
        super().visit_ast_array_declaration(ast)
        self.add_to_dot_node(ast)

    def visit_ast_var_declaration_and_init(self, ast):
        super().visit_ast_var_declaration_and_init(ast)
        self.add_to_dot_node(ast)

    def visit_ast_dereference(self, ast: ASTDereference):
        super().visit_ast_dereference(ast)
        self.add_to_dot_node(ast)

    def visit_ast_array_declaration_and_init(self, ast: ASTArrayVarDeclarationAndInit):
        super().visit_ast_array_declaration_and_init(ast)
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

    def visit_ast_function_definition(self, ast: ASTFunctionDefinition):
        super().visit_ast_function_definition(ast)
        self.add_to_dot_node(ast)

    def visit_ast_return_statement(self, ast: ASTReturnStatement):
        super().visit_ast_return_statement(ast)
        self.add_to_dot_node(ast)

    def visit_ast_access_element(self, ast: ASTAccessArrayVarExpression):
        super().visit_ast_access_element(ast)
        self.add_to_dot_node(ast, content='access[]')
