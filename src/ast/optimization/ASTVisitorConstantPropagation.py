from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import ASTVariableDeclarationAndInit, ASTAssignmentExpression


class ASTVisitorConstantPropagation(ASTBaseVisitor):

    def __init__(self):
        pass

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        super().visit_ast_assignment_expression(ast)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        super().visit_ast_variable_declaration_and_init(ast)
