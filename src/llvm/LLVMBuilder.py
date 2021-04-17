import src.DataType as DataType
import src.ast.ASTTokens as ASTTokens
import src.ast.ASTs as ASTs
import src.llvm.LLVMFunction as LLVMFunctions
import src.llvm.LLVMGlobalContainer as LLVMGlobalContainer
import src.llvm.LLVMInstruction as LLVMInstructions
import src.llvm.LLVMInterfaces as LLVMInterfaces
import src.llvm.LLVMSymbolTable as LLVMSymbolTable
import src.llvm.LLVMUtils as LLVMUtils
import src.llvm.LLVMValue as LLVMValues
from src.llvm import LLVMValue


class LLVMBuilder(LLVMInterfaces.IToLLVM):

    def __init__(self):
        """
        variable_holder: holds variables and their corresponding registers
        """
        self.global_container = LLVMGlobalContainer.LLVMGlobalContainer()
        self.functions = list()
        # Not really a symbol table but just to keep track of the registers assigned to the variables for later outputting
        self.symbol_table_stack = list()
        self.symbol_table_stack.append(LLVMSymbolTable.LLVMSymbolTable())

    def get_printf_function_declaration(self):
        return 'declare dso_local i32 @printf(i8*, ...)'

    def get_last_symbol_table(self):
        last_symbol_table = self.symbol_table_stack[-1]
        assert isinstance(last_symbol_table, LLVMSymbolTable.LLVMSymbolTable)
        return last_symbol_table

    def get_variable_register(self, variable_name: str):
        return self.get_last_symbol_table().get_variable_register(variable_name)

    def update_numbering(self, counter):
        """
        Does nothing as it only applies to LLVMFunctions and below
        """
        pass

    def find_best_match(self, function_identifier: str, params):

        assert isinstance(function_identifier, str)
        functions_with_same_nr_params = list()

        for function in self.functions:
            assert isinstance(function, LLVMFunctions.LLVMFunction)

            if not function.identifier == function_identifier:
                continue

            if len(function.params) == len(params):
                functions_with_same_nr_params.append(function)

        if len(functions_with_same_nr_params) > 1:
            raise NotImplementedError('We currently do not support function which overloaded parameters')
        else:
            assert len(functions_with_same_nr_params) != 0
            return functions_with_same_nr_params[0]

    def add_function(self, function: LLVMFunctions.LLVMFunction):
        self.functions.append(function)

    def create_function_call(self, ast: ASTs.ASTFunctionCall):
        best_match_function = self.find_best_match(ast.get_function_called().get_name(), ast.get_params())

        params_llvm_value = list()

        for param in ast.get_params():
            resulting_llvm_value = self.compute_expression(param)
            params_llvm_value.append(resulting_llvm_value)

        self.get_current_function().add_instruction(
            LLVMInstructions.CallInstruction(best_match_function, params_llvm_value))

    def get_current_function(self):
        """
        Returns the current function that is being generated in LLVM code. Instructions should be appended to this
        function's current basic block
        """
        function = self.functions[-1]
        assert isinstance(function, LLVMFunctions.LLVMFunction)
        return function

    def get_global_container(self):
        assert isinstance(self.global_container, LLVMGlobalContainer.LLVMGlobalContainer)
        return self.global_container

    def create_register(self, data_type=None):
        """
        Creates a register with specific data type and returns this register
        """
        register = LLVMValues.LLVMRegister(data_type)
        return register

    def compute_compare_expression(self, operation: ASTTokens.RelationalExprToken, operand1: LLVMValues.LLVMValue,
                                   operand2: LLVMValues.LLVMValue):

        # TODO remove duplicate code
        if operand1.get_data_type() != operand2.get_data_type():

            richest_data_type = DataType.DataType.get_resulting_data_type(operand1.get_data_type(),
                                                                          operand2.get_data_type())
            if operand1 == richest_data_type:
                richest_data_type_index = 0
            else:
                richest_data_type_index = 1

            # If it is -1 they are equally rich
            if richest_data_type_index == 0:
                richest_value = operand1
                poorest_value = operand2

            else:

                richest_value = operand2
                poorest_value = operand1

            resulting_data_type = richest_value.get_data_type()

            # Must be a literal so just change the notation of the operand
            if isinstance(poorest_value, LLVMValues.LLVMLiteral):

                converted_poorest_value = LLVMValues.LLVMLiteral(
                    LLVMUtils.get_llvm_for_literal(poorest_value.get_value(), resulting_data_type),
                    poorest_value.get_data_type())

            # Must be a register
            elif isinstance(poorest_value, LLVMValues.LLVMRegister):

                converted_poorest_value = self.get_current_function().get_new_register().set_data_type(
                    operand1.get_data_type())

                self.get_current_function().add_instruction(
                    LLVMInstructions.DataTypeConvertInstruction(converted_poorest_value, poorest_value))

            # Convert the richest register to scientific notation as well if necessary

            else:
                raise ValueError('Register must either be a literal or a register')

            if poorest_value == operand1:
                operand1 = converted_poorest_value
            else:
                operand2 = converted_poorest_value

            if (isinstance(richest_value, LLVMValues.LLVMLiteral) and
                    richest_value.get_data_type().get_token() == (
                            DataType.DataTypeToken.FLOAT | DataType.DataTypeToken.DOUBLE)):

                if richest_value == operand1:
                    operand1 = LLVMUtils.get_llvm_for_literal(richest_value, operand1.get_data_type())
                else:
                    operand2 = LLVMUtils.get_llvm_for_literal(richest_value, operand2.get_data_type())

        compare_instruction = LLVMInstructions.CompareInstruction(operation, operand1, operand2)
        self.get_current_function().add_instruction(compare_instruction)

        return compare_instruction.get_resulting_register()

    def compute_expression(self, ast: ASTs.AST):
        """
        Computes an expression of the given AST, generating the corresponding instructions in the process
        ast: the AST to compute the expression for

        returns: LLVMValue:
        """

        if isinstance(ast, ASTs.ASTBinaryExpression):
            operand1 = self.compute_expression(ast.left)
            operand2 = self.compute_expression(ast.right)

            instruction = None
            operation = ast.get_token()

            if isinstance(operation, ASTs.BinaryArithmeticExprToken):
                register_to_return = self.get_current_function().get_new_register(
                    DataType.DataType.get_resulting_data_type(operand1.get_data_type(), operand2.get_data_type()))
                instruction = LLVMInstructions.BinaryArithmeticInstruction(register_to_return,
                                                                           operation, operand1,
                                                                           operand2)
            elif isinstance(operation, ASTTokens.RelationalExprToken):

                return self.compute_compare_expression(operation, operand1, operand2)
            else:
                raise NotImplementedError("This type of instructions are not yet supported")

            if instruction is not None:
                assert isinstance(instruction, LLVMInstructions.AssignInstruction)
                self.get_current_function().add_instruction(instruction)
                return register_to_return

        elif isinstance(ast, ASTs.ASTUnaryExpression):
            # TODO compute unary expressions

            if isinstance(ast, ASTs.ASTUnaryArithmeticExpression):

                raise NotImplementedError
                value_register = self.compute_expression(ast.value_applied_to)

            elif isinstance(ast, ASTs.ASTUnaryPointerExpression):
                raise NotImplementedError
            else:
                raise NotImplementedError

        elif isinstance(ast, ASTs.ASTLiteral):
            # If it's a literal, just return the value and data type of this value instead of creating a register for it
            return LLVMValues.LLVMLiteral(ast.get_value(), ast.get_data_type())
        elif isinstance(ast, ASTs.ASTVariable):

            # First look up the variable in the symbol table, then retrieve the data type of this variable
            # TODO remove symbol table and put into some kind of dictionary
            variable_register = self.get_variable_register(ast.get_content())

            # We're assuming the variable register is always of pointer type,
            # so first load the variable value into a register and return it

            # TODO not tested with pointers
            register_to_return = self.get_current_function().get_new_register(
                DataType.DataType(variable_register.get_data_type().get_token(), 0))
            self.get_current_function().add_instruction(
                LLVMInstructions.LoadInstruction(register_to_return, variable_register))
            return register_to_return
        else:
            raise NotImplementedError

    # TODO also be able to print literals
    def print_variable(self, variable_name):
        variable_register = self.get_variable_register(variable_name)
        assert variable_register is not None

        assert variable_register.get_data_type().get_pointer_level() == 1, "We currently support no pointers"
        register_to_print = self.get_current_function().get_new_register(
            DataType.DataType(variable_register.get_data_type().get_token(), 0))

        self.get_current_function().add_instruction(
            LLVMInstructions.LoadInstruction(register_to_print,
                                             variable_register))

        # The global variable that contains the string of the corresponding type of variable to call (printf(%i, your_int))
        # has the string %i\00 as type to use for the print. The global variable contains this string
        global_var_data_type = self.get_global_container().get_printf_type_string(register_to_print.get_data_type())
        resulting_register = self.get_current_function().get_new_register()
        # TODO handle assignments: printing variable results in the amount of characters printed, but they need to be
        # able to be assigned to a variable
        instruction = LLVMInstructions.PrintfInstruction(register_to_print, global_var_data_type)
        self.get_current_function().add_instruction(instruction)

        return resulting_register

    def declare_variable(self, ast: ASTs.ASTVariableDeclaration):
        resulting_register = self.get_current_function().get_new_register(
            DataType.DataType(ast.get_data_type().get_token(), ast.get_data_type().get_pointer_level() + 1))
        self.get_last_symbol_table().insert_variable(ast.get_content(), resulting_register)

        instruction = LLVMInstructions.AllocaInstruction(resulting_register)
        self.get_current_function().add_instruction(instruction)

    def declare_and_init_variable(self, ast: ASTs.ASTVariableDeclarationAndInit):
        """
        Declares and initializes a variable using LLVM instructions. Computes expressions if necessary
        Adds the corresponding instructions to the current basic block
        """
        value_to_store = self.compute_expression(ast.value)

        new_register = self.get_current_function().get_new_register(
            DataType.DataType(ast.get_data_type().get_token(), ast.get_data_type().get_pointer_level() + 1))

        # TODO remove from code: don't work with symbol table anymore
        self.get_last_symbol_table().insert_variable(ast.var_name_ast.get_content(), new_register)

        self.get_current_function().add_instruction(LLVMInstructions.AllocaInstruction(new_register))
        self.get_current_function().add_instruction(LLVMInstructions.StoreInstruction(new_register, value_to_store))

    def declare_array(self, ast: ASTs.ASTArrayDeclaration):
        """
        Declares an array using LLVM instructions
        """
        resulting_register = LLVMValue.LLVMRegister(
                DataType.DataType(ast.get_data_type().get_token(), ast.get_data_type().get_pointer_level() + 1))
        llvm_size = LLVMValue.LLVMLiteral(ast.get_size().get_value(), ast.get_size().get_data_type())
        self.get_last_symbol_table().insert_array(ast.get_var_name(), resulting_register, llvm_size)
        instruction = LLVMInstructions.AllocaArrayInstruction(resulting_register, llvm_size)
        self.get_current_function().add_instruction(instruction)

    def assign_value(self, ast: ASTs.ASTAssignmentExpression):
        """
        Assigns a value to an existing variable (which has a current register),
        generating instructions in the process and adding them to the current basic block
        """

        # TODO Type conversions are not supported yet
        right = ast.get_right()
        left = ast.get_left()
        if isinstance(left, ASTs.ASTVariable):
            variable_register = self.get_variable_register(left.get_content())

            computed_expression_value = self.compute_expression(right)

            if computed_expression_value.get_data_type().is_pointer():
                # TODO: This must be done using a derefence operator
                # TODO: This register is used to load from pointer type into an actual value of that data type (sure?)
                value_to_store = self.get_current_function().get_new_register()
                self.get_current_function().add_instruction(
                    LLVMInstructions.LoadInstruction(value_to_store, computed_expression_value))
            else:
                value_to_store = computed_expression_value

            self.get_current_function().add_instruction(
                LLVMInstructions.StoreInstruction(variable_register, value_to_store))

        elif isinstance(left, ASTs.ASTArrayAccessElement):
            array_symbol = self.get_last_symbol_table().get_array_symbol(left.get_content())

            computed_expression_value = self.compute_expression(right)

            #Gewoon overgenomen van hierboven, moet nog misschien nog aangepast worden?
            if computed_expression_value.get_data_type().is_pointer():
                # TODO: This must be done using a derefence operator
                # TODO: This register is used to load from pointer type into an actual value of that data type (sure?)
                value_to_store = self.get_current_function().get_new_register()
                self.get_current_function().add_instruction(
                    LLVMInstructions.LoadInstruction(value_to_store, computed_expression_value))
            else:
                value_to_store = computed_expression_value
            register_to_store = self.get_current_function().get_new_register(DataType.DataType(array_symbol.get_register().get_data_type().get_token(), array_symbol.get_register().get_data_type().get_pointer_level() + 1))
            instruction_1 = LLVMInstructions.GetElementPtrInstruction(register_to_store, left.get_index_accessed().get_content(), array_symbol.get_size(), array_symbol.get_register())
            self.get_current_function().add_instruction(instruction_1)
            instruction_2 = LLVMInstructions.StoreInstruction(register_to_store, computed_expression_value)
            self.get_current_function().add_instruction(instruction_2)
        else:
            raise NotImplementedError

    def to_file(self, filename: str):
        f = open(filename, "w+")
        f.write(self.to_llvm())
        f.close()

    # TODO optimize
    def to_llvm(self):
        llvm_code = self.get_global_container().to_llvm() + "\n"

        if self.get_global_container().has_printf_type_string():
            llvm_code += self.get_printf_function_declaration() + "\n\n"

        for function in self.functions:
            llvm_code += function.to_llvm() + "\n"

        return llvm_code
