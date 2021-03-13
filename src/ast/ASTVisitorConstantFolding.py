from src.ast.ASTToken import TokenType
from src.ast.ASTVisitor import ASTVisitor
from src.ast.ASTs import ASTBinaryExpression, ASTLeaf, ASTInternal, ASTVariableDeclaration, \
    ASTVariableDeclarationAndInit


class ASTVisitorConstantFolding(ASTVisitor):

    def get_leaf_result(self, ast: ASTLeaf):
        value = ast.get_token_content()

        if ast.get_token_type() == TokenType.CHAR_LITERAL:
            value = value.replace("\'", "")
            char = list()
            for c in value:
                char.append(c)

            assert len(char) == 1, "Character defined consists of multiple characters. This should not be possible"
            return ord(char[0])
        elif ast.get_token_type() == TokenType.INT_LITERAL:
            return int(value)
        elif ast.get_token_type() == TokenType.FLOAT_LITERAL:
            return float(value)
        else:
            raise NotImplementedError("This should not be possible")

    def fold_binary_expression(self, ast: ASTBinaryExpression):
        assert isinstance(ast, ASTBinaryExpression)
        if isinstance(ast.left, ASTLeaf):
            left_value = self.get_leaf_result(ast.left)
        else:
            raise NotImplementedError("This should not be possible")

        if isinstance(ast.right, ASTLeaf):
            right_value = self.get_leaf_result(ast.right)
        else:
            raise NotImplementedError("This should not be possible")

        if ast.get_token_type() == TokenType.ADD_EXPRESSION:
            return left_value + right_value
        elif ast.get_token_type() == TokenType.SUB_EXPRESSION:
            return left_value - right_value
        elif ast.get_token_type() == TokenType.MULT_EXPRESSION:
            return left_value * right_value
        elif ast.get_token_type() == TokenType.DIV_EXPRESSION:
            return left_value / right_value
        elif ast.get_token_type() == TokenType.EQUALS_EXPRESSION:
            # TODO check: does it work for floats? Or should we use something like epsilon for this
            return left_value == right_value
        elif ast.get_token_type() == TokenType.GREATER_THAN_EXPRESSION:
            return left_value > right_value
        elif ast.get_token_type() == TokenType.LESS_THAN_EXPRESSION:
            return left_value < right_value
        else:
            raise NotImplementedError("Should not be possible")

    def visit_ast_internal(self, ast: ASTInternal):
        for child in ast.children:
            if isinstance(child, ASTBinaryExpression):
                self.fold_binary_expression(child)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        super().visit_ast_variable_declaration_and_init(ast)
        if isinstance(ast.value, ASTBinaryExpression):
            ast.value = self.fold_binary_expression(ast.value)
