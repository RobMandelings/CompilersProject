import src.DataType as DataType
import src.SymbolTable as SymbolTable


class Symbol:

    def __init__(self, symbol_name: str):
        self.symbol_name = symbol_name

    def get_name(self):
        return self.symbol_name


class VariableSymbol(Symbol):

    def __init__(self, symbol_name: str, data_type: DataType.DataType, const, initialized):
        super().__init__(symbol_name)
        self.data_type = data_type
        self.const = const
        self.initialized = initialized
        self.reaching_definition_ast = None

    def get_data_type(self):
        assert isinstance(self.data_type, DataType.DataType)
        return self.data_type

    def is_const(self):
        assert isinstance(self.const, bool)
        return self.const

    def has_reaching_defintion(self):
        return self.reaching_definition_ast is not None

    def get_reaching_definition(self):
        return self.reaching_definition_ast

    def is_initialized(self):
        return self.initialized


class FunctionSymbol(Symbol):

    def __init__(self, symbol_name: str, params: list, return_type: DataType.DataType):
        """
        params: list of ast variable declarations which correspond to the paramters of this function
        return type: DataType to indicate what the return type is
        """
        super().__init__(symbol_name)
        self.params = params
        self.return_type = return_type

    def get_params(self):
        return self.params

    def get_return_type(self):
        return self.return_type


class SymbolTableSemanticAnalyser(SymbolTable.SymbolTable):

    def __init__(self):
        super().__init__()

    def lookup_variable(self, symbol: str):
        """
        Looks up a variable in the symbol table
        PRE-CONDITION: the symbol name given for lookup should result in a symbol which is actually a VariableSymbol.
        The semantic error checks should be executed before using this
        """
        symbol = self.lookup(symbol)
        assert isinstance(symbol, Symbol)
        variable = symbol
        assert isinstance(variable, VariableSymbol)
        return variable

    def set_parent(self, parent):
        """
        Sets the parent of this symbol table to another symbol table.
        """
        assert isinstance(parent, SymbolTableSemanticAnalyser) and not id(self) == id(parent)
        self.parent = parent
