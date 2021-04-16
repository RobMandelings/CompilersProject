import src.ast.ASTBaseVisitor as ASTBaseVisitor
import src.ast.ASTTokens as ASTTokens
import src.ast.ASTs as ASTs
import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMBuilder as LLVMBuilder
import src.llvm.LLVMInstruction as LLVMInstructions
from src.ast.ASTs import ASTFunctionDeclaration
from src.llvm.LLVMFunction import LLVMFunction
from src.llvm.LLVMValue import LLVMRegister


class ASTVisitorToLLVM(ASTBaseVisitor.ASTBaseVisitor):
    """
    Converts the ASTs to LLVM code using the proper builder methods.
    Completely builds every statement in the same order as the instructions will be placed in LLVM, for easier implementation
    and to avoid confusion
    """

    def __init__(self):
        self.builder = LLVMBuilder.LLVMBuilder()
        self.current_basic_block = None

    def get_builder(self):
        return self.builder

    def get_current_function(self):
        return self.builder.get_current_function()

    def get_current_basic_block(self):
        """
        Returns the current basic block we're working on, in the current function
        """
        return self.get_current_function().get_current_basic_block()

    def build_while_loop(self, while_loop_ast: ASTs.ASTWhileLoop):
        assert isinstance(while_loop_ast, ASTs.ASTWhileLoop)

        # The basic block the function was at before the while began
        # (branch will be added to the correct beginning-of-while-loop label)
        before_while_basic_block = self.get_current_basic_block()
        basic_block_of_condition, resulting_reg_of_condition = self.build_conditional_statement(while_loop_ast)
        before_while_basic_block.add_instruction(
            LLVMInstructions.UnconditionalBranchInstruction(basic_block_of_condition))

        # First we need to keep track of the label of the condition block, then we make two new blocks:
        # one for the code within the loop and one label for what happens after the loop
        while_loop_body_basic_block = LLVMBasicBlock.LLVMBasicBlock()
        after_while_loop_basic_block = LLVMBasicBlock.LLVMBasicBlock()

        # Add the basic block to the function so that it becomes the current basic block
        self.get_current_function().add_basic_block(while_loop_body_basic_block)

        for child in while_loop_ast.get_execution_body().children:
            if not isinstance(child, ASTs.ASTControlFlowStatement):
                child.accept(self)
            else:
                if child.control_flow_token == ASTTokens.ControlFlowToken.CONTINUE:
                    # For-loops only: make sure that the update step is executed before branching to the condition again
                    if while_loop_ast.get_update_step() is not None:
                        while_loop_ast.get_update_step().accept(self)
                    self.get_current_basic_block().add_instruction(
                        LLVMInstructions.UnconditionalBranchInstruction(basic_block_of_condition))

                    # Add a basic block to continue writing instructions
                    self.get_current_function().add_basic_block(LLVMBasicBlock.LLVMBasicBlock())
                elif child.control_flow_token == ASTTokens.ControlFlowToken.BREAK:
                    self.get_current_basic_block().add_instruction(
                        LLVMInstructions.UnconditionalBranchInstruction(after_while_loop_basic_block))
                    self.get_current_function().add_basic_block(LLVMBasicBlock.LLVMBasicBlock())
                elif child.control_flow_token == ASTTokens.ControlFlowToken.RETURN:
                    pass
                else:
                    raise NotImplementedError

        # Only used in the for loop, the update step is different from the execution body itself
        if while_loop_ast.get_update_step() is not None:
            while_loop_ast.get_update_step().accept(self)

        self.get_current_basic_block().add_instruction(
            LLVMInstructions.UnconditionalBranchInstruction(basic_block_of_condition))

        # Branch to the body of the loop or branch to the location after the loop, based on the outcome of the while loop condition
        basic_block_of_condition.add_instruction(
            LLVMInstructions.ConditionalBranchInstruction(resulting_reg_of_condition,
                                                          while_loop_body_basic_block,
                                                          after_while_loop_basic_block))

        self.get_current_function().add_basic_block(after_while_loop_basic_block)

    def build_if_statement_execution(self, if_statement_ast: ASTs.ASTIfStatement, if_statement_ending_basic_blocks):
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

    def build_conditional_statement(self, conditional_ast: ASTs.ASTConditionalStatement):
        """
        Adds a basic block and generates the instructions in this basic block to compute the result of the condition
        Used for branching to other basic blocks depending on the result (this branch instruction is up to you)
        """

        new_basic_block = LLVMBasicBlock.LLVMBasicBlock()
        self.get_current_function().add_basic_block(new_basic_block)

        # Calculates the expression as a condition, which either returns (TODO: True or False)
        resulting_reg = self.builder.compute_expression(conditional_ast.get_condition())

        return new_basic_block, resulting_reg

    def build_if_statement(self, if_statement_ast: ASTs.ASTIfStatement, if_statement_ending_basic_blocks):
        """
        if_statement_ending_basic_blocks: the last basic block of every if statement clause, used to add
        the final branch instructions to these basic blocks at the end of their execution
        e.g. with if (cond) { basicblock1 basicblock2 } else if (cond) { basicblockB1 basicblockB2 basicBlockB3 },
        if_statement_ending_basic_blocks yields [basicblock2, basicblockB3]
        """
        assert isinstance(if_statement_ast, ASTs.ASTIfStatement)

        # This must be an if (cond) {} or else if (cond) {} statement
        if if_statement_ast.has_condition():

            basic_block_of_condition, resulting_reg = self.build_conditional_statement(if_statement_ast)
            exec_body = self.build_if_statement_execution(if_statement_ast, if_statement_ending_basic_blocks)

            # 2) If the if statement has an else statement (else if {} ... or else {} ...) construct it as well
            if if_statement_ast.has_else_statement():
                else_statement_entry = self.build_if_statement(if_statement_ast.get_else_statement(),
                                                               if_statement_ending_basic_blocks)
            else:
                else_statement_entry = self.builder.get_current_function().add_basic_block()

            basic_block_of_condition.add_instruction(
                LLVMInstructions.ConditionalBranchInstruction(resulting_reg, exec_body,
                                                              else_statement_entry))

            # Return the conditional statement entry as it is the start of an if-statement with condition
            return basic_block_of_condition

        # This must be an else {} statement
        else:
            exec_body = self.build_if_statement_execution(if_statement_ast, if_statement_ending_basic_blocks)

            self.builder.get_current_function().add_basic_block()

            # Just return the execution body as there are no checks to be made
            return exec_body

    def visit_ast_leaf(self, ast: ASTs.ASTLeaf):
        super().visit_ast_leaf(ast)

    def visit_ast_internal(self, ast: ASTs.ASTInternal):
        super().visit_ast_internal(ast)

    def visit_ast_if_statement(self, ast: ASTs.ASTIfStatement):

        before_if_basic_block = self.builder.get_current_function().get_current_basic_block()
        if_statement_ending_basic_blocks = list()
        if_statement_entry = self.build_if_statement(ast, if_statement_ending_basic_blocks)
        basic_block_outside_if_statement = self.builder.get_current_function().get_current_basic_block()

        before_if_basic_block.add_instruction(
            LLVMInstructions.UnconditionalBranchInstruction(if_statement_entry))
        for basic_block in if_statement_ending_basic_blocks:
            assert isinstance(basic_block, LLVMBasicBlock.LLVMBasicBlock)
            if not basic_block.has_terminal_instruction():
                basic_block.add_instruction(
                    LLVMInstructions.UnconditionalBranchInstruction(basic_block_outside_if_statement))

    def visit_ast_while_loop(self, ast: ASTs.ASTWhileLoop):
        self.build_while_loop(ast)

    def visit_ast_binary_expression(self, ast: ASTs.ASTBinaryExpression):
        print(
            "WARN: binary expression directly visited in ASTVisitorToLLVM. Does nothing as it has no meaning by itself.")

    def visit_ast_assignment_expression(self, ast: ASTs.ASTAssignmentExpression):
        self.builder.assign_value_to_variable(ast)

    def visit_ast_variable_declaration_and_init(self, ast: ASTs.ASTVariableDeclarationAndInit):
        self.builder.declare_and_init_variable(ast)

    def visit_ast_variable_declaration(self, ast: ASTs.ASTVariableDeclaration):
        self.builder.declare_variable(ast)

    def visit_ast_printf_instruction(self, ast: ASTs.ASTPrintfInstruction):
        self.builder.print_variable(ast.get_content())

    def visit_ast_function_declaration(self, ast: ASTFunctionDeclaration):
        param_registers = list()

        for param in ast.get_params():
            assert isinstance(param, ASTs.ASTVariableDeclaration)
            param_registers.append(LLVMRegister(param.get_data_type()))

        return_type = ast.get_return_type().get_data_type()

        self.builder.add_function(LLVMFunction(ast.get_name(), return_type, param_registers))
        ast.get_execution_body().accept(self)

    def to_file(self, output_filename: str):
        self.builder.to_file(output_filename)
