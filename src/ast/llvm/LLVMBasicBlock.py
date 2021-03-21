from src.ast.llvm.LLVMInstruction import Instruction


class BasicBlock:

    def __init__(self):
        self.instructions = list()
        self.__terminator_instruction = None

    def set_terminator_instruction(self, instruction: Instruction):
        assert instruction.is_terminator()
        self.__terminator_instruction = instruction

    def get_terminal_instruction(self):
        return self.__terminator_instruction
