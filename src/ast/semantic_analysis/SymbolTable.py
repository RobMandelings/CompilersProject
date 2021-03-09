from enum import Enum, auto


class DataType(Enum):
    CHAR = auto()
    INT = auto()
    FLOAT = auto()
    DOUBLE = auto()
    CONST = auto()


class SymbolType:

    def __init__(self):
        pass


class VariableSymbolType(SymbolType):

    def __init__(self, type_specifier: DataType, type_attributes: list):
        super().__init__()
        self.type_specifier = type_specifier
        self.type_attributes = type_attributes


class SymbolTableElement:

    def __init__(self, symbol_name: str, symbol_type: SymbolType):
        self.symbol_name = symbol_name
        self.symbol_type = symbol_type


class SymbolTable:

    def __init__(self):
        self.parent = None
        self.symbols = dict()

    def lookupLocal(self, symbol: str):
        lookup = self.symbols[symbol]
        assert lookup is None or isinstance(lookup, SymbolTableElement)
        return lookup

    def lookup(self, symbol):
        lookup_local = self.symbols[symbol]
        if lookup_local is None:
            if self.parent is not None:
                assert isinstance(self.parent, SymbolTable)
                return self.parent.lookup(symbol)
            else:
                return None
        else:
            return lookup_local
