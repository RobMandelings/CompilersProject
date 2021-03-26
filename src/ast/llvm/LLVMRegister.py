from src.ast.ASTTokens import DataTypeToken


class LLVMRegister:
    """
    Represents a local register in LLVM. Also keeps track of the current DataType of this register
    """

    def __init__(self, name, data_type: DataTypeToken = None):
        self.data_type = data_type
        self.__name = name

    def get_data_type(self):
        assert isinstance(self.data_type, DataTypeToken)
        return self.data_type

    def get_name(self):
        return self.__name
