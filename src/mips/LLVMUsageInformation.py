import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMValue as LLVMValue


class LLVMInstructionInformation:
    """
    Usage and liveness information for all registers in this instruction
    """

    def __init__(self):
        self.registers_information = dict()

    def get_register_information(self, llvm_register: LLVMValue.LLVMRegister):
        register_information = self.registers_information[llvm_register]
        assert isinstance(register_information, LLVMRegisterInformation)
        return register_information


class LLVMRegisterInformation:
    """
    Usage and liveness information for this register in a specific instruction
    """

    def __init__(self, alive, next_usage):
        self.live = alive
        self.next_usage = next_usage

    def is_live(self):
        """
        Returns whether or not the register is alive (from the definition)
        """
        return self.live

    def get_next_usage(self):
        """
        Returns the next usage of the register, or None if it doesn't have a next usage
        """
        return self.next_usage


class LLVMUsageInformation:
    """
    Table which keeps track, for each instruction within a basic block whether or not the variable is live and used
    """

    def __init__(self):
        self.llvm_instructions_information = dict()

    def get_instruction_information(self, llvm_instruction: LLVMInstruction.LLVMInstruction):
        """
        Retrieves the usage and liveness information for a given instruction
        """
        instruction_information = self.llvm_instructions_information[llvm_instruction]
        assert isinstance(instruction_information, LLVMInstructionInformation)
        return instruction_information
