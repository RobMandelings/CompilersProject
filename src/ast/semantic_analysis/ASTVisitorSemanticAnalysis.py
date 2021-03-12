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
            table_element = self.last_symbol_table.lookup(ast.get_token_content())
            assert isinstance(table_element, SymbolTableElement)
            assert isinstance(table_element.symbol, VariableSymbol)
            assert table_element.symbol.current_value
            self.update_current_data_type(table_element.symbol.data_type)
        elif ast.token.token_type == TokenType.INT_LITERAL:
            self.update_current_data_type(DataType.INT)
        elif ast.token.token_type == TokenType.FLOAT_LITERAL:
            self.update_current_data_type(DataType.FLOAT)
        elif ast.token.token_type == TokenType.CHAR_LITERAL:
            self.update_current_data_type(DataType.CHAR)
        else:
            raise NotImplementedError("Token type '" + str(ast.token.token_type) + "' not recognized")


class ASTVisitorUnavailableVariableUsage(ASTVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains an unitialized variable
    """

    def __init__(self, last_symbol_table: SymbolTable):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = last_symbol_table
        self.unitialized_variables_used = list()
        self.undeclared_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_leaf(self, ast):
        if ast.token.token_type == TokenType.IDENTIFIER:
            table_element = self.last_symbol_table.lookup(ast.get_token_content())
            if not table_element:
                self.undeclared_variables_used.append(ast)
            else:
                assert isinstance(table_element, SymbolTableElement)
                assert isinstance(table_element.symbol, VariableSymbol)
                if not table_element.symbol.current_value:
                    self.unitialized_variables_used.append(ast)


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
        symbol_table = self.symbol_table_stack[-1]
        assert isinstance(symbol_table, SymbolTable)
        return symbol_table

    def check_for_narrowing_result(self, declared_data_type: DataType, ast: AST):
        resulting_data_type_visitor = ASTVisitorResultingDataType(self.get_last_symbol_table())
        ast.accept(resulting_data_type_visitor)
        assert resulting_data_type_visitor.resulting_data_type is not None

        # This is the data type that was declared in the input program

        if declared_data_type != resulting_data_type_visitor.resulting_data_type and not is_richer_than(
                declared_data_type, resulting_data_type_visitor.resulting_data_type):
            print(
                "WARN: narrowing result of expression from datatype '" +
                resulting_data_type_visitor.resulting_data_type.name + "' to datatype '" + declared_data_type.name)

    def visit_ast_assignment(self, binExpr: ASTBinaryExpression):
        assert binExpr.token.token_type == TokenType.ASSIGNMENT_EXPRESSION
        symbol_table = self.get_last_symbol_table()
        invalid_var_usage = ASTVisitorUnavailableVariableUsage(symbol_table)
        binExpr.left.accept(invalid_var_usage)
        invalid_var_usage.visit_ast_binary_expression(binExpr.right)
        if len(invalid_var_usage.unitialized_variables_used) == 0 and len(
                invalid_var_usage.undeclared_variables_used) == 0:
            symbol = symbol_table.lookup(binExpr.left.get_token_content()).symbol
            assert isinstance(symbol, VariableSymbol)
            if not symbol.is_const:

                self.check_for_narrowing_result(binExpr.left.token.token_type, binExpr)

                symbol.current_value = binExpr.right

            else:
                raise SemanticError("Cannot assign value to const variable '" + binExpr.left.get_token_content() + "'")
        else:

            error_text = ""

            if len(invalid_var_usage.unitialized_variables_used) != 0:
                for variable in invalid_var_usage.unitialized_variables_used:
                    error_text += "Variable with name '" + variable.get_token_content() + "' used in an expression is found but is unitialized! \n"

            if len(invalid_var_usage.undeclared_variables_used) != 0:
                for variable in invalid_var_usage.undeclared_variables_used:
                    error_text += "Variable with name '" + variable.get_token_content() + "' is undeclared: not found in the symbol table \n"

            raise SemanticError(error_text)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        if ast.get_token().token_type == TokenType.ASSIGNMENT_EXPRESSION:
            self.visit_ast_assignment(ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        symbol_table = self.get_last_symbol_table()

        if symbol_table.lookup(ast.var_name.get_token_content()) is None:
            data_type, is_const = divide_type_attributes(ast.type_attributes)
            symbol_table.insert_symbol(
                SymbolTableElement(ast.var_name.get_token_content(), VariableSymbol(data_type, is_const)))
        else:
            raise AlreadyDeclaredError(
                "Variable with name '" + str(ast.var_name) + "' has already been declared in this scope!")

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.visit_ast_variable_declaration(ast)
        variable_symbol = self.get_last_symbol_table().lookup(ast.var_name.get_token_content()).symbol
        assert isinstance(variable_symbol, VariableSymbol)
        try:

            data_type, is_const = divide_type_attributes(ast.type_attributes)
            self.check_for_narrowing_result(data_type, ast.value)

            variable_symbol.current_value = ast.value
        except IncompatibleTypesError as e:
            raise e
