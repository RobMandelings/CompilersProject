from src.ast.semantic_analysis.SymbolTable import *
from src.ast.ASTs import *


class SemanticError(Exception):
    pass


class AlreadyDeclaredError(SemanticError):
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

    def visit_ast_leaf(self, ast: ASTLeaf):
        pass

    def visit_ast_internal(self, ast: ASTInternal):
        # TODO if isBlock()
        # self.create_symbol_table()
        # if ast.token.token_type == TokenType.VARIABLE_DECLARATION:
        pass
        # if ast.token.token_type == TokenType.ADD_EXPRESSION

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        symbol_table = self.get_last_symbol_table()

        if symbol_table.lookup(ast.var_name.get_token_content()) is None:
            symbol_table.insert_symbol(
                SymbolTableElement(ast.var_name.get_token_content(), VariableSymbol(ast.type_attributes)))
        else:
            raise AlreadyDeclaredError(
                "Variable with name '" + str(ast.var_name) + "' has already been declared in this scope!")

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        pass
