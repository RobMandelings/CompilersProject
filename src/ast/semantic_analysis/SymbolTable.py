from enum import Enum

from src.ast.ASTs import TokenType


class DataType(Enum):
    CHAR = 0
    INT = 1
    FLOAT = 2

    @staticmethod
    def get_data_type_from_name(name: str):
        if name == 'int':
            return DataType.INT
        elif name == 'float':
            return DataType.FLOAT
        elif name == 'double':
            return DataType.DOUBLE
        elif name == 'char':
            return DataType.CHAR
        else:
            return None


def convert_token_type_to_data_type(token_type: TokenType):
    if token_type == TokenType.CHAR_TYPE or token_type == TokenType.CHAR_LITERAL:
        return DataType.CHAR
    elif token_type == TokenType.INT_TYPE or token_type == TokenType.INT_LITERAL:
        return DataType.INT
    elif token_type == TokenType.FLOAT_TYPE or token_type == TokenType.FLOAT_LITERAL:
        return DataType.FLOAT
    else:
        raise NotImplementedError("Cannot convert the given tokentype ' " + str(token_type) + "' to a datatype")


def is_richer_than(datatype1: DataType, datatype2: DataType):
    """
    Must be placed outside the DataType class because it would not be fully 'defined' when setting the expected parameter types, weird stuff
    """
    assert isinstance(datatype1, DataType), "Given datatype1 is not an instance of DataType"
    assert isinstance(datatype2, DataType), "Given datatype2 is not an instance of DataType"
    return datatype1.value > datatype2.value


class Symbol:

    def __init__(self):
        pass


class VariableSymbol(Symbol):

    def __init__(self, data_type: DataType, const, initialized):
        super().__init__()
        self.data_type = data_type
        self.const = const
        self.initialized = initialized

    def get_data_type(self):
        assert isinstance(self.data_type, DataType)
        return self.data_type

    def is_const(self):
        assert isinstance(self.const, bool)
        return self.const

    def is_initialized(self):
        return self.initialized


class SymbolTableElement:

    def __init__(self, symbol_name: str, symbol: Symbol):
        self.symbol_name = symbol_name
        self.symbol = symbol


class SymbolTable:

    def __init__(self):
        self.parent = None
        self.symbols = dict()

    def lookup_local(self, symbol: str):
        lookup = self.symbols[symbol]
        assert lookup is None or isinstance(lookup, SymbolTableElement)
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
        symbol_table_element = self.lookup(symbol)
        assert isinstance(symbol_table_element, SymbolTableElement)
        variable = symbol_table_element.symbol
        assert isinstance(variable, VariableSymbol)
        return variable

    def insert_symbol(self, symbol: SymbolTableElement):
        assert self.lookup(symbol.symbol_name) is None
        self.symbols[symbol.symbol_name] = symbol
        assert self.lookup(symbol.symbol_name) is not None
