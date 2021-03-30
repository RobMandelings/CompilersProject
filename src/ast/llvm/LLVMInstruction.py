from abc import ABC, abstractmethod

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

    def __str__(self):
        return self.to_llvm()

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

    def get_resulting_data_type(self):
        raise NotImplementedError

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

    def is_terminator(self):
        return False


class LoadInstruction(AssignInstruction):
    """
    Loads the value of a pointer type into a register (for example, load an i32 from register %1 of type i32* in register %2)
    """

    def __init__(self, resulting_reg: str, data_type_to_allocate: DataTypeToken, load_from_reg: str):
        """
        LLVM Load instruction
        data_type_to_allocate: the data type that will be allocated
        load_from_reg: the register to load the value from
        """
        super().__init__(resulting_reg)
        self.data_type_to_allocate = data_type_to_allocate
        self.load_from_reg = load_from_reg

    def to_llvm(self):
        llvm_type = get_llvm_type(self.data_type_to_allocate)
        return super().to_llvm() + f"load {llvm_type}, {llvm_type}* {self.load_from_reg}"

    def get_resulting_data_type(self):
        return self.data_type_to_allocate


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
        dest label: the label to branch to (format: dest_label, just numerical)
        """
        super().__init__()
        self.dest_label = dest_label

    def to_llvm(self):
        return f"br label {self.dest_label}"

    def is_terminator(self):
        return True


class BinaryAssignInstruction(AssignInstruction):

    def __init__(self, resulting_reg: str, operation, data_type1: DataTypeToken,
                 operand1: str,
                 data_type2: DataTypeToken, operand2: str):
        """
        Instruction that has a resulting register
        """
        super().__init__(resulting_reg)
        self.operation = operation
        self.data_type1 = data_type1
        self.operand1 = operand1
        self.data_type2 = data_type2
        self.operand2 = operand2

    def get_data_types(self):
        """
        Returns the data types of the two operands as a DataTypeToken
        """
        assert isinstance(self.data_type1, DataTypeToken) and isinstance(self.data_type2, DataTypeToken)
        return self.data_type1, self.data_type2

    def get_llvm_data_types(self):
        """
        Returns the data types of the two operands (1 and 2) in llvm code (as a string)
        """
        return LLVMUtils.get_llvm_type(self.data_type1), LLVMUtils.get_llvm_type(self.data_type2)

    @abstractmethod
    def get_llvm_for_operation(self):
        raise NotImplementedError


class BinaryArithmeticInstruction(BinaryAssignInstruction):
    """
    Instructions which apply arithmetics on registers and puts the result in another register
    """

    def __init__(self, resulting_reg: str, operation: BinaryArithmeticExprToken, data_type1: DataTypeToken,
                 operand1: str,
                 data_type2: DataTypeToken, operand2: str):
        super().__init__(resulting_reg, operation, data_type1, operand1, data_type2, operand2)
        self.resulting_data_type = DataTypeToken.get_resulting_data_type(data_type1, data_type2)
        self.operation_type = self.get_operation_type()

    def get_resulting_data_type(self):
        assert isinstance(self.resulting_data_type, DataTypeToken)
        return self.resulting_data_type

    def get_operation_type(self):
        if self.data_type1 == DataTypeToken.INT and self.data_type2 == DataTypeToken.INT:
            return 'i32'
        elif self.data_type1 == DataTypeToken.FLOAT and self.data_type2 == DataTypeToken.FLOAT:
            return 'float'
        else:
            raise NotImplementedError

    def get_llvm_for_operation(self):
        """
        Returns the corresponding llvm code the operation token in this instance, in string format
        """
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
        operation_string = self.get_llvm_for_operation()
        return super().to_llvm() + operation_string + f'{self.operand1}, {self.operand2}'


class CompareInstruction(BinaryAssignInstruction):

    def __init__(self, resulting_reg: str, operation: RelationalExprToken, data_type1: DataTypeToken, operand1: str,
                 data_type2: DataTypeToken, operand2: str):
        super().__init__(resulting_reg, operation, data_type1, operand1, data_type2, operand2)
        self.operation = operation
        self.comparison_type, self.llvm_type = self.deduce_comparison_type()

    def get_resulting_data_type(self):
        return DataTypeToken.BOOL

    def deduce_comparison_type(self):
        """
        Checks the entered datatypes to determine which ComparisonDataType will be used and what the llvm code will be as comparison type (for example, i32)
        """
        if self.data_type1 == DataTypeToken.INT and self.data_type2 == DataTypeToken.INT:
            return ComparisonDataType.INT, LLVMUtils.get_llvm_type(DataTypeToken.INT)
        elif self.data_type1 == DataTypeToken.FLOAT or self.data_type2 == DataTypeToken.FLOAT:
            return ComparisonDataType.FLOAT, LLVMUtils.get_llvm_type(DataTypeToken.FLOAT)
        else:
            raise NotImplementedError

    def get_llvm_for_operation(self):
        if self.operation == RelationalExprToken.EQUALS:
            return 'oeq'
        elif self.operation == RelationalExprToken.NOT_EQUALS:
            return 'one'
        elif self.operation == RelationalExprToken.GREATER_THAN:
            return 'ogt'
        elif self.operation == RelationalExprToken.LESS_THAN:
            return 'olt'
        else:
            raise NotImplementedError

    def to_llvm(self):
        return super().to_llvm() + f'{self.comparison_type} {self.operation} {self.llvm_type} {self.data_type1} {self.operand1}, {self.data_type2} {self.operand2}'


# TODO must be implemented
class UnaryArithmeticInstruction(AssignInstruction):

    def __init__(self, resulting_reg: str):
        super().__init__(resulting_reg)
        raise NotImplementedError

    def to_llvm(self):
        raise NotImplementedError
        return super().to_llvm()
