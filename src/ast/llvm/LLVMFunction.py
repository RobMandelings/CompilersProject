import src.ast.llvm.LLVMInstruction as LLVMInstruction
import src.ast.llvm.LLVMInterfaces as LLVMInterfaces
import src.ast.llvm.LLVMUtils as LLVMUtils
import src.ast.llvm.LLVMValue as LLVMValue
import src.ast.llvm.LLVMBasicBlock as LLVMBasicBlock


class LLVMFunction(LLVMInterfaces.IToLLVM):

    def __init__(self, name: str):
        self.name = name
        self.local_variables_registers = dict()
        self.basic_blocks = list()
        self.first_basic_block = LLVMBasicBlock.LLVMBasicBlock()
        self.basic_blocks.append(self.first_basic_block)

    def get_first_basic_block(self):
        return self.first_basic_block

    def get_basic_block_index(self, basic_block):
        """
        Returns the index of the basic block given from the list of basic blocks in this function if applicable.
        Otherwise return None
        """

        for i in range(len(self.basic_blocks)):
            if id(self.basic_blocks[i]) == id(basic_block):
                assert isinstance(basic_block, LLVMBasicBlock.LLVMBasicBlock)
                return i

        return None

    def get_current_basic_block(self):
        assert self.basic_blocks[-1] is not None
        return self.basic_blocks[-1]

    def add_instruction(self, instruction: LLVMInstruction.Instruction):
        self.get_current_basic_block().add_instruction(instruction)

    def insert_basic_block(self, basic_block: LLVMBasicBlock = None, after=None):
        """
        Adds the given basic block to this function and makes it the current basic block to continue with
        after: by default None, specifies the basic block after which to place this basic block. If None, the basic
        block will be appended to the end.
        Returns the inserted basic block
        """

        assert self.get_basic_block_index(basic_block) is None, "Basic block would be inserted twice"

        if basic_block is None:
            basic_block = LLVMBasicBlock.LLVMBasicBlock()

        if after is not None:
            after_basic_block_index = self.get_basic_block_index(after)
            assert after_basic_block_index is not None
            self.basic_blocks.insert(after_basic_block_index, basic_block)
        else:
            self.basic_blocks.append(basic_block)

        return basic_block

    def get_new_register(self, data_type=None):
        """
        Returns the first local available register in LLVM (e.g. if registers %0-%6 are already in use, the newest register will be %7)
        The register will be returned in string notation (e.g. '%7')

        After this call, the returned register will be seen as 'reserved', thus, the counter (for registers & labels) increases (by one)
        afterwards for retrieval of new available registers.
        """
        register_to_return = LLVMValue.LLVMRegister(data_type)
        return register_to_return

    def update_numbering(self, counter):
        first = True
        for basic_block in self.basic_blocks:

            if not first:
                basic_block._number = counter.get_value()
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
