from src.ast.ASTTokens import DataTypeToken


class Symbol:

    def __init__(self, symbol_name: str):
        self.symbol_name = symbol_name


class VariableSymbol(Symbol):

    def __init__(self, symbol_name: str, data_type: DataTypeToken, const, initialized):
        super().__init__(symbol_name)
        self.data_type = data_type
        self.const = const
        self.initialized = initialized
        self.reaching_definition_ast = None

    def get_data_type(self):
        assert isinstance(self.data_type, DataTypeToken)
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


class SymbolTable:

    def __init__(self):
        self.parent = None
        self.symbols = dict()

    def __lookup_local(self, symbol: str):
        lookup = self.symbols[symbol]
        assert lookup is None or isinstance(lookup, Symbol)
        return lookup

    def lookup(self, symbol: str):
        if symbol in self.symbols:
            lookup_local = self.symbols[symbol]
            return lookup_local
        else:
            if self.parent is not None:
                assert isinstance(self.parent, SymbolTable)
                return self.parent.lookup(symbol)
            else:
                return None

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

    def insert_symbol(self, symbol: Symbol):
        assert self.lookup(symbol.symbol_name) is None
        self.symbols[symbol.symbol_name] = symbol
        assert self.lookup(symbol.symbol_name) is not None
