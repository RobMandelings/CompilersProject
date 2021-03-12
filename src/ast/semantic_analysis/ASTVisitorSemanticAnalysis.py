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


class ASTVisitorInvalidVariableUsage(ASTVisitor):
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

    @staticmethod
    def types_compatible(data_type: DataType, token_type: TokenType, value):
        """
        Returns true if the given data type and token type are compatible.
        If convertible, does a conversion to the data type first and then returns a (bool, newValue) pair
        If not convertible, returns false
        """
        if data_type == DataType.INT:
            if token_type == TokenType.INT_LITERAL or token_type == TokenType.DOUBLE_LITERAL:
                return True
        elif data_type == DataType.FLOAT:
            if token_type == TokenType.INT_LITERAL:
                return True
            elif token_type == TokenType.DOUBLE_LITERAL:
                return True
        elif data_type == DataType.CHAR:
            if token_type == TokenType.INT_LITERAL:
                return True

        return False

    def do_type_conversion(self, destination_data_type: DataType, value: AST):
        """

        """

    def set_value_if_possible(self, symbol: Symbol, value: AST):
        if not isinstance(symbol, VariableSymbol):
            # TODO maybe for functions it's different
            raise IncompatibleTypesError(
                "The symbol is not of type VariableSymbol, so we can't assign it to such a value")
        else:

            compatible = self.types_compatible(symbol.data_type, value.token.token_type,
                                               value.get_token_content())

            if compatible:
                symbol.current_value = value
            else:
                raise IncompatibleTypesError("Types are incompatible: trying to set a variable of data type " + str(
                    symbol.data_type) + " to a value of type " + value.token.token_type + " (content: " + value.get_token_content() + ")")

    def visit_ast_assignment(self, ast: ASTBinaryExpression):
        assert ast.token.token_type == TokenType.ASSIGNMENT_EXPRESSION
        symbol_table = self.get_last_symbol_table()
        invalid_var_usage = ASTVisitorInvalidVariableUsage(symbol_table)
        invalid_var_usage.visit_ast_leaf(ast.left)
        invalid_var_usage.visitor_ast_binary_expression(ast.right)
        if len(invalid_var_usage.unitialized_variables_used) == 0 and len(
                invalid_var_usage.undeclared_variables_used) == 0:
            try:
                # We know that there are no undeclared or uninitialied variables found, so there must exist a symbol element
                self.set_value_if_possible(symbol_table.lookup(ast.left.get_token_content()).symbol, ast.right)
            except IncompatibleTypesError:
                raise
        else:

            error_text = ""

            if len(invalid_var_usage.unitialized_variables_used) != 0:
                for variable in invalid_var_usage.unitialized_variables_used:
                    error_text += "Variable with name '" + variable.get_token_content() + "' used in an expression is found but is unitialized! \n"

            if len(invalid_var_usage.undeclared_variables_used) != 0:
                for variable in invalid_var_usage.undeclared_variables_used:
                    error_text += "Variable with name '" + variable.get_token_content() + "' is undeclared: not found in the symbol table \n"

            raise SemanticError(error_text)

    def visitor_ast_binary_expression(self, ast: ASTBinaryExpression):
        if ast.get_token().token_type == TokenType.ASSIGNMENT_EXPRESSION:
            self.visit_ast_assignment(ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        symbol_table = self.get_last_symbol_table()

        if symbol_table.lookup(ast.var_name.get_token_content()) is None:
            symbol_table.insert_symbol(
                SymbolTableElement(ast.var_name.get_token_content(), VariableSymbol(ast.type_attributes)))
        else:
            raise AlreadyDeclaredError(
                "Variable with name '" + str(ast.var_name) + "' has already been declared in this scope!")

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.visit_ast_variable_declaration(ast)
        variable_symbol = self.get_last_symbol_table().lookup(ast.var_name.get_token_content()).symbol
        assert isinstance(variable_symbol, VariableSymbol)
        try:
            self.set_value_if_possible(variable_symbol, ast.value)
        except IncompatibleTypesError as e:
            print("An error occurred during semantical analysis:")
            print(e)
