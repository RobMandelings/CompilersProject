# TODO import asts to get some 'expected' types as parameters


class ASTVisitor:

    def visit_ast_leaf(self, ast):
        pass

    def visit_ast_internal(self, ast):
        for child in ast.children:
            child.accept(self)

    def visit_ast_binary_expression(self, ast):
        ast.left.accept(self)
        ast.right.accept(self)

    def visit_ast_assignment_expression(self, ast):
        """
        Does nothing special by default, just goes to the visit binary expression method.
        If you would want to do something special in case of the assignment expression, override this method
        """
        self.visit_ast_binary_expression(ast)

    def visit_ast_variable_declaration(self, ast):
        for attribute in ast.type_attributes:
            attribute.accept(self)
        ast.var_name.accept(self)

    def visit_ast_variable_declaration_and_init(self, ast):
        for attribute in ast.type_attributes:
            attribute.accept(self)
        ast.var_name.accept(self)
        ast.value.accept(self)
