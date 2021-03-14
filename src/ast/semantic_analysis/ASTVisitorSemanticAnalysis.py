from src.ast.semantic_analysis.SymbolTable import *
from src.ast.ASTs import *


class SemanticError(Exception):
    pass


class AlreadyDeclaredError(SemanticError):
    pass


class UndeclaredError(SemanticError):
    pass


class UninitializedError(SemanticError):
    pass


class IncompatibleTypesError(Exception):
    pass


def divide_type_attributes(type_attributes: list):
    """
    Separates the type attributes from the list into a tuple of specific type specifier and type qualifier(s)
    Returns: tuple (data_type, is_const)
    """
    data_type = None
    is_const = False
    for attribute in type_attributes:
        assert isinstance(attribute, AST)
        if DataType.get_data_type_from_name(attribute.get_token_content()) is not None:
            assert data_type is None, "There are multiple datatypes defined. " \
                                      "This should not be possible as it should have halted with a syntax error"
            data_type = DataType.get_data_type_from_name(attribute.get_token_content())
        elif attribute.get_token_content() == 'const':
            is_const = True
        else:
            NotImplementedError('This attribute is not supported yet')
    assert data_type is not None and is_const is not None

    return data_type, is_const


class ASTVisitorResultingDataType(ASTVisitor):
    """
    This visitor is used whenever the semantic analysis visitor needs to decide what the data type of the result
    of a (binary) expression is.

    PRE-CONDITION: all variables within the tree should exist and be defined. This can be checked using the unavailable variable usage visitor
    """

    def __init__(self, last_symbol_table: SymbolTable):
        self.last_symbol_table = last_symbol_table
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
            if is_richer_than(other_data_type, self.resulting_data_type):
                self.resulting_data_type = other_data_type

    def visit_ast_leaf(self, ast):
        if ast.token.token_type == TokenType.IDENTIFIER:
            variable = self.last_symbol_table.lookup_variable(ast.get_token_content())
            assert variable.is_initialized()
            self.update_current_data_type(variable.data_type)
        elif ast.token.token_type == TokenType.INT_LITERAL:
            self.update_current_data_type(DataType.INT)
        elif ast.token.token_type == TokenType.FLOAT_LITERAL:
            self.update_current_data_type(DataType.FLOAT)
        elif ast.token.token_type == TokenType.CHAR_LITERAL:
            self.update_current_data_type(DataType.CHAR)
        else:
            raise NotImplementedError("Token type '" + str(ast.token.token_type) + "' not recognized")


class ASTVisitorUndeclaredVariableUsed(ASTVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains undeclared variables
    """

    def __init__(self, last_symbol_table: SymbolTable):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = last_symbol_table
        self.undeclared_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_leaf(self, ast):
        if ast.token.token_type == TokenType.IDENTIFIER:
            table_element = self.last_symbol_table.lookup(ast.get_token_content())
            if not table_element:
                self.undeclared_variables_used.append(ast)


class ASTVisitorUninitializedVariableUsed(ASTVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains an unitialized variables
    """

    def __init__(self, last_symbol_table: SymbolTable):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = last_symbol_table
        self.uninitialized_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_leaf(self, ast):
        if ast.token.token_type == TokenType.IDENTIFIER:
            table_element = self.last_symbol_table.lookup(ast.get_token_content())
            if table_element:
                assert isinstance(table_element, SymbolTableElement)
                assert isinstance(table_element.symbol, VariableSymbol)
                if not table_element.symbol.is_initialized():
                    self.uninitialized_variables_used.append(ast)


class ASTVisitorSemanticAnalysis(ASTVisitor):

    def __init__(self):
        super().__init__()
        self.symbol_table_stack = list()
        # TODO needs to be removed once the concept of 'blocks' is introduced
        self.create_symbol_table()

    def create_symbol_table(self):
        if len(self.symbol_table_stack) == 0:
            # First symbol table created
            self.symbol_table_stack.append(SymbolTable())
        else:
            parent_symbol_table = self.symbol_table_stack[-1]
            new_symbol_table = SymbolTable()
            new_symbol_table.parent = parent_symbol_table
            self.symbol_table_stack.append(new_symbol_table)

    def get_last_symbol_table(self):
        """
        Retrieve the symbol table that was last created (top of the stack)
        This corresponds the scope you are currently in
        """
        symbol_table = self.symbol_table_stack[-1]
        assert isinstance(symbol_table, SymbolTable)
        return symbol_table

    def check_for_narrowing_result(self, declared_data_type: DataType, ast: AST):
        """
        Checks if the result would be narrowed down into another data type (e.g. float to int). If so, warn to the log
        PRE-CONDITION: All variables need to be declared and initialized in order for lookups to work
        """
        resulting_data_type_visitor = ASTVisitorResultingDataType(self.get_last_symbol_table())
        ast.accept(resulting_data_type_visitor)
        assert resulting_data_type_visitor.resulting_data_type is not None

        # This is the data type that was declared in the input program

        if declared_data_type != resulting_data_type_visitor.resulting_data_type and not is_richer_than(
                declared_data_type, resulting_data_type_visitor.resulting_data_type):
            print(
                "WARN: narrowing result of expression from datatype '" +
                resulting_data_type_visitor.resulting_data_type.name + "' to datatype '" + declared_data_type.name + "'")

    def check_rvalue_assignment(self, bin_expr: ASTBinaryExpression):
        # TODO Needs to be improved with derefencing and all that stuff
        assert bin_expr.token.token_type == TokenType.ASSIGNMENT_EXPRESSION

        if bin_expr.left.token.token_type == TokenType.CHAR_LITERAL or bin_expr.left.token.token_type == TokenType.INT_LITERAL or bin_expr.left.token.token_type == TokenType.FLOAT_LITERAL:
            raise SemanticError("Assignment to an rValue (value is " + bin_expr.left.get_token_content() + ")")

    def check_undeclared_variable_usage(self, ast: AST):

        undeclared_var_usage = ASTVisitorUndeclaredVariableUsed(self.get_last_symbol_table())
        ast.accept(undeclared_var_usage)

        if len(undeclared_var_usage.undeclared_variables_used) != 0:
            error_text = ""

            for variable in undeclared_var_usage.undeclared_variables_used:
                error_text += "Variable with name '" + variable.get_token_content() + "' is undeclared! \n"

            raise SemanticError(error_text)

    def check_uninitialized_variable_usage(self, ast: AST):

        uninitialized_var_usage = ASTVisitorUninitializedVariableUsed(self.get_last_symbol_table())
        ast.accept(uninitialized_var_usage)

        if len(uninitialized_var_usage.uninitialized_variables_used) != 0:
            error_text = ""

            for variable in uninitialized_var_usage.uninitialized_variables_used:
                error_text += "Variable with name '" + variable.get_token_content() + "' is found but uninitialized! \n"

            raise SemanticError(error_text)

    def check_const_assignment(self, bin_expr: ASTBinaryExpression):
        """
        Checks if a variable being assigned a new value is const, and if so, raise a semantic error
        PRE-CONDITION: Variable must exist (check must have gone before)
        """
        assert bin_expr.token.token_type == TokenType.ASSIGNMENT_EXPRESSION

        symbol_element = self.get_last_symbol_table().lookup(bin_expr.left.get_token_content())
        assert symbol_element
        assert symbol_element.symbol and isinstance(symbol_element.symbol, VariableSymbol)

        variable = symbol_element.symbol

        if variable.const:
            raise SemanticError("Cannot assign value to const variable '" + bin_expr.left.get_token_content() + "'")

    def visit_ast_assignment(self, bin_expr: ASTBinaryExpression):
        assert bin_expr.token.token_type == TokenType.ASSIGNMENT_EXPRESSION
        symbol_table = self.get_last_symbol_table()

        # Do some semantic checks. If all checks don't raise any errors, continue on with the new value
        self.check_undeclared_variable_usage(bin_expr.right)
        self.check_undeclared_variable_usage(bin_expr.left)
        self.check_uninitialized_variable_usage(bin_expr.right)

        variable = symbol_table.lookup_variable(bin_expr.left.get_token_content())
        if not variable.is_initialized():
            variable.initialized = True

        self.check_const_assignment(bin_expr)

        # Warn in case the result will be narrowed down into another data type
        self.check_for_narrowing_result(variable.data_type, bin_expr)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        # Do nothing
        pass

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        self.visit_ast_assignment(ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        symbol_table = self.get_last_symbol_table()

        if symbol_table.lookup(ast.var_name.get_token_content()) is None:
            data_type, is_const = divide_type_attributes(ast.type_attributes)
            symbol_table.insert_symbol(
                SymbolTableElement(ast.var_name.get_token_content(), VariableSymbol(data_type, is_const, False)))
        else:
            raise AlreadyDeclaredError(
                "Variable with name '" + str(ast.var_name) + "' has already been declared in this scope!")

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.visit_ast_variable_declaration(ast)
        variable_symbol = self.get_last_symbol_table().lookup_variable(ast.var_name.get_token_content())

        # Do some semantic checks
        self.check_undeclared_variable_usage(ast.value)
        self.check_uninitialized_variable_usage(ast.value)

        variable_symbol.initialized = True

        data_type, is_const = divide_type_attributes(ast.type_attributes)
        self.check_for_narrowing_result(data_type, ast.value)
