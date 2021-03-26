from abc import abstractmethod

from src.ast.ASTTokens import BinaryArithmeticExprToken
from src.ast.llvm import LLVMUtils
from src.ast.llvm.LLVMRegister import *
from src.ast.llvm.LLVMUtils import *


def isConstant(operand: str):
    if operand.startswith('%'):
        return False
    return True


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

    def __init__(self, resulting_reg: LLVMRegister):
        super().__init__()
        assert resulting_reg is not None
        self.resulting_reg = resulting_reg

    def is_terminator(self):
        return False

    def get_resulting_data_type(self):
        return self.resulting_reg

    def to_llvm(self):
        return f"{self.resulting_reg} = "


class AllocaInstruction(AssignInstruction):

    def __init__(self, register_name: str, underlying_data_type: DataTypeToken):
        """
        data_type: the underlying datatype you wish to allocate for. This is NOT the pointer type but the underlying datatype (e.g. i32 instead of i32*)
        """
        resulting_reg = LLVMRegister(register_name, underlying_data_type)
        super().__init__(resulting_reg)

    def to_llvm(self):
        return super().to_llvm() + f"alloca {get_llvm_type(self.resulting_reg.get_data_type().__name)}, align 4"

    def is_terminator(self):
        return False


class StoreInstruction(Instruction):

    def __init__(self, register_name: str, value, value_data_type: DataTypeToken):
        """
        register: the register you want to store the value in
        value: the actual value to store
        """
        super().__init__()
        self.register_name = register_name
        self.value = value
        self.value_data_type = value_data_type

    def to_llvm(self):
        return f"store {self.value_data_type.name} {self.value}, {self.value_data_type.name}* {self.register_name}, align 4"

    def is_terminator(self):
        return False


class LoadInstruction(AssignInstruction):
    """
    Loads the value of a pointer type into a register (for example, load an i32 from register %1 of type i32* in register %2)
    """

    def __init__(self, resulting_reg: LLVMRegister, data_type_to_load: DataTypeToken, load_from_reg: str):
        super().__init__(resulting_reg)
        self.data_type_to_allocate = data_type_to_load
        self.load_from_reg = load_from_reg

    def to_llvm(self):
        llvm_type = get_llvm_type(self.data_type_to_allocate)
        return super().to_llvm() + f"load {llvm_type}, {llvm_type}* {self.load_from_reg}"


class ConditionalBranchInstruction(Instruction):
    """
    Conditional Branch instruction for LLVM
    """

    def __init__(self, condition_reg_name: str, label_iftrue: str, label_iffalse):
        super().__init__()
        self.condition_reg_name = condition_reg_name
        self.label_iftrue = label_iftrue
        self.label_iffalse = label_iffalse

    def to_llvm(self):
        return f"br i1 {self.condition_reg_name}, label {self.label_iftrue}, label {self.label_iffalse}"

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


class BinaryAssignInstruction(AssignInstruction):

    def __init__(self, resulting_reg_name):
        super().__init__(LLVMRegister(resulting_reg_name, self.get_resulting_data_type()))

    @abstractmethod
    def get_resulting_data_type(self):
        pass


class BinaryArithmeticInstruction(BinaryAssignInstruction):
    """
    Instructions which apply arithmetics on registers and puts the result in another register
    """

    def __init__(self, result_reg_name: str, operation: BinaryArithmeticExprToken, operand1: LLVMRegister,
                 operand2: LLVMRegister):

        super().__init__(result_reg_name)
        self.operation_type = self.get_resulting_data_type()
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2

    def get_resulting_data_type(self):
        if self.operand1.get_data_type() == DataTypeToken.INT and self.operand2.get_data_type() == DataTypeToken.INT:
            return get_llvm_type(self.operand1.data_type)
        elif self.operand1.get_data_type() == DataTypeToken.FLOAT and self.operand2.get_data_type() == DataTypeToken.FLOAT:
            return get_llvm_type(self.operand1.data_type)
        else:
            raise NotImplementedError

    def get_operation(self):
        operation_string = None
        if self.operation_type == 'i32':
            if self.operation == BinaryArithmeticExprToken.ADD:
                operation_string = 'add nsw'
            elif self.operation == BinaryArithmeticExprToken.SUB:
                operation_string = 'sub nsw'
            elif self.operation == BinaryArithmeticExprToken.MUL:
                operation_string = 'mul nsw'
            elif self.operation == BinaryArithmeticExprToken.DIV:
                operation_string = 'sdiv'
            else:
                raise NotImplementedError
        elif self.operation_type == 'float':
            if self.operation == BinaryArithmeticExprToken.ADD:
                operation_string = 'fadd'
            elif self.operation == BinaryArithmeticExprToken.SUB:
                operation_string = 'fsub'
            elif self.operation == BinaryArithmeticExprToken.MUL:
                operation_string = 'fmul'
            elif self.operation == BinaryArithmeticExprToken.DIV:
                operation_string = 'fdiv'
            else:
                raise NotImplementedError

        assert operation_string is not None
        return operation_string + f'{self.operation_type}'

    def to_llvm(self):
        operation_string = self.get_operation()
        return super().to_llvm() + operation_string + f'{self.operand1}, {self.operand2}'


class CompareInstruction(BinaryAssignInstruction):

    def __init__(self, resulting_reg_name: str, operation: RelationalExprToken, operand1: LLVMRegister,
                 operand2: LLVMRegister):
        super().__init__(resulting_reg_name)
        self.operation = LLVMUtils.get_llvm_for_relational_operation(operation)
        self.operand1 = operand1
        self.operand2 = operand2
        self.comparison_type, self.llvm_type = self.deduce_comparison_type()

    def get_resulting_data_type(self):
        return get_llvm_type(DataTypeToken.BOOL)

    def deduce_comparison_type(self):
        data_type1 = self.operand1.get_data_type()
        data_type2 = self.operand2.get_data_type()
        if data_type1 == DataTypeToken.INT and data_type2 == DataTypeToken.INT:
            return ComparisonDataType.INT, LLVMUtils.get_llvm_type(DataTypeToken.INT)
        elif data_type1 == DataTypeToken.FLOAT or data_type2 == DataTypeToken.FLOAT:
            return ComparisonDataType.FLOAT, LLVMUtils.get_llvm_type(DataTypeToken.FLOAT)
        else:
            raise NotImplementedError

    def to_llvm(self):
        return super().to_llvm() + f"{self.comparison_type} {self.operation} {self.llvm_type} {self.operand1.get_data_type()} {self.operand1.get_name()}, {self.operand2.get_data_type()} {self.operand2.get_name()}"
