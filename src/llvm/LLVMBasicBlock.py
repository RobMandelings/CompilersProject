import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMInterfaces as LLVMInterfaces
import src.llvm.LLVMUtils as LLVMUtils


class LLVMBasicBlock(LLVMInterfaces.IToLLVM):

    def __init__(self):
        self.instructions = list()
        self._number = None

    def add_instruction(self, instruction):
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
        Returns the _number of this basic block
        """
        assert self._number is not None, "the number of this basic block has not been initialized yet"
        return self._number

    def update_numbering(self, counter: LLVMUtils.LLVMCounter):
        for instruction in self.instructions:
            instruction.update_numbering(counter)

    def to_llvm(self):
        llvm_code = ""

        for instruction in self.instructions:
            llvm_code += f"  {instruction.to_llvm()}\n"

        return llvm_code
