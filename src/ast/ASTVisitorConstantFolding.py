from src.ast.ASTToken import TokenType, ASTToken
from src.ast.ASTVisitor import ASTVisitor
from src.ast.ASTs import ASTBinaryExpression, ASTLeaf, ASTInternal, ASTVariableDeclaration, \
    ASTVariableDeclarationAndInit
from src.ast.semantic_analysis.SymbolTable import is_richer_than


class ASTVisitorConstantFolding(ASTVisitor):

    def get_leaf_result(self, ast: ASTLeaf):
        value = ast.get_token_content()

        if ast.get_token_type() == TokenType.CHAR_LITERAL:
            value = value.replace("\'", "")
            char = list()
            for c in value:
                char.append(c)

            assert len(char) == 1, "Character defined consists of multiple characters. This should not be possible"
            return ord(char[0]),
        elif ast.get_token_type() == TokenType.INT_LITERAL:
            return int(value)
        elif ast.get_token_type() == TokenType.FLOAT_LITERAL:
            return float(value)
        else:
            raise NotImplementedError("This should not be possible")

    def fold_binary_expression(self, ast: ASTBinaryExpression):
        assert isinstance(ast, ASTBinaryExpression)

        if isinstance(ast.left, ASTBinaryExpression):
            ast.left = self.fold_binary_expression(ast.left)

        if isinstance(ast.right, ASTBinaryExpression):
            ast.right = self.fold_binary_expression(ast.right)

        # After recursively folding the binary expression,
        if isinstance(ast.left, ASTLeaf) and isinstance(ast.right, ASTLeaf):
            if not ast.left.get_token_type() == TokenType.IDENTIFIER and not ast.right.get_token_type() == TokenType.IDENTIFIER:
                left_value = self.get_leaf_result(ast.left)
                right_value = self.get_leaf_result(ast.right)

                if is_richer_than(ast.left.get_token_type(), ast.right.get_token_type()):
                    token_type = ast.left.get_token_type()
                else:
                    token_type = ast.right.get_token_type()

                if ast.get_token_type() == TokenType.ADD_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value + right_value))
                elif ast.get_token_type() == TokenType.SUB_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value - right_value))
                elif ast.get_token_type() == TokenType.MULT_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value * right_value))
                elif ast.get_token_type() == TokenType.DIV_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value / right_value))
                elif ast.get_token_type() == TokenType.EQUALS_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value == right_value))
                elif ast.get_token_type() == TokenType.GREATER_THAN_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value > right_value))
                elif ast.get_token_type() == TokenType.LESS_THAN_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value < right_value))
                else:
                    raise NotImplementedError("Should not be possible")

        return ast

    def visit_ast_internal(self, ast: ASTInternal):
        super().visit_ast_internal(ast)
        for child in ast.children:
            if isinstance(child, ASTBinaryExpression):
                child = self.fold_binary_expression(child)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        super().visit_ast_variable_declaration_and_init(ast)
        if isinstance(ast.value, ASTBinaryExpression):
            ast.value = self.fold_binary_expression(ast.value)
