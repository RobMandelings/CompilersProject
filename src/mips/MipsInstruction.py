import src.Instruction as Instruction
import src.mips.MipsValue as MipsValue
import src.mips.MipsBasicBlock as MipsBasicBlock
import src.ast.ASTTokens as ASTTokens
import abc

"""
Contains all mips instructions that the compiler can generate
"""

# One line per instruction

class MipsInstruction(abc.ABC, Instruction.Instruction):
    """
    Abstract class for all the mips instructions
    """

    def __init__(self):
        super().__init__()

    def to_mips(self):
        raise NotImplementedError


# ######################### #
# DataTransfer Instructions #
# ######################### #


class LoadWordInstruction(MipsInstruction):

    def __init__(self, register_to_store: MipsValue.MipsRegister, register_address: MipsValue.MipsRegister, offset: int):
        super().__init__()
        self.register_to_store = register_to_store
        self.register_address = register_address
        self.offset = offset

    def to_mips(self):
        return f"lw {self.register_to_store},{self.offset}({self.register_address})"


class StoreWordInstruction(MipsInstruction):

    def __init__(self, register_to_store: MipsValue.MipsRegister, register_address: MipsValue.MipsRegister, offset: int):
        super().__init__()
        self.register_to_store = register_to_store
        self.register_address = register_address
        self.offset = offset

    def to_mips(self):
        return f"sw {self.register_to_store},{self.offset}({self.register_address})"


class LoadUpperImmediateInstruction(MipsInstruction):

    def __init__(self, register_to_store: MipsValue.MipsRegister, immediate: MipsValue.MipsLiteral):
        super().__init__()
        self.register_to_store = register_to_store
        self.immediate = immediate

    def to_mips(self):
        return f"lui {self.register_to_store},{self.immediate}"


class LoadAddressInstruction(MipsInstruction):

    def __init__(self, register_to_load: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__()
        self.register_to_load = register_to_load
        self.label = label

    def to_mips(self):
        return f"la {self.register_to_load},{self.label}"


class LoadImmediateInstruction(MipsInstruction):

    def __init__(self, register_to_load: MipsValue.MipsRegister, immediate: MipsValue.MipsLiteral):
        super().__init__()
        self.register_to_load = register_to_load
        self.immediate = immediate

    def to_mips(self):
        return f"li {self.register_to_load},{self.immediate}"


class MoveFromHiInstruction(MipsInstruction):

    def __init__(self, register_to_move_in: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in

    def to_mips(self):
        return f"mfhi {self.register_to_move_in}"


class MoveFromLoInstruction(MipsInstruction):

    def __init__(self, register_to_move_in: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in

    def to_mips(self):
        return f"mflo {self.register_to_move_in}"


class MoveInstruction(MipsInstruction):

    def __init__(self, register_to_move_in: MipsValue.MipsRegister, register_to_move_from: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in
        self.register_to_move_from = register_to_move_from

    def to_mips(self):
        return f"move {self.register_to_move_in},{self.register_to_move_from}"


# ####################### #
# Arithmetic Instructions #
# ####################### #

class ArithmeticInstruction(MipsInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsValue, resulting_register: MipsValue.MipsRegister = None):
        super().__init__()
        self.resulting_register = resulting_register
        self.first_register = first_register
        self.second_register = second_register


class ArithmeticBinaryInstruction(ArithmeticInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsValue, token: ASTTokens.BinaryArithmeticExprToken, resulting_register: MipsValue.MipsRegister = None):
        super().__init__(first_register, second_register, resulting_register)
        self.token = token

    def to_mips(self):
        operation_string = ""
        if self.token == ASTTokens.BinaryArithmeticExprToken.ADD:
            operation_string = "add"
        elif self.token == ASTTokens.BinaryArithmeticExprToken.SUB:
            operation_string = "sub"
        elif self.token == ASTTokens.BinaryArithmeticExprToken.MUL:
            operation_string = "mul"
        elif self.token == ASTTokens.BinaryArithmeticExprToken.DIV:
            operation_string = "div"
            return operation_string + f" {self.resulting_register.get_name()}, {self.first_register.get_name()}"

        return operation_string + f" {self.resulting_register.get_name()}, {self.first_register.get_name()}, {self.second_register.get_content()}"


class ArithmeticMultiplyOverflowInstruction(ArithmeticInstruction):

    def __init__(self, register_to_multiply_1: MipsValue.MipsRegister, register_to_multiply_2: MipsValue.MipsRegister):
        super().__init__(register_to_multiply_1, register_to_multiply_2)

    def to_mips(self):
        raise NotImplementedError

# ############################### #
# Conditional Branch Instructions #
# ############################### #


class BranchInstruction(MipsInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__()
        self.first_register = first_register
        self.second_register = second_register
        self.label = label


class BranchEqualInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        return f"beq {self.first_register.get_name()},{self.second_register.get_name()},{self.label.name}"


class BranchNotEqualInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        return f"bne {self.first_register.get_name()},{self.second_register.get_name()},{self.label.name}"


class BranchGreaterThanInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        return f"bgt {self.first_register.get_name()},{self.second_register.get_name()},{self.label.name}"


class BranchGreaterThanOrEqualInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        return f"bge {self.first_register.get_name()},{self.second_register.get_name()},{self.label.name}"


class BranchLessThaninstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        return f"blt {self.first_register.get_name},{self.second_register.get_name()},{self.label.name}"


class BranchLessThanOrEqualInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        return f"ble {self.first_register.get_name},{self.second_register.get_content},{self.label.name}"

# ############################### #
# Unconditional Jump Instructions #
# ############################### #


class UnconditionalJumpInstruction(MipsInstruction):

    def __init__(self, to_jump_to: MipsBasicBlock.MipsBasicBlock or MipsValue.MipsRegister):
        super().__init__()
        self.to_jump_to = to_jump_to


class JumpInstruction(UnconditionalJumpInstruction):

    def __init__(self, to_jump_to: MipsBasicBlock.MipsBasicBlock):
        super().__init__(to_jump_to)

    def to_mips(self):
        return f"j {self.to_jump_to.name}"


class JumpRegisterInstruction(UnconditionalJumpInstruction):

    def __init__(self, to_jump_to: MipsValue.MipsRegister):
        super().__init__(to_jump_to)

    def to_mips(self):
        return f"jr {self.to_jump_to.get_name()}"


class JumpAndLinkInstruction(UnconditionalJumpInstruction):

    def __init__(self, to_jump_to: MipsBasicBlock.MipsBasicBlock):
        super().__init__(to_jump_to)

    def to_mips(self):
        return f"jal {self.to_jump_to.name}"

# ####################### #
# Comparison Instructions #
# ####################### #


class SetOnLessThanInstruction(MipsInstruction):

    def __init__(self, resulting_register: MipsValue.MipsRegister, first_register: MipsValue.MipsRegister, second_value: MipsValue.MipsValue):
        super().__init__()
        self.resulting_register = resulting_register
        self.first_register = first_register
        self.second_value = second_value

    def to_mips(self):
        if isinstance(self.second_value, MipsValue.MipsLiteral):
            immediate = True
        elif isinstance(self.second_value, MipsValue.MipsRegister):
            immediate = False
        else:
            raise NotImplementedError

        operation_string = ""
        if immediate:
            operation_string = "slti"
        else:
            operation_string = "slt"

        return f"{operation_string} {self.resulting_register.get_name()},{self.first_register.get_name()},{self.second_value.get_content()}"

