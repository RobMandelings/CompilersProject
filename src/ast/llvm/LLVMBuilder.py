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

        if isinstance(ast, ASTBinaryExpression):
            left_register = self._compute_expression(ast.left)
            right_register = self._compute_expression(ast.right)

            operation_string = None
            if ast.get_token_type() == TokenType.ADD_EXPRESSION:
                operation_string = 'add'
            elif ast.get_token_type() == TokenType.SUB_EXPRESSION:
                operation_string = 'sub'
            elif ast.get_token_type() == TokenType.MULT_EXPRESSION:
                operation_string = 'mul'
            elif ast.get_token_type() == TokenType.DIV_EXPRESSION:
                # TODO sdiv or udiv?
                operation_string = 'sdiv'
            else:
                raise NotImplementedError

            self.instructions.append(
                f"%{self.register_count} = {operation_string} i32 {left_register}, {right_register}")

            assert operation_string is not None

        elif isinstance(ast, ASTLeaf):
            # Generate a single instructions and return the register for this instruction
            if ast.get_token_type() == TokenType.INT_LITERAL:
                value = int(ast.get_token_content())
                self.instructions.append(f"%{self.register_count} = add i32 0, {value}")

            else:
                raise NotImplementedError
            pass
        else:
            raise NotImplementedError

        register_to_return = f"%{self.register_count}"
        self.register_count += 1
        return register_to_return

    def assign_value_to_variable(self, variable_name: str, ast: AST):
        self.symbol_table[variable_name] = self._compute_expression(ast)

    def _generate_begin_of_file(self):
        pass

    def _generate_end_of_file(self):
        pass

    def to_file(self, filename: str):
        pass
