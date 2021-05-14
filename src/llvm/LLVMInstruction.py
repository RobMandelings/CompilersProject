import abc

import src.DataType as DataType
import src.ast.ASTTokens as ASTTokens
import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMInterfaces as LLVMInterfaces
import src.llvm.LLVMUtils as LLVMUtils
import src.llvm.LLVMValue as LLVMValue
import src.interfaces.IVisitable as IVisitable
import src.Instruction as Instruction
from src.interfaces import ILLVMVisitor as ILLVMVisitor


def is_constant(operand: str):
    if operand.startswith('%'):
        return False
    return True


class LLVMInstruction(LLVMInterfaces.IToLLVM, IVisitable.ILLVMVisitable, Instruction.Instruction):

    def __init__(self):
        super().__init__()

    def to_llvm(self):
        raise NotImplementedError

    def update_numbering(self, counter):
        """
        Updates the numbering. Do nothing by default
        """
        pass


class LLVMReturnInstruction(LLVMInstruction):

    def __init__(self, return_value: LLVMValue.LLVMValue):
        super().__init__()
        self.return_value = return_value

    def get_return_value(self):
        assert isinstance(self.return_value, LLVMValue.LLVMValue)
        return self.return_value

    def is_terminator(self):
        return True

    def to_llvm(self):
        return f'ret {self.get_return_value().get_data_type().get_llvm_name()} {self.get_return_value().to_llvm()}'

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_return_instruction(self)


class LLVMAssignInstruction(LLVMInstruction):
    """
    Instruction which has a resulting register
    """

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister):
        super().__init__()
        assert resulting_reg is not None
        self.resulting_reg = resulting_reg

    def is_terminator(self):
        return False

    def get_resulting_register(self):
        assert isinstance(self.resulting_reg, LLVMValue.LLVMRegister)
        return self.resulting_reg

    def update_numbering(self, counter):
        self.resulting_reg.value = counter.get_value()
        counter.increase()

    def to_llvm(self):
        return f"{self.resulting_reg.to_llvm()} = "


class LLVMRawAssignInstruction(LLVMAssignInstruction):

    def __init__(self, resulting_reg, instruction_parts: list, terminator: bool = False):
        super().__init__(resulting_reg)
        self.instruction_parts = instruction_parts
        self.terminator = terminator

    def is_terminator(self):
        return self.terminator

    def to_llvm(self):

        llvm_code = super().to_llvm()
        for instruction_part in self.instruction_parts:
            if isinstance(instruction_part, str):
                llvm_code += instruction_part
            elif isinstance(instruction_part, LLVMInterfaces.IToLLVM):
                llvm_code += instruction_part.to_llvm()

        return llvm_code

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_raw_assign_instruction(self)


class LLVMAllocaInstruction(LLVMAssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister):
        super().__init__(resulting_reg)
        assert resulting_reg.get_data_type().is_pointer()

    def to_llvm(self):
        data_type = self.resulting_reg.get_data_type()
        # You need to allocate with a data type that has pointer level of resulting reg - 1,
        # the resulting reg will be a pointer to that data type
        llvm_for_data_type = DataType.get_llvm_for_data_type(data_type.get_token(), data_type.get_pointer_level() - 1)
        return super().to_llvm() + f"alloca {llvm_for_data_type}, align 4"

    def is_terminator(self):
        return False

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_alloca_instruction(self)


class LLVMAllocaArrayInstruction(LLVMAllocaInstruction):
    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, size: LLVMValue.LLVMLiteral):
        super().__init__(resulting_reg)
        self.size = size
        assert resulting_reg.get_data_type().is_pointer()

    def to_llvm(self):
        data_type = self.resulting_reg.get_data_type()
        # You need to allocate with a data type that has pointer level of resulting reg - 1,
        # the resulting reg will be a pointer to that data type
        llvm_for_data_type = DataType.get_llvm_for_data_type(data_type.get_token(), data_type.get_pointer_level() - 1)
        align_const = 0
        array_size = self.size.get_value()
        if array_size < 4:
            align_const = 4
        elif array_size >= 4:
            align_const = 16
        return LLVMAssignInstruction.to_llvm(
            self) + f"alloca [{self.size.get_value()} x {llvm_for_data_type}], align {align_const}"

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_alloca_array_instruction(self)


class LLVMStoreInstruction(LLVMInstruction):

    def __init__(self, put_in_register: LLVMValue.LLVMRegister, value_to_store: LLVMValue):
        """
        put_in_register: the register to put the value-to-store in
        value_to_store: either an LLVMLiteral or LLVMRegister which value will be stored in the LLVMRegister
        """
        super().__init__()
        assert (
                put_in_register.get_data_type().get_pointer_level() ==
                value_to_store.get_data_type().get_pointer_level() + 1), \
            "The value to store must be one pointer level lower than the" \
            "register to store it in"

        self.resulting_reg = put_in_register
        self.value_to_store = value_to_store

    def to_llvm(self):
        datatype_str = self.value_to_store.get_data_type().get_llvm_name()
        return f"store {datatype_str} {self.value_to_store.to_llvm()}, {datatype_str}* {self.resulting_reg}, align 4"

    def is_terminator(self):
        return False

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_store_instruction(self)


class LLVMLoadInstruction(LLVMAssignInstruction):
    """
    Loads the value of a pointer type into a register (for example, load an i32 from register %1 of type i32* in register %2)
    """

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, load_from_reg: LLVMValue.LLVMRegister):
        """
        LLVM Load instruction
        data_type_to_allocate: the data type that will be allocated
        load_from_reg: the register to load the value from
        """
        assert load_from_reg.get_data_type().is_pointer()

        super().__init__(resulting_reg)
        self.load_from_reg = load_from_reg

    def to_llvm(self):
        llvm_data_type_to_load = self.resulting_reg.get_data_type().get_llvm_name()
        return super().to_llvm() + f"load {llvm_data_type_to_load}, {llvm_data_type_to_load}* {self.load_from_reg}, align 4"

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_load_instruction(self)


class LLVMConditionalBranchInstruction(LLVMInstruction):
    """
    Conditional Branch instruction for LLVM
    """

    def __init__(self, condition_reg: LLVMValue.LLVMRegister, if_true: LLVMBasicBlock, if_false: LLVMBasicBlock):
        assert condition_reg.get_data_type().get_token() == DataType.DataTypeToken.BOOL, "Condition register must be of i1 (bool) type"
        assert not condition_reg.get_data_type().is_pointer(), "Condition register may not be a pointer"
        super().__init__()
        self.condition_reg = condition_reg
        self.if_true = if_true
        self.if_false = if_false

    def to_llvm(self):
        return f"br i1 {self.condition_reg.to_llvm()}, label %{self.if_true.get_number()}, label %{self.if_false.get_number()}"

    def is_terminator(self):
        return True

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_conditional_branch_instruction(self)


class LLVMUnconditionalBranchInstruction(LLVMInstruction):

    def __init__(self, destination: LLVMBasicBlock):
        """
        dest label: the label to branch to (format: dest_label, just numerical)
        """
        super().__init__()
        self.destination = destination

    def to_llvm(self):
        return f"br label %{self.destination.get_number()}"

    def is_terminator(self):
        return True

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_unconditional_branch_instruction(self)


class LLVMUnaryAssignInstruction(LLVMAssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, operand: LLVMValue.LLVMRegister):
        """
        Constructs a unary assignment instruction (one register as operand -> one register as result)
        operand: the operand register
        data_type: the data type of the operand
        """
        super().__init__(resulting_reg)
        self.operand = operand

    def get_operand(self):
        return self.operand

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_unary_assign_instruction(self)


class LLVMBinaryAssignInstruction(LLVMAssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister, operation, operand1: LLVMValue,
                 operand2: LLVMValue):
        """
        Instruction that has a resulting register
        """
        super().__init__(resulting_reg)
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2

    def get_llvm_data_types(self):
        """
        Returns the data types of the two operands (1 and 2) in llvm code (as a string)
        """
        return self.operand1.get_data_type().get_llvm_name(), self.operand2.get_data_type().get_llvm_name()

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_binary_assign_instruction(self)

    @abc.abstractmethod
    def get_llvm_for_operation(self):
        raise NotImplementedError


class LLVMBinaryArithmeticInstruction(LLVMBinaryAssignInstruction):
    """
    Instructions which apply arithmetics on registers and puts the result in another register
    """

    def __init__(self, operation: ASTTokens.BinaryArithmeticExprToken,
                 operand1: LLVMValue,
                 operand2: LLVMValue):
        resulting_data_type = DataType.DataType.get_resulting_data_type(operand1.get_data_type(),
                                                                        operand2.get_data_type())
        super().__init__(LLVMValue.LLVMRegister(resulting_data_type),
                         operation, operand1, operand2)
        self.operation_type = self.get_operation_type()

    def get_operation_type(self):
        if self.operand1.get_data_type() == DataType.NORMAL_INT and self.operand2.get_data_type() == DataType.NORMAL_INT:
            return 'i32'
        elif self.operand1.get_data_type() == DataType.NORMAL_FLOAT and self.operand2.get_data_type() == DataType.NORMAL_FLOAT:
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

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_binary_arithmetic_instruction(self)


class LLVMDataTypeConvertInstruction(LLVMUnaryAssignInstruction):

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
        if (self.get_operand().get_data_type().is_integral() and
                self.get_resulting_register().get_data_type().is_floating_point()):
            return 'sitofp', f'to {self.get_resulting_register().get_data_type().get_llvm_name()}'
        elif (self.get_operand().get_data_type().is_floating_point() and
              self.get_resulting_register().get_data_type().is_integral()):
            return 'fptosi', f'to {self.get_resulting_register().get_data_type().get_llvm_name()}'
        else:
            raise NotImplementedError

    def to_llvm(self):
        return super().to_llvm() + f'{self.llvm_operation} {self.get_operand().get_data_type().get_llvm_name()}' \
                                   f' {self.get_operand().to_llvm()} {self.llvm_to_data_type}'

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_data_type_convert_instruction(self)


class LLVMCompareInstruction(LLVMBinaryAssignInstruction):
    """
    Creates 1 compare instruction for the two resulting registers. Does not do any type conversions first, so make
    sure you do that. The LLVMBuilder has such a method to create the full compare statement (with type conversions)
    # TODO comparing with constants such as 0 and stuff
    """

    def __init__(self, operation: ASTTokens.RelationalExprToken,
                 operand1: LLVMValue,
                 operand2: LLVMValue):
        super().__init__(LLVMValue.LLVMRegister(DataType.NORMAL_BOOL), operation, operand1, operand2)
        assert operand1.get_data_type() == operand2.get_data_type(), \
            "Data types to compare must be equal. Perform an instruction to convert a" \
            "lower data type to a higher one (e.g. sitofp for i32 -> float)"

        self.operation = operation
        self.comparison_type = self.get_comparison_type()

    def get_resulting_data_type(self):
        return self.get_resulting_register().get_data_type()

    def get_comparison_type(self):
        """
        Checks the entered datatypes to determine which LLVMUtils.ComparisonDataType will be used and what the llvm code will be as comparison type (for example, i32)
        """

        # Its the same, whether you pick operand1 or operand2 (they have the same data type)
        data_type_to_compare = self.operand1.get_data_type()

        if data_type_to_compare == DataType.NORMAL_DOUBLE or data_type_to_compare == DataType.NORMAL_FLOAT:
            return LLVMUtils.ComparisonDataType.FLOAT
        elif data_type_to_compare == DataType.NORMAL_INT:
            return LLVMUtils.ComparisonDataType.INT
        elif data_type_to_compare == DataType.NORMAL_CHAR:
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
                                   f'{self.operand1.get_data_type().get_llvm_name()} {self.operand1}, {self.operand2}'

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_compare_instruction(self)


# TODO must be implemented
class LLVMUnaryArithmeticInstruction(LLVMAssignInstruction):

    def __init__(self, resulting_reg: LLVMValue.LLVMRegister):
        super().__init__(resulting_reg)
        raise NotImplementedError

    def to_llvm(self):
        raise NotImplementedError

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_unary_arithmetic_instruction(self)


class LLVMGetElementPtrInstruction(LLVMAssignInstruction):

    def __init__(self, resulting_register: LLVMValue.LLVMRegister, index: str, size: LLVMValue.LLVMLiteral,
                 array_register: LLVMValue.LLVMRegister):
        super().__init__(resulting_register)
        self.index = index
        self.size = size
        self.array_register = array_register
        assert isinstance(index, str)
        assert isinstance(size, LLVMValue.LLVMLiteral)
        assert isinstance(array_register, LLVMValue.LLVMRegister)

    def to_llvm(self):
        datatype = DataType.DataType(self.array_register.get_data_type().get_token(),
                                     self.array_register.get_data_type().get_pointer_level() - 1)
        return super().to_llvm() + f'getelementptr inbounds [{self.size.get_value()} x {datatype.get_llvm_name()}], ' \
                                   f'[{self.size.get_value()} x {datatype.get_llvm_name()}]* {self.array_register.to_llvm()}, i64 0, i64 {self.index}'

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_get_elementptr_instruction(self)


class LLVMPrintfInstruction(LLVMAssignInstruction):

    def __init__(self, register_to_print: LLVMValue.LLVMRegister,
                 string_to_print_name: str):
        """
        Creates a PrintfInstructions string
        result_register: the register where the result of the function goes in (the number of chars printed)
        type_to_print: the type to print (most likely a global constant you have defined)
        string_to_print_name: the global variable which contains the string to print (e.g. @.str.0)
        """
        super().__init__(LLVMValue.LLVMRegister(DataType.NORMAL_INT))

        self.register_to_print = register_to_print
        self.string_to_print_name = string_to_print_name

    def is_terminator(self):
        return False

    def to_llvm(self):
        # TODO must be customized to be able to print completely custom names
        return super().to_llvm() + f"call i32 (i8*, ...) @printf(i8* getelementptr inbounds([3 x i8], [3 x i8]* {self.string_to_print_name}, i64 0, i64 0), i32 {self.register_to_print})"

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_printf_instruction(self)


class LLVMCallInstruction(LLVMAssignInstruction):

    def __init__(self, function_to_call, args: list, infinity_params=False):
        from src.llvm.LLVMFunction import LLVMFunction
        """
        Function to call: should be an LLVMFunction.LLVMFunction instance
        Params: list of LLVMValues
        """
        assert isinstance(function_to_call, LLVMFunction)
        self.function_to_call = function_to_call
        self.args = args
        self.infinity_args = infinity_params
        super().__init__(LLVMValue.LLVMRegister(function_to_call.get_return_type()))

    def to_llvm(self):
        llvm_code = f'{super().to_llvm()}call {self.function_to_call.get_return_type().get_llvm_name()} ' \
                    f'@{self.function_to_call.get_identifier()}('

        for i in range(len(self.args)):
            arg = self.args[i]
            assert isinstance(arg, LLVMValue.LLVMValue)

            llvm_code += f'{arg.get_data_type().get_llvm_name()} {arg.to_llvm()}'

            if i != len(self.args) - 1:
                llvm_code += ','

        llvm_code += ')'

        return llvm_code

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_call_instruction(self)


class LLVMBitcastInstruction(LLVMAssignInstruction):

    def __init__(self, reg_to_convert: LLVMValue.LLVMRegister, from_type: str, to_type: str):
        super().__init__(LLVMValue.LLVMRegister())
        self.reg_to_convert = reg_to_convert
        self.from_type = from_type
        self.to_type = to_type

    def to_llvm(self):
        return super().to_llvm() + f'bitcast {self.from_type} {self.reg_to_convert} to {self.to_type}'

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_bitcast_instruction(self)


class LLVMMemcpyInstruction(LLVMInstruction):

    def __init__(self, copy_into_reg: LLVMValue.LLVMRegister, size: int, from_global_var: str):
        self.copy_in_reg = copy_into_reg
        self.size = size
        self.from_global_var = from_global_var
        super().__init__()

    def is_terminator(self):
        return False

    def to_llvm(self):
        return f'call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 {self.copy_in_reg.to_llvm()}, i8* align 1 ' \
               f'getelementptr inbounds ([{self.size} x i8], [{self.size} x i8]* {self.from_global_var}, i32 0, i32 0), ' \
               f'i64 {self.size}, i1 false)'

    def update_numbering(self, counter):
        super().update_numbering(counter)

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_memcpy_instruction(self)
