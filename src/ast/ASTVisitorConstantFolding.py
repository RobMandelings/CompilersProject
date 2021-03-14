from src.ast.ASTToken import TokenType, ASTToken
from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import ASTBinaryExpression, ASTLeaf, ASTInternal, ASTVariableDeclaration, \
    ASTVariableDeclarationAndInit
from src.ast.semantic_analysis.SymbolTable import is_richer_than, DataType


class ASTVisitorConstantFolding(ASTBaseVisitor):

    def get_leaf_result(self, ast: ASTLeaf):
        value = ast.get_token_content()
        value_as_number = float(value)

        # If its a char, we first need to convert the char into a number notation

        return value_as_number

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

                if is_richer_than(DataType.get_data_type_for_token_type(ast.left.get_token_type()),
                                  DataType.get_data_type_for_token_type(ast.right.get_token_type())):
                    token_type = ast.left.get_token_type()
                else:
                    token_type = ast.right.get_token_type()

                if ast.get_token_type() == TokenType.ADD_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value + right_value)).set_parent(ast.parent)
                elif ast.get_token_type() == TokenType.SUB_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value - right_value)).set_parent(ast.parent)
                elif ast.get_token_type() == TokenType.MULT_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value * right_value)).set_parent(ast.parent)
                elif ast.get_token_type() == TokenType.DIV_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value / right_value)).set_parent(ast.parent)
                elif ast.get_token_type() == TokenType.EQUALS_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value == right_value)).set_parent(ast.parent)
                elif ast.get_token_type() == TokenType.GREATER_THAN_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value > right_value)).set_parent(ast.parent)
                elif ast.get_token_type() == TokenType.LESS_THAN_EXPRESSION:
                    return ASTLeaf(ASTToken(token_type, left_value < right_value)).set_parent(ast.parent)
                else:
                    raise NotImplementedError("Should not be possible")

        return ast

    def visit_ast_internal(self, ast: ASTInternal):
        super().visit_ast_internal(ast)
        for i in range(len(ast.children)):
            if isinstance(ast.children[i], ASTBinaryExpression):
                ast.children[i] = self.fold_binary_expression(ast.children[i])

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        super().visit_ast_variable_declaration_and_init(ast)
        if isinstance(ast.value, ASTBinaryExpression):
            ast.value = self.fold_binary_expression(ast.value)
