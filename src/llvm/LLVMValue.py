from abc import ABC, abstractmethod
from enum import Enum, auto

import src.DataType
import src.DataType as DataType
import src.ast.ASTs as ASTs
import src.llvm.LLVMInterfaces as LLVMInterfaces


class LLVMValueToken(Enum):
    LITERAL = auto()
    REGISTER = auto()


class LLVMValue(LLVMInterfaces.IToLLVM, src.DataType.IHasDataType, ABC):

    def __init__(self, value, data_type: DataType.DataType):
        self.data_type = data_type
        self.value = value

    def __str__(self):
        return self.to_llvm()

    def set_data_type(self, data_type: DataType.DataType):
        """
        PRE-CONDITION: Can only be set once (must be None before)

        Used if the data type of the value is not know when creating the new value so you can set it at a later time
        e.g. when the resulting data type is computed somewhere else than were you create the value.
        """
        if self.data_type is not None:
            if self.data_type is data_type:
                print(
                    f"WARN: Register data type has already been set to {self.data_type.get_name()}. "
                    "You might want to remove the duplicate 'set_data_type'")
            else:
                raise ValueError('Register cannot be set to another other once initialised')
        self.data_type = data_type
        return self

    def get_data_type(self):
        """
        PRE-CONDITION: the data type must be set at this point
        """
        assert isinstance(self.data_type, DataType.DataType)
        return self.data_type

    def get_data_type_token(self):
        return self.get_data_type().get_token()

    def update_numbering(self, counter):
        pass

    @abstractmethod
    def get_llvm_value_token(self):
        pass

    def get_value(self):
        return self.value

    def to_llvm(self):
        return str(self.value)


class LLVMLiteral(LLVMValue):

    def __init__(self, value: str, data_type: DataType.DataType):
        assert data_type.get_pointer_level() == 0
        super().__init__(value, data_type)

    def get_llvm_value_token(self):
        return LLVMValueToken.LITERAL


class LLVMRegister(LLVMValue):

    def __init__(self, data_type=None):
        """
        By default, sets the data type to none (usually the data type of the newly created register is not known immediately)
        """
        assert data_type is None or isinstance(data_type, DataType.DataType)
        super().__init__(None, data_type)

    def get_value(self):
        """
        Returns the number of this register. Still None if the numbers have not been updated (using update_numbering)
        """
        assert isinstance(self.value, int)
        return self.value

    def to_llvm(self):
        return f'%{self.get_value()}'

    def get_llvm_value_token(self):
        return LLVMValueToken.REGISTER
