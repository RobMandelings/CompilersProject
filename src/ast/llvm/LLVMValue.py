from abc import ABC, abstractmethod
from enum import Enum, auto

from src.ast.ASTTokens import DataTypeToken
from src.ast.ASTs import IHasDataType
from src.ast.llvm.LLVMUtils import IToLLVM


class LLVMValueToken(Enum):
    LITERAL = auto()
    REGISTER = auto()


class LLVMValue(IToLLVM, IHasDataType, ABC):

    def __init__(self, data_type: DataTypeToken, value: str):
        self.data_type = data_type
        self.value = value

    def get_data_type(self):
        return self.data_type

    @abstractmethod
    def get_llvm_value_token(self):
        pass

    def to_llvm(self):
        return self.value


class LLVMLiteral(LLVMValue):

    def get_llvm_value_token(self):
        return LLVMValueToken.LITERAL


class LLVMRegister(LLVMValue):

    def get_llvm_value_token(self):
        return LLVMValueToken.REGISTER
