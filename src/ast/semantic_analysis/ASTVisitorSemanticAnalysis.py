from src.ast.semantic_analysis import SymbolTable
from src.ast.ASTs import *


class ASTVisitorSemanticAnalysis(ASTVisitor):

    def __init__(self):
        super().__init__()
        self.symbol_table_stack = list()
        # TODO needs to be removed once the concept of 'blocks' is introduced
        self.create_symbol_table()

    def create_symbol_table(self):
        if len(self.symbol_table_stack) == 0:
            # First symbol table created
            self.symbol_table_stack.append(SymbolTable.SymbolTable())
        else:
            parent_symbol_table = self.symbol_table_stack[-1]
            new_symbol_table = SymbolTable.SymbolTable()
            new_symbol_table.parent = parent_symbol_table
            self.symbol_table_stack.append(new_symbol_table)

    def visitASTLeaf(self, ast):
        pass

    def visitASTInternal(self, ast):
        # TODO if isBlock()
        # self.create_symbol_table()
        # if ast.token.token_type == TokenType.VARIABLE_DECLARATION:
        pass
