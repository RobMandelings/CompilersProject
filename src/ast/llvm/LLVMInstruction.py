import abc

import src.ast.ASTTokens as ASTTokens
import src.ast.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.ast.llvm.LLVMInterfaces as LLVMInterfaces
import src.ast.llvm.LLVMUtils as LLVMUtils
import src.ast.llvm.LLVMValue as LLVMValue


def isConstant(operand: str):
    if operand.startswith('%'):
        return False
    return True


class Instruction(LLVMInterfaces.IToLLVM, abc.ABC):

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

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister):
        super().__init__()
        assert resulting_reg is not None
        self.resulting_reg = resulting_reg

    def __str__(self):
        self.to_llvm()

    def is_terminator(self):
        return False

    def get_resulting_register(self):
        assert isinstance(self.resulting_reg, LLVMValue.LLVMRegister)
        return self.resulting_reg

    def to_llvm(self):
        return f"{self.resulting_reg.get_value()} = "


class AllocaInstruction(AssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister):
        super().__init__(resulting_reg)
        assert resulting_reg.get_data_type().is_pointer_type()

    def __str__(self):
        self.to_llvm()

    def to_llvm(self):
        return super().to_llvm() + f"alloca {LLVMUtils.get_llvm_type(self.get_resulting_register().get_data_type().get_normal_version())}, align 4"

    def is_terminator(self):
        return False


class StoreInstruction(Instruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, value_to_store: LLVMValue):
        super().__init__()
        assert resulting_reg.get_data_type().is_pointer_type(), "The resulting register must be of " \
                                                                "pointer type for a value to be stored in it!"
        self.resulting_reg = resulting_reg
        self.value_to_store = value_to_store

    def __str__(self):
        self.to_llvm()

    def to_llvm(self):
        datatype_str = LLVMUtils.get_llvm_type(self.value_to_store.get_data_type())
        return f"store {datatype_str} {self.value_to_store.to_llvm()}, {datatype_str}* {self.resulting_reg}, align 4"

    def is_terminator(self):
        return False


class LoadInstruction(AssignInstruction):
    """
    Loads the value of a pointer type into a register (for example, load an i32 from register %1 of type i32* in register %2)
    """

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, load_from_reg: LLVMValue.LLVMRegister):
        """
        LLVM Load instruction
        data_type_to_allocate: the data type that will be allocated
        load_from_reg: the register to load the value from
        """
        assert load_from_reg.get_data_type().is_pointer_type()

        super().__init__(resulting_reg)
        self.load_from_reg = load_from_reg
        self.resulting_reg.set_data_type(load_from_reg.get_data_type().get_normal_version())

    def __str__(self):
        self.to_llvm()

    def to_llvm(self):
        llvm_data_type_to_load = LLVMUtils.get_llvm_type(self.resulting_reg.get_data_type())
        return super().to_llvm() + f"load {llvm_data_type_to_load}, {llvm_data_type_to_load}* {self.load_from_reg}"


class ConditionalBranchInstruction(Instruction):
    """
    Conditional Branch instruction for LLVM
    """

    def __init__(self, condition_reg: LLVMValue.LLVMRegister, if_true: LLVMBasicBlock, if_false: LLVMBasicBlock):
        assert condition_reg.get_data_type() == ASTTokens.DataTypeToken.BOOL, "Condition register must be of i1 (bool) type"
        super().__init__()
        self.condition_reg = condition_reg
        self.if_true = if_true
        self.if_false = if_false

    def __str__(self):
        self.to_llvm()

    def to_llvm(self):
        return f"br i1 {self.condition_reg.to_llvm()}, label %{self.if_true.get_number()}, label %{self.if_false.get_number()}"

    def is_terminator(self):
        return True


class UnconditionalBranchInstruction(Instruction):

    def __init__(self, destination: LLVMBasicBlock):
        """
        dest label: the label to branch to (format: dest_label, just numerical)
        """
        super().__init__()
        self.destination = destination

    def __str__(self):
        self.to_llvm()

    def to_llvm(self):
        return f"br label %{self.destination.get_number()}"

    def is_terminator(self):
        return True


class UnaryAssignInstruction(AssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, operand: LLVMValue.LLVMRegister):
        """
        Constructs a unary assignment instruction (one register as operand -> one register as result)
        operand: the operand register
        data_type: the data type of the operand
        """
        super().__init__(resulting_reg)
        self.operand = operand

    def __str__(self):
        self.to_llvm()

    def get_operand(self):
        return self.operand

    def get_llvm_data_type(self):
        return LLVMUtils.get_llvm_type(self.operand.get_data_type())


class BinaryAssignInstruction(AssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, operation, operand1: LLVMValue,
                 operand2: LLVMValue):
        """
        Instruction that has a resulting register
        """
        super().__init__(resulting_reg)
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2

    def __str__(self):
        self.to_llvm()

    def get_llvm_data_types(self):
        """
        Returns the data types of the two operands (1 and 2) in llvm code (as a string)
        """
        return LLVMUtils.get_llvm_type(self.operand1.get_data_type()), LLVMUtils.get_llvm_type(
            self.operand2.get_data_type())

    @abc.abstractmethod
    def get_llvm_for_operation(self):
        raise NotImplementedError


class BinaryArithmeticInstruction(BinaryAssignInstruction):
    """
    Instructions which apply arithmetics on registers and puts the result in another register
    """

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, operation: ASTTokens.BinaryArithmeticExprToken,
                 operand1: LLVMValue,
                 operand2: LLVMValue):
        super().__init__(resulting_reg, operation, operand1, operand2)
        self.resulting_data_type = ASTTokens.DataTypeToken.get_resulting_data_type(operand1.get_data_type(),
                                                                                   operand2.get_data_type())
        self.operation_type = self.get_operation_type()

    def __str__(self):
        self.to_llvm()

    def get_operation_type(self):
        if self.operand1.get_data_type() == ASTTokens.DataTypeToken.INT and self.operand2.get_data_type() == ASTTokens.DataTypeToken.INT:
            return 'i32'
        elif self.operand1.get_data_type() == ASTTokens.DataTypeToken.FLOAT and self.operand2.get_data_type() == ASTTokens.DataTypeToken.FLOAT:
            return 'float'
        else:
            raise NotImplementedError

    def get_llvm_for_operation(self):
        """
        Returns the corresponding llvm code the operation token in this instance, in string format
        """
        operation_string = None
        if self.operation_type == 'i32':
            if self.operation == ASTTokens.BinaryArithmeticExprToken.ADD:
                operation_string = 'add nsw'
            elif self.operation == ASTTokens.BinaryArithmeticExprToken.SUB:
                operation_string = 'sub nsw'
            elif self.operation == ASTTokens.BinaryArithmeticExprToken.MUL:
                operation_string = 'mul nsw'
            elif self.operation == ASTTokens.BinaryArithmeticExprToken.DIV:
                operation_string = 'sdiv'
            else:
                raise NotImplementedError
        elif self.operation_type == 'float':
            if self.operation == ASTTokens.BinaryArithmeticExprToken.ADD:
                operation_string = 'fadd'
            elif self.operation == ASTTokens.BinaryArithmeticExprToken.SUB:
                operation_string = 'fsub'
            elif self.operation == ASTTokens.BinaryArithmeticExprToken.MUL:
                operation_string = 'fmul'
            elif self.operation == ASTTokens.BinaryArithmeticExprToken.DIV:
                operation_string = 'fdiv'
            else:
                raise NotImplementedError

        assert operation_string is not None
        return operation_string + f' {self.operation_type} '

    def to_llvm(self):
        operation_string = self.get_llvm_for_operation()
        return super().to_llvm() + operation_string + f'{self.operand1.to_llvm()}, {self.operand2.to_llvm()}'


class DataTypeConvertInstruction(UnaryAssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, reg_to_convert: LLVMValue.LLVMRegister):
        """
        Creates an instruction to convert a given register with data type 'data_type' to a resulting data type 'resulting_data_type'
        resulting_reg: the register where the converted value will be put in
        reg_to_convert: the register that holds the value in previous data type
        """
        super().__init__(resulting_reg, reg_to_convert)
        self.llvm_operation, self.llvm_to_data_type = self.get_llvm_for_operation()

    def __str__(self):
        self.to_llvm()

    def get_llvm_for_operation(self):
        """
        Returns the corresponding llvm code for the operation, given the two data types
        returns: <operation, to <llvm_data_type>>
        """
        assert not self.get_operand().get_data_type() == self.get_resulting_register().get_data_type(), "Converting to the same data type has no point"

        # TODO What to do with bool conversion and such? Is it a signed integer conversion or no?
        if (self.get_operand().get_data_type().is_integral_type() and
                self.get_resulting_register().get_data_type().is_floating_point_type()):
            return 'sitofp', f'to {LLVMUtils.get_llvm_type(self.get_resulting_register().get_data_type())}'
        elif (self.get_operand().get_data_type().is_floating_point_type() and
              self.get_resulting_register().get_data_type().is_integral_type()):
            return 'fptosi', f'to {LLVMUtils.get_llvm_type(self.get_resulting_register().get_data_type())}'
        else:
            raise NotImplementedError

    def to_llvm(self):
        return super().to_llvm() + f'{self.llvm_operation} {LLVMUtils.get_llvm_type(self.get_operand().get_data_type())}' \
                                   f' {self.get_operand().to_llvm()} {self.llvm_to_data_type}'


class CompareInstruction(BinaryAssignInstruction):
    """
    Creates 1 compare instruction for the two resulting registers. Does not do any type conversions first, so make
    sure you do that. The LLVMBuilder has such a method to create the full compare statement (with type conversions)
    # TODO comparing with constants such as 0 and stuff
    """

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, operation: ASTTokens.RelationalExprToken,
                 operand1: LLVMValue,
                 operand2: LLVMValue):
        super().__init__(resulting_reg, operation, operand1, operand2)
        assert operand1.get_data_type() == operand2.get_data_type(), \
            "Data types to compare must be equal. Perform an instruction to convert a" \
            "lower data type to a higher one (e.g. sitofp for i32 -> float)"

        self.operation = operation
        self.comparison_type = self.get_comparison_type()

    def __str__(self):
        self.to_llvm()

    def get_resulting_data_type(self):
        return ASTTokens.DataTypeToken.BOOL

    def get_comparison_type(self):
        """
        Checks the entered datatypes to determine which LLVMUtils.ComparisonDataType will be used and what the llvm code will be as comparison type (for example, i32)
        """

        # Its the same, whether you pick operand1 or operand2 (they have the same data type)
        data_type_to_compare = self.operand1.get_data_type()

        if data_type_to_compare == ASTTokens.DataTypeToken.DOUBLE or data_type_to_compare == ASTTokens.DataTypeToken.FLOAT:
            return LLVMUtils.ComparisonDataType.FLOAT
        elif data_type_to_compare == ASTTokens.DataTypeToken.INT:
            return LLVMUtils.ComparisonDataType.INT
        elif data_type_to_compare == ASTTokens.DataTypeToken.CHAR:
            print("WARN: data type to compare is char, returning comparison data type INT. Not tested yet")
            return LLVMUtils.ComparisonDataType.INT
        else:
            raise NotImplementedError

    def get_llvm_comparison_type(self):
        if self.comparison_type == LLVMUtils.ComparisonDataType.INT:
            return 'icmp'
        else:
            return 'fcmp'

    def get_llvm_for_operation(self):
        if self.operation == ASTTokens.RelationalExprToken.EQUALS:
            if self.comparison_type == LLVMUtils.ComparisonDataType.INT:
                return 'eq'
            else:
                return 'oeq'
        elif self.operation == ASTTokens.RelationalExprToken.NOT_EQUALS:
            if self.comparison_type == LLVMUtils.ComparisonDataType.INT:
                return 'ne'
            else:
                return 'one'
        elif self.operation == ASTTokens.RelationalExprToken.GREATER_THAN:
            if self.comparison_type == LLVMUtils.ComparisonDataType.INT:
                # TODO maybe later do with unsigned as well
                return 'sgt'
            else:
                return 'ogt'
        elif self.operation == ASTTokens.RelationalExprToken.LESS_THAN:
            if self.comparison_type == LLVMUtils.ComparisonDataType.INT:
                return 'slt'
            else:
                return 'olt'
        else:
            raise NotImplementedError

    def to_llvm(self):
        return super().to_llvm() + f'{self.get_llvm_comparison_type()} {self.get_llvm_for_operation()} ' \
                                   f'{LLVMUtils.get_llvm_type(self.operand1.get_data_type())} {self.operand1}, {self.operand2}'


# TODO must be implemented
class UnaryArithmeticInstruction(AssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister):
        super().__init__(resulting_reg)
        raise NotImplementedError

    def __str__(self):
        self.to_llvm()

    def to_llvm(self):
        raise NotImplementedError


class PrintfInstruction(AssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, register_to_print: LLVMValue.LLVMRegister,
                 string_to_print_name: str):
        """
        Creates a PrintfInstructions string
        result_register: the register where the result of the function goes in (the number of chars printed)
        type_to_print: the type to print (most likely a global constant you have defined)
        string_to_print_name: the global variable which contains the string to print (e.g. @.str.0)
        """
        super().__init__(resulting_reg)

        self.resulting_reg.set_data_type(ASTTokens.DataTypeToken.INT)

        self.register_to_print = register_to_print
        self.string_to_print_name = string_to_print_name

    def __str__(self):
        self.to_llvm()

    def is_terminator(self):
        return False

    def to_llvm(self):
        # TODO must be customized to be able to print completely custom names
        return super().to_llvm() + f"call i32 (i8*, ...) @printf(i8* getelementptr inbounds([3 x i8], [3 x i8]* {self.string_to_print_name}, i64 0, i64 0), i32 {self.register_to_print})"
