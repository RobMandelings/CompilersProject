from abc import abstractmethod, ABC

from src.ast.ASTTokens import DataTypeToken
from src.ast.llvm.LLVMBuilder import LLVMBuilder, IToLLVM


class Instruction(IToLLVM, ABC):

    def __init__(self):
        pass

    def is_terminator(self):
        raise NotImplementedError

    def to_llvm(self):
        raise NotImplementedError


class AssignInstruction(Instruction):
    """
    Instruction which has a resulting register
    """

    def __init__(self, resulting_register: str):
        super().__init__()
        assert resulting_register is not None
        self.resulting_register = resulting_register

    def is_terminator(self):
        return False

    def get_resulting_register(self):
        return self.resulting_register

    def to_llvm(self):
        return f"{self.resulting_register} = "


class AllocaInstruction(AssignInstruction):

    def __init__(self, resulting_register: str, data_type_to_allocate: DataTypeToken):
        super().__init__(resulting_register)
        self.data_type_to_allocate = data_type_to_allocate

    def to_llvm(self):
        return super().to_llvm() + f"alloca {LLVMBuilder.get_llvm_type(self.data_type_to_allocate)}, align 4"

    def is_terminator(self):
        return False
