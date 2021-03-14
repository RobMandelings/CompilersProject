from abc import abstractmethod


class IASTVisitor:
    """
    Interface for the visitors of the abstract syntax tree
    """

    @abstractmethod
    def visit_ast_leaf(self, ast):
        pass

    @abstractmethod
    def visit_ast_literal(self, ast):
        pass

    @abstractmethod
    def visit_ast_internal(self, ast):
        pass

    @abstractmethod
    def visit_ast_unary_expression(self, ast):
        pass

    @abstractmethod
    def visit_ast_binary_expression(self, ast):
        pass

    @abstractmethod
    def visit_ast_binary_arithmetic_expression(self, ast):
        pass

    @abstractmethod
    def visit_ast_binary_compare_expression(self, ast):
        pass

    @abstractmethod
    def visit_ast_assignment_expression(self, ast):
        pass

    @abstractmethod
    def visit_ast_variable_declaration(self, ast):
        pass

    @abstractmethod
    def visit_ast_variable_declaration_and_init(self, ast):
        pass

    @abstractmethod
    def visit_ast_printf_instruction(self, ast):
        pass
