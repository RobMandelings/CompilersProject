import src.llvm.visitors.LLVMBaseVisitor as LLVMBaseVisitor
from src.llvm import LLVMInstruction as LLVMInstruction, LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMValue as LLVMValue
import src.mips.LLVMUsageInformation as LLVMUsageInformation


class LLVMFillUsageTableVisitor(LLVMBaseVisitor.LLVMBaseVisitor):
    """
    Fills a usage and liveness table for each instructio
    """

    def __init__(self):
        self.usage_table = None
        self.register_usage = dict()

    def get_usage_table(self):
        assert isinstance(self.usage_table, LLVMUsageInformation.LLVMUsageInformation)
        return self.usage_table

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        self.usage_table = LLVMUsageInformation.LLVMUsageInformation()
        for instruction in reversed(llvm_basic_block.instructions):
            instruction.accept(self)

    def get_register_usage(self, llvm_register: LLVMValue.LLVMRegister):
        if not llvm_register in self.register_usage:
            return LLVMUsageInformation.LLVMRegisterInformation(alive=False, next_usage=None)
        else:
            return self.register_usage.get(llvm_register)

    def visit_llvm_binary_assign_instruction(self, instruction: LLVMInstruction.LLVMBinaryAssignInstruction):

        # Attach to the instruction the current liveness and usage information and
        # Update the register usage
        instruction_information = LLVMUsageInformation.LLVMInstructionInformation()
        instruction_information.registers_information[instruction.get_resulting_register()] = self.get_register_usage(
            instruction.get_resulting_register())

        self.register_usage[instruction.get_resulting_register()] = \
            LLVMUsageInformation.LLVMRegisterInformation(alive=False, next_usage=None)

        if isinstance(instruction.operand1, LLVMValue.LLVMRegister):
            instruction_information.registers_information[instruction.operand1] = self.get_register_usage(
                instruction.operand1)
            self.register_usage[instruction.operand1] = \
                LLVMUsageInformation.LLVMRegisterInformation(alive=True,
                                                             next_usage=instruction)

        if isinstance(instruction.operand2, LLVMValue.LLVMRegister):
            instruction_information.registers_information[instruction.operand2] = self.get_register_usage(
                instruction.operand2)
            self.register_usage[instruction.operand2] = \
                LLVMUsageInformation.LLVMRegisterInformation(alive=True,
                                                             next_usage=instruction)

        self.get_usage_table().llvm_instructions_information[instruction] = instruction_information
