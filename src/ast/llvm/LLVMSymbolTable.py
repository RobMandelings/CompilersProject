from src.ast.semantic_analysis.SymbolTable import *


class LLVMVariableSymbol(Symbol):

    def __init__(self, symbol_name: str, data_type: DataTypeToken, current_register):
        super().__init__(symbol_name)
        self.data_type = data_type
        self.current_register = current_register

    def get_data_type(self):
        assert isinstance(self.data_type, DataTypeToken)
        return self.data_type

    def get_current_register(self):
        return self.current_register

    def set_current_register(self, register):
        self.current_register = register


class LLVMSymbolTable(SymbolTable):

    def insert_symbol(self, symbol: Symbol):
        # This assertion will expand if more and more symbols are added
        assert isinstance(symbol, LLVMVariableSymbol)
        super().insert_symbol(symbol)

    def lookup_variable(self, symbol_name: str):
        lookup = self.lookup(symbol_name)
        assert isinstance(lookup, LLVMVariableSymbol)
        return lookup
