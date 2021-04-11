from src.ast.ASTBaseVisitor import *
from src.ast.llvm.LLVMBuilder import *


class ASTVisitorToLLVM(ASTBaseVisitor):
    """
    Converts the ASTs to LLVM code using the proper builder methods.
    Completely builds every statement in the same order as the instructions will be placed in LLVM, for easier implementation
    and to avoid confusion
    """

    def __init__(self):
        self.builder = LLVMBuilder()

    def build_while_loop(self, while_loop_ast: ASTWhileLoop):
        assert isinstance(while_loop_ast, ASTWhileLoop)

        current_function = self.builder.get_current_function()
        # The basic block the function was at before the while began (branch will be added to the correct beginning-of-while-loop label)
        before_while_basic_block = current_function.get_current_basic_block()
        condition = current_function.add_basic_block()
        before_while_basic_block.add_instruction(UnconditionalBranchInstruction(f'%{condition.get_number()}'))

        resulting_reg_of_condition, data_type_of_condition = self.builder.compute_expression(
            while_loop_ast.get_condition())

        # First we need to keep track of the label of the condition block, then we make two new blocks: one for the code within the loop and one label for what happens after the loop
        basic_block_of_condition = current_function.get_current_basic_block()
        condition_if_true = current_function.add_basic_block()
        while_loop_ast.get_execution_body().accept(self)
        current_function.get_current_basic_block().add_instruction(
            UnconditionalBranchInstruction(f'%{condition.get_number()}'))

        condition_if_false = current_function.add_basic_block()

        # Branch to the body of the loop or branch to the location after the loop, based on the outcome of the while loop condition
        basic_block_of_condition.add_instruction(
            ConditionalBranchInstruction(resulting_reg_of_condition, f'%{condition_if_true.get_number()}',
                                         f'%{condition_if_false.get_number()}'))

    def build_if_statement_execution(self, if_statement_ast: ASTIfStatement, if_statement_ending_basic_blocks):
        """
        if_statement_ending_basic_blocks: a list of the last basic block of the execution body that was added (after the accept)
        append_to_list: true if you want to append the basic block to the list of 'if statement ending basic blocks'
        false if not. For example, for the 'else' statement you wouldn't want to do this as it would result in branching to itself
        """
        # Execution body of the if statement
        exec_body_entry = self.builder.get_current_function().add_basic_block()

        # 1) construct the body of the function in llvm, adding instructions (starting from exec body)
        # and basic blocks to the current function
        if not if_statement_ast.get_execution_body().is_empty():
            if_statement_ast.get_execution_body().accept(self)

        # The last basic block of the execution body that was added (after the accept)
        if_statement_ending_basic_blocks.append(self.builder.get_current_function().get_current_basic_block())
        return exec_body_entry

    def build_conditional_statement(self, conditional_ast: ASTConditionalStatement):
        """
        Adds a basic block and generates the instructions in this basic block to compute the result of the condition
        Used for branching to other basic blocks depending on the result (this branch instruction is up to you)
        """

        new_basic_block = self.builder.get_current_function().add_basic_block()

        # Calculates the expression as a condition, which either returns (TODO: True or False)
        resulting_reg, data_type = self.builder.compute_expression(conditional_ast.get_condition())

        if data_type is not DataTypeToken.BOOL:
            raise NotImplementedError

        return new_basic_block, resulting_reg

    def build_if_statement(self, if_statement_ast: ASTIfStatement, if_statement_ending_basic_blocks):
        """
        if_statement_ending_basic_blocks: the last basic block of every if statement clause, used to add
        the final branch instructions to these basic blocks at the end of their execution
        e.g. with if (cond) { basicblock1 basicblock2 } else if (cond) { basicblockB1 basicblockB2 basicBlockB3 },
        if_statement_ending_basic_blocks yields [basicblock2, basicblockB3]
        """
        assert isinstance(if_statement_ast, ASTIfStatement)

        # This must be an if (cond) {} or else if (cond) {} statement
        if if_statement_ast.has_condition():

            conditional_statement_entry, resulting_reg = self.build_conditional_statement(if_statement_ast)
            exec_body_entry = self.build_if_statement_execution(if_statement_ast, if_statement_ending_basic_blocks)

            # 2) If the if statement has an else statement (else if {} ... or else {} ...) construct it as well
            if if_statement_ast.has_else_statement():
                else_statement_entry = self.build_if_statement(if_statement_ast.get_else_statement(),
                                                               if_statement_ending_basic_blocks)
            else:
                else_statement_entry = self.builder.get_current_function().add_basic_block()

            conditional_statement_entry.add_instruction(
                ConditionalBranchInstruction(resulting_reg, f"%{exec_body_entry.get_number()}",
                                             f"%{else_statement_entry.get_number()}"))

            # Return the conditional statement entry as it is the start of an if-statement with condition
            return conditional_statement_entry

        # This must be an else {} statement
        else:
            exec_body_entry = self.build_if_statement_execution(if_statement_ast, if_statement_ending_basic_blocks)

            self.builder.get_current_function().add_basic_block()

            # Just return the execution body as there are no checks to be made
            return exec_body_entry

    def visit_ast_leaf(self, ast: ASTLeaf):
        super().visit_ast_leaf(ast)

    def visit_ast_internal(self, ast: ASTInternal):
        super().visit_ast_internal(ast)

    def visit_ast_if_statement(self, ast: ASTIfStatement):

        before_if_basic_block = self.builder.get_current_function().get_current_basic_block()
        if_statement_ending_basic_blocks = list()
        if_statement_entry = self.build_if_statement(ast, if_statement_ending_basic_blocks)
        basic_block_outside_if_statement = self.builder.get_current_function().get_current_basic_block()

        before_if_basic_block.add_instruction(
            UnconditionalBranchInstruction(f'%{if_statement_entry.get_number()}'))
        for basic_block in if_statement_ending_basic_blocks:
            assert isinstance(basic_block, LLVMBasicBlock)
            if not basic_block.has_terminal_instruction():
                basic_block.add_instruction(
                    UnconditionalBranchInstruction(f'%{basic_block_outside_if_statement.get_number()}'))

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
