import collections

import src.DataType as DataType
import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMInterfaces as LLVMInterfaces
import src.llvm.LLVMUtils as LLVMUtils
import src.llvm.LLVMValue as LLVMValue


class LLVMFunction(LLVMInterfaces.IToLLVM):

    def __init__(self, identifier: str, return_type: DataType.DataType, params: list):
        """
        Creates a new function in llvm.
        return_type: DataType of the return type of this function
        params: a list of LLVMRegisters with a specific data type
        """
        self.identifier = identifier
        self.return_type = return_type
        self.params = params

        self.basic_blocks = collections.OrderedDict()
        self.first_basic_block = LLVMBasicBlock.LLVMBasicBlock()
        self.basic_blocks[id(self.first_basic_block)] = self.first_basic_block

    def get_identifier(self):
        return self.identifier

    def get_nr_params(self):
        """
        Returns the number of parameters of this function
        """
        return len(self.params)

    def get_first_basic_block(self):
        return self.first_basic_block

    def has_basic_block(self, basic_block):
        """
        Returns the index of the basic block given from the list of basic blocks in this function if applicable.
        Otherwise return None
        """
        return self.basic_blocks.get(id(basic_block)) is not None

    def get_current_basic_block(self):
        return self.basic_blocks.get(next(reversed(self.basic_blocks)))

    def add_instruction(self, instruction: LLVMInstruction.Instruction):
        self.get_current_basic_block().add_instruction(instruction)

    def add_basic_block(self, basic_block: LLVMBasicBlock = None):
        """
        Adds the given basic block to this function and makes it the current basic block to continue with
        after: by default None, specifies the basic block after which to place this basic block. If None, the basic
        block will be appended to the end.
        Returns the inserted basic block
        """

        if basic_block is None:
            basic_block = LLVMBasicBlock.LLVMBasicBlock()

        assert not self.has_basic_block(basic_block), "Basic block would be inserted twice"
        self.basic_blocks[id(basic_block)] = basic_block

        return basic_block

    def get_return_type(self):
        assert isinstance(self.return_type, DataType.DataType)
        return self.return_type

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

        for i in range(len(self.params)):
            param = self.params[i]
            assert isinstance(param, LLVMValue.LLVMRegister)
            param.value = counter.get_value()
            counter.increase()

        # No idea why the counter has to be increased again but its necessary
        counter.increase()

        first_basic_block = True
        for basic_block_id, basic_block in self.basic_blocks.items():

            if not first_basic_block:
                basic_block._number = counter.get_value()
                counter.increase()
            else:
                first_basic_block = False

            basic_block.update_numbering(counter)

    def to_llvm(self):

        # This is the counter that will be used to give names to the definitive registers and labels of the basic blocks
        # We need to do this because due to building purposes, the current numbering is wrong
        counter = LLVMUtils.LLVMCounter()
        self.update_numbering(counter)

        llvm_code = f'define dso_local {self.get_return_type().get_llvm_name()} @{self.identifier}('

        for i in range(len(self.params)):
            param = self.params[i]
            assert isinstance(param, LLVMValue.LLVMRegister)

            llvm_code += f'{param.get_data_type().get_llvm_name()} %{param.get_value()}'
            if i != len(self.params) - 1:
                llvm_code += ','

        llvm_code += ') {\n'

        first = True
        for basic_block_id, basic_block in self.basic_blocks.items():

            if not first:
                llvm_code += f"{basic_block.get_number()}:\n"
            else:
                first = False

            llvm_code += f'{basic_block.to_llvm()}\n'

        llvm_code += '}'

        return llvm_code
