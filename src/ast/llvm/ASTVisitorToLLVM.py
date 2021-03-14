from src.ast.ASTBaseVisitor import *
from LLVMBuilder import *


class ASTVisitorToLLVM(ASTBaseVisitor):

    def __init__(self):
        self.llvm_builder = LLVMBuilder()

    def visit_ast_leaf(self, ast: ASTLeaf):
        super().visit_ast_leaf(ast)

    def visit_ast_internal(self, ast: ASTInternal):
        super().visit_ast_internal(ast)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        raise NotImplementedError

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        identifier = ast.left.get_token_content()
        self.llvm_builder.assign_value_to_variable(identifier, ast.right)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        super().visit_ast_variable_declaration(ast)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        super().visit_ast_variable_declaration_and_init(ast)

    def to_file(self, output_filename: str):
        self.llvm_builder.to_file(output_filename)