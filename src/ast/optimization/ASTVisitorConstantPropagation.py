from src.ast.ASTBaseVisitor import *
from src.ast.semantic_analysis.SymbolTableManager import SymbolTableManager


class ASTVisitorConstantPropagation(ASTBaseVisitor):
    """
    Replaces identifiers in expressions with their value if it is known at compile-time.
    """

    def __init__(self, symbol_table_manager: SymbolTableManager):
        self.symbol_table_manager = symbol_table_manager
        # This needs to be the current scope you are in
        self.current_symbol_table = self.symbol_table_manager.get_global_symbol_table()

    def replace_identifier_ast_if_applicable(self, ast: ASTIdentifier):
        assert isinstance(ast, ASTIdentifier)

    def do_constant_propagation(self, ast: AST):
        if isinstance(ast, ASTBinaryExpression):
            if isinstance(ast.left, ASTIdentifier):
                self.left = self.replace_identifier_ast_if_applicable(ast.left)
            else:
                self.do_constant_propagation(ast.left)

            if isinstance(ast.right, ASTIdentifier):
                self.right = self.replace_identifier_ast_if_applicable(ast.right)
            else:
                self.do_constant_propagation(ast.right)
        elif isinstance(ast, ASTUnaryExpression):

            if isinstance(ast.value_applied_to_ast, ASTIdentifier):
                ast.value_applied_to_ast = self.replace_identifier_ast_if_applicable(ast.value_applied_to_ast)
            else:
                self.do_constant_propagation(ast.value_applied_to_ast)
        elif isinstance(ast, ASTIdentifier):
            variable = self.current_symbol_table.lookup_variable(ast.get_content())
            # TODO replace the current node with its

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        super().visit_ast_binary_expression(ast)
