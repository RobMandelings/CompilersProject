from enum import Enum, auto

from src.ast.ASTs import AST, TokenType


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
    if token_type == TokenType.CHAR_TYPE:
        return DataType.CHAR
    elif token_type == TokenType.INT_TYPE:
        return DataType.INT
    elif token_type == TokenType.FLOAT_TYPE:
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

    def __init__(self, data_type: DataType, is_const):
        super().__init__()
        self.data_type = data_type
        self.is_const = is_const
        self.current_value = None

    def get_data_type(self):
        assert isinstance(self.data_type, DataType)
        return self.data_type

    def is_const(self):
        assert isinstance(self.is_const, bool)
        return self.is_const


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

    def insert_symbol(self, symbol: SymbolTableElement):
        assert self.lookup(symbol.symbol_name) is None
        self.symbols[symbol.symbol_name] = symbol
        assert self.lookup(symbol.symbol_name) is not None
