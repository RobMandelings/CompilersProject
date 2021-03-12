from enum import Enum, auto

from src.ast.ASTs import AST


class DataType(Enum):
    CHAR = auto()
    INT = auto()
    FLOAT = auto()

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


class Symbol:

    def __init__(self):
        pass


class VariableSymbol(Symbol):

    def __init__(self, attributes: list):
        super().__init__()
        self.data_type = None
        self.is_const = False
        self.current_value = None
        self.init_member_variables(attributes)
        print("Hello")

    def init_member_variables(self, attributes: list):
        for attribute in attributes:
            assert isinstance(attribute, AST)
            if DataType.get_data_type_from_name(attribute.get_token_content()) is not None:
                assert self.data_type is None, "There are multiple datatypes defined. " \
                                               "This should not be possible as it should have halted with a syntax error"
                self.data_type = DataType.get_data_type_from_name(attribute.get_token_content())
            elif attribute.get_token_content() == 'const':
                self.is_const = True
            else:
                NotImplementedError('This attribute is not supported yet')
        assert self.data_type is not None and self.is_const is not None

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
