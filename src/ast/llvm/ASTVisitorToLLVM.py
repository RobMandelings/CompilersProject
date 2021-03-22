from src.ast.ASTBaseVisitor import *
from src.ast.llvm.LLVMBuilder import *


class ASTVisitorToLLVM(ASTBaseVisitor):

    def __init__(self):
        self.builder = LLVMBuilder()

    def build_if_statement(self, if_statement_ast: ASTIfStatement):
        assert isinstance(if_statement_ast, ASTIfStatement)

        current_function = self.builder.get_current_function()
        # The basic block the function was at before the if statement began (branch will be added to the correct beginning-of-if-statement label)
        before_if_basic_block = current_function.get_current_basic_block()

        # This one becomes the new 'current' basic block of the function where instructions will automatically be added
        exec_body_label = current_function.add_basic_block()

        # First, construct the body of the function in llvm, adding instructions and basic blocks to the current function
        if_statement_ast.get_execution_body().accept(self)

        if if_statement_ast.has_condition():

            # Calculates the expression as a condition, which either returns (TODO: True or False)
            resulting_reg = self.builder.compute_expression(if_statement_ast.get_condition())

            if if_statement_ast.has_else_statement():
                else_exec_body_label = self.build_if_statement(if_statement_ast.get_else_statement())
            else:
                # This means there is are no more else statements in this chain, so we can continue writing to the newest basic block
                else_exec_body_label = current_function.add_basic_block()

            instruction = ConditionalBranchInstruction(resulting_reg, f"%{exec_body_label}", f"%{else_exec_body_label}")

            # Finish up the before_if_basic block
            before_if_basic_block.add_instruction(instruction)

        else:

            # Must be an if statements which never has any other conditions
            instruction = UnconditionalBranchInstruction(exec_body_label)
            before_if_basic_block.add_instruction(instruction)

        return exec_body_label

    def visit_ast_leaf(self, ast: ASTLeaf):
        super().visit_ast_leaf(ast)

    def visit_ast_internal(self, ast: ASTInternal):
        super().visit_ast_internal(ast)

    def visit_ast_if_statement(self, ast: ASTIfStatement):
        self.build_if_statement(ast)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        raise NotImplementedError

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        self.builder.assign_value_to_variable(ast)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.builder.declare_and_init_variable(ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        self.builder.declare_variable(ast)

    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        self.builder.print_variable(ast.get_content())

    def to_file(self, output_filename: str):
        self.builder.to_file(output_filename)
