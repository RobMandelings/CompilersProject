from src.ast.semantic_analysis.SymbolTable import SymbolTable


class SymbolTableManager:
    """
    Holds all the symbol tables within a dictionary: <scope, symbol-table>
    as we still need the SymbolTable after the Semantical Analyser analysed the AST. This is what will be returned afterwards
    """

    def __init__(self):
        # Dict containing all symbol tables in the program.
        # Only retrieve the symbol table corresponding to your current scope
        self.symbol_tables = dict()
        self.symbol_tables["global"] = SymbolTable()

    def add_symbol_table(self, current_scope: str, parent_scope: str):
        assert current_scope != "global", "The 'global' scope name is reserved!"
        assert self.symbol_tables[
                   current_scope] is None, f"The symbol table corresponding with scope name {current_scope} already exists!"

        new_symbol_table = SymbolTable()
        new_symbol_table.parent = self.get_symbol_table(parent_scope)
        self.symbol_tables[current_scope] = new_symbol_table

    def get_symbol_table(self, scope: str):
        """
        Returns the corresponding symbol table for the corresponding scope name
        """
        assert self.symbol_tables[
                   scope] is not None, f"Symbol table not found for name (scope) {scope}. " \
                                       f"Only get the symbol table for your current scope!"

        symbol_table = self.symbol_tables[scope]
        assert isinstance(symbol_table, SymbolTable)
        return symbol_table

    def get_global_symbol_table(self):
        """
        The symbol table you have access to from all places
        """
        return self.get_symbol_table("global")
