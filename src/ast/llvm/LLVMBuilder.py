from src.ast.ASTs import *
from src.ast.llvm.LLVMFunction import *
from src.ast.llvm.LLVMSymbolTable import *
from src.ast.llvm.LLVMUtils import IToLLVM, get_llvm_type
from src.ast.llvm.LLVMInstruction import *


class LLVMBuilder(IToLLVM):

    def __init__(self):
        self.functions = list()
        self.functions.append(LLVMFunction("main"))
        self.instructions = list()
        self.symbol_table = LLVMSymbolTable()
        self.register_count = 0
        pass

    def get_current_function(self):
        function = self.functions[-1]
        assert isinstance(function, LLVMFunction)
        return function

    def compute_expression(self, ast: AST):
        """
        """

        if isinstance(ast, ASTBinaryArithmeticExpression):
            left_register = self.compute_expression(ast.left)
            right_register = self.compute_expression(ast.right)

            operation_string = None
            if ast.get_token() == BinaryArithmeticExprToken.ADD:
                operation_string = 'fadd'
            elif ast.get_token() == BinaryArithmeticExprToken.SUB:
                operation_string = 'fsub'
            elif ast.get_token() == BinaryArithmeticExprToken.MUL:
                operation_string = 'fmul'
            elif ast.get_token() == BinaryArithmeticExprToken.DIV:
                # TODO sdiv or udiv?
                operation_string = 'fdiv'
            else:
                # TODO less than,...
                raise NotImplementedError

            self.instructions.append(
                f"%{self.register_count} = {operation_string} float {left_register}, {right_register}")

            assert operation_string is not None

        elif isinstance(ast, ASTUnaryExpression):

            if isinstance(ast, ASTUnaryArithmeticExpression):
                if ast.get_token() == UnaryArithmeticExprToken.PLUS:
                    factor = 1.0
                elif ast.get_token() == UnaryArithmeticExprToken.MINUS:
                    factor = -1.0
                else:
                    raise NotImplementedError

                value_register = self.compute_expression(ast.value_applied_to)

                self.instructions.append(f"%{self.register_count} = fmul float {factor}, {value_register}")

            elif isinstance(ast, ASTUnaryPointerExpression):
                pass
            else:
                raise NotImplementedError

        elif isinstance(ast, ASTRValue):
            # Generate a single instructions and return the register for this instruction
            value = float(ast.get_content())
            self.instructions.append(f"%{self.register_count} = fadd float 0.0, {float(value)}")
        elif isinstance(ast, ASTLValue):

            variable = self.symbol_table.lookup_variable(ast.get_content())
            return variable.get_current_register()
        else:
            raise NotImplementedError

        register_to_return = f"%{self.register_count}"
        self.register_count += 1
        return register_to_return

    def _convert_float_register_to(self, register, to_type: DataTypeToken):

        register_to_return = f"%{self.register_count}"

        if to_type != DataTypeToken.FLOAT:
            self.instructions.append(
                f"%{self.register_count} = fptosi float {register} to {get_llvm_type(to_type)}")
            self.register_count += 1
            return register_to_return

        return register

    # TODO also be able to print literals
    def print_variable(self, variable_name):
        variable = self.symbol_table.lookup_variable(variable_name)
        assert variable is not None
        self.instructions.append(
            f"call i32 (i8*, ...) @printf(i8* getelementptr inbounds([3 x i8], [3 x i8]* @.i, i64 0, i64 0), i32 {variable.get_current_register()})")

    def declare_variable(self, ast: ASTVariableDeclaration):
        resulting_register = self.get_current_function().get_new_register()
        declared_variable = LLVMVariableSymbol(ast.var_name_ast.get_content(), ast.data_type_ast.get_token(),
                                               resulting_register)
        self.symbol_table.insert_symbol(
            declared_variable)

        instruction = AllocaInstruction(f'%{resulting_register}', declared_variable.get_data_type())
        self.get_current_function().add_instruction(instruction)

    def declare_and_init_variable(self, ast: ASTVariableDeclarationAndInit):
        if not isinstance(ast.value, ASTRValue):
            value_to_store = self.compute_expression(ast.value)
            value_to_store = self._convert_float_register_to(value_to_store, ast.get_data_type())
        else:
            value_to_store = ast.value.get_content()

        register = f"%{self.get_current_function().get_new_register()}"

        declared_variable = LLVMVariableSymbol(ast.var_name_ast.get_content(), ast.data_type_ast.get_token(),
                                               register)
        self.symbol_table.insert_symbol(declared_variable)
        datatype = declared_variable.get_data_type()

        self.get_current_function().add_instruction(AllocaInstruction(f'%{register}', datatype))
        self.get_current_function().add_instruction(StoreInstruction(f'%{register}', value_to_store, datatype))

    def assign_value_to_variable(self, ast: ASTAssignmentExpression):
        # TODO Type conversions are not supported yet
        right = ast.get_right()

        variable = self.symbol_table.lookup_variable(ast.get_left().get_content())
        current_register = variable.get_current_register()
        left_datatype = get_llvm_type(variable.get_data_type())

        if not isinstance(right, ASTRValue):
            value_register = self.compute_expression(right)
            temporary_register = self.register_count  # REGISTER NUMBER (without %)

            self.instructions.append(
                f"%{temporary_register} = load {left_datatype}, {left_datatype}* {value_register}, align 4")
            self.register_count += 1
            self.instructions.append(
                f"store {left_datatype} %{temporary_register}, {left_datatype}* {current_register}, align 4")
        else:

            self.instructions.append(
                f"store {left_datatype} {right.get_content()}, {left_datatype}* {current_register}, align 4")

    def _generate_begin_of_file(self):
        begin_of_file = ""
        begin_of_file += "declare i32 @printf(i8*, ...)\n"
        begin_of_file += "@.i = private unnamed_addr constant [3 x i8] c\"%i\\00\", align 1\n"
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

        llvm_code = self._generate_begin_of_file()

        for function in self.functions:
            llvm_code += function.to_llvm()

        llvm_code += self._generate_end_of_file()

        return llvm_code
