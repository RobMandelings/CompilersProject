import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMValue as LLVMValue
import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.mips.MipsValue as MipsValue
import src.mips.MipsBasicBlock as MipsBasicBlock
import src.mips.MipsInstruction as MipsInstruction
import src.mips.LLVMUsageInformation as LLVMUsageInformation


class RegisterPool:
    """
    Makes it easier to work with registers if
    there are more of the same kind as it puts them in a list
    TODO registers pool should be immutable
    """

    def __init__(self):
        """
        temporary_registers: all temporary registers available in MIPS
        saved_registers: all saved temporary registers available in MIPS
        """
        self.__temporary_registers = list()
        self.__saved_registers = list()

    def __init_pool(self):
        """
        Initializes the pool of registers by filling the lists
        """
        for temp_reg_index in range(0, 9):
            self.__temporary_registers.append(MipsValue.MipsRegister[f'T{temp_reg_index}'])

        for saved_reg_index in range(0, 8):
            self.__saved_registers.append(MipsValue.MipsRegister[f'S{saved_reg_index}'])

    def get_temporary_registers(self):
        """
        Returns the temporary registers in this pool
        """
        return self.__temporary_registers

    def get_saved_registers(self):
        """
        Returns the saved registers in this pool
        """
        return self.__saved_registers


class Descriptors:
    """
    Holds the two types of descriptor
    """

    def __init__(self):
        """
        allocated_registers: registers from LLVM that were allocated and thus contain values that must be preserved
        by spilling into memory once the register descriptor
        """
        self.__allocated_registers = list()
        self.__reg_descriptor = dict()
        self.__address_descriptor = dict()

    def is_empty(self, mips_register: MipsValue.MipsRegister):
        """
        Returns true if the given mips register is currently being used by any of the llvm registers
        """
        return self.get_assigned_register(mips_register) is None

    def get_assigned_register(self, mips_register: MipsValue.MipsRegister):
        """
        Returns the register that is currently assigned to a the given mips register if possible
        """
        for assigned_llvm_reg, current_mips_reg in self.__reg_descriptor.items():

            if current_mips_reg == mips_register:
                return assigned_llvm_reg

        return None

    def assign_to_mips_reg(self, llvm_register: LLVMValue.LLVMRegister, mips_register: MipsValue.MipsRegister):
        """
        Assigns an LLVM Register from the original LLVM Code to a mips register so that the current value of this
        llvm register can be found in a mips register (reg descriptor).
        """
        assert isinstance(llvm_register, LLVMValue.LLVMRegister)
        assert isinstance(mips_register, MipsValue.MipsRegister)

        # Mips registers can only be assigned to one llvm register at a time
        assigned_register = self.get_assigned_register(mips_register)
        if assigned_register is not None:
            self.__reg_descriptor[assigned_register] = None

        self.__reg_descriptor[llvm_register] = mips_register

    def assign_to_address(self, llvm_register: LLVMValue.LLVMRegister, stack_pointer_offset):
        """
        Assign an llvm register to an address with specified offset
        """

        # TODO (very optional) freeing of locations if you don't need them anymore
        # opens the locations for other llvm registers to me stored there
        # Which in turn decreases the rate at which the stack pointer lowers.

        assert not self.has_address_location(llvm_register), "Address can only be assigned once."

        self.__address_descriptor[
            llvm_register] = f'{stack_pointer_offset}({MipsValue.MipsRegister.STACK_POINTER.get_name()})'

    def has_address_location(self, llvm_register: LLVMValue.LLVMRegister):
        """
        Returns whether or not the
        """
        return self.get_address_location(llvm_register) is not None

    def get_address_location(self, llvm_register: LLVMValue.LLVMRegister):
        return self.__address_descriptor.get(llvm_register)

    def has_register_location(self, llvm_register: LLVMValue.LLVMRegister):
        return self.get_register_location(llvm_register) is not None

    def get_register_location(self, llvm_register: LLVMValue.LLVMRegister):
        return self.__reg_descriptor.get(llvm_register)

    def get_current_location(self, llvm_register: LLVMValue.LLVMRegister):
        """
        Returns the current location of an llvm register, either currently in a mips register or in memory
        """
        if llvm_register in self.__reg_descriptor:
            return self.__reg_descriptor[llvm_register]
        else:
            assert llvm_register in self.__address_descriptor
            return self.__address_descriptor[llvm_register]

    def add_allocated_register(self, llvm_register: LLVMValue.LLVMRegister):
        """
        Adds an allocated register from llvm into the list of allocated register
        """
        assert isinstance(llvm_register, LLVMValue.LLVMRegister)
        self.__allocated_registers.append(llvm_register)

    def is_allocated(self, llvm_register: LLVMValue.LLVMRegister):
        """
        Returns whether or not a given llvm register was allocated or not (if this is true, it means that
        the register corresponds to a variable from C, which means that the value needs to be spilled in memory
        as we don't know the liveness and usage information for this allocated register
        (might be used in another basic block)
        """
        return llvm_register in self.__allocated_registers


class MipsFunction:

    def __init__(self, name):
        """
        usage_information: the current usage information of the basic block
        descriptors: contains register and address descriptor
        saved_registers_used: list of saved mips registers ($s) that are used within the current function
        temporary_registers_used: list of temporary mips registers ($t) that are used within the current function
        stack_pointer_offset: the current offset for the stack pointer
        """
        self.name = name
        self.saved_registers_used = list()
        self.temporary_registers_used = list()
        self.usage_information = LLVMUsageInformation.LLVMUsageInformation()
        self.descriptors = Descriptors()
        self.stack_pointer_offset = 0
        self.basic_blocks = list()
        self.add_mips_basic_block(MipsBasicBlock.MipsBasicBlock(self.name))

    def get_name(self):
        return self.name

    def add_mips_basic_block(self, basic_block: MipsBasicBlock.MipsBasicBlock):
        basic_block.name = f'{self.get_name()}_{len(self.basic_blocks)}'
        self.basic_blocks.append(basic_block)

    def refresh_usage_information(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        self.usage_information.refresh(llvm_basic_block)

    def get_current_basic_block(self):
        current_basic_block = self.basic_blocks[-1]
        assert isinstance(current_basic_block, MipsBasicBlock.MipsBasicBlock)
        return current_basic_block

    def add_instruction(self, mips_instruction: MipsInstruction.MipsInstruction):
        self.get_current_basic_block().add_instruction(mips_instruction)


class MipsBuilder:
    """
    Helper to build mips code more easily
    """

    def __init__(self):
        """
        basic_blocks: the basic blocks containing the currently-generated mips code
        """
        self.functions = list()
        self.reg_pool = RegisterPool()

    def get_current_function(self):
        current_function = self.functions[-1]
        assert isinstance(current_function, MipsFunction)
        return current_function

    def get_current_descriptors(self):
        return self.get_current_function().descriptors

    def __get_candidate_register(self, llvm_register: LLVMValue.LLVMRegister):
        """
        Selects a candidate register from the register pool
        """

        # TODO support for t registers being used for allocated registers as well if necessary

    def convert_to_mips_literal(self, llvm_literal: LLVMValue.LLVMLiteral):
        """
        Simply converts the llvm literal instance into an instance of mips literal
        """

        return MipsValue.MipsLiteral(llvm_literal.get_value())

    def get_mips_values(self, instruction: LLVMInstruction.LLVMBinaryAssignInstruction):
        """
        Retrieves:
        - Mips registers for the result and operands of the given instruction, spilling old values into memory if
        necessary
        - Mips literal(s) for operands if the operand(s) in the given instruction also holds literal(s)
        """

        # The llvm registers in the instruction to get the corresponding mips registers from
        # List of tuples <llvmregister, operand-bool>, the operand bool indicating whether or
        # not the register is for a result or for operand. As the algorithm differs a little bit
        llvm_values = list()

        llvm_values.append((instruction.get_resulting_register(), False))
        llvm_values.append((instruction.operand1, True))
        llvm_values.append((instruction.operand2, True))

        # List of mips registers or mips literals returned from the instruction
        results = list()

        for pair in llvm_values:

            if isinstance(pair[0], LLVMValue.LLVMLiteral):
                results.append(self.convert_to_mips_literal(pair[0]))

            # Its not a literal, so it must be a register, continue with the algorithm
            llvm_register = pair[0]

            # Bool indicating whether its a register for operand or not
            operand = pair[0]

            assert isinstance(llvm_register, LLVMValue.LLVMRegister)

            if self.get_current_function().descriptors.has_register_location(llvm_register):
                return self.get_current_function().descriptors.get_register_location(llvm_register)

            mips_registers_to_choose_from = self.reg_pool.get_saved_registers() if \
                self.get_current_function().descriptors.is_allocated(
                    llvm_register) else self.reg_pool.get_temporary_registers()

            # Not operand means register for result, we first check if the
            # result llvm register is already assigned to a mips register, because we can easily return this one
            # (always a safe option)
            if not operand:
                for mips_register in mips_registers_to_choose_from:
                    if self.get_current_descriptors().get_assigned_register(mips_register) == llvm_register:
                        results.append(mips_register)
                        continue

            # First choose from the mips registers that are empty
            for mips_register in mips_registers_to_choose_from:
                if self.get_current_descriptors().is_empty(mips_register):
                    results.append(mips_register)
                    continue

                assigned_llvm_register = self.get_current_descriptors().get_assigned_register(mips_register)

                # TODO check x not element of y or z
                # If the only variable whose descriptor says their value is in r is x
                # and x not y or z, then return r. (We will overwrite it anyways!)
                if assigned_llvm_register == llvm_register:
                    results.append(mips_register)
                    continue

                if not self.get_current_function().usage_information.get_instruction_information(
                        instruction).get_register_information(assigned_llvm_register).is_live():
                    results.append(mips_register)
                    continue

            # Filter the mips registers to choose from to make sure you won't spill already
            # chosen mips registers for the same instruction
            filtered_mips_registers_to_choose_from = \
                [mips_register for mips_register in mips_registers_to_choose_from if not mips_register in results]

            for mips_register in filtered_mips_registers_to_choose_from:
                # Spill the variable for which the mips register is currently assigned into memory first
                self.spill_into_memory(self.get_current_descriptors().get_assigned_register(mips_register))

                # Now the mips register can be used
                results.append(mips_register)
                continue

        assert len(results) == len(llvm_values)

        # Update the descriptors as there are mips registers assigned to different llvm registers now
        for i in range(0, len(results)):

            if isinstance(llvm_values[i][0], LLVMValue.LLVMLiteral):
                break

            llvm_register = llvm_values[i][0]
            mips_register = results[i]

            assert isinstance(mips_register, MipsValue.MipsRegister)

            assigned_llvm_register = self.get_current_descriptors().get_assigned_register(mips_register)

            # We only need to update information if it has to be updated
            if llvm_register is not assigned_llvm_register:
                self.get_current_descriptors().assign_to_mips_reg(llvm_register, mips_register)

        return results

    def spill_into_memory(self, llvm_reg: LLVMValue.LLVMRegister):
        """
        Stores the given llvm register into memory, generating instructions and updating the descriptors in the process
        """

    def store_saved_registers(self):
        """
        Generate the instructions to store the saved temporary instructions into memory.
        Should be executed whenever the program enters a function (the callees' responsibility)
        """

    def load_saved_registers(self):
        pass

    def store_temporary_registers(self):
        """
        Generate the instructions to store the temporary instructions into memory
        Should be executed before the program enters a function (the callers' responsibility)
        """

    def load_temporary_registers(self):
        """

        """
