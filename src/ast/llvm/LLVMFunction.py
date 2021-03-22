from src.ast.llvm.LLVMBasicBlock import LLVMBasicBlock
from src.ast.llvm.LLVMBuilder import IToLLVM
from src.ast.llvm.LLVMInstruction import Instruction


class FunctionLLVM(IToLLVM):

    def __init__(self, name: str):
        # Counts the number of registers
        self.counter = 0
        self.name = name
        self.local_variables_registers = dict()
        self.basic_blocks = dict()
        self.basic_blocks[-1] = LLVMBasicBlock()

    def get_current_basic_block(self):
        return self.basic_blocks[-1]

    def add_basic_block(self, basic_block: LLVMBasicBlock):
        """
        Adds a new basic block to the list of basic blocks which will now be current
        PRE-CONDITION: the previous basic block must have ended (have a terminal instruction in the end)
        """
        assert self.get_current_basic_block().has_terminal_instruction()
        label_to_return = self.counter
        self.basic_blocks[label_to_return] = basic_block
        self.counter += 1
        return label_to_return

    def add_instruction(self, instruction: Instruction):
        assert isinstance(instruction, Instruction)
        self.get_current_basic_block().add_instruction(instruction)

    def get_new_register(self):
        register_to_return = f"%{self.counter}"
        self.counter += 1
        return register_to_return

    def to_llvm(self):
        llvm_code = ""

        first = True
        for label in self.basic_blocks:

            basic_block = self.basic_blocks[label]

            if not first:
                llvm_code = f"{label}:\n"
            else:
                llvm_code = ""

            llvm_code += basic_block.to_llvm()

        return llvm_code
