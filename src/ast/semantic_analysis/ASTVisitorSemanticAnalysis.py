from src.ast.semantic_analysis.SymbolTable import *
from src.ast.ASTs import *


class SemanticError(Exception):
    pass


class AlreadyDeclaredError(SemanticError):
    pass


class UndeclaredError(SemanticError):
    pass


class IncompatibleTypesError(Exception):
    pass


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

    def compatible_types_or_convert(self, data_type: DataType, token_type: TokenType, value):
        """
        Returns true if the given data type and token type are compatible.
        If convertible, does a conversion to the data type first and then returns a (bool, newValue) pair
        If not convertible, returns false
        """
        if data_type == DataType.INT:
            if token_type == TokenType.INT_LITERAL:
                return True, None
            elif token_type == TokenType.DOUBLE_LITERAL:
                return True, int(value)
        elif data_type == DataType.FLOAT:
            if token_type == TokenType.INT_LITERAL:
                return True, None
            elif token_type == TokenType.DOUBLE_LITERAL:
                return True, None
        elif data_type == DataType.CHAR:
            if token_type == TokenType.INT_LITERAL:
                return True, None

        return False, None

    def do_type_conversion(self, destination_data_type: DataType, value: AST):
        """

        """

    def set_value_if_possible(self, symbol: Symbol, value: ASTLeaf):
        if not isinstance(symbol, VariableSymbol):
            # TODO maybe for functions it's different
            raise IncompatibleTypesError(
                "The symbol is not of type VariableSymbol, so we can't assign it to such a value")
        else:

            compatible, new_value = self.compatible_types_or_convert(symbol.data_type, value.token.token_type,
                                                                     value.get_token_content())

            if compatible:
                if new_value is None:
                    symbol.current_value = value.get_token_content()
                else:
                    symbol.current_value = new_value
            else:
                raise IncompatibleTypesError("Types are incompatible: trying to set a variable of data type " + str(
                    symbol.data_type) + " to a value of type " + value.token.token_type + " (content: " + value.get_token_content() + ")")

    def visit_ast_assignment(self, ast: ASTBinaryExpression):
        assert ast.token.token_type == TokenType.ASSIGNMENT_EXPRESSION
        symbol_table = self.get_last_symbol_table()
        symbol_element = symbol_table.lookup(ast.left.get_token_content())
        if not symbol_element:
            raise UndeclaredError(
                "The symbol_element with name '" + ast.left.get_token_content() + "' is undeclared: not found in the symbol table")
        else:
            try:
                self.set_value_if_possible(symbol_element.symbol, ast.right)
            except IncompatibleTypesError:
                raise

    def visit_ast_leaf(self, ast: ASTLeaf):
        pass

    def visit_ast_internal(self, ast: ASTInternal):
        pass

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
