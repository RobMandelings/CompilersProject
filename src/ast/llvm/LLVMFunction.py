import src.ast.llvm.LLVMInstruction as LLVMInstruction
import src.ast.llvm.LLVMInterfaces as LLVMInterfaces
import src.ast.llvm.LLVMUtils as LLVMUtils
import src.ast.llvm.LLVMValue as LLVMValue
from src.ast.llvm.LLVMBasicBlock import LLVMBasicBlock


class LLVMFunction(LLVMInterfaces.IToLLVM):

    def __init__(self, name: str):
        # Counts the number of registers and basic blocks. This is just a temporary counter to give unique references
        # as the real definitive registers & labels are unknown at building time
        self.internal_counter = LLVMUtils.LLVMCounter()
        self.name = name
        self.local_variables_registers = dict()
        self.basic_blocks = list()
        self.basic_blocks.append(LLVMBasicBlock(-1))

    def get_basic_block(self, number):
        for basic_block in self.basic_blocks:
            if basic_block.get_number() == number:
                return basic_block
        raise ValueError(f'No basic block with number {number} exists')

    def get_current_basic_block(self):
        assert self.basic_blocks[-1] is not None
        return self.basic_blocks[-1]

    def add_basic_block(self):
        """
        Adds a new basic block to the list of basic blocks and returns this basic block
        """
        new_basic_block = LLVMBasicBlock(self.internal_counter.get_value())
        self.basic_blocks.append(new_basic_block)
        self.internal_counter.increase()
        return new_basic_block

    def add_instruction(self, instruction: LLVMInstruction.Instruction):
        """
        Adds an instruction to the current basic block of this function, for later llvm code generation
        """
        assert isinstance(instruction, LLVMInstruction.Instruction)
        self.get_current_basic_block().add_instruction(instruction)

    def get_new_register(self, data_type=None):
        """
        Returns the first local available register in LLVM (e.g. if registers %0-%6 are already in use, the newest register will be %7)
        The register will be returned in string notation (e.g. '%7')

        After this call, the returned register will be seen as 'reserved', thus, the counter (for registers & labels) increases (by one)
        afterwards for retrieval of new available registers.
        """
        register_to_return = LLVMValue.LLVMRegister(f'%{self.internal_counter}', data_type)
        self.internal_counter.increase()
        return register_to_return

    def update_numbering(self, counter):
        first = True
        for basic_block in self.basic_blocks:

            if not first:
                basic_block.number = counter.get_value()
                counter.increase()
            else:
                first = False

            basic_block.update_numbering(counter)

    def to_llvm(self):
        llvm_code = ""

        # This is the counter that will be used to give names to the definitive registers and labels of the basic blocks
        # We need to do this because due to building purposes, the current numbering is wrong
        counter = LLVMUtils.LLVMCounter()
        self.update_numbering(counter)

        first = True
        for basic_block in self.basic_blocks:

            if not first:
                llvm_code += f"{basic_block.get_number()}:\n"
            else:
                first = False

            llvm_code += f'{basic_block.to_llvm()} \n'

        return llvm_code
