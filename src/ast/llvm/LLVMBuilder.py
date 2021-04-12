import src.ast.ASTTokens as ASTTokens
import src.ast.ASTs as ASTs
import src.ast.llvm.LLVMFunction as LLVMFunctions
import src.ast.llvm.LLVMGlobalContainer as LLVMGlobalContainer
import src.ast.llvm.LLVMInstruction as LLVMInstructions
import src.ast.llvm.LLVMInterfaces as LLVMInterfaces
import src.ast.llvm.LLVMSymbolTable as LLVMSymbolTable
import src.ast.llvm.LLVMUtils as LLVMUtils
import src.ast.llvm.LLVMValue as LLVMValues


class LLVMBuilder(LLVMInterfaces.IToLLVM):

    def __init__(self):
        self.global_container = LLVMGlobalContainer.LLVMGlobalContainer()
        self.functions = list()
        self.functions.append(LLVMFunctions.LLVMFunction("main"))
        self.symbol_table = LLVMSymbolTable.LLVMSymbolTable()
        pass

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

    def compute_compare_expression(self, operation: ASTTokens.RelationalExprToken, operand1: LLVMValues.LLVMValue,
                                   operand2: LLVMValues.LLVMValue):

        # TODO remove duplicate code
        if operand1.get_data_type() != operand2.get_data_type():

            richest_data_type_index = ASTTokens.DataTypeToken.get_richest_data_type(operand1.get_data_type(),
                                                                                    operand2.get_data_type())

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
                    richest_value.get_data_type() == (ASTTokens.DataTypeToken.FLOAT | ASTTokens.DataTypeToken.DOUBLE)):

                if richest_value == operand1:
                    operand1 = LLVMUtils.get_llvm_for_literal(richest_value, operand1.get_data_type())
                else:
                    operand2 = LLVMUtils.get_llvm_for_literal(richest_value, operand2.get_data_type())

        register_to_return = self.get_current_function().get_new_register(ASTTokens.DataTypeToken.BOOL)
        self.get_current_function().add_instruction(
            LLVMInstructions.CompareInstruction(register_to_return, operation, operand1, operand2))

        return register_to_return

    def compute_expression(self, ast: ASTs.AST):
        """
        Computes an expression of the given AST, generating the corresponding instructions in the process
        ast: the AST to compute the expression for

        returns: <value, data_type>:
        - value: holds the value of the computed expression. Can either be
            - The register that was last used to compute this expression
            - Or a literal if possible
        - data_type: the resulting data type of the operation (ASTTokens.DataTypeToken.INT, FLOAT,...)
        """

        if isinstance(ast, ASTs.ASTBinaryExpression):
            operand1 = self.compute_expression(ast.left)
            operand2 = self.compute_expression(ast.right)

            instruction = None
            operation = ast.get_token()

            if isinstance(operation, ASTs.BinaryArithmeticExprToken):
                register_to_return = self.get_current_function().get_new_register()
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
            variable = self.symbol_table.lookup_variable(ast.get_content())

            # We're assuming the variable register is always of pointer type,
            # so first load the variable value into a register and return it

            register_to_return = self.get_current_function().get_new_register(
                ASTTokens.DataTypeToken.get_normal_version(variable.get_data_type()))
            self.get_current_function().add_instruction(
                LLVMInstructions.LoadInstruction(register_to_return, variable.get_current_register()))
            return register_to_return
        else:
            raise NotImplementedError

    # TODO also be able to print literals
    def print_variable(self, variable_name):
        variable = self.symbol_table.lookup_variable(variable_name)
        assert variable is not None

        register_to_print = self.get_current_function().get_new_register(variable.get_data_type().get_normal_version())

        self.get_current_function().add_instruction(
            LLVMInstructions.LoadInstruction(register_to_print,
                                             variable.get_current_register()))

        # The global variable that contains the string of the corresponding type of variable to call (printf(%i, your_int))
        # has the string %i\00 as type to use for the print. The global variable contains this string
        global_var_data_type = self.get_global_container().get_printf_type_string(register_to_print.get_data_type())
        resulting_register = self.get_current_function().get_new_register()
        instruction = LLVMInstructions.PrintfInstruction(resulting_register, register_to_print, global_var_data_type)
        self.get_current_function().add_instruction(instruction)

        return resulting_register

    def declare_variable(self, ast: ASTs.ASTVariableDeclaration):
        resulting_register = self.get_current_function().get_new_register()
        declared_variable = LLVMSymbolTable.LLVMVariableSymbol(ast.var_name_ast.get_content(),
                                                               ast.data_type_ast.get_token(),
                                                               resulting_register)
        self.symbol_table.insert_symbol(
            declared_variable)

        instruction = LLVMInstructions.AllocaInstruction(resulting_register, declared_variable.get_data_type())
        self.get_current_function().add_instruction(instruction)

    def declare_and_init_variable(self, ast: ASTs.ASTVariableDeclarationAndInit):
        """
        Declares and initializes a variable using LLVM instructions. Computes expressions if necessary
        Adds the corresponding instructions to the current basic block
        """
        value_to_store = self.compute_expression(ast.value)

        new_register = self.get_current_function().get_new_register(
            ast.data_type_ast.get_data_type().get_pointer_version())

        # TODO remove from code: don't work with symbol table anymore
        declared_variable = LLVMSymbolTable.LLVMVariableSymbol(ast.var_name_ast.get_content(),
                                                               new_register)
        self.symbol_table.insert_symbol(declared_variable)

        self.get_current_function().add_instruction(LLVMInstructions.AllocaInstruction(new_register))
        self.get_current_function().add_instruction(LLVMInstructions.StoreInstruction(new_register, value_to_store))

    def assign_value_to_variable(self, ast: ASTs.ASTAssignmentExpression):
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

        computed_expression_value = self.compute_expression(right)

        if computed_expression_value.get_data_type().is_pointer_type():
            # TODO: This register is used to load from pointer type into an actual value of that data type (sure?)
            value_to_store = self.get_current_function().get_new_register()
            self.get_current_function().add_instruction(
                LLVMInstructions.LoadInstruction(value_to_store, computed_expression_value))
        else:
            value_to_store = computed_expression_value

        self.get_current_function().add_instruction(
            LLVMInstructions.StoreInstruction(current_variable_reg, value_to_store))

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
