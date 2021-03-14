# TODO import asts to get some 'expected' types as parameters
from src.ast.ASTs import *


class ASTBaseVisitor(IASTVisitor):
    """
    Base class for the abstract syntax tree visitor which implements the basic post-order traversal.
    Specific visitors should inherit from this class
    """

    def visit_ast_leaf(self, ast: ASTLeaf):
        assert isinstance(ast, ASTLeaf), "The AST is not an ASTLeaf"

    def visit_ast_literal(self, ast: ASTLiteral):
        assert isinstance(ast, ASTLiteral), "The AST is not an ASTLiteral"
        self.visit_ast_leaf(ast)

    def visit_ast_type(self, ast: ASTType):
        assert isinstance(ast, ASTType)
        self.visit_ast_leaf(ast)

    def visit_ast_identifier(self, ast: ASTIdentifier):
        assert isinstance(ast, ASTIdentifier)
        self.visit_ast_leaf(ast)

    def visit_ast_internal(self, ast: ASTInternal):
        assert isinstance(ast, ASTInternal), "The AST is not an ASTInternal"
        for child in ast.children:
            child.accept(self)

    def visit_ast_unary_expression(self, ast: ASTUnaryExpression):
        assert isinstance(ast, ASTUnaryExpression), "The AST is not an ASTUnaryExpression"
        ast.value_applied_to.accept(self)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        assert isinstance(ast, ASTBinaryExpression), "The AST is not an ASTBinaryExpression"
        ast.left.accept(self)
        ast.right.accept(self)

    def visit_ast_binary_arithmetic_expression(self, ast: ASTBinaryArithmeticExpression):
        assert isinstance(ast, ASTBinaryArithmeticExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_binary_compare_expression(self, ast: ASTBinaryCompareExpression):
        assert isinstance(ast, ASTBinaryArithmeticExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        """
        Does nothing special by default, just goes to the visit binary expression method.
        If you would want to do something special in case of the assignment expression, override this method
        """
        assert isinstance(ast, ASTAssignmentExpression), "The AST is not an ASTAssignmentExpression"
        self.visit_ast_binary_expression(ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        assert isinstance(ast, ASTVariableDeclaration), "The AST is not an ASTVariableDeclaration"
        for attribute in ast.type_attributes:
            attribute.accept(self)
        ast.var_name.accept(self)

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        assert isinstance(ast, ASTVariableDeclarationAndInit), "The AST is not an ASTVariableDeclarationAndInit"
        for attribute in ast.type_attributes:
            attribute.accept(self)
        ast.var_name.accept(self)
        ast.value.accept(self)

    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        pass

    def reset(self):
        """
        Resets the visitor to use it for another tree for example
        """
        self.__init__()
