from src.ast.llvm.LLVMBasicBlock import LLVMBasicBlock
from src.ast.llvm.LLVMBuilder import IToLLVM
from src.ast.llvm.LLVMInstruction import Instruction


class FunctionLLVM(IToLLVM):

    def __init__(self, name: str):
        self.instruction_counter = 0
        self.name = name
        self.local_variables_registers = dict()
        self.basic_blocks = list()
        self.basic_blocks.append(LLVMBasicBlock())

    def get_current_basic_block(self):
        return self.basic_blocks[-1]

    def start_new_basic_block(self):
        """
        Creates a new basic block within this function and adds it to the list of basic blocks.
        PRE-CONDITION: the current basic block must have ended (have a terminal instruction)
        """
        assert self.get_current_basic_block().has_terminal_instruction()
        self.basic_blocks.append(LLVMBasicBlock())

    def add_instruction(self, instruction: Instruction):
        assert isinstance(instruction, Instruction)
        self.get_current_basic_block().add_instruction(instruction)

    def to_llvm(self):
        llvm_code = ""

        for basic_block in self.basic_blocks:
            llvm_code += basic_block.to_llvm()

        return llvm_code
