from src.ast.ASTBaseVisitor import *
from LLVMBuilder import *


class ASTVisitorToLLVM(ASTBaseVisitor):

    def __init__(self, output_filename):
        self.llvm_builder = LLVMBuilder()
        self.output_file = open(output_filename, "w+")


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
