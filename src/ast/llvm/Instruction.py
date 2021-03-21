from abc import abstractmethod

from src.ast.ASTTokens import DataTypeToken
from src.ast.llvm.LLVMBuilder import LLVMBuilder


class Instruction:

    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def is_terminator(self):
        raise NotImplementedError


class AssignInstruction(Instruction):
    """
    Instruction which has a resulting register
    """

    def __init__(self, resulting_register: str):
        super().__init__()
        assert resulting_register is not None
        self.resulting_register = resulting_register

    def get_resulting_register(self):
        return self.resulting_register

    @abstractmethod
    def __str__(self):
        return f"{self.resulting_register} = "


class AllocaInstruction(AssignInstruction):

    def __init__(self, resulting_register: str, data_type_to_allocate: DataTypeToken):
        super().__init__(resulting_register)
        self.data_type_to_allocate = data_type_to_allocate

    def __str__(self):
        return super().__str__() + f"alloca {LLVMBuilder.get_llvm_type(self.data_type_to_allocate)}, align 4"

    def is_terminator(self):
        return False
