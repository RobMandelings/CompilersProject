from src.ast.ASTBaseVisitor import *
from src.ast.llvm.LLVMBuilder import *


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
        self.llvm_builder.assign_value_to_variable(ast)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.llvm_builder.declare_and_init_variable(ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        self.llvm_builder.declare_variable(ast)

    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        self.llvm_builder.print_variable(ast.get_content())

    def to_file(self, output_filename: str):
        self.llvm_builder.to_file(output_filename)
