from src.ast.llvm.LLVMInstruction import *


class LLVMBasicBlock(IToLLVM):

    def __init__(self):
        self.instructions = list()

    def add_instruction(self, instruction: Instruction):
        """
        Safely adds a new instruction to the list of instructions
        """
        assert isinstance(instruction, Instruction)
        assert not self.has_terminal_instruction()
        self.instructions.append(instruction)

    def has_terminal_instruction(self):
        """
        Checks whether or not this basic block has a terminator at the end (has a terminator at the end)
        """
        return self.instructions[-1].is_terminator()

    def to_llvm(self):
        llvm_code = ""

        for instruction in self.instructions:
            llvm_code += f"{instruction.to_llvm()}\n"

        return llvm_code
