from abc import ABC

from src.ast.ASTTokens import DataTypeToken


class IToLLVM(ABC):

    def to_llvm(self):
        """
        returns: string which contains all the LLVM generated llvm code of the object
        """
        raise NotImplementedError


def get_llvm_type(data_type: DataTypeToken):
    """
    Converts the given data type into a string which represents the corresponding data type in llvm
    data_type: the datatype to get the string for
    """
    if data_type == DataTypeToken.CHAR:
        return "i8"
    elif data_type == DataTypeToken.INT:
        return "i32"
    elif data_type == DataTypeToken.FLOAT:
        return "float"
