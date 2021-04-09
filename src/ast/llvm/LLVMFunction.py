from src.ast.llvm.LLVMBasicBlock import LLVMBasicBlock
from src.ast.llvm.LLVMInstruction import *


class LLVMFunction(IToLLVM):

    def __init__(self, name: str):
        # Counts the number of registers
        self.counter = 0
        self.name = name
        self.local_variables_registers = dict()
        self.basic_blocks = dict()
        self.basic_blocks[-1] = LLVMBasicBlock()
        self.last_added_basic_block_label = -1

    def get_basic_block(self, label):
        return self.basic_blocks[label]

    def get_current_basic_block(self):
        assert self.basic_blocks[self.last_added_basic_block_label] is not None
        return self.basic_blocks[self.last_added_basic_block_label]

    def add_basic_block(self):
        """
        Adds a new basic block to the list of basic blocks and returns this basic block
        """
        label_to_return = self.counter
        self.basic_blocks[label_to_return] = LLVMBasicBlock()
        self.counter += 1
        self.last_added_basic_block_label = label_to_return
        return label_to_return

    def add_instruction(self, instruction: Instruction):
        """
        Adds an instruction to the current basic block of this function, for later llvm code generation
        """
        assert isinstance(instruction, Instruction)
        self.get_current_basic_block().add_instruction(instruction)

    def get_new_register(self):
        """
        Returns the first local available register in LLVM (e.g. if registers %0-%6 are already in use, the newest register will be %7)
        The register will be returned in string notation (e.g. '%7')

        After this call, the returned register will be seen as 'reserved', thus, the counter (for registers & labels) increases (by one)
        afterwards for retrieval of new available registers.
        """
        register_to_return = f"%{self.counter}"
        self.counter += 1
        return register_to_return

    def to_llvm(self):
        llvm_code = ""

        first = True
        for label in self.basic_blocks:

            basic_block = self.basic_blocks[label]

            if not first:
                llvm_code += f"{label}:\n"

            llvm_code += basic_block.to_llvm() + '\n'
            first = False

        return llvm_code
