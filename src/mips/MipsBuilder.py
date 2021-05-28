import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMValue as LLVMValue
import src.llvm.LLVMCode as LLVMCode
import src.llvm.LLVMFunction as LLVMFunction
import src.ast.ASTTokens as ASTTokens
import src.mips.LLVMFillRefMapperVisitor as LLVMFillRefMapperVisitor
import src.mips.LLVMUsageInformation as LLVMUsageInformation
import src.mips.MipsBasicBlock as MipsBasicBlock
import src.mips.MipsInstruction as MipsInstruction
import src.mips.MipsValue as MipsValue


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
        by spilling into memory once the register descriptor is used for another register
        """
        self.__allocated_registers = list()
        self.__reg_descriptor = dict()
        self.__address_descriptor = dict()

    def is_empty(self, mips_register: MipsValue.MipsRegister):
        """
        Returns true if the given mips register is currently being used by any of the llvm registers
        """
        return self.get_assigned_register_for_mips_reg(mips_register) is None

    def loaded_in_mips_reg(self, llvm_reg: LLVMValue.LLVMRegister, mips_reg: MipsValue.MipsRegister):
        """
        Returns whether or not the given llvm register is currently loaded in the given mips register
        """
        assigned_reg = self.get_assigned_register_for_mips_reg(mips_reg)
        return assigned_reg is llvm_reg

    def get_assigned_register_for_mips_reg(self, mips_register: MipsValue.MipsRegister):
        """
        Returns the register that is currently assigned to a the given mips register if possible
        """
        for assigned_llvm_reg, current_mips_reg in self.__reg_descriptor.items():

            if current_mips_reg == mips_register:
                return assigned_llvm_reg

        return None

    def get_assigned_register_for_address_location(self, address_location: int):
        for assigned_llvm_reg, current_address_location in self.__address_descriptor.items():

            if current_address_location == address_location:
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
        assigned_register = self.get_assigned_register_for_mips_reg(mips_register)
        if assigned_register is not None:
            self.__reg_descriptor[assigned_register] = None

        self.__reg_descriptor[llvm_register] = mips_register

    def assign_address_location_to_llvm_reg(self, llvm_register: LLVMValue.LLVMRegister, stack_pointer_offset):
        """
        Assign an llvm register to an address with specified offset
        """

        # TODO (very optional) freeing of locations if you don't need them anymore
        # opens the locations for other llvm registers to me stored there
        # Which in turn decreases the rate at which the stack pointer lowers.

        assert not self.has_address_location(llvm_register), "Address can only be assigned once."
        assert self.get_assigned_register_for_address_location(
            stack_pointer_offset) is not None, "This address location already belongs to another register"

        self.__address_descriptor[
            llvm_register] = stack_pointer_offset

    def has_address_location(self, llvm_register: LLVMValue.LLVMRegister):
        """
        Returns whether or not the
        """
        return self.get_address_location(llvm_register) is not None

    def get_address_location(self, llvm_register: LLVMValue.LLVMRegister):
        """
        The address location is an offset specifying from where to load the value of the llvm register
        """
        return self.__address_descriptor.get(llvm_register)

    def has_register_location(self, llvm_register: LLVMValue.LLVMRegister):
        return self.get_mips_reg_for_llvm_reg(llvm_register) is not None

    def get_mips_reg_for_llvm_reg(self, llvm_register: LLVMValue.LLVMRegister):
        """
        Returns the mips register that currently holds the value of the given llvm register if there is such a mips register
        Otherwise, returns None
        """
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

    def __init__(self, name, nr_params: int, nr_return_values: int):
        """
        usage_information: the current usage information of the basic block
        descriptors: contains register and address descriptor
        saved_registers_used: list of saved mips registers ($s) that are used within the current function
        temporary_registers_used: list of temporary mips registers ($t) that are used within the current function
        stack_pointer_offset: the current offset for the stack pointer
        """
        self.name = name
        self.saved_registers_used = set()
        self.temporary_registers_used = set()
        self.usage_information = LLVMUsageInformation.LLVMUsageInformation()
        self.descriptors = Descriptors()
        self.__frame_pointer_offset = 0
        self.basic_blocks = list()
        self.add_mips_basic_block()
        self.nr_params = nr_params
        self.nr_return_values = nr_return_values

    def get_name(self):
        return self.name

    def get_entry_basic_block(self):
        return self.basic_blocks[0]

    def add_mips_basic_block(self):
        """
        Adds a basic block to the current function. Initially empty.

        No argument as basic block required for mips in comparison to llvm, because the conversion from llvm
        to mips is always top-down (this wasn't the case with asts to llvm)
        """

        self.basic_blocks.append(MipsBasicBlock.MipsBasicBlock(f'{self.get_name()}_{len(self.basic_blocks)}'))

    def get_frame_pointer_offset(self):
        return self.__frame_pointer_offset

    def increase_fp_offset_by_four(self):
        """
        Increases the stack pointer offset by one word (4) as mips is byte addressed
        """
        self.__frame_pointer_offset += 4

    def refresh_usage_information(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        # TODO implement this
        raise NotImplementedError('Refresh usage information not yet working')

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

    def __init__(self, llvm_code: LLVMCode.LLVMCode):
        """
        functions: the functions containing the currently-generated mips code
        reg_pool: contains the available mips registers for usage (temporary and saved temporary),
        but is used for more easy retrieval instead of using the enum directly.
        ref_mapper: maps loaded llvm registers to their corresponding 'allocated' registers from which they were loaded.
        This is because we don't need the load instruction from mips anymore,
        and can just 'assign' new values to the allocated reg
        """
        self.functions = list()
        self.reg_pool = RegisterPool()

        # Look in the docs of LLVMFillRefMapper to see why its necessary
        ref_mapper_visitor = LLVMFillRefMapperVisitor.LLVMFillRefMapperVisitor()
        llvm_code.accept(ref_mapper_visitor)
        self.ref_mapper = ref_mapper_visitor.ref_mapper

    def add_function(self, mips_function: MipsFunction):
        """
        Adds a mips function to the builder which makes the added function the current one (to add instructions to)
        mips_function: the mips function to add
        """
        self.functions.append(mips_function)

    def get_current_function(self):
        current_function = self.functions[-1]
        assert isinstance(current_function, MipsFunction)
        return current_function

    def get_current_descriptors(self):
        """
        Returns the current descriptors of the current function
        """
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

    def get_mips_registers(self, amount: int, saved_temporary_preference: bool):
        """
        Retrieves a mips value that can be used to put other values in, spilling the old values into memory if
        necessary

        amount: the amount of mips registers to retrieve
        saved_temporary_preference: whether or not to give preference to the save temporary registers or not
        (only if this is not a valid option, look in the temporary registers)
        """

        mips_registers_to_choose_from = self.reg_pool.get_saved_registers() if saved_temporary_preference else \
            self.reg_pool.get_temporary_registers()

        chosen_mips_regs = []

        for mips_reg in mips_registers_to_choose_from:

            if mips_reg in chosen_mips_regs:
                continue

            # If we have chosen the requested amount, stop here (and return the mips registers)
            if len(chosen_mips_regs) == amount:
                break

            if self.get_current_descriptors().is_empty(mips_reg):
                chosen_mips_regs.append(mips_reg)

        if len(chosen_mips_regs) == amount:
            return chosen_mips_regs

        # Filter out already chosen mips registers to get the last ones
        mips_registers_to_choose_from = [mips_reg for mips_reg in mips_registers_to_choose_from if
                                         not mips_reg in chosen_mips_regs]

        # We know the registers are not empty otherwise
        for mips_reg in mips_registers_to_choose_from:
            if mips_reg in chosen_mips_regs:
                continue

            if len(chosen_mips_regs) == amount:
                break

            self.store_in_memory(mips_reg)

        assert len(
            chosen_mips_regs) == amount, "The requested amount of mips registers " \
                                         "cannot be given at once: too many registers asked"

        return chosen_mips_regs

    def get_mips_values(self, llvm_instruction: LLVMInstruction.LLVMInstruction,
                        resulting_reg: LLVMValue.LLVMRegister or None,
                        operands: list, all_registers=False):
        """

        Returns the corresponding mips registers and values from the given instruction with resulting register
        and operands. Also spills the old values that were mapped onto these registers into memory if necessary

        resulting_reg: llvm_register used to put the result of an expression in
        operands: list operands used for the operation. Either LLVMValue or LLVMRegister

        Returns tuple of <mips_result, mips_operands>
        Mips result: an instance of the MipsRegister class
        Mips operands: list of instances of MipsValue, either MipsRegisters or MipsLiterals
        """

        # The llvm registers in the instruction to get the corresponding mips registers from
        # List of tuples <llvmregister, operand-bool>, the operand bool indicating whether or
        # not the register is for a result or for operand. As the algorithm differs a little bit
        llvm_values = list()

        if resulting_reg is not None:
            llvm_values.append((resulting_reg, False))

        for operand in operands:
            assert isinstance(operand, LLVMValue.LLVMValue)
            llvm_values.append((operand, True))

        # Everywhere were a 'loaded llvm register' is used, map it to the corresponding 'allocated llvm register'
        # As the load instruction from llvm is not necessary anymore
        for i in range(0, len(llvm_values)):

            llvm_value = llvm_values[i]
            if isinstance(llvm_value, LLVMValue.LLVMRegister):
                if llvm_value in self.ref_mapper:
                    llvm_values[i] = self.ref_mapper[llvm_value]

        # List of mips registers or mips literals returned from the instruction
        results = list()

        for pair in llvm_values:

            if isinstance(pair[0], LLVMValue.LLVMLiteral) and not all_registers:
                results.append(self.convert_to_mips_literal(pair[0]))

            # Its not a literal, so it must be a register, continue with the algorithm
            llvm_value = pair[0]

            # Bool indicating whether its a register for operand or not
            operand = pair[0]

            assert isinstance(llvm_value, LLVMValue.LLVMRegister)

            # TODO Use reference mapper to map the llvm register to its allocated llvm register to get rid of
            # The load and store operations from llvm (not required anymore)

            if self.get_current_function().descriptors.has_register_location(llvm_value):
                return self.get_current_function().descriptors.get_mips_reg_for_llvm_reg(llvm_value)

            # Either choose from the s registers or the t registers as preference, depending on whether or not
            # an allocated llvm register is used (corresponding to variables) or not (temporary values that were calculated)
            # TODO implement 'as preference' meaning that t registers may be used for allocated llvm registers as well
            # if necessary and vice versa, but make sure that the saving into memory is done properly in function calls
            mips_registers_to_choose_from = self.reg_pool.get_saved_registers() if \
                isinstance(llvm_value,
                           LLVMValue.LLVMRegister) and self.get_current_function().descriptors.is_allocated(
                    llvm_value) else self.reg_pool.get_temporary_registers()

            # Not operand means register for result, we first check if the
            # result llvm register is already assigned to a mips register, because we can easily return this one
            # (always a safe option)
            if not operand:
                for mips_reg in mips_registers_to_choose_from:
                    if self.get_current_descriptors().get_assigned_register_for_mips_reg(mips_reg) == llvm_value:
                        results.append(mips_reg)
                        continue

            # First choose from the mips registers that are empty
            for mips_reg in mips_registers_to_choose_from:
                if self.get_current_descriptors().is_empty(mips_reg):
                    results.append(mips_reg)
                    continue

                assigned_llvm_reg = self.get_current_descriptors().get_assigned_register_for_mips_reg(mips_reg)

                # TODO check x not element of y or z
                # If the only variable whose descriptor says their value is in r is x
                # and x not y or z, then return r. (We will overwrite it anyways!)
                if assigned_llvm_reg == llvm_value:
                    results.append(mips_reg)
                    continue

                if not self.get_current_function().usage_information.get_instruction_information(
                        llvm_instruction).get_register_information(assigned_llvm_reg).is_live():
                    results.append(mips_reg)
                    # TODO remove all assignments made in the descriptors as the assigned llvm register will
                    # not be used anymore
                    continue

            # Filter the mips registers to choose from to make sure you won't spill already
            # chosen mips registers for the same instruction
            filtered_mips_registers_to_choose_from = \
                [mips_register for mips_register in mips_registers_to_choose_from if not mips_register in results]

            for mips_reg in filtered_mips_registers_to_choose_from:
                # Spill the variable for which the mips register is currently assigned into memory first
                self.store_in_memory(mips_reg)

                # Now the mips register can be used
                results.append(mips_reg)
                continue

        assert len(results) == len(llvm_values)

        # Load the given llvm values into mips registers and updates the descriptors if necessary
        for i in range(0, len(results)):

            llvm_value = llvm_values[i][0]
            mips_reg = results[i]

            # No need to update the descriptors as literals will never be re-used afterwards
            # But we need to load the value into the corresponding mips mips register
            if isinstance(llvm_value, LLVMValue.LLVMLiteral):
                self.load_in_reg(llvm_value, store_in_reg=mips_reg)

            # Update the descriptors as there are mips registers assigned to different llvm registers now
            elif isinstance(llvm_value, LLVMValue.LLVMRegister):

                assert isinstance(mips_reg, MipsValue.MipsRegister)

                # We only need to update information if it has to be updated
                if self.get_current_descriptors().loaded_in_mips_reg(llvm_value, mips_reg):
                    self.load_in_reg(llvm_value, store_in_reg=mips_reg)

                # TODO Add these registers to saved registers used and temporary registers used
                # if mips_reg.name.startswith('t'):
                # elif mips_reg.name.startswith('s'):

            else:

                raise NotImplementedError('Not supported!')

        # Return tuple of <mips_result, mips_operands>
        return results[0], results[1:]

    def load_in_reg(self, llvm_value: LLVMValue.LLVMValue, store_in_reg: MipsValue.MipsRegister):

        # TODO what happens when the register to be assigned neither in a mips register or address?
        """
        Generates the instructions to load the given value (literal/register) in a designated mips register,
        from memory if this is necessary, else uses assignment instructions.
        Also updates the register descriptor properly if necessary.
        """
        assert isinstance(store_in_reg, MipsValue.MipsRegister)

        if isinstance(llvm_value, LLVMValue.LLVMRegister):

            # Mips register which currently holds the value of the llvm register
            current_mips_reg = self.get_current_descriptors().get_mips_reg_for_llvm_reg(llvm_value)

            if current_mips_reg is None:
                offset = self.get_current_descriptors().get_address_location(llvm_value)
                assert offset is not None

                instruction = MipsInstruction.LoadWordInstruction(register_to_load_into=store_in_reg,
                                                                  register_address=MipsValue.MipsRegister.STACK_POINTER,
                                                                  offset=offset)
            else:

                instruction = MipsInstruction.ArithmeticBinaryInstruction(first_operand=MipsValue.MipsRegister.ZERO,
                                                                          second_operand=current_mips_reg,
                                                                          token=ASTTokens.BinaryArithmeticExprToken.ADD,
                                                                          resulting_register=store_in_reg)

        elif isinstance(llvm_value, LLVMValue.LLVMLiteral):

            mips_literal = self.convert_to_mips_literal(llvm_value)
            instruction = MipsInstruction.ArithmeticBinaryInstruction(first_operand=MipsValue.MipsRegister.ZERO,
                                                                      second_operand=mips_literal,
                                                                      token=ASTTokens.BinaryArithmeticExprToken.ADD,
                                                                      resulting_register=store_in_reg)
        else:

            raise NotImplementedError('Should either be literal or register')

        self.get_current_function().add_instruction(instruction)
        self.get_current_descriptors().assign_to_mips_reg(llvm_value, store_in_reg)

    def store_in_memory(self, mips_register: MipsValue.MipsRegister):
        """
        'Spills' the given mips register into memory, generating instructions and
        updating the descriptors in the process.

        PRE-PROCESSING STEP: in order to store the given mips register in memory, it must have a current llvm register
        assigned to it (otherwise the offset will be lost at which the value was stored).
        """

        assigned_llvm_reg = self.get_current_descriptors().get_assigned_register_for_mips_reg(mips_register)
        assert assigned_llvm_reg is not None, "Mips register must have a current llvm register mapped to it"

        offset = self.get_current_descriptors().get_address_location(assigned_llvm_reg)

        # Assign a new address location to the llvm register with current offset and increase it afterwards
        if offset is None:
            self.get_current_descriptors() \
                .assign_address_location_to_llvm_reg(assigned_llvm_reg,
                                                     self.get_current_function().get_frame_pointer_offset())
            self.get_current_function().increase_fp_offset_by_four()
            offset = self.get_current_descriptors().get_address_location(assigned_llvm_reg)

        sw_instruction = MipsInstruction.StoreWordInstruction(register_to_store=mips_register,
                                                              register_address=MipsValue.MipsRegister.STACK_POINTER,
                                                              offset=offset)
        self.get_current_function().add_instruction(sw_instruction)

    def add_function_body_initial_instructions(self):
        """

        Applied to the current function in the mips builder:

        Generate the instructions that a function body must contain at the beginning, such as Saving
        saved temporary registers, loading the arguments in registers,... everything to do with the stack frame
        """

        entry_basic_block = MipsBasicBlock.MipsBasicBlock(f'{self.get_current_function().get_name()}_entry')

        # Store the old frame pointer in the stack pointer
        entry_basic_block.add_instruction(
            MipsInstruction.StoreWordInstruction(register_to_store=MipsValue.MipsRegister.FRAME_POINTER,
                                                 register_address=MipsValue.MipsRegister.STACK_POINTER,
                                                 offset=0))

        # The frame pointer now points to the top of the stack
        entry_basic_block.add_instruction(
            MipsInstruction.MoveInstruction(register_to_move_in=MipsValue.MipsRegister.FRAME_POINTER,
                                            register_to_move_from=MipsValue.MipsRegister.STACK_POINTER))

        # Decrease the stack pointer by the maximum fp offset acquired in the function
        # (this space will be used by the function body to store its mips registers)
        entry_basic_block.add_instruction(
            MipsInstruction.ArithmeticBinaryInstruction(first_operand=MipsValue.MipsRegister.STACK_POINTER,
                                                        second_operand=MipsValue.MipsLiteral(
                                                            self.get_current_function().get_frame_pointer_offset()),
                                                        token=ASTTokens.BinaryArithmeticExprToken.SUB,
                                                        resulting_register=MipsValue.MipsRegister.STACK_POINTER))

        current_fp_offset = -4
        # Store the return address on the stack
        entry_basic_block.add_instruction(
            MipsInstruction.StoreWordInstruction(register_to_store=MipsValue.MipsRegister.RETURN_ADDRESS,
                                                 register_address=MipsValue.MipsRegister.FRAME_POINTER,
                                                 offset=current_fp_offset))

        current_fp_offset -= 4
        # Store the saved registers used to restore it later on
        for saved_register in self.get_current_function().saved_registers_used:
            entry_basic_block.add_instruction(MipsInstruction.StoreWordInstruction(register_to_store=saved_register,
                                                                                   register_address=MipsValue.MipsRegister.FRAME_POINTER,
                                                                                   offset=current_fp_offset))
            current_fp_offset -= 4

        # Params that were stored in memory are not loaded here, the descriptors will contain the correct information
        # To retrieve these arguments correctly (and load them in whenever necessary)

        self.get_current_function().basic_blocks.insert(0, entry_basic_block)

    # Now that all registers have been used, we can start loading in the extra arguments if there are any

    def add_function_body_ending_instructions(self):
        """

        Applied to the current function in the mips builder:

        Generate the instructions that a function body must contain at the beginning, such as
        Restoring saved temporary registers, storing return values in registers,... everything to do with the stack frame
        """

        end_basic_block = MipsBasicBlock.MipsBasicBlock(f'{self.get_current_function().get_name()}_end')

        if self.get_current_function().nr_return_values > 1:
            raise NotImplementedError(f'Nr return values greater than 1 not supported yet')

        current_fp_offset = self.get_current_function().get_frame_pointer_offset()

        for saved_reg in self.get_current_function().saved_registers_used:
            end_basic_block.add_instruction(MipsInstruction.LoadWordInstruction(
                register_to_load_into=saved_reg,
                register_address=MipsValue.MipsRegister.FRAME_POINTER,
                offset=current_fp_offset))
            current_fp_offset += 4

        end_basic_block.add_instruction(MipsInstruction.LoadWordInstruction(
            register_to_load_into=MipsValue.MipsRegister.RETURN_ADDRESS,
            register_address=MipsValue.MipsRegister.FRAME_POINTER,
            offset=current_fp_offset
        ))
        current_fp_offset += 4

        # Get old stack pointer from current frame pointer
        end_basic_block.add_instruction(
            MipsInstruction.MoveInstruction(register_to_move_in=MipsValue.MipsRegister.STACK_POINTER,
                                            register_to_move_from=MipsValue.MipsRegister.FRAME_POINTER))

        # Restore the old frame pointer by retrieving it from memory
        end_basic_block.add_instruction(
            MipsInstruction.LoadWordInstruction(register_to_load_into=MipsValue.MipsRegister.FRAME_POINTER,
                                                register_address=MipsValue.MipsRegister.STACK_POINTER,
                                                offset=current_fp_offset))

        self.get_current_function().basic_blocks.append(end_basic_block)

    def store_temporary_registers(self):
        """
        Generate the instructions to store the temporary instructions into memory
        Should be executed before the program enters a function (the callers' responsibility)
        """

    def load_temporary_registers(self):
        """

        """
