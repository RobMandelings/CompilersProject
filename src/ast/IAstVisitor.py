import abc


class IASTVisitor(abc.ABC):
    """
    Interface for the visitors of the abstract syntax tree
    """

    def visit_ast_leaf(self, ast):
        pass

    def visit_ast_literal(self, ast):
        pass

    def visit_ast_data_type(self, ast):
        pass

    def visit_ast_type_attribute(self, ast):
        pass

    def visit_ast_identifier(self, ast):
        pass

    def visit_ast_internal(self, ast):
        pass

    def visit_ast_expression(self, ast):
        pass

    def visit_ast_unary_expression(self, ast):
        pass

    def visit_ast_pointer_expression(self, ast):
        pass

    def visit_ast_binary_expression(self, ast):
        pass

    def visit_ast_binary_arithmetic_expression(self, ast):
        pass

    def visit_ast_binary_compare_expression(self, ast):
        pass

    def visit_ast_assignment_expression(self, ast):
        pass

    def visit_ast_array_init(self, ast):
        pass

    def visit_ast_variable_declaration(self, ast):
        pass

    def visit_ast_array_declaration(self, ast):
        pass

    def visit_ast_variable_declaration_and_init(self, ast):
        pass

    def visit_ast_array_declaration_and_init(self, ast):
        pass

    def visit_ast_printf_instruction(self, ast):
        pass

    def visit_ast_scope(self, ast):
        pass

    def visit_ast_control_flow_statement(self, ast):
        pass

    def visit_ast_if_statement(self, ast):
        pass

    def visit_ast_while_loop(self, ast):
        pass

    def visit_conditional_statement(self, ast):
        pass

    def visit_ast_function_declaration(self, ast):
        pass

    def visit_ast_function_call(self, ast):
        pass

    def visit_ast_return_statement(self, ast):
        pass
