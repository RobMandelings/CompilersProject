from src.ast.ASTs import *


class LLVMBuilder:

    def __init__(self):
        self.instructions = list()
        self.symbol_table = dict()
        self.register_count = 0
        pass

    def _compute_expression(self, ast: AST):
        """
        """

        if isinstance(ast, ASTBinaryArithmeticExpression):
            left_register = self._compute_expression(ast.left)
            right_register = self._compute_expression(ast.right)

            operation_string = None
            if ast.get_token() == BinaryArithmeticExprToken.ADD_EXPRESSION:
                operation_string = 'add'
            elif ast.get_token() == BinaryArithmeticExprToken.SUB_EXPRESSION:
                operation_string = 'sub'
            elif ast.get_token() == BinaryArithmeticExprToken.MUL_EXPRESSION:
                operation_string = 'mul'
            elif ast.get_token() == BinaryArithmeticExprToken.DIV_EXPRESSION:
                # TODO sdiv or udiv?
                operation_string = 'sdiv'
            else:
                # TODO less than,...
                raise NotImplementedError

            self.instructions.append(
                f"%{self.register_count} = {operation_string} f32 {left_register}, {right_register}")

            assert operation_string is not None

        elif isinstance(ast, ASTUnaryExpression):

            if ast.get_token() == UnaryExprToken.UNARY_PLUS_EXPRESSION:
                factor = 1
            elif ast.get_token() == UnaryExprToken.UNARY_MINUS_EXPRESSION:
                factor = -1
            else:
                raise NotImplementedError

            value_register = self._compute_expression(ast.value_applied_to)

            self.instructions.append(f"%{self.register_count} = mul f32 {factor}, {value_register}")

        elif isinstance(ast, ASTLiteral):
            # Generate a single instructions and return the register for this instruction
            if ast.get_token() == LiteralToken.INT_LITERAL:
                value = int(ast.get_content())
                self.instructions.append(f"%{self.register_count} = add f32 0, {value}")

            else:
                raise NotImplementedError
            pass
        else:
            raise NotImplementedError

        register_to_return = f"%{self.register_count}"
        self.register_count += 1
        return register_to_return

    # TODO also be able to print literals
    def print_variable(self, variable_name):
        assert self.symbol_table[variable_name] is not None
        self.instructions.append(
            f"call i32 (i8*, ...) @printf(i8* getelementptr inbounds([3 x i8], [3 x i8]* @.i, i64 0, i64 0), i32 {self.symbol_table[variable_name]})")

    def assign_value_to_variable(self, variable_name: str, ast: AST):
        self.symbol_table[variable_name] = self._compute_expression(ast)

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

        f.write(self._generate_begin_of_file())

        for instruction in self.instructions:
            f.write(instruction + "\n")

        f.write(self._generate_end_of_file())

        f.close()
