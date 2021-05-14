import src.Instruction as Instruction
import src.mips.MipsValue as MipsValue
import src.mips.MipsBasicBlock as MipsBasicBlock
import abc

"""
Contains all mips instructions that the compiler can generate
"""


class MipsInstruction(abc.ABC, Instruction.Instruction):

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
        raise NotImplementedError


class StoreWordInstruction(MipsInstruction):

    def __init__(self, register_to_store: MipsValue.MipsRegister, register_address: MipsValue.MipsRegister, offset: int):
        super().__init__()
        self.register_to_store = register_to_store
        self.register_address = register_address
        self.offset = offset

    def to_mips(self):
        raise NotImplementedError


class LoadUpperImmediateInstruction(MipsInstruction):

    def __init__(self, register_to_store: MipsValue.MipsRegister, immediate: MipsValue.MipsLiteral):
        super().__init__()
        self.register_to_store = register_to_store
        self.immediate = immediate

    def to_mips(self):
        raise NotImplementedError


class LoadAddressInstruction(MipsInstruction):

    def __init__(self, register_to_load: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__()
        self.register_to_load = register_to_load
        self.label = label

    def to_mips(self):
        raise NotImplementedError


class LoadImmediateInstruction(MipsInstruction):

    def __init__(self, register_to_load: MipsValue.MipsRegister, immediate: MipsValue.MipsLiteral):
        super().__init__()
        self.register_to_load = register_to_load
        self.immediate = immediate

    def to_mips(self):
        raise NotImplementedError


class MoveFromHiInstruction(MipsInstruction):

    def __init__(self, register_to_move_in: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in

    def to_mips(self):
        raise NotImplementedError


class MoveFromLoInstruction(MipsInstruction):

    def __init__(self, register_to_move_in: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in

    def to_mips(self):
        raise NotImplementedError


class MoveInstruction(MipsInstruction):

    def __init__(self, register_to_move_in: MipsValue.MipsRegister, register_to_move_from: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in
        self.register_to_move_from = register_to_move_from

    def to_mips(self):
        raise NotImplementedError


# ####################### #
# Arithmetic Instructions #
# ####################### #

class ArithmeticInstruction(MipsInstruction):

    def __init__(self, resulting_register: MipsValue.MipsRegister, register_to_add: MipsValue.MipsRegister, secondary_value_to_add: MipsValue.MipsValue = None):
        super().__init__()
        self.resulting_register = resulting_register
        self.register_to_add = register_to_add
        self.secondary_value_to_add = secondary_value_to_add


class ArithmeticAddInstruction(ArithmeticInstruction):

    def __init__(self, resulting_register: MipsValue.MipsRegister, register_to_add: MipsValue.MipsRegister, secondary_value_to_add: MipsValue.MipsValue):
        super().__init__(resulting_register, register_to_add, secondary_value_to_add)

    def to_mips(self):
        raise NotImplementedError


class ArithmeticSubInstruction(ArithmeticInstruction):

    def __init__(self, resulting_register: MipsValue.MipsRegister, register_to_sub: MipsValue.MipsRegister,
                 secondary_value_to_sub: MipsValue.MipsRegister):
        super().__init__(resulting_register, register_to_sub, secondary_value_to_sub)

    def to_mips(self):
        raise NotImplementedError


class ArithmeticMultiplyInstruction(ArithmeticInstruction):

    def __init__(self, resulting_register: MipsValue.MipsRegister, register_to_multiply: MipsValue.MipsRegister,
                 secondary_value_to_multiply: MipsValue.MipsRegister = None):
        super().__init__(resulting_register, register_to_multiply, secondary_value_to_multiply)

    def to_mips(self):
        raise NotImplementedError


class ArithmeticMultiplyOverflowInstruction(ArithmeticMultiplyInstruction):

    def __init__(self, register_to_multiply_1: MipsValue.MipsRegister, register_to_multiply_2: MipsValue.MipsRegister):
        super().__init__(register_to_multiply_1, register_to_multiply_2)

    def to_mips(self):
        raise NotImplementedError


class ArithmeticDivideInstruction(ArithmeticInstruction):

    def __init__(self, register_to_divide_1: MipsValue.MipsRegister, register_to_divide_2: MipsValue.MipsRegister):
        super().__init__(register_to_divide_1, register_to_divide_2)

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
        raise NotImplementedError


class BranchNotEqualInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        raise NotImplementedError


class BranchGreaterThanInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        raise NotImplementedError


class BranchGreaterThanOrEqualInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        raise NotImplementedError


class BranchLessThaninstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        raise NotImplementedError


class BranchLessThanOrEqualInstruction(BranchInstruction):

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister, label: MipsBasicBlock.MipsBasicBlock):
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        raise NotImplementedError

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
        raise NotImplementedError


class JumpRegisterInstruction(UnconditionalJumpInstruction):

    def __init__(self, to_jump_to: MipsValue.MipsRegister):
        super().__init__(to_jump_to)

    def to_mips(self):
        raise NotImplementedError


class JumpAndLinkInstruction(UnconditionalJumpInstruction):

    def __init__(self, to_jump_to: MipsBasicBlock.MipsBasicBlock):
        super().__init__(to_jump_to)

    def to_mips(self):
        raise NotImplementedError

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
        raise NotImplementedError
