import src.Instruction as Instruction
import src.mips.MipsValue as MipsValue
import src.mips.MipsBasicBlock as MipsBasicBlock
import src.ast.ASTTokens as ASTTokens
import src.mips.FPOffset as FPOffset
import src.BasicBlock as BasicBlock
import abc

"""
Contains all mips instructions that the compiler can generate
"""


# One line per instruction

class MipsInstruction(Instruction.Instruction, abc.ABC):
    """
    Abstract class for all the mips instructions
    """

    def __init__(self):
        super().__init__()

    def is_terminator(self):
        return False

    def to_mips(self):
        """
        Abstract function declaration of the to_mips
        Has to be implemented in lowest child of inheritance
        :return: has to return a string which contains the syntactical mips form of the instruction with given parameters
        """
        raise NotImplementedError


# ######################### #
# DataTransfer Instructions #
# ######################### #


class LoadWordInstruction(MipsInstruction):
    """
    This class corresponds to the load word mips instruction
    """

    def __init__(self, register_to_load_into: MipsValue.MipsRegister, register_address: MipsValue.MipsRegister,
                 offset: FPOffset.FPOffset or int):
        super().__init__()
        self.register_to_store = register_to_load_into
        self.register_address = register_address
        self.offset = offset

    def to_mips(self):
        return f"lw {self.register_to_store}, {self.offset.get_value() if isinstance(self.offset, FPOffset.FPOffset) else self.offset}({self.register_address})"


class LoadWordCoProcInstruction(MipsInstruction):

    def __init__(self, register_to_load_into: MipsValue.MipsRegister, floating_point_data: str):
        """
        register_to_load_into: one of the floating point registers
        floating_point_data: identifier which links to one of the data placed in the .data segment
        """
        super().__init__()
        assert MipsValue.MipsRegister.is_floating_point_register(
            register_to_load_into), "Should only be used with floating point numbers"
        self.register_to_load_into = register_to_load_into
        self.floating_point_data = floating_point_data

    def to_mips(self):
        return f"lwc1 {self.register_to_load_into} {self.floating_point_data}"


class StoreWordInstruction(MipsInstruction):
    """
    This class corresponds to the store word mips instruction
    """

    def __init__(self, register_to_store: MipsValue.MipsRegister, register_address: MipsValue.MipsRegister,
                 offset: FPOffset.FPOffset or int):
        super().__init__()
        self.register_to_store = register_to_store
        self.register_address = register_address
        self.offset = offset
        assert offset is not None

    def to_mips(self):
        if isinstance(self.offset, FPOffset.FPOffset):
            offset = self.offset.get_value()
        else:
            offset = self.offset

        return f"sw {self.register_to_store}, {offset}({self.register_address})"


class LoadUpperImmediateInstruction(MipsInstruction):
    """
    This class corresponds to the load upper immediate mips instruction
    """

    def __init__(self, register_to_store: MipsValue.MipsRegister, immediate: MipsValue.MipsLiteral):
        super().__init__()
        self.register_to_store = register_to_store
        self.immediate = immediate

    def to_mips(self):
        return f"lui {self.register_to_store},{self.immediate}"


class LoadAddressInstruction(MipsInstruction):
    """
    This class corresponds to the load address mips instruction
    """

    def __init__(self, register_to_load: MipsValue.MipsRegister, identifier):
        super().__init__()
        self.register_to_load = register_to_load
        self.identifier = identifier

    def to_mips(self):
        return f"la {self.register_to_load},{self.identifier}"


class LoadAddressWithOffsetInstruction(MipsInstruction):

    def __init__(self, register_to_load: MipsValue.MipsRegister, register_address: MipsValue.MipsRegister,
                 fp_offset: FPOffset.FPOffset):
        super().__init__()
        self.register_to_load = register_to_load
        self.register_address = register_address
        self.fp_offset = fp_offset

    def to_mips(self):
        return f"la {self.register_to_load},{self.fp_offset.get_value()}({self.register_address})"


class LoadImmediateInstruction(MipsInstruction):
    """
    This class corresponds to the load immediate mips instruction
    """

    def __init__(self, register_to_load: MipsValue.MipsRegister, immediate: MipsValue.MipsLiteral):
        super().__init__()
        self.register_to_load = register_to_load
        self.immediate = immediate

    def to_mips(self):
        return f"li {self.register_to_load}, {self.immediate} "


class MoveFromHiInstruction(MipsInstruction):
    """
    This class corresponds to the move from hi mips instruction
    """

    def __init__(self, register_to_move_in: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in

    def to_mips(self):
        return f"mfhi {self.register_to_move_in}"


class MoveFromLoInstruction(MipsInstruction):
    """
    This class corresponds to the move from lo mips instruction
    """

    def __init__(self, register_to_move_in: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in

    def to_mips(self):
        return f"mflo {self.register_to_move_in}"


class MoveInstruction(MipsInstruction):
    """
    This class corresponds to the move mips instruction
    """

    def __init__(self, register_to_move_in: MipsValue.MipsRegister, register_to_move_from: MipsValue.MipsRegister):
        super().__init__()
        self.register_to_move_in = register_to_move_in
        self.register_to_move_from = register_to_move_from
        self.move_operation = self.get_move_operation()

    def get_move_operation(self):
        assert MipsValue.MipsRegister.is_floating_point_register(
            self.register_to_move_in) == MipsValue.MipsRegister.is_floating_point_register(
            self.register_to_move_from), "Registers must be of same type to move"

        if MipsValue.MipsRegister.is_floating_point_register(self.register_to_move_in):
            return "mov.s"
        else:
            return "move"

    def to_mips(self):
        return f"{self.move_operation} {self.register_to_move_in}, {self.register_to_move_from}"


# ####################### #
# Arithmetic Instructions #
# ####################### #

class ArithmeticInstruction(MipsInstruction):
    """
    This class is an abstract class for all arithmetic mips instructions
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsValue,
                 resulting_register: MipsValue.MipsRegister = None):
        super().__init__()
        self.resulting_register = resulting_register
        self.first_register = first_register
        self.second_register = second_register


class ArithmeticBinaryInstruction(ArithmeticInstruction):
    """
    This class handles the different arithmetic instructions by using the given token,
    based on the tokens value it will decide which arithmetic instruction is needed
    Token values in this case can be : [ADD, SUB, MUL, DIV]
    """

    def __init__(self, first_operand: MipsValue.MipsRegister, second_operand: MipsValue.MipsValue,
                 token: ASTTokens.BinaryArithmeticExprToken, resulting_register: MipsValue.MipsRegister = None):
        assert isinstance(first_operand, MipsValue.MipsRegister)
        assert isinstance(second_operand, MipsValue.MipsValue)
        assert isinstance(resulting_register, MipsValue.MipsRegister)
        super().__init__(first_operand, second_operand, resulting_register)
        self.token = token
        if MipsValue.MipsRegister.is_floating_point_register(
                first_operand):
            if not isinstance(second_operand, MipsValue.MipsRegister):
                raise AssertionError(
                    'First operand is a floating point register but second operand is a literal. With floating points, all must be registers')
            else:
                assert MipsValue.MipsRegister.is_floating_point_register(
                    first_operand) and MipsValue.MipsRegister.is_floating_point_register(
                    second_operand), "Floating point types must match don't match"
        else:
            if isinstance(second_operand, MipsValue.MipsRegister):
                assert not MipsValue.MipsRegister.is_floating_point_register(
                    second_operand), "Floating point types must match don't match"

    def to_mips(self):

        operation_string = ""
        if self.token == ASTTokens.BinaryArithmeticExprToken.ADD:
            if isinstance(self.second_register, MipsValue.MipsRegister):
                operation_string = "add"
            elif isinstance(self.second_register, MipsValue.MipsLiteral):
                operation_string = "addi"
            else:
                raise NotImplementedError

        elif self.token == ASTTokens.BinaryArithmeticExprToken.SUB:
            operation_string = "sub"
        elif self.token == ASTTokens.BinaryArithmeticExprToken.MUL:
            operation_string = "mul"
        elif self.token == ASTTokens.BinaryArithmeticExprToken.DIV:
            operation_string = "div"
            return operation_string + f" {self.resulting_register.get_name()}, {self.first_register.get_name()}"
        else:
            raise NotImplementedError

        # We have asserted before that if the first register is floating point, the second must be as well
        # So its enough to check the first register. We add '.s' to the instruction
        if MipsValue.MipsRegister.is_floating_point_register(self.first_register):
            operation_string += '.s'

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
    """
    This class is an abstract class for all conditional branch mips instructions
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister
                 , label):
        assert isinstance(label, BasicBlock.BasicBlock)
        super().__init__()
        self.first_register = first_register
        self.second_register = second_register
        self.label = label

    def is_terminator(self):
        return True


class BranchEqualInstruction(BranchInstruction):
    """
    This class corresponds to the branch equal mips instruction
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister,
                 label):
        assert isinstance(label, BasicBlock.BasicBlock)
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        # References should be updated now
        assert isinstance(self.label, MipsBasicBlock.MipsBasicBlock)
        return f"beq {self.first_register.get_name()}, {self.second_register.get_name()}, {self.label.name}"


class BranchNotEqualInstruction(BranchInstruction):
    """
    This class corresponds to the branch not equal mips instruction
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister,
                 label):
        assert isinstance(label, BasicBlock.BasicBlock)
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        # References should be updated now
        assert isinstance(self.label, MipsBasicBlock.MipsBasicBlock)
        return f"bne {self.first_register.get_name()}, {self.second_register.get_name()}, {self.label.name}"


class BranchGreaterThanInstruction(BranchInstruction):
    """
    This class corresponds to the branch greater than mips instruction
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister,
                 label):
        assert isinstance(label, BasicBlock.BasicBlock)
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        # References should be updated now
        assert isinstance(self.label, MipsBasicBlock.MipsBasicBlock)
        return f"bgt {self.first_register.get_name()}, {self.second_register.get_name()}, {self.label.name}"


class BranchGreaterThanOrEqualInstruction(BranchInstruction):
    """
    This class corresponds to the branch greater than or equal mips instruction
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister,
                 label):
        assert isinstance(label, BasicBlock.BasicBlock)
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        # References should be updated now
        assert isinstance(self.label, MipsBasicBlock.MipsBasicBlock)
        return f"bge {self.first_register.get_name()}, {self.second_register.get_name()}, {self.label.name}"


class BranchLessThaninstruction(BranchInstruction):
    """
    This class corresponds to the branch less than mips instruction
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister,
                 label):
        assert isinstance(label, BasicBlock.BasicBlock)
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        # References should be updated now
        assert isinstance(self.label, MipsBasicBlock.MipsBasicBlock)
        return f"blt {self.first_register.get_name}, {self.second_register.get_name()}, {self.label.name}"


class BranchLessThanOrEqualInstruction(BranchInstruction):
    """
    This class corresponds to the branch less than or equal mips instruction
    """

    def __init__(self, first_register: MipsValue.MipsRegister, second_register: MipsValue.MipsRegister,
                 label):
        assert isinstance(label, BasicBlock.BasicBlock)
        super().__init__(first_register, second_register, label)

    def to_mips(self):
        # References should be updated now
        assert isinstance(self.label, MipsBasicBlock.MipsBasicBlock)
        return f"ble {self.first_register.get_name}, {self.second_register.get_content}, {self.label.name}"


# ############################### #
# Unconditional Jump Instructions #
# ############################### #


class UnconditionalJumpInstruction(MipsInstruction):
    """
    This class is an abstract class for all unconditional jump mips instructions
    """

    def __init__(self, to_jump_to):
        super().__init__()
        self.to_jump_to = to_jump_to

    def is_terminator(self):
        return True


class JumpInstruction(UnconditionalJumpInstruction):
    """
    This class corresponds to the jump mips instruction
    """

    def __init__(self, to_jump_to):
        super().__init__(to_jump_to)

    def to_mips(self):
        return f"j {self.to_jump_to.name}"

    def is_terminator(self):
        return True


class JumpRegisterInstruction(UnconditionalJumpInstruction):
    """
    This class corresponds to the jump register mips instruction
    """

    def __init__(self, to_jump_to: MipsValue.MipsRegister):
        super().__init__(to_jump_to)

    def to_mips(self):
        return f"jr {self.to_jump_to.get_name()}"

    def is_terminator(self):
        return True


class JumpAndLinkInstruction(UnconditionalJumpInstruction):
    """
    This class corresponds to the jump and link mips instruction
    """

    def __init__(self, to_jump_to):
        super().__init__(to_jump_to)

    def to_mips(self):
        return f"jal {self.to_jump_to.name}"

    def is_terminator(self):
        return False


# ####################### #
# Comparison Instructions #
# ####################### #

class CompareInstruction(MipsInstruction):
    """
    This class corresponds to the llvm comparison instructions
    This is a general class that will generate the right comparison instruction according to the given token
    """

    def __init__(self, resulting_register: MipsValue.MipsRegister, first_operand: MipsValue.MipsRegister,
                 second_operand: MipsValue.MipsValue, token: ASTTokens.RelationalExprToken):
        super().__init__()
        self.resulting_register = resulting_register
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.token = token

    def to_mips(self):
        operation_string = ""
        if self.token == ASTTokens.RelationalExprToken.EQUALS:
            operation_string = "seq"
        elif self.token == ASTTokens.RelationalExprToken.NOT_EQUALS:
            operation_string = "sne"
        elif self.token == ASTTokens.RelationalExprToken.LESS_THAN:
            if isinstance(self.second_operand, MipsValue.MipsRegister):
                operation_string = "slt"
            elif isinstance(self.second_operand, MipsValue.MipsLiteral):
                operation_string = "slti"
        elif self.token == ASTTokens.RelationalExprToken.GREATER_THAN:
            operation_string = "sgt"
        elif self.token == ASTTokens.RelationalExprToken.LESS_THAN_OR_EQUALS:
            operation_string = "sle"
        elif self.token == ASTTokens.RelationalExprToken.GREATER_THAN_OR_EQUALS:
            operation_string = "sge"
        else:
            raise NotImplementedError

        return f"{operation_string} {self.resulting_register.get_name()},{self.first_operand.get_name()},{self.second_operand.get_content()}"


class SyscallInstruction(MipsInstruction):

    def __init__(self):
        super().__init__()

    def to_mips(self):
        return f"syscall"
