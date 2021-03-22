from abc import ABC

from src.ast.ASTTokens import DataTypeToken, BinaryArithmeticExprToken
from src.ast.llvm.LLVMBuilder import LLVMBuilder
from src.ast.llvm.LLVMUtils import IToLLVM


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

    def __init__(self, resulting_reg: str):
        super().__init__()
        assert resulting_reg is not None
        self.resulting_reg = resulting_reg

    def is_terminator(self):
        return False

    def get_resulting_register(self):
        return self.resulting_reg

    def to_llvm(self):
        return f"{self.resulting_reg} = "


class AllocaInstruction(AssignInstruction):

    def __init__(self, resulting_reg: str, data_type_to_allocate: DataTypeToken):
        super().__init__(resulting_reg)
        self.data_type_to_allocate = data_type_to_allocate

    def to_llvm(self):
        return super().to_llvm() + f"alloca {LLVMBuilder.get_llvm_type(self.data_type_to_allocate)}, align 4"

    def is_terminator(self):
        return False


class LoadInstruction(AssignInstruction):
    """
    Loads the value of a pointer type into a register (for example, load an i32 from register %1 of type i32* in register %2)
    """

    def __init__(self, resulting_reg: str, data_type_to_load: DataTypeToken, load_from_reg: str):
        super().__init__(resulting_reg)
        self.data_type_to_allocate = data_type_to_load
        self.load_from_reg = load_from_reg

    def to_llvm(self):
        llvm_type = LLVMBuilder.get_llvm_type(self.data_type_to_allocate)
        return super().to_llvm() + f"load {llvm_type}, {llvm_type}* {self.load_from_reg}"


class ConditionalBranchInstruction(Instruction):
    """
    Conditional Branch instruction for LLVM
    """

    def __init__(self, condition_reg: str, label_iftrue: str, label_iffalse):
        super().__init__()
        self.condition_reg = condition_reg
        self.label_iftrue = label_iftrue
        self.label_iffalse = label_iffalse

    def to_llvm(self):
        return f"br i1 {self.condition_reg}, label {self.label_iftrue}, label {self.label_iffalse}"

    def is_terminator(self):
        return True


class UnconditionalBranchInstruction(Instruction):

    def __init__(self, dest_label: str):
        """
        dest label: the label to branch to
        """
        super().__init__()
        self.dest_label = dest_label

    def to_llvm(self):
        return f"br label {self.dest_label}"

    def is_terminator(self):
        return True


class BinaryArithmeticInstruction(AssignInstruction):
    """
    Instructions which apply arithmetics on registers and puts the result in another register
    """

    def __init__(self, resulting_reg: str, operation: BinaryArithmeticExprToken, data_type_reg1: DataTypeToken,
                 operand_reg1: str,
                 data_type_reg2: DataTypeToken, operand_reg2: str):
        super().__init__(resulting_reg)

    def to_llvm(self):
        return super().to_llvm()
