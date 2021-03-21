from src.ast.llvm.BasicBlock import BasicBlock
from src.ast.llvm.Instruction import Instruction


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
        assert self.get_current_basic_block().terminator_instruction is not None
        self.basic_blocks.append(BasicBlock())

    def add_instruction(self, instruction: Instruction):
        assert isinstance(instruction, Instruction)
        self.get_current_basic_block().instructions.append(instruction)
