import abc
import src.Instruction as Instruction


class BasicBlock(abc.ABC):
    """
    Generic basic block class that is inherited in the LLVMBasicBlock class and MipsBasicBlock class
    """

    def __init__(self):
        self.instructions = list()

    def has_terminal_instruction(self):
        """
        Checks whether or not this basic block has a terminator at the end (has a terminator at the end)
        """

        return len(self.instructions) > 0 and self.instructions[-1].is_terminator()

    # Abstract method as either the Mips or LLVM basic block should check for valid instruction insertion
    @abc.abstractmethod
    def add_instruction(self, instruction):
        """
        Safely adds a new instruction to the list of instructions
        """
        assert isinstance(instruction, Instruction.Instruction)
        assert not self.has_terminal_instruction()
        self.instructions.append(instruction)

    def is_empty(self):
        return len(self.instructions) == 0
