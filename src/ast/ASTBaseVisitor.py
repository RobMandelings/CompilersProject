# TODO import asts to get some 'expected' types as parameters
from src.ast.ASTs import *


class ASTBaseVisitor(IASTVisitor):
    """
    Base class for the abstract syntax tree visitor which implements the basic post-order traversal.
    Specific visitors should inherit from this class
    """

    def visit_ast_leaf(self, ast: ASTLeaf):
        assert isinstance(ast, ASTLeaf)

    def visit_ast_literal(self, ast: ASTLiteral):
        assert isinstance(ast, ASTLiteral)
        self.visit_ast_leaf(ast)

    def visit_ast_data_type(self, ast: ASTDataType):
        assert isinstance(ast, ASTDataType)
        self.visit_ast_leaf(ast)

    def visit_ast_type_attribute(self, ast: ASTTypeAttribute):
        assert isinstance(ast, ASTTypeAttribute)
        self.visit_ast_leaf(ast)

    def visit_ast_identifier(self, ast: ASTIdentifier):
        assert isinstance(ast, ASTIdentifier)
        self.visit_ast_leaf(ast)

    def visit_ast_access_element(self, ast: ASTAccessArrayVarExpression):
        assert isinstance(ast, ASTAccessArrayVarExpression)
        ast.get_variable_accessed().accept(self)
        ast.get_index_accessed().accept(self)

    def visit_ast_internal(self, ast: ASTInternal):
        assert isinstance(ast, ASTInternal)
        for child in ast.children:
            child.accept(self)

    def visit_ast_expression(self, ast: ASTExpression):
        pass

    def visit_ast_unary_expression(self, ast: ASTUnaryExpression):
        assert isinstance(ast, ASTUnaryExpression)
        ast.value_applied_to.accept(self)
        self.visit_ast_expression(ast)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        assert isinstance(ast, ASTBinaryExpression)
        ast.left.accept(self)
        ast.right.accept(self)

    def visit_ast_binary_arithmetic_expression(self, ast: ASTBinaryArithmeticExpression):
        assert isinstance(ast, ASTBinaryArithmeticExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_relational_expression(self, ast: ASTRelationalExpression):
        assert isinstance(ast, ASTRelationalExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        """
        Does nothing special by default, just goes to the visit binary expression method.
        If you would want to do something special in case of the assignment expression, override this method
        """
        assert isinstance(ast, ASTAssignmentExpression)
        self.visit_ast_binary_expression(ast)

    def visit_ast_array_init(self, ast: ASTArrayInit):
        assert isinstance(ast, ASTArrayInit)
        for value in ast.get_values():
            value.accept(self)

    def visit_ast_var_declaration(self, ast: ASTVarDeclaration):
        assert isinstance(ast, ASTVarDeclaration)
        ast.data_type_ast.accept(self)
        for attribute in ast.type_attributes:
            attribute.accept(self)
        ast.var_name_ast.accept(self)

    def visit_ast_array_declaration(self, ast: ASTArrayVarDeclaration):
        ASTBaseVisitor.visit_ast_var_declaration(self, ast)

    def visit_ast_var_declaration_and_init(self, ast: ASTVarDeclarationAndInit):
        assert isinstance(ast, ASTVarDeclarationAndInit)
        ast.get_var_declaration().accept(self)
        ast.initial_value.accept(self)

    def visit_ast_array_declaration_and_init(self, ast: ASTArrayVarDeclarationAndInit):
        ast.get_array_declaration_ast().accept(self)
        self.visit_ast_array_init(ast.get_array_init())

    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        pass

    def visit_ast_scope(self, ast: ASTScope):
        assert isinstance(ast, ASTScope)
        for child in ast.children:
            child.accept(self)

    def visit_ast_dereference(self, ast: ASTDereference):
        ast.get_value_to_dereference().accept(self)

    def visit_ast_control_flow_statement(self, ast: ASTControlFlowStatement):
        assert isinstance(ast, ASTControlFlowStatement)

    def visit_ast_if_statement(self, ast: ASTIfStatement):
        assert isinstance(ast, ASTIfStatement)
        if ast.get_condition() is not None:
            ast.get_condition().accept(self)
        self.visit_conditional_statement(ast)
        if ast.get_else_statement() is not None:
            ast.get_else_statement().accept(self)

    def visit_ast_while_loop(self, ast: ASTWhileLoop):
        assert isinstance(ast, ASTWhileLoop)
        ast.get_condition().accept(self)
        self.visit_conditional_statement(ast)
        if ast.get_update_step() is not None:
            ast.get_update_step().accept(self)

    def visit_conditional_statement(self, ast: ASTConditionalStatement):
        ast.get_execution_body().accept(self)

    def visit_ast_function_call(self, ast: ASTFunctionCall):
        for param in ast.get_arguments():
            param.accept(self)

    def visit_ast_function_declaration(self, ast: ASTFunctionDeclaration):
        for param in ast.get_params():
            param.accept(self)

    def visit_ast_function_definition(self, ast: ASTFunctionDefinition):
        ast.get_function_declaration().accept(self)
        ast.get_execution_body().accept(self)

    def visit_ast_return_statement(self, ast: ASTReturnStatement):
        ast.return_value.accept(self)

    def visit_ast_include(self, ast: ASTInclude):
        pass

    def reset(self):
        """
        Resets the visitor to use it for another tree for example
        """
        self.__init__()
