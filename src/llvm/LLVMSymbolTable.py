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
        assert lookup is not None and isinstance(lookup, LLVMValue.LLVMRegister)
        return lookup

    def insert_variable(self, variable_name: str, variable_register: LLVMValue.LLVMRegister):
        assert isinstance(variable_register, LLVMValue.LLVMRegister)
        assert self.lookup_local(variable_name) is None
        self.insert_symbol(variable_name, variable_register)
