from abc import ABC, abstractmethod
from enum import Enum, auto

import src.ast.ASTTokens as ASTTokens
import src.ast.ASTs as ASTs
import src.ast.llvm.LLVMInterfaces as LLVMInterfaces


class LLVMValueToken(Enum):
    LITERAL = auto()
    REGISTER = auto()


class LLVMValue(LLVMInterfaces.IToLLVM, ASTs.IHasDataType, ABC):

    def __init__(self, value: str, data_type):
        self.data_type = data_type
        self.value = value

    def __str__(self):
        return self.to_llvm()

    def set_data_type(self, data_type: ASTTokens.DataTypeToken):
        """
        PRE-CONDITION: Can only be set once (must be None before)

        Used if the data type of the value is not know when creating the new value so you can set it at a later time
        e.g. when the resulting data type is computed somewhere else than were you create the value.
        """
        if self.data_type is not None:
            if self.data_type is data_type:
                print(
                    f"WARN: Register data type has already been set to {self.data_type.name}. "
                    "You might want to remove the duplicate 'set_data_type'")
            else:
                raise ValueError('Register cannot be set to another data_type once initialised')
        self.data_type = data_type
        return self

    def get_data_type(self):
        """
        PRE-CONDITION: the data type must be set at this point
        """
        assert isinstance(self.data_type, ASTTokens.DataTypeToken)
        return self.data_type

    @abstractmethod
    def get_llvm_value_token(self):
        pass

    def get_value(self):
        return self.value

    def to_llvm(self):
        return str(self.value)


class LLVMLiteral(LLVMValue):

    def __init__(self, value: str, data_type: ASTTokens.DataTypeToken):
        super().__init__(value, data_type)

    def get_llvm_value_token(self):
        return LLVMValueToken.LITERAL


class LLVMRegister(LLVMValue):

    def __init__(self, value: str, data_type=None):
        """
        By default, sets the data type to none (usually the data type of the newly created register is not know immediately)
        """
        assert value.startswith('%')
        super().__init__(data_type, value)

    def get_llvm_value_token(self):
        return LLVMValueToken.REGISTER
