from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import *
from src.ast.ASTTokens import *
from src.ast.semantic_analysis.SymbolTable import *
from src.ast.semantic_analysis.SymbolTableManager import SymbolTableManager


class SemanticError(Exception):
    pass


class ASTVisitorResultingDataType(ASTBaseVisitor):
    """
    This visitor is used whenever the semantic analysis visitor needs to decide what the data type of the result
    of a (binary) expression is.

    PRE-CONDITION: all variables within the tree should exist and be defined. This can be checked using the unavailable variable usage visitor
    """

    def __init__(self, last_symbol_table: SymbolTable):
        self.current_symbol_table = last_symbol_table
        # This becomes the actual data type after doing some lookups of the
        # variables and their data types and the literals entered as well
        self.resulting_data_type = None
        assert last_symbol_table is not None

    def update_current_data_type(self, other_data_type):
        """
        Checks if the other data type given is richer than the current type and replaces it, otherwise do nothing
        """

        # TODO raise a semantic error if the data types are incomparable

        if self.resulting_data_type is None:
            self.resulting_data_type = other_data_type
        else:
            if DataTypeToken.is_richer_than(other_data_type, self.resulting_data_type):
                self.resulting_data_type = other_data_type

    def visit_ast_literal(self, ast: ASTLiteral):
        if ast.get_token() == LiteralToken.CHAR_LITERAL:
            self.update_current_data_type(DataTypeToken.CHAR)
        elif ast.get_token() == LiteralToken.INT_LITERAL:
            self.update_current_data_type(DataTypeToken.INT)
        elif ast.get_token() == LiteralToken.FLOAT_LITERAL:
            self.update_current_data_type(DataTypeToken.FLOAT)
        else:
            raise NotImplementedError(f"Token type '{ast.get_token()}' not recognized as literal")

    def visit_ast_identifier(self, ast: ASTIdentifier):
        variable = self.current_symbol_table.lookup_variable(ast.get_content())
        assert variable.is_initialized()
        self.update_current_data_type(variable.data_type)


class ASTVisitorUndeclaredVariableUsed(ASTBaseVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains undeclared variables
    """

    def __init__(self, last_symbol_table: SymbolTable):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.current_symbol_table = last_symbol_table
        self.undeclared_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_identifier(self, ast: ASTIdentifier):
        table_element = self.current_symbol_table.lookup(ast.get_content())
        if not table_element:
            self.undeclared_variables_used.append(ast)


class ASTVisitorUninitializedVariableUsed(ASTBaseVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains an unitialized variables
    """

    def __init__(self, current_symbol_table: SymbolTable):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = current_symbol_table
        self.uninitialized_variables_used = list()
        assert current_symbol_table is not None

    def visit_ast_identifier(self, ast: ASTIdentifier):
        super().visit_ast_identifier(ast)
        table_element = self.last_symbol_table.lookup(ast.get_content())
        if table_element:
            assert isinstance(table_element, Symbol)
            assert isinstance(table_element, VariableSymbol)
            if not table_element.is_initialized():
                self.uninitialized_variables_used.append(ast)


class ASTVisitorSemanticAnalysis(ASTBaseVisitor):

    def __init__(self):
        super().__init__()
        # Holds all symbol tables that were created and filled during semantical analysis.
        # Useful for generating intermediate code and code optimization
        self.symbol_table_manager = SymbolTableManager()
        self.current_symbol_table = self.symbol_table_manager.get_symbol_table("global")

    def check_for_narrowing_result(self, declared_data_type: DataTypeToken, ast: AST):
        """
        Checks if the result would be narrowed down into another data type (e.g. float to int). If so, warn to the log
        PRE-CONDITION: All variables need to be declared and initialized in order for lookups to work
        """
        resulting_data_type_visitor = ASTVisitorResultingDataType(self.current_symbol_table)
        ast.accept(resulting_data_type_visitor)
        assert resulting_data_type_visitor.resulting_data_type is not None

        # This is the data type that was declared in the input program

        if declared_data_type != resulting_data_type_visitor.resulting_data_type and not DataTypeToken.is_richer_than(
                declared_data_type, resulting_data_type_visitor.resulting_data_type):
            print(
                "WARN: narrowing result of expression from datatype '" +
                resulting_data_type_visitor.resulting_data_type.name + "' to datatype '" + declared_data_type.name + "'")

    def check_r_value_assignment(self, bin_expr: ASTAssignmentExpression):
        # TODO Needs to be improved with derefencing and all that stuff

        if isinstance(bin_expr.left, ASTLiteral):
            raise SemanticError(
                f"Assignment to an R-VALUE of type {bin_expr.left.token.name} (value is {bin_expr.left.get_content()})")

    def check_undeclared_variable_usage(self, ast: AST):

        undeclared_var_usage = ASTVisitorUndeclaredVariableUsed(self.current_symbol_table)
        ast.accept(undeclared_var_usage)

        if len(undeclared_var_usage.undeclared_variables_used) != 0:
            error_text = ""

            for variable in undeclared_var_usage.undeclared_variables_used:
                error_text += "Variable with name '" + variable.get_content() + "' is undeclared! \n"

            raise SemanticError(error_text)

    def check_uninitialized_variable_usage(self, ast: AST):

        uninitialized_var_usage = ASTVisitorUninitializedVariableUsed(self.current_symbol_table)
        ast.accept(uninitialized_var_usage)

        if len(uninitialized_var_usage.uninitialized_variables_used) != 0:
            error_text = ""

            for variable in uninitialized_var_usage.uninitialized_variables_used:
                error_text += "Variable with name '" + variable.get_content() + "' is found but uninitialized! \n"

            raise SemanticError(error_text)

    def check_const_assignment(self, bin_expr: ASTAssignmentExpression):
        """
        Checks if a variable being assigned a new value is const, and if so, raise a semantic error
        PRE-CONDITION: Variable must exist (check must have gone before)
        """

        variable = self.current_symbol_table.lookup_variable(bin_expr.left.get_content())

        if variable.const:
            raise SemanticError("Cannot assign value to const variable '" + bin_expr.left.get_content() + "'")

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        # Do nothing, just some optimization
        pass

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        symbol_table = self.current_symbol_table

        # Do some semantic checks. If all checks don't raise any errors, continue on with the new value
        self.check_undeclared_variable_usage(ast.right)
        self.check_undeclared_variable_usage(ast.left)
        self.check_uninitialized_variable_usage(ast.right)

        variable = symbol_table.lookup_variable(ast.left.get_content())
        if not variable.is_initialized():
            variable.initialized = True

        self.check_const_assignment(ast)

        # Warn in case the result will be narrowed down into another data type
        self.check_for_narrowing_result(variable.data_type, ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        symbol_table = self.current_symbol_table

        if symbol_table.lookup(ast.var_name_ast.get_content()) is None:
            symbol_table.insert_symbol(
                VariableSymbol(ast.var_name_ast.get_content(), ast.get_data_type(), ast.is_const(), False))
        else:
            raise SemanticError(
                f"Variable with name '{str(ast.var_name_ast)}' has already been declared in this scope!")

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.visit_ast_variable_declaration(ast)
        variable_symbol = self.current_symbol_table.lookup_variable(ast.var_name_ast.get_content())

        # Do some semantic checks
        self.check_undeclared_variable_usage(ast.value)
        self.check_uninitialized_variable_usage(ast.value)

        variable_symbol.initialized = True

        self.check_for_narrowing_result(ast.get_data_type(), ast.value)

    # TODO implement this!
    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        super().visit_ast_printf_instruction(ast)
