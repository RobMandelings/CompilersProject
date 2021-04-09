from src.ast.ASTs import *
from src.ast.llvm.LLVMFunction import *
from src.ast.llvm.LLVMGlobalContainer import LLVMGlobalContainer
from src.ast.llvm.LLVMInstruction import *
from src.ast.llvm.LLVMSymbolTable import *


class LLVMBuilder(IToLLVM):

    def __init__(self):
        self.global_container = LLVMGlobalContainer()
        self.functions = list()
        self.functions.append(LLVMFunction("main"))
        self.symbol_table = LLVMSymbolTable()
        pass

    def get_current_function(self):
        """
        Returns the current function that is being generated in LLVM code. Instructions should be appended to this
        function's current basic block
        """
        function = self.functions[-1]
        assert isinstance(function, LLVMFunction)
        return function

    def get_global_container(self):
        assert isinstance(self.global_container, LLVMGlobalContainer)
        return self.global_container

    def build_while_loop(self, while_loop_ast: ASTWhileLoop):
        pass

    def build_if_statement(self, if_statement_ast: ASTIfStatement):
        assert isinstance(if_statement_ast, ASTIfStatement)

        current_function = self.get_current_function()
        # The basic block the function was at before the if statement began (branch will be added to the correct beginning-of-if-statement label)
        before_if_basic_block = current_function.get_current_basic_block()

        if if_statement_ast.has_condition():

            # Calculates the expression as a condition, which either returns (TODO: True or False)
            resulting_reg, data_type = self.compute_expression(if_statement_ast.get_condition())

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

    def compute_expression(self, ast: AST):
        """
        Computes an expression of the given AST, generating the corresponding instructions in the process
        ast: the AST to compute the expression for

        returns: <value, data_type>:
        - value: holds the value of the computed expression. Can either be
            - The register that was last used to compute this expression
            - Or a literal if possible
        - data_type: the resulting data type of the operation (DataTypeToken.INT, FLOAT,...)
        """

        if isinstance(ast, ASTBinaryExpression):
            operand1, data_type1 = self.compute_expression(ast.left)
            operand2, data_type2 = self.compute_expression(ast.right)

            instruction = None
            operation = ast.get_token()
            register_to_return = self.get_current_function().get_new_register()

            if isinstance(operation, BinaryArithmeticExprToken):
                instruction = BinaryArithmeticInstruction(register_to_return,
                                                          operation, data_type1, operand1, data_type2, operand2)
            elif isinstance(operation, RelationalExprToken):
                instruction = CompareInstruction(register_to_return, operation, data_type1,
                                                 operand1, data_type2, operand2)
            else:
                raise NotImplementedError("This type of instructions are not yet supported")

            assert isinstance(instruction, AssignInstruction)
            self.get_current_function().add_instruction(instruction)

            return register_to_return, instruction.get_resulting_data_type()

        elif isinstance(ast, ASTUnaryExpression):
            # TODO compute unary expressions

            if isinstance(ast, ASTUnaryArithmeticExpression):

                raise NotImplementedError
                value_register = self.compute_expression(ast.value_applied_to)

            elif isinstance(ast, ASTUnaryPointerExpression):
                raise NotImplementedError
            else:
                raise NotImplementedError

        elif isinstance(ast, ASTLiteral):
            # If it's a literal, just return the value and data type of this value instead of creating a register for it
            return ast.get_value(), ast.get_data_type()
        elif isinstance(ast, ASTVariable):

            # First look up the variable in the symbol table, then retrieve the data type of this variable
            # TODO remove symbol table and put into some kind of dictionary
            variable = self.symbol_table.lookup_variable(ast.get_content())
            variable_data_type = variable.get_data_type()

            # We're assuming the variable register is always of pointer type, so first load the variable value into a register and return it

            register_to_return = self.get_current_function().get_new_register()
            self.get_current_function().add_instruction(
                LoadInstruction(register_to_return, variable.get_data_type(), variable.get_current_register()))
            return register_to_return, variable.get_data_type()
        else:
            raise NotImplementedError

    def _convert_float_register_to(self, register, to_type: DataTypeToken):
        register_to_return = f"%{self.register_count}"

        if to_type != DataTypeToken.FLOAT:
            self.instructions.append(
                f"{self.register_count} = fptosi float {register} to {get_llvm_type(to_type)}")
            self.register_count += 1
            return register_to_return

        return register

    # TODO also be able to print literals
    def print_variable(self, variable_name):
        variable = self.symbol_table.lookup_variable(variable_name)
        assert variable is not None

        register_to_print = self.get_current_function().get_new_register()

        self.get_current_function().add_instruction(
            LoadInstruction(register_to_print, variable.get_data_type(),
                            variable.get_current_register()))

        # The global variable that contains the string of the corresponding type of variable to call (printf(%i, your_int))
        # has the string %i\00 as type to use for the print. The global variable contains this string
        global_var_data_type = self.get_global_container().get_printf_type_string(variable.get_data_type())
        self.get_current_function().add_instruction(PrintfInstruction(register_to_print, global_var_data_type))

    def declare_variable(self, ast: ASTVariableDeclaration):
        resulting_register = self.get_current_function().get_new_register()
        declared_variable = LLVMVariableSymbol(ast.var_name_ast.get_content(), ast.data_type_ast.get_token(),
                                               resulting_register)
        self.symbol_table.insert_symbol(
            declared_variable)

        instruction = AllocaInstruction(f'{resulting_register}', declared_variable.get_data_type())
        self.get_current_function().add_instruction(instruction)

    def declare_and_init_variable(self, ast: ASTVariableDeclarationAndInit):
        """
        Declares and initializes a variable using LLVM instructions. Computes expressions if necessary
        Adds the corresponding instructions to the current basic block
        """
        value_to_store, data_type = self.compute_expression(ast.value)

        register = self.get_current_function().get_new_register()

        # TODO remove from code: don't work with symbol table anymore
        declared_variable = LLVMVariableSymbol(ast.var_name_ast.get_content(), ast.data_type_ast.get_token(),
                                               register)
        self.symbol_table.insert_symbol(declared_variable)

        data_type = declared_variable.get_data_type()
        self.get_current_function().add_instruction(AllocaInstruction(f'{register}', data_type))
        self.get_current_function().add_instruction(StoreInstruction(f'{register}', value_to_store, data_type))

    def assign_value_to_variable(self, ast: ASTAssignmentExpression):
        """
        Assigns a value to an existing variable (which has a current register),
        generating instructions in the process and adding them to the current basic block
        """
        # TODO Type conversions are not supported yet
        right = ast.get_right()

        # TODO remove from code: don't work with symbol table anymore
        variable_symbol = self.symbol_table.lookup_variable(ast.get_variable().get_content())

        # The current register of the variable to-be-assigned
        current_variable_reg = variable_symbol.get_current_register()

        # The data type of the variable to-be-assigned
        current_variable_data_type = variable_symbol.get_data_type()

        computed_expression_value, computed_data_type = self.compute_expression(right)

        if computed_data_type.is_pointer_type():
            # TODO: This register is used to load from pointer type into an actual value of that data type (sure?)
            value_to_store = self.get_current_function().get_new_register()
            self.get_current_function().add_instruction(
                LoadInstruction(value_to_store, current_variable_data_type, computed_expression_value))
        else:
            value_to_store = computed_expression_value

        self.get_current_function().add_instruction(
            StoreInstruction(current_variable_reg, value_to_store, current_variable_data_type))

    def _generate_begin_of_file(self):
        begin_of_file = ""
        begin_of_file += "declare i32 @printf(i8*, ...)\n"
        # begin_of_file += "@.i = private unnamed_addr constant [3 x i8] c\"%i\\00\", align 1\n"
        begin_of_file += "define i32 @main() {\n"
        begin_of_file += "    start:\n"
        return begin_of_file

    def _generate_end_of_file(self):
        end_of_file = ""
        end_of_file += "; we exit with code 0 = success\n"
        end_of_file += "ret i32 0\n"
        end_of_file += "}\n"
        return end_of_file

    def to_file(self, filename: str):
        f = open(filename, "w+")
        f.write(self.to_llvm())
        f.close()

    # TODO optimize
    def to_llvm(self):
        llvm_code = self.get_global_container().to_llvm() + "\n"

        # Remove this and replace with just function things and other initializations
        llvm_code += self._generate_begin_of_file() + "\n"

        for function in self.functions:
            llvm_code += function.to_llvm()

        llvm_code += self._generate_end_of_file()

        return llvm_code
