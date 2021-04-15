from enum import Enum

import src.ast.ASTTokens as ASTTokens
import src.llvm.LLVMValue as LLVMValue


class LLVMCounter:

    def __init__(self):
        self.__counter = 0

    def __str__(self):
        return str(self.__counter)

    def get_value(self):
        return self.__counter

    def increase(self):
        """
        Increases the counter by one and returns the counter
        """
        self.__counter += 1
        return self


def get_llvm_type(data_type: ASTTokens.DataTypeToken):
    """
    Converts the given data type into a string which represents the corresponding data type in llvm
    data_type: the datatype to get the string for
    """
    if data_type == ASTTokens.DataTypeToken.CHAR:
        return 'i8'
    elif data_type == ASTTokens.DataTypeToken.INT:
        return 'i32'
    elif data_type == ASTTokens.DataTypeToken.FLOAT:
        return 'float'
    elif data_type == ASTTokens.DataTypeToken.DOUBLE:
        return 'double'
    else:
        raise NotImplementedError


def get_llvm_for_literal(literal: LLVMValue.LLVMLiteral, as_data_type: ASTTokens.DataTypeToken):
    """
    A literal needs to be put in the correct notation depending on where it is used.
    E.g if you want to compare a double to an integer, both types need to be converted to double.
    If the literal is the integer, this needs to put into scientific notation to be recognized as a double
    """

    assert literal.get_data_type() == as_data_type or ASTTokens.DataTypeToken.is_richer_than(as_data_type,
                                                                                             literal.get_data_type())

    if as_data_type.is_integral_type():
        return str(literal.get_value())
    elif as_data_type.is_floating_point_type():
        # Put the number into scientific notation
        return "{:e}".format(literal.get_value())
    else:
        raise NotImplementedError


class ComparisonDataType(Enum):
    INT = 'icmp',
    FLOAT = 'fcmp'
