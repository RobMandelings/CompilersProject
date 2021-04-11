from abc import ABC
from enum import Enum

from src.ast.ASTTokens import DataTypeToken


class IToLLVM(ABC):

    def to_llvm(self):
        """
        Returns a string which contains all the LLVM generated llvm code of the object
        """
        raise NotImplementedError


def get_llvm_type(data_type: DataTypeToken):
    """
    Converts the given data type into a string which represents the corresponding data type in llvm
    data_type: the datatype to get the string for
    """
    if data_type == DataTypeToken.CHAR:
        return 'i8'
    elif data_type == DataTypeToken.INT:
        return 'i32'
    elif data_type == DataTypeToken.FLOAT:
        return 'float'
    elif data_type == DataTypeToken.DOUBLE:
        return 'double'
    else:
        raise NotImplementedError


def get_llvm_for_literal(literal, as_data_type: DataTypeToken):
    """
    A literal needs to be put in the correct notation depending on where it is used.
    E.g if you want to compare a double to an integer, both types need to be converted to double.
    If the literal is the integer, this needs to put into scientific notation to be recognized as a double
    """
    assert isinstance(literal, int) or isinstance(literal, float)

    if as_data_type.is_integral_type():
        return str(literal)
    elif as_data_type.is_floating_point_type():
        # Put the number into scientific notation
        return "{:e}".format(literal)
    else:
        raise NotImplementedError


class ComparisonDataType(Enum):
    INT = 'icmp',
    FLOAT = 'fcmp'
