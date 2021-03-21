from src.ast.llvm.LLVMBasicBlock import BasicBlock
from src.ast.llvm.LLVMInstruction import Instruction


class FunctionLLVM:

    def __init__(self, name: str):
        self.instruction_counter = 0
        self.name = name
        self.local_variables_registers = dict()
        self.basic_blocks = list()
        self.basic_blocks.append(BasicBlock())

    def get_current_basic_block(self):
        return self.basic_blocks[-1]

    def start_new_basic_block(self):
        """
        Creates a new basic block within this function and adds it to the list of basic blocks.
        PRE-CONDITION: the current basic block must have ended (have a terminal instruction)
        """
        assert self.get_current_basic_block().get_terminal_instruction() is not None
        self.basic_blocks.append(BasicBlock())

    def add_instruction(self, instruction: Instruction):
        assert isinstance(instruction, Instruction)
        self.get_current_basic_block().instructions.append(instruction)
