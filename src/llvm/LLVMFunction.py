import abc
import collections

import src.DataType
import src.DataType as DataType
import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMInterfaces as LLVMInterfaces
import src.llvm.LLVMUtils as LLVMUtils
import src.llvm.LLVMValue as LLVMValue
import src.ast.ASTs as ASTs
import src.interfaces.IVisitable as IVisitable


class LLVMFunction(LLVMInterfaces.IToLLVM, abc.ABC):

    def __init__(self, identifier: str, return_type: DataType.DataType, params: list):
        self.identifier = identifier
        self.return_type = return_type
        self.params = params

    def get_identifier(self):
        return self.identifier

    def get_return_type(self):
        assert isinstance(self.return_type, DataType.DataType)
        return self.return_type

    def get_param_data_types(self):
        param_data_types = list()
        for param in self.params:
            if isinstance(param, src.DataType.IHasDataType):
                param_data_types.append(param.get_data_type())
            elif isinstance(param, DataType.DataType):
                param_data_types.append(param)
            else:
                raise ValueError('Param must have a data type or be a data type')

        return param_data_types


class LLVMDeclaredFunction(LLVMFunction):

    def __init__(self, identifier: str, return_type: DataType.DataType, params_data_types: list):
        super().__init__(identifier, return_type, params_data_types)
        self.params_data_types = params_data_types

        for param in self.params_data_types:
            assert isinstance(param, DataType.DataType)

    def get_param_data_types(self):
        return self.params_data_types

    def to_llvm(self):
        llvm_code = f'declare dso_local {self.return_type.get_llvm_name()} @{self.identifier}('
        param_data_types = self.get_param_data_types()
        if len(param_data_types) == 0:
            llvm_code += '...'
        else:
            for i in range(len(param_data_types)):
                param_data_type = param_data_types[i]
                llvm_code += param_data_type.get_llvm_name()

                if i != len(param_data_types) - 1:
                    llvm_code += ','

        llvm_code += ')'
        return llvm_code


class LLVMDefinedFunction(LLVMFunction):

    def __init__(self, identifier: str, return_type: DataType.DataType, params: list):
        """
        Creates a new function in llvm.
        return_type: DataType of the return type of this function
        params: a list of LLVMRegisters with a specific data type
        """
        super().__init__(identifier, return_type, params)
        self.__alloca_instructions = list()
        self.basic_blocks = collections.OrderedDict()
        self.first_basic_block = LLVMBasicBlock.LLVMBasicBlock()
        self.basic_blocks[id(self.first_basic_block)] = self.first_basic_block

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
        if isinstance(instruction, LLVMInstruction.AllocaInstruction):
            self.__alloca_instructions.append(instruction)
        else:
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

        for alloca_instruction in self.__alloca_instructions:
            assert isinstance(alloca_instruction, LLVMInstruction.AllocaInstruction)
            alloca_instruction.update_numbering(counter)

        first_basic_block = True
        for basic_block_id, basic_block in self.basic_blocks.items():

            if not first_basic_block:
                basic_block._number = counter.get_value()
                counter.increase()
            else:
                first_basic_block = False

            basic_block.update_numbering(counter)

    def _add_ret_if_necessary(self):

        # Maybe do this in a better way but for now it's good, just append ret to the basic block if it is empty
        # LLVM does this in a weird way
        if not self.get_current_basic_block().has_terminal_instruction():
            allocated_reg = LLVMValue.LLVMRegister(DataType.DataType(self.get_return_type().get_token(),
                                                                     self.get_return_type().get_pointer_level() + 1))
            alloca_instruction = LLVMInstruction.AllocaInstruction(allocated_reg)
            self.add_instruction(alloca_instruction)

            loaded_reg = LLVMValue.LLVMRegister(self.get_return_type())
            self.add_instruction(LLVMInstruction.LoadInstruction(loaded_reg, allocated_reg))
            self.add_instruction(LLVMInstruction.ReturnInstruction(loaded_reg))

    def to_llvm(self):

        self._add_ret_if_necessary()

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

        for alloca_instruction in self.__alloca_instructions:
            llvm_code += f'  {alloca_instruction.to_llvm()}\n'

        first = True
        for basic_block_id, basic_block in self.basic_blocks.items():

            if not first:
                llvm_code += f"{basic_block.get_number()}:\n"
            else:
                first = False

            llvm_code += f'{basic_block.to_llvm()}\n'

        llvm_code += '}'

        return llvm_code
