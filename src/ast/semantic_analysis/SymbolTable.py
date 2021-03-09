class SymbolTableElement:

    def __init__(self, symbol_name: str, type: str, ):
        self.symbol_name = symbol_name
        self.type = type


class SymbolTable:

    def __init__(self):
        self.parent = None
        self.symbols = dict()

    def lookupLocal(self, symbol: str):
        lookup = self.symbols[symbol]
        assert isinstance(lookup, SymbolTableElement)
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
