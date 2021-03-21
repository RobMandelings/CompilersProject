# TODO import asts to get some 'expected' types as parameters
from src.ast.ASTs import *


class ASTBaseVisitor(IASTVisitor):
    """
    Base class for the abstract syntax tree visitor which implements the basic post-order traversal.
    Specific visitors should inherit from this class
    """

    def visit_ast_leaf(self, ast: ASTLeaf):
        assert isinstance(ast, ASTLeaf)

    def visit_ast_literal(self, ast: ASTRValue):
        assert isinstance(ast, ASTRValue)
        self.visit_ast_leaf(ast)

    def visit_ast_data_type(self, ast: ASTDataType):
        assert isinstance(ast, ASTDataType)
        self.visit_ast_leaf(ast)

    def visit_ast_type_attribute(self, ast: ASTTypeAttribute):
        assert isinstance(ast, ASTTypeAttribute)
        self.visit_ast_leaf(ast)

    def visit_ast_identifier(self, ast: ASTLValue):
        assert isinstance(ast, ASTLValue)
        self.visit_ast_leaf(ast)

    def visit_ast_internal(self, ast: ASTInternal):
        assert isinstance(ast, ASTInternal)
        for child in ast.children:
            child.accept(self)

    def visit_ast_unary_expression(self, ast: ASTUnaryExpression):
        assert isinstance(ast, ASTUnaryExpression)
        ast.value_applied_to.accept(self)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        assert isinstance(ast, ASTBinaryExpression)
        ast.left.accept(self)
        ast.right.accept(self)

    def visit_ast_binary_arithmetic_expression(self, ast: ASTBinaryArithmeticExpression):
        assert isinstance(ast, ASTBinaryArithmeticExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_binary_compare_expression(self, ast: ASTRelationalExpression):
        assert isinstance(ast, ASTBinaryArithmeticExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        """
        Does nothing special by default, just goes to the visit binary expression method.
        If you would want to do something special in case of the assignment expression, override this method
        """
        assert isinstance(ast, ASTAssignmentExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        assert isinstance(ast, ASTVariableDeclaration)
        ast.data_type_ast.accept(self)
        for attribute in ast.type_attributes:
            attribute.accept(self)
        ast.var_name_ast.accept(self)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        assert isinstance(ast, ASTVariableDeclarationAndInit)
        ast.data_type_ast.accept(self)
        for attribute in ast.type_attributes:
            attribute.accept(self)
        ast.var_name_ast.accept(self)
        ast.value.accept(self)

    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        pass

    def visit_ast_scope(self, ast: ASTScope):
        assert isinstance(ast, ASTScope)
        for child in ast.children:
            child.accept(self)

    def visit_ast_if_statement(self, ast: ASTIfStatement):
        assert isinstance(ast, ASTIfStatement)
        ast.get_condition().accept(self)
        ast.get_execution_body().accept(self)
        ast.get_else_statement().accept(self)

    def visit_ast_while_loop(self, ast: ASTWhileLoop):
        assert isinstance(ast, ASTWhileLoop)
        ast.get_condition().accept(self)
        ast.get_execution_body().accept(self)

    def reset(self):
        """
        Resets the visitor to use it for another tree for example
        """
        self.__init__()
