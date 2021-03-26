from abc import ABC

from src.ast.ASTTokens import DataTypeToken, BinaryArithmeticExprToken, RelationalExprToken
from src.ast.llvm import LLVMUtils
from src.ast.llvm.LLVMUtils import ComparisonDataType
from src.ast.llvm.LLVMUtils import IToLLVM, get_llvm_type


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
        return super().to_llvm() + f"alloca {get_llvm_type(self.data_type_to_allocate)}, align 4"

    def is_terminator(self):
        return False


class StoreInstruction(Instruction):

    def __init__(self, resulting_reg: str, value, data_type_to_store: DataTypeToken):
        super().__init__()
        self.resulting_reg = resulting_reg
        self.value = value
        self.data_type_to_store = data_type_to_store

    def to_llvm(self):
        datatype_str = get_llvm_type(self.data_type_to_store)
        return f"store {datatype_str} {self.value}, {datatype_str}* {self.resulting_reg}, align 4"


class LoadInstruction(AssignInstruction):
    """
    Loads the value of a pointer type into a register (for example, load an i32 from register %1 of type i32* in register %2)
    """

    def __init__(self, resulting_reg: str, data_type_to_load: DataTypeToken, load_from_reg: str):
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
                 operand1: str,
                 data_type_reg2: DataTypeToken, operand2: str):
        super().__init__(resulting_reg)
        self.operation = operation
        self.data_type_reg1 = data_type_reg1
        self.operand1 = operand1
        self.data_type_reg2 = data_type_reg2
        self.operand2 = operand2
        self.operation_type = self.get_operation_type()

    def get_operation_type(self):
        if self.data_type_reg1 == 'i32' and self.data_type_reg2 == 'i32':
            return 'i32'
        elif self.data_type_reg1 == 'float' and self.data_type_reg2 == 'float':
            return 'float'
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


class CompareInstruction(AssignInstruction):

    def __init__(self, resulting_reg: str, operation: RelationalExprToken, data_type1: DataTypeToken, reg1: str,
                 data_type2: DataTypeToken, reg2: str):
        super().__init__(resulting_reg)
        self.operation = LLVMUtils.get_llvm_for_relational_operation(operation)
        self.data_type1 = LLVMUtils.get_llvm_type(data_type1)
        self.data_type2 = LLVMUtils.get_llvm_type(data_type2)
        self.reg1 = reg1
        self.reg2 = reg2
        self.comparison_type, self.llvm_type = self.deduce_comparison_type()

    def deduce_comparison_type(self):
        if self.data_type1 == DataTypeToken.INT and self.data_type2 == DataTypeToken.INT:
            return ComparisonDataType.INT, LLVMUtils.get_llvm_type(DataTypeToken.INT)
        elif self.data_type1 == DataTypeToken.FLOAT or self.data_type2 == DataTypeToken.FLOAT:
            return ComparisonDataType.FLOAT, LLVMUtils.get_llvm_type(DataTypeToken.FLOAT)
        else:
            raise NotImplementedError

    def to_llvm(self):
        return super().to_llvm() + f"{self.comparison_type} {self.operation} {self.llvm_type} {self.data_type1} {self.reg1}, {self.data_type2} {self.reg2}"
