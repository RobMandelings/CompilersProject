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


class UnaryAssignInstruction(AssignInstruction):

    def __init__(self, resulting_reg: str, operand: str, data_type: DataTypeToken):
        """
        Constructs a unary assignment instruction (one register as operand -> one register as result)
        operand: the operand register
        data_type: the data type of the operand
        """
        super().__init__(resulting_reg)
        self.operand_reg = operand
        self.data_type = data_type

    def get_data_type(self):
        return self.data_type

    def get_llvm_data_type(self):
        return LLVMUtils.get_llvm_type(self.data_type)

    @abstractmethod
    def get_resulting_data_type(self):
        raise NotImplementedError


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
        return operation_string + f' {self.operation_type} '

    def to_llvm(self):
        operation_string = self.get_llvm_for_operation()
        return super().to_llvm() + operation_string + f'{self.operand1}, {self.operand2}'


class DataTypeConvertInstruction(UnaryAssignInstruction):

    def __init__(self, resulting_reg: str, operand: str, data_type: DataTypeToken, resulting_data_type: DataTypeToken):
        """
        Creates an instruction to convert a given register with data type 'data_type' to a resulting data type 'resulting_data_type'
        llvm operation: specifies the conversions, such as fptosi
        llvm_to_data_type: to which data type you want to convert (llvm code such as 'to double')
        """
        super().__init__(resulting_reg, operand, data_type)

        self.resulting_data_type = resulting_data_type
        self.llvm_operation, self.llvm_to_data_type = self.get_llvm_for_operation()

    def get_llvm_for_operation(self):
        """
        Returns the corresponding llvm code for the operation, given the two data types
        returns: <operation, to <llvm_data_type>>
        """
        assert not self.data_type == self.resulting_data_type, "Converting to the same data type has no point"
        if not DataTypeToken.is_richer_than(self.resulting_data_type, self.data_type):
            raise NotImplementedError

        # TODO What to do with bool conversion and such? Is it a signed integer conversion or no?
        if self.data_type.is_integral_type() and self.resulting_data_type.is_floating_point_type():
            return 'sitofp', f'to {LLVMUtils.get_llvm_type(self.resulting_data_type)}'
        elif self.data_type.is_floating_point_type() and self.resulting_data_type.is_integral_type():
            return 'fptosi', f'to {LLVMUtils.get_llvm_type(self.resulting_data_type)}'
        else:
            raise NotImplementedError

    def get_resulting_data_type(self):
        return self.resulting_data_type

    def to_llvm(self):
        return super().to_llvm() + f'{self.llvm_operation} {LLVMUtils.get_llvm_type(self.get_data_type())} {self.operand_reg} {self.llvm_to_data_type}'


class CompareInstruction(BinaryAssignInstruction):
    """
    Creates 1 compare instruction for the two resulting registers. Does not do any type conversions first, so make
    sure you do that. The LLVMBuilder has such a method to create the full compare statement (with type conversions)
    # TODO comparing with constants such as 0 and stuff
    """

    def __init__(self, resulting_reg: str, operation: RelationalExprToken, data_type1: DataTypeToken, operand1: str,
                 data_type2: DataTypeToken, operand2: str):
        super().__init__(resulting_reg, operation, data_type1, operand1, data_type2, operand2)
        assert data_type1 == data_type2, "Data types to compare must be equal. Perform an instruction to convert a" \
                                         "lower data type to a higher one (e.g. sitofp for i32 -> float)"
        self.operation = operation
        self.data_type_to_compare = self.data_type1
        self.comparison_type = self.get_comparison_type()

    def get_resulting_data_type(self):
        return DataTypeToken.BOOL

    def get_comparison_type(self):
        """
        Checks the entered datatypes to determine which ComparisonDataType will be used and what the llvm code will be as comparison type (for example, i32)
        """

        if self.data_type_to_compare == DataTypeToken.DOUBLE or self.data_type_to_compare == DataTypeToken.FLOAT:
            return ComparisonDataType.FLOAT
        elif self.data_type_to_compare == DataTypeToken.INT:
            return ComparisonDataType.INT
        elif self.data_type_to_compare == DataTypeToken.CHAR:
            print("WARN: data type to compare is char, returning comparison data type INT. Not tested yet")
            return ComparisonDataType.INT
        else:
            raise NotImplementedError

    def get_llvm_comparison_type(self):
        if self.comparison_type == ComparisonDataType.INT:
            return 'icmp'
        else:
            return 'fcmp'

    def get_llvm_for_operation(self):
        if self.operation == RelationalExprToken.EQUALS:
            if self.comparison_type == ComparisonDataType.INT:
                return 'eq'
            else:
                return 'oeq'
        elif self.operation == RelationalExprToken.NOT_EQUALS:
            if self.comparison_type == ComparisonDataType.INT:
                return 'ne'
            else:
                return 'one'
        elif self.operation == RelationalExprToken.GREATER_THAN:
            if self.comparison_type == ComparisonDataType.INT:
                return 'gt'
            else:
                return 'ogt'
        elif self.operation == RelationalExprToken.LESS_THAN:
            if self.comparison_type == ComparisonDataType.INT:
                return 'lt'
            else:
                return 'olt'
        else:
            raise NotImplementedError

    def to_llvm(self):
        return super().to_llvm() + f'{self.get_llvm_comparison_type()} {self.get_llvm_for_operation()} ' \
                                   f'{get_llvm_type(self.data_type_to_compare)} {self.operand1}, {self.operand2}'


# TODO must be implemented
class UnaryArithmeticInstruction(AssignInstruction):

    def __init__(self, resulting_reg: str):
        super().__init__(resulting_reg)
        raise NotImplementedError

    def to_llvm(self):
        raise NotImplementedError
        return super().to_llvm()


class PrintfInstruction(Instruction):

    def __init__(self, register_to_print: str, global_variable_data_type: str):
        """
        Creates a PrintfInstructions string
        type_to_print: the type to print (most likely a global constant you have defined)
        global_variable_data_type: the global variable which contains the string of the datatype to print (e.g. @.str.1 -> '%i\00')
        """
        super().__init__()
        self.register_to_print = register_to_print
        self.type_to_print = global_variable_data_type

    def get_instruction_type(self):
        return self.type_to_print

    def is_terminator(self):
        return False

    def to_llvm(self):
        # TODO remove call from @.i ot
        return f"call i32 (i8*, ...) @printf(i8* getelementptr inbounds([3 x i8], [3 x i8]* {self.type_to_print}, i64 0, i64 0), i32 {self.register_to_print})"
