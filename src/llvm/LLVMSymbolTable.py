import src.SymbolTable as SymbolTable
import src.llvm.LLVMValue as LLVMValue


class LLVMSymbolTable(SymbolTable.SymbolTable):
    """
    (Sort of) symbol table which maps variables to their corresponding registers, in LLVM scopes don't really
    exist but they are necessary in order to generate keep track of the right registers
    """

    def __init__(self):
        """
        variable_mapper: maps variables to LLVMRegisters
        """
        super().__init__()

    def get_variable_register(self, variable_name):
        lookup = self.lookup(variable_name)
        assert lookup is not None and isinstance(lookup, LLVMSymbol)
        return lookup.get_register()

    def get_array_symbol(self, array_name):
        lookup = self.lookup(array_name)
        assert lookup is not None and isinstance(lookup, LLVMArraySymbol)
        return lookup

    def get_variable_symbol(self, variable_name):
        lookup = self.lookup(variable_name)
        assert lookup is not None and isinstance(lookup, LLVMSymbol)
        return lookup

    def insert_variable(self, variable_name: str, variable_register: LLVMValue.LLVMRegister):
        assert isinstance(variable_register, LLVMValue.LLVMRegister)
        assert self.lookup_local(variable_name) is None
        symbol = LLVMSymbol(variable_register)
        self.insert_symbol(variable_name, symbol)

    def insert_array(self, array_name: str, array_register: LLVMValue.LLVMRegister, array_size: LLVMValue.LLVMLiteral):
        assert isinstance(array_register, LLVMValue.LLVMRegister)
        assert self.lookup_local(array_name) is None
        assert isinstance(array_size, LLVMValue.LLVMLiteral)
        symbol = LLVMArraySymbol(array_register, array_size)
        self.insert_symbol(array_name, symbol)


class LLVMSymbol:
    """
    Wrapper for LLVMSymbolTable dict values
    """
    def __init__(self, register: LLVMValue.LLVMRegister):
        self.register = register
        assert isinstance(self.register, LLVMValue.LLVMRegister)

    def get_register(self):
        return self.register


class LLVMArraySymbol(LLVMSymbol):
    """
    Wrapper for LLVMSymbolTable dict values which refer to array objects
    """
    def __init__(self, register: LLVMValue.LLVMRegister, size: LLVMValue.LLVMLiteral):
        super(LLVMArraySymbol, self).__init__(register)
        self.size = size
        assert isinstance(self.size, LLVMValue.LLVMLiteral)

    def get_size(self):
        return self.size
