import src.DataType as DataType
import src.ast.ASTBaseVisitor as ASTBaseVisitor
import src.ast.ASTTokens as ASTTokens
import src.ast.ASTs as ASTs
import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMBuilder as LLVMBuilder
import src.llvm.LLVMFunction as LLVMFunctions
import src.llvm.LLVMInstruction as LLVMInstructions
import src.llvm.LLVMSymbolTable as LLVMSymbolTable
import src.llvm.LLVMValue as LLVMValue
from src.ast.ASTs import ASTFunctionDeclaration, ASTReturnStatement, ASTScope, ASTFunctionCall, ASTFunctionDefinition, \
    ASTControlFlowStatement


class ASTVisitorToLLVM(ASTBaseVisitor.ASTBaseVisitor):
    """
    Converts the ASTs to LLVM code using the proper builder methods.
    Completely builds every statement in the same order as the instructions will be placed in LLVM, for easier implementation
    and to avoid confusion
    """

    def __init__(self):
        """
        while_loop_basic_blocks: dictionary which holds as a key the instance of an ASTWhileLoop, and as values the following basic blocks:
            - basic block of condition
            - after while loop basic block (outside the body)
        """
        self.builder = LLVMBuilder.LLVMBuilder()
        self.current_basic_block = None

        self.while_loop_basic_blocks = dict()

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
            LLVMInstructions.LLVMUnconditionalBranchInstruction(basic_block_of_condition))

        # First we need to keep track of the label of the condition block, then we make two new blocks:
        # one for the code within the loop and one label for what happens after the loop
        while_loop_body_basic_block = LLVMBasicBlock.LLVMBasicBlock()
        after_while_loop_basic_block = LLVMBasicBlock.LLVMBasicBlock()

        self.while_loop_basic_blocks[while_loop_ast] = {
            "basic_block_of_condition": basic_block_of_condition,
            "after_while_loop_basic_block": after_while_loop_basic_block
        }

        # Add the basic block to the function so that it becomes the current basic block
        self.get_current_function().add_basic_block(while_loop_body_basic_block)

        for child in while_loop_ast.get_execution_body().children:
            child.accept(self)

        # Only used in the for loop, the update step is different from the execution body itself
        if while_loop_ast.get_update_step() is not None:
            while_loop_ast.get_update_step().accept(self)

        self.get_current_basic_block().add_instruction(
            LLVMInstructions.LLVMUnconditionalBranchInstruction(basic_block_of_condition))

        # Branch to the body of the loop or branch to the location after the loop, based on the outcome of the while loop condition
        basic_block_of_condition.add_instruction(
            LLVMInstructions.LLVMConditionalBranchInstruction(resulting_reg_of_condition,
                                                              while_loop_body_basic_block,
                                                              after_while_loop_basic_block))

        self.get_current_function().add_basic_block(after_while_loop_basic_block)

    def visit_ast_control_flow_statement(self, ast: ASTControlFlowStatement):

        while_loop = None
        current_node = ast
        while while_loop is None and current_node.parent is not None:
            current_node = current_node.parent
            if isinstance(current_node, ASTs.ASTWhileLoop):
                while_loop = current_node

        assert while_loop is not None, "No while loop was found!"

        while_loop_basic_blocks = self.while_loop_basic_blocks[while_loop]
        basic_block_of_condition = while_loop_basic_blocks['basic_block_of_condition']
        after_while_loop_basic_block = while_loop_basic_blocks['after_while_loop_basic_block']

        if ast.control_flow_token == ASTTokens.ControlFlowToken.CONTINUE:
            # For-loops only: make sure that the update step is executed before branching to the condition again
            if while_loop.get_update_step() is not None:
                while_loop.get_update_step().accept(self)
            self.get_current_basic_block().add_instruction(
                LLVMInstructions.LLVMUnconditionalBranchInstruction(basic_block_of_condition))

            # Add a basic block to continue writing instructions
            self.get_current_function().add_basic_block(LLVMBasicBlock.LLVMBasicBlock())
        elif ast.control_flow_token == ASTTokens.ControlFlowToken.BREAK:
            self.get_current_basic_block().add_instruction(
                LLVMInstructions.LLVMUnconditionalBranchInstruction(after_while_loop_basic_block))
            self.get_current_function().add_basic_block(LLVMBasicBlock.LLVMBasicBlock())
        else:
            raise NotImplementedError

        super().visit_ast_control_flow_statement(ast)

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
        resulting_reg = self.builder.compute_expression(conditional_ast.get_condition(), force_boolean_result=True)

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
                LLVMInstructions.LLVMConditionalBranchInstruction(resulting_reg, exec_body,
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
            LLVMInstructions.LLVMUnconditionalBranchInstruction(if_statement_entry))
        for basic_block in if_statement_ending_basic_blocks:
            assert isinstance(basic_block, LLVMBasicBlock.LLVMBasicBlock)
            if not basic_block.has_terminal_instruction():
                basic_block.add_instruction(
                    LLVMInstructions.LLVMUnconditionalBranchInstruction(basic_block_outside_if_statement))

    def visit_ast_while_loop(self, ast: ASTs.ASTWhileLoop):
        self.build_while_loop(ast)

    def visit_ast_binary_expression(self, ast: ASTs.ASTBinaryExpression):
        print(
            "WARN: binary expression directly visited in ASTVisitorToLLVM. Does nothing as it has no meaning by itself.")

    def visit_ast_assignment_expression(self, ast: ASTs.ASTAssignmentExpression):
        self.builder.assign_value(ast)

    def visit_ast_var_declaration_and_init(self, ast: ASTs.ASTVarDeclarationAndInit):
        self.builder.declare_and_init_variable(ast)

    def visit_ast_var_declaration(self, ast: ASTs.ASTVarDeclaration):
        self.builder.declare_variable(ast)

    def visit_ast_printf_instruction(self, ast: ASTs.ASTPrintfInstruction):
        self.builder.print_variable(ast.get_content())

    def on_scope_entered(self):
        new_symbol_table = LLVMSymbolTable.LLVMSymbolTable()
        new_symbol_table.parent = self.builder.get_last_symbol_table()
        self.builder.symbol_table_stack.append(new_symbol_table)

    def on_scope_exit(self):
        self.builder.symbol_table_stack.pop()

    def visit_ast_scope(self, ast: ASTScope):
        self.on_scope_entered()
        super().visit_ast_scope(ast)
        self.on_scope_exit()

    def visit_ast_function_call(self, ast: ASTFunctionCall):
        self.builder.compute_expression(ast)

    def visit_ast_function_declaration(self, ast: ASTFunctionDeclaration):

        param_data_types = list()

        for param in ast.get_params():
            param_data_types.append(param.get_data_type())

        self.builder.get_function_holder().add_function(
            LLVMFunctions.LLVMDeclaredFunction(ast.get_identifier(), ast.get_return_type_ast().get_data_type(),
                                               param_data_types))

    def visit_ast_function_definition(self, ast: ASTFunctionDefinition):
        param_registers = list()

        for param in ast.get_function_declaration().get_params():
            assert isinstance(param, ASTs.ASTVarDeclaration)
            param_registers.append(LLVMValue.LLVMRegister(param.get_data_type()))

        assert len(param_registers) == len(ast.get_function_declaration().get_params())

        return_type = ast.get_function_declaration().get_return_type_ast().get_data_type()

        self.builder.get_function_holder().add_function(
            LLVMFunctions.LLVMDefinedFunction(ast.get_function_declaration().get_identifier(), return_type,
                                              param_registers))
        self.builder.get_function_holder().set_current_function(
            self.get_builder().get_function_holder().get_function(ast.get_function_declaration().get_identifier()))

        # Now that the function has been created, loop again over each of the parameters
        for i in range(len(ast.get_function_declaration().get_params())):
            param_register = param_registers[i]
            param = ast.get_function_declaration().get_params()[i]
            assert isinstance(param, ASTs.ASTVarDeclaration)
            resulting_reg = self.builder.declare_variable(param)
            self.builder.get_current_function().add_instruction(
                LLVMInstructions.LLVMStoreInstruction(resulting_reg, param_register))

        ast.get_execution_body().accept(self)

    def visit_ast_array_declaration(self, ast: ASTs.ASTArrayVarDeclaration):
        self.builder.declare_array(ast)

    def visit_ast_array_init(self, ast: ASTs.ASTArrayInit):
        raise NotImplementedError

    def visit_ast_array_declaration_and_init(self, ast: ASTs.ASTArrayVarDeclarationAndInit):
        self.builder.declare_and_init_array(ast)

    def visit_ast_return_statement(self, ast: ASTReturnStatement):

        if ast.get_return_value() is not None:

            if isinstance(ast.get_return_value(), ASTs.ASTExpression):
                return_value = self.builder.compute_expression(ast.get_return_value())
            elif isinstance(ast.get_return_value(), ASTs.ASTIdentifier):
                variable_register = self.builder.get_variable_register(ast.get_return_value().get_name())
                return_value = LLVMValue.LLVMRegister(DataType.DataType(variable_register.get_data_type().get_token(),
                                                                        variable_register.get_data_type().get_pointer_level() - 1))
                self.builder.get_current_function().add_instruction(
                    LLVMInstructions.LLVMLoadInstruction(return_value, variable_register))
            elif isinstance(ast.get_return_value(), ASTs.ASTLiteral):
                return_value = LLVMValue.LLVMLiteral(ast.get_return_value().get_value(),
                                                     ast.get_return_value().get_data_type())
            else:
                raise NotImplementedError

        else:
            
            return_value = None

        self.builder.get_current_function().add_instruction(LLVMInstructions.LLVMReturnInstruction(return_value))
        self.builder.get_current_function().add_basic_block()

    def to_file(self, output_filename: str):
        self.builder.to_file(output_filename)
