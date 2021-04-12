import src.ast.llvm.LLVMInstruction as LLVMInstruction
import src.ast.llvm.LLVMInterfaces as LLVMInterfaces


class LLVMBasicBlock(LLVMInterfaces.IToLLVM):

    def __init__(self, number: int):
        self.instructions = list()
        self.number = number

    def add_instruction(self, instruction: LLVMInstruction.Instruction):
        """
        Safely adds a new instruction to the list of instructions
        """
        assert isinstance(instruction, LLVMInstruction.Instruction)
        assert not self.has_terminal_instruction()
        self.instructions.append(instruction)

    def has_terminal_instruction(self):
        """
        Checks whether or not this basic block has a terminator at the end (has a terminator at the end)
        """

        return len(self.instructions) > 0 and self.instructions[-1].is_terminator()

    def get_number(self):
        """
        Returns the number of this basic block
        """
        return self.number

    def to_llvm(self):
        llvm_code = ""

        for instruction in self.instructions:
            llvm_code += f"  {instruction.to_llvm()}\n"

        return llvm_code
