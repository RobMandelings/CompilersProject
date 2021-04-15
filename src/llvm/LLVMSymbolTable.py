from src.semantic_analysis.SymbolTable import *
import src.llvm.LLVMValue as LLVMValues


class LLVMVariableSymbol(Symbol):

    def __init__(self, symbol_name: str, current_register: LLVMValues.LLVMRegister):
        super().__init__(symbol_name)
        assert current_register.data_type is not None
        self.current_register = current_register

    def get_data_type(self):
        return self.get_current_register().get_data_type()

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
