from src.ast.ASTTokens import DataTypeToken
from src.ast.llvm.LLVMUtils import IToLLVM


class LLVMRegister(IToLLVM):
    """
    Represents a local register in LLVM. Also keeps track of the current DataType of this register
    """

    def __init__(self, index, data_type: DataTypeToken, pointer_type=False):
        """
        index: should uniquely represent this register in LLVM

        """
        self.__index = index
        self.data_type = data_type
        self.pointer_type = pointer_type

    def get_data_type(self):
        assert isinstance(self.data_type, DataTypeToken)
        return self.data_type

    def is_pointer_type(self):
        """
        Returns whether or not this register is a pointer (e.g. i32*) to the datatype
        """
        return self.pointer_type

    def get_index(self):
        return self.__index

    def to_llvm(self):
        return f'%{self.__index}'
