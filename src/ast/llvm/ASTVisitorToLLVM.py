from src.ast.ASTBaseVisitor import *
from src.ast.llvm.LLVMBuilder import *


class ASTVisitorToLLVM(ASTBaseVisitor):

    def __init__(self):
        self.builder = LLVMBuilder()

    def build_while_loop(self, while_loop_ast: ASTWhileLoop):
        assert isinstance(while_loop_ast, ASTWhileLoop)

        current_function = self.builder.get_current_function()
        # The basic block the function was at before the while began (branch will be added to the correct beginning-of-while-loop label)
        before_while_basic_block = current_function.get_current_basic_block()
        label_of_condition = current_function.add_basic_block()
        before_while_basic_block.add_instruction(UnconditionalBranchInstruction(f'%{label_of_condition}'))

        resulting_reg_of_condition, data_type_of_condition = self.builder.compute_expression(while_loop_ast.get_condition())

        # First we need to keep track of the label of the condition block, then we make two new blocks: one for the code within the loop and one label for what happens after the loop
        basic_block_of_condition = current_function.get_current_basic_block()
        label_of_condition_if_true = current_function.add_basic_block()
        while_loop_ast.get_execution_body().accept(self)
        current_function.get_current_basic_block().add_instruction(UnconditionalBranchInstruction(f'%{label_of_condition}'))

        label_of_condition_if_false = current_function.add_basic_block()

        # Branch to the body of the loop or branch to the location after the loop, based on the outcome of the while loop condition
        basic_block_of_condition.add_instruction(ConditionalBranchInstruction(resulting_reg_of_condition, label_of_condition_if_true, label_of_condition_if_false))



    def build_if_statement(self, if_statement_ast: ASTIfStatement):
        assert isinstance(if_statement_ast, ASTIfStatement)

        current_function = self.builder.get_current_function()
        # The basic block the function was at before the if statement began (branch will be added to the correct beginning-of-if-statement label)
        before_if_basic_block = current_function.get_current_basic_block()

        if if_statement_ast.has_condition():

            # Calculates the expression as a condition, which either returns (TODO: True or False)
            resulting_reg, data_type = self.builder.compute_expression(if_statement_ast.get_condition())

            if data_type is not DataTypeToken.BOOL:
                raise NotImplementedError

            # This one becomes the new 'current' basic block of the function where instructions will automatically be added
            # Execution body of the if statement
            exec_body_label = current_function.add_basic_block()

            if not if_statement_ast.get_execution_body().is_empty():
                # First, construct the body of the function in llvm, adding instructions (starting from exec body) and basic blocks to the current function
                if_statement_ast.get_execution_body().accept(self)

            if if_statement_ast.has_else_statement():
                else_exec_body_label = self.build_if_statement(if_statement_ast.get_else_statement())
            else:
                # This means there is are no more else statements in this chain, so we can continue writing to the newest basic block
                else_exec_body_label = current_function.add_basic_block()

            if if_statement_ast.get_execution_body().is_empty():
                current_function.get_basic_block(exec_body_label).add_instruction(
                    UnconditionalBranchInstruction(f'%{else_exec_body_label}'))

            instruction = ConditionalBranchInstruction(resulting_reg, f"%{exec_body_label}", f"%{else_exec_body_label}")

            # Finish up the before_if_basic block with a conditional branch instruction to go either to the exec_body label or to the else_exec_body_label
            before_if_basic_block.add_instruction(instruction)

        else:

            exec_body_label = current_function.add_basic_block()
            if_statement_ast.get_execution_body().accept(self)

            # Must be an else statement (doesn't have any conditions)
            instruction = UnconditionalBranchInstruction(exec_body_label)
            before_if_basic_block.add_instruction(instruction)

        # Add a final branch instruction to the

        return exec_body_label

    def visit_ast_leaf(self, ast: ASTLeaf):
        super().visit_ast_leaf(ast)

    def visit_ast_internal(self, ast: ASTInternal):
        super().visit_ast_internal(ast)

    def visit_ast_if_statement(self, ast: ASTIfStatement):
        self.build_if_statement(ast)

    def visit_ast_while_loop(self, ast: ASTWhileLoop):
        self.build_while_loop(ast)

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
