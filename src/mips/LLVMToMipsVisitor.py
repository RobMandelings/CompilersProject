import src.llvm.visitors.LLVMBaseVisitor as LLVMBaseVisitor
import src.mips.MipsValue as MipsValue
import src.llvm.LLVMValue as LLVMValue
import src.mips.MipsBuilder as MipsBuilder
from src.llvm import LLVMFunction as LLVMFunction, LLVMCode as LLVMCode, LLVMBasicBlock as LLVMBasicBlock, \
    LLVMInstruction as LLVMInstruction
import src.mips.MipsInstruction as MipsInstruction
import src.ast.ASTTokens as ASTTokens

class LLVMToMipsVisitor(LLVMBaseVisitor.LLVMBaseVisitor):
    """
    Visitor which will generate MIPS code from LLVM IR
    """

    def __init__(self):
        """
        Symbol table holds for each basic block the liveness and usage information for each instruction within this
        basic block as well as some other useful information
        """
        self.mips_builder = None

    def get_mips_builder(self):
        assert isinstance(self.mips_builder, MipsBuilder.MipsBuilder)
        return self.mips_builder

    def visit_llvm_code(self, llvm_code: LLVMCode.LLVMCode):
        self.mips_builder = MipsBuilder.MipsBuilder(llvm_code)

    def visit_llvm_defined_function(self, llvm_defined_function: LLVMFunction.LLVMDefinedFunction):
        mips_function = MipsBuilder.MipsFunction(llvm_defined_function.get_identifier())
        self.get_mips_builder().add_function(mips_function)

        # Continue visiting the other instructions / basic blocks
        super().visit_llvm_defined_function(llvm_defined_function)

        # We need to do this after the visitor has been through all instructions, in order to know which
        # Registers needs to be saved
        # We need to save the used registers from within the function definition to make sure that the
        # Registers can be restored after the function is done.
        self.get_mips_builder().store_saved_registers()

        # Load the saved registers after executing instructions
        self.get_mips_builder().load_saved_registers()

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        self.get_mips_builder().get_current_function().add_mips_basic_block()
        super().visit_llvm_basic_block(llvm_basic_block)

    def visit_llvm_store_instruction(self, instruction: LLVMInstruction.LLVMStoreInstruction):
        super().visit_llvm_store_instruction(instruction)

        mips = self.get_mips_builder().get_mips_values(instruction, instruction.resulting_reg, [instruction.value_to_store])
        mips_resulting_register = mips[0]
        mips_operands = mips[1]
        token = ASTTokens.BinaryArithmeticExprToken.ADD

        mips_instruction = MipsInstruction.ArithmeticBinaryInstruction(MipsValue.MipsRegister.ZERO, mips_operands[0], token, mips_resulting_register)
        self.get_mips_builder().get_current_function().add_instruction(mips_instruction)

    def visit_llvm_call_instruction(self, instruction: LLVMInstruction.LLVMCallInstruction):
        # Callers responsibility: store the registers used that you want to keep after the function call
        self.get_mips_builder().store_temporary_registers()

        # The argument mips registers are used first ($a) to put values in. If this is not enough,
        # The remaining arguments will be stored in memory.
        arg_mips_registers = list()

        # You can only take 4 $a registers, so range is (0, 3) at most
        for i in range(0, min(3, len(instruction.args))):

            llvm_arg = instruction.args[i]
            current_mips_reg = MipsValue.MipsRegister.get_arg_registers()

            if isinstance(llvm_arg, LLVMValue.LLVMRegister):
                # Make sure to save the currently assigned register in case its used within the function
                current_assigned_llvm_reg = self.get_mips_builder().get_current_descriptors() \
                    .get_assigned_register_for_mips_reg(current_mips_reg)
                self.get_mips_builder().store_in_memory(current_assigned_llvm_reg)
                self.get_mips_builder().load_in_reg(llvm_value=llvm_arg, store_in_reg=current_mips_reg)

        mips_result, mips_operands = self.get_mips_builder().get_mips_values(instruction,
                                                                             instruction.get_resulting_register(),
                                                                             instruction.args)

        super().visit_llvm_call_instruction(instruction)

        # Callers responsibility: load the registers used that you want to keep
        self.get_mips_builder().load_temporary_registers()
