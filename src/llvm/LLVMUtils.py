from enum import Enum

import src.DataType as DataType
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


def get_llvm_for_literal(literal: LLVMValue.LLVMLiteral, as_data_type: DataType.DataTypeToken):
    """
    A literal needs to be put in the correct notation depending on where it is used.
    E.g if you want to compare a double to an integer, both types need to be converted to double.
    If the literal is the integer, this needs to put into scientific notation to be recognized as a double
    """

    assert literal.get_data_type_token() == as_data_type or DataType.DataTypeToken.is_richer_than(as_data_type,
                                                                                                  literal.get_data_type_token())

    if as_data_type.is_integral():
        return str(literal.get_value())
    elif as_data_type.is_floating_point():
        # Put the number into scientific notation
        return "{:e}".format(literal.get_value())
    else:
        raise NotImplementedError


class ComparisonDataType(Enum):
    INT = 'icmp',
    FLOAT = 'fcmp'
