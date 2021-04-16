import abc


class SymbolTable(abc.ABC):

    def __init__(self):
        self.parent = None
        self.symbols = dict()

    def lookup_local(self, symbol: str):
        if symbol in self.symbols:
            lookup = self.symbols[symbol]
            return lookup
        return None

    def lookup(self, symbol: str):
        lookup = self.lookup_local(symbol)
        if lookup is not None:
            return lookup
        else:
            if self.parent is not None:
                assert isinstance(self.parent, SymbolTable)
                return self.parent.lookup(symbol)
            else:
                return None

    def set_parent(self, parent):
        """
        Sets the parent of this symbol table to another symbol table.
        """
        assert isinstance(parent, SymbolTable) and not id(self) == id(parent)
        self.parent = parent

    def insert_symbol(self, symbol_name, symbol):
        assert self.lookup_local(symbol_name) is None
        self.symbols[symbol_name] = symbol
        assert self.lookup_local(symbol_name) is not None
