import src.llvm.visitors.LLVMBaseVisitor as LLVMBaseVisitor
import src.mips.MipsValue as MipsValue
import src.llvm.LLVMValue as LLVMValue
import src.mips.MipsBuilder as MipsBuilder
import src.mips.LLVMFillUsageTableVisitor as FillUsageTableVisitor
from src.llvm import LLVMFunction as LLVMFunction, LLVMCode as LLVMCode, LLVMBasicBlock as LLVMBasicBlock, \
    LLVMInstruction as LLVMInstruction, LLVMGlobalContainer as LLVMGlobalContainer
import src.mips.MipsInstruction as MipsInstruction
import src.ast.ASTTokens as ASTTokens
import src.DataType as DataType
import re


class LLVMToMipsVisitor(LLVMBaseVisitor.LLVMBaseVisitor):
    """
    Visitor which will generate MIPS code from LLVM IR
    """

    def __init__(self):
        """
        Symbol table holds for each basic block the liveness and usage information for each instruction within this
        basic block as well as some other useful information
        mips_builder: the builder used to generate mips code
        basic_block_mapper: maps LLVMBasicBlocks to their corresponding MipsBasicBocks
        """
        self.mips_builder = None
        self.basic_block_mapper = dict()

    def update_basic_block_references(self):
        """
        Updates the mips branch instructions to branch to a mips basic block label instead of the llvm basic block label
        This is used if the mips basic block to branch to was not yet created at the time the branch instruction was created

        Pre-condition: all code must be converted into mips code, so that the references can be updated properly
        """

        for function in self.get_mips_builder().functions:
            for basic_block in function.basic_blocks:
                for instruction in basic_block.instructions:
                    if isinstance(instruction, MipsInstruction.BranchInstruction):
                        if isinstance(instruction.label, LLVMBasicBlock.LLVMBasicBlock):
                            instruction.label = self.basic_block_mapper[instruction.label]

                    elif isinstance(instruction,
                                    MipsInstruction.UnconditionalJumpInstruction):
                        if isinstance(instruction.to_jump_to, LLVMBasicBlock.LLVMBasicBlock):
                            instruction.to_jump_to = self.basic_block_mapper[instruction.to_jump_to]

    def get_mips_builder(self):
        assert isinstance(self.mips_builder, MipsBuilder.MipsBuilder)
        return self.mips_builder

    def create_entry_basic_blocks(self, main_function: MipsBuilder.MipsFunction):

        entry_function = MipsBuilder.MipsFunction('entry',
                                                  nr_params=0, nr_return_values=0)

        entry_function.add_mips_basic_block()
        entry_function.get_current_basic_block().add_instruction(
            MipsInstruction.JumpAndLinkInstruction(main_function.get_entry_basic_block())
        )

        entry_function.add_mips_basic_block()
        entry_function.get_current_basic_block().add_instruction(
            MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.V0, MipsValue.MipsLiteral(10))
        )
        entry_function.get_current_basic_block().add_instruction(
            MipsInstruction.SyscallInstruction()
        )

        self.get_mips_builder().functions.insert(0, entry_function)

    def visit_llvm_code(self, llvm_code: LLVMCode.LLVMCode):

        self.mips_builder = MipsBuilder.MipsBuilder()
        super().visit_llvm_code(llvm_code)
        self.update_basic_block_references()

    def visit_llvm_global_container(self, llvm_global_container: LLVMGlobalContainer.LLVMGlobalContainer):
        super().visit_llvm_global_container(llvm_global_container)

        call_f_strings = llvm_global_container.global_strings
        data_segment = self.get_mips_builder().get_data_segment()

        for call_f_key, call_f_string in call_f_strings.items():
            pattern = "c\"(.*)"
            pattern += "\\\\"
            type_string = re.search(pattern, call_f_string).group(1)
            list_of_substrings = re.split('%[dcsf]', type_string)
            list_of_type_strings = list()
            for i in range(0, len(list_of_substrings)):
                list_of_type_strings.append(list_of_substrings[i])
                if i != len(list_of_substrings) - 1:
                    list_of_type_strings.append('%')
            data_segment.add_call_f_string(call_f_key, list_of_type_strings)

    def visit_llvm_defined_function(self, llvm_defined_function: LLVMFunction.LLVMDefinedFunction):

        mips_function = MipsBuilder.MipsFunction(llvm_defined_function.get_identifier(),
                                                 nr_params=len(llvm_defined_function.params), nr_return_values=1)

        for alloca_instruction in llvm_defined_function.get_alloca_instructions():
            assert isinstance(alloca_instruction, LLVMInstruction.LLVMAllocaInstruction)
            mips_function.descriptors.add_allocated_register(alloca_instruction.get_resulting_register())
            mips_function.descriptors.assign_address_location_to_llvm_reg(alloca_instruction.get_resulting_register(),
                                                                          mips_function.get_new_fp_offset(
                                                                              initial_instructions=False))

        self.get_mips_builder().add_function(mips_function)

        # We need to update the descriptors to point the argument llvm registers to their respective $a
        # mips registers or memory locations (if more than 4 registers are specified)

        # These are the parameters that were saved in the $a registers
        # Simply assign the llvm registers from this function to their corresponding mips reg ($a registers)
        for i in range(0, min(3, len(llvm_defined_function.params))):
            llvm_reg = llvm_defined_function.params[i]
            mips_reg = MipsValue.MipsRegister.get_arg_registers()[i]

            self.get_mips_builder().get_current_descriptors().assign_to_mips_reg(llvm_reg, mips_reg)

        if len(llvm_defined_function.params) > 4:
            # These llvm registers are stored in memory, so assign them to a memory location
            # The offset will be 'above' the frame pointer of the function,
            # as the variables are stored outside of this function body

            # e.g. we have 6 params, so 2 params are stored in memory. The first argument is stored at the highest
            # fp offset (8), the second one at offset (4).
            # After that the frame pointer reaches zero and the function body scope begins
            for stored_llvm_reg in llvm_defined_function.params[4:]:
                self.get_mips_builder().get_current_descriptors() \
                    .assign_address_location_to_llvm_reg(stored_llvm_reg,
                                                         self.get_mips_builder().get_current_function() \
                                                         .get_new_fp_offset(initial_instructions=False))

        # Continue visiting the other instructions / basic blocks
        super().visit_llvm_defined_function(llvm_defined_function)

        # We need to do this after the visitor has been through all instructions, in order to know which
        # Registers needs to be saved
        # We need to save the used registers from within the function definition to make sure that the
        # Registers can be restored after the function is done.
        self.get_mips_builder().add_function_body_initial_instructions()

        # Load the saved registers after executing instructions. This just adds the final basic block to the function
        self.get_mips_builder().add_function_body_ending_instructions()
        self.get_mips_builder().get_current_function().update_fp_offset_values()

        self.get_mips_builder().get_current_function().replace_return_instruction_point_with_actual_instructions(
            self.get_mips_builder().get_current_function().get_current_basic_block())

        if llvm_defined_function.get_identifier() == 'main':
            self.create_entry_basic_blocks(mips_function)

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        mips_basic_block = self.get_mips_builder().get_current_function().add_mips_basic_block()
        self.basic_block_mapper[llvm_basic_block] = mips_basic_block

        usage_table_visitor = FillUsageTableVisitor.LLVMFillUsageTableVisitor()
        llvm_basic_block.accept(usage_table_visitor)
        self.get_mips_builder().get_current_function().usage_information = usage_table_visitor.usage_table

        super().visit_llvm_basic_block(llvm_basic_block)

    def visit_llvm_load_instruction(self, instruction: LLVMInstruction.LLVMLoadInstruction):

        resulting_reg, operand = self.get_mips_builder().get_mips_values(instruction,
                                                                         instruction.get_resulting_register(),
                                                                         [instruction.load_from_reg])

        operand = operand[0]

        self.get_mips_builder().get_current_function().add_instruction(
            MipsInstruction.LoadWordInstruction(register_to_load_into=resulting_reg, register_address=operand, offset=0)
        )

        super().visit_llvm_load_instruction(instruction)



    def visit_llvm_store_instruction(self, instruction: LLVMInstruction.LLVMStoreInstruction):

        # First convert the literal into a register as we cannot store it otherwise
        address_reg, value_to_store_mips_reg = self.get_mips_builder().get_mips_values(instruction,
                                                                                       instruction.resulting_reg,
                                                                                       [instruction.value_to_store],
                                                                                       all_registers=True,
                                                                                       auto_assign_result_reg_in_descriptor=False)

        # First load the address in the mips register if it isn't already
        if not self.get_mips_builder().get_current_descriptors().loaded_in_mips_reg(instruction.resulting_reg,
                                                                                    address_reg):
            address_location = self.get_mips_builder().get_current_descriptors().get_address_location(
                instruction.resulting_reg)

            assert address_location is not None, "Should either be in a register or have a location"

            self.get_mips_builder().get_current_function().add_instruction(
                MipsInstruction.LoadAddressWithOffsetInstruction(register_to_load=address_reg,
                                                                 register_address=MipsValue.MipsRegister.FRAME_POINTER,
                                                                 fp_offset=address_location)
            )

            self.get_mips_builder().get_current_descriptors().assign_to_mips_reg(instruction.resulting_reg, address_reg)

        value_to_store_mips_reg = value_to_store_mips_reg[0]

        self.get_mips_builder().get_current_function().add_instruction(
            MipsInstruction.StoreWordInstruction(register_to_store=value_to_store_mips_reg,
                                                 register_address=address_reg,
                                                 offset=0))

    def visit_llvm_conditional_branch_instruction(self, instruction: LLVMInstruction.LLVMConditionalBranchInstruction):
        super().visit_llvm_conditional_branch_instruction(instruction)

        # TODO Extend get_mips_values for LLVMConditionalBranchInstruction
        mips_values = self.get_mips_builder().get_mips_values(instruction, None, [instruction.condition_reg])
        mips_conditional_register = mips_values[1][0]

        mips_instruction_bne = MipsInstruction.BranchNotEqualInstruction(mips_conditional_register,
                                                                         MipsValue.MipsRegister.ZERO,
                                                                         instruction.if_true)
        mips_instruction_beq = MipsInstruction.BranchEqualInstruction(mips_conditional_register,
                                                                      MipsValue.MipsRegister.ZERO, instruction.if_false)

        # Creation of mips instructions is done, now adding the instructions to the current function
        self.get_mips_builder().get_current_function().add_instruction(mips_instruction_bne)

        # Previous basic block has ended; Create a new one to add the next branch instruction
        # (not really necessary, but for consistency of the concept 'basic blocks')

        self.get_mips_builder().get_current_function().add_mips_basic_block()
        self.get_mips_builder().get_current_function().add_instruction(mips_instruction_beq)

    def visit_llvm_unconditional_branch_instruction(self,
                                                    instruction: LLVMInstruction.LLVMUnconditionalBranchInstruction):
        super().visit_llvm_unconditional_branch_instruction(instruction)

        mips_instruction = MipsInstruction.JumpInstruction(instruction.destination)

        # Creation of mips instruction is done, now adding the instruction to the current function
        self.get_mips_builder().get_current_function().add_instruction(mips_instruction)

    def visit_llvm_printf_instruction(self, instruction: LLVMInstruction.LLVMPrintfInstruction):
        super().visit_llvm_printf_instruction(instruction)

        string_key = instruction.get_string_to_print()
        data_segment = self.get_mips_builder().get_data_segment()
        printf_elements = data_segment.get_call_f_string(string_key)

        llvm_args = instruction.get_llvm_args()

        all_registers = False
        for llvm_arg in llvm_args:
            if llvm_arg.get_data_type().is_floating_point():
                # Floats can't be used for immediate operations
                # TODO improve so that only the float llvm values will get float mips registers instead of all
                all_registers = True

        mips = self.get_mips_builder().get_mips_values(instruction, None, llvm_args, all_registers=all_registers)
        mips_args = mips[1]

        percent_counter = 0
        for i in range(0, len(printf_elements)):
            string_element = printf_elements[i]
            if not string_element == '%':
                if not i == len(printf_elements) - 1:
                    identifier = data_segment.add_ascii_data(string_element)
                else:
                    identifier = data_segment.add_ascii_data(string_element, True)

                load_syscall_instruction = MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.V0,
                                                                                    MipsValue.MipsLiteral(4))
                set_data_instruction = MipsInstruction.LoadAddressInstruction(MipsValue.MipsRegister.A0, identifier)
            else:
                arg_type = llvm_args[percent_counter].get_data_type().get_token()

                if isinstance(mips_args[percent_counter], MipsValue.MipsRegister):

                    argument_register = MipsValue.MipsRegister.F12 if MipsValue.MipsRegister.is_floating_point_register(
                        mips_args[percent_counter]) else MipsValue.MipsRegister.A0

                    set_data_instruction = MipsInstruction.MoveInstruction(argument_register,
                                                                           mips_args[percent_counter])
                elif isinstance(mips_args[percent_counter], MipsValue.MipsLiteral):
                    set_data_instruction = MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.A0,
                                                                                    mips_args[percent_counter])
                else:
                    raise NotImplementedError

                if arg_type == DataType.DataTypeToken.INT:
                    load_syscall_instruction = MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.V0,
                                                                                        MipsValue.MipsLiteral(1))
                elif arg_type == DataType.DataTypeToken.FLOAT or arg_type == DataType.DataTypeToken.DOUBLE:
                    load_syscall_instruction = MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.V0,
                                                                                        MipsValue.MipsLiteral(2))
                elif arg_type == DataType.DataTypeToken.CHAR:
                    load_syscall_instruction = MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.V0,
                                                                                        MipsValue.MipsLiteral(11))
                else:
                    raise NotImplementedError

                percent_counter += 1

            self.get_mips_builder().get_current_function().add_instruction(set_data_instruction)
            self.get_mips_builder().get_current_function().add_instruction(load_syscall_instruction)
            syscall_instruction = MipsInstruction.SyscallInstruction()
            self.get_mips_builder().get_current_function().add_instruction(syscall_instruction)

    def visit_llvm_scanf_instruction(self, instruction: LLVMInstruction.LLVMScanfInstruction):
        super().visit_llvm_scanf_instruction(instruction)

        string_key = instruction.get_string_to_print()
        data_segment = self.get_mips_builder().get_data_segment()
        scanf_elements = data_segment.get_call_f_string(string_key)

        llvm_args = instruction.get_llvm_args()

        percent_counter = 0
        for i in range(0, len(scanf_elements)):
            string_element = scanf_elements[i]
            if string_element == '%':

                llvm_arg = llvm_args[percent_counter]

                arg_type = llvm_arg.get_data_type().get_token()

                fp_offset = self.get_mips_builder().get_current_descriptors().get_address_location(llvm_arg)

                if arg_type == DataType.DataTypeToken.INT:
                    load_syscall_instruction = MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.V0,
                                                                                        MipsValue.MipsLiteral(5))
                    syscall_instruction = MipsInstruction.SyscallInstruction()
                    store_instruction = MipsInstruction.StoreWordInstruction(
                        register_to_store=MipsValue.MipsRegister.V0,
                        register_address=MipsValue.MipsRegister.FRAME_POINTER,
                        offset=fp_offset)

                elif arg_type == DataType.DataTypeToken.FLOAT or arg_type == DataType.DataTypeToken.DOUBLE:
                    load_syscall_instruction = MipsInstruction.LoadImmediateInstruction(MipsValue.MipsRegister.V0,
                                                                                        MipsValue.MipsLiteral(6))
                    syscall_instruction = MipsInstruction.SyscallInstruction()
                    store_instruction = MipsInstruction.StoreWordInstruction(
                        register_to_store=MipsValue.MipsRegister.F0,
                        register_address=MipsValue.MipsRegister.FRAME_POINTER,
                        offset=fp_offset)

                else:
                    raise NotImplementedError

                self.get_mips_builder().get_current_function().add_instruction(load_syscall_instruction)
                self.get_mips_builder().get_current_function().add_instruction(syscall_instruction)
                self.get_mips_builder().get_current_function().add_instruction(store_instruction)
                percent_counter += 1

    def visit_llvm_compare_instruction(self, instruction: LLVMInstruction.LLVMCompareInstruction):
        super().visit_llvm_compare_instruction(instruction)

        mips_values = self.get_mips_builder().get_mips_values(instruction, instruction.get_resulting_register(),
                                                              [instruction.operand1, instruction.operand2])

        mips_resulting_register = mips_values[0]
        mips_operands = mips_values[1]

        mips_instruction = MipsInstruction.CompareInstruction(mips_resulting_register, mips_operands[0],
                                                              mips_operands[1], instruction.operation)

        self.get_mips_builder().get_current_function().add_instruction(mips_instruction)

    def visit_llvm_binary_arithmetic_instruction(self, instruction: LLVMInstruction.LLVMBinaryArithmeticInstruction):
        super().visit_llvm_binary_arithmetic_instruction(instruction)

        if instruction.get_operation_type() == 'float' or (
                isinstance(instruction.operand1, LLVMValue.LLVMLiteral) and isinstance(instruction.operand2,
                                                                                       LLVMValue.LLVMLiteral)):
            # Mips can't handle multiple literals in arithmetic instruction, so if the instruction has two literal operands,
            # 2 Mips registers will be returned instead of two literals

            # With floating points, this must always be 'all registers' as there is no immediate option for this
            all_registers = True
        else:

            # Either no literal operands or one, mips can handle this
            all_registers = False

        mips_values = self.get_mips_builder().get_mips_values(instruction, instruction.get_resulting_register(),
                                                              [instruction.operand1, instruction.operand2],
                                                              all_registers=all_registers)

        mips_resulting_register = mips_values[0]
        mips_operands = mips_values[1]

        current_function = self.get_mips_builder().get_current_function()

        if instruction.operation == ASTTokens.BinaryArithmeticExprToken.DIV:
            mips_division_instruction = MipsInstruction.ArithmeticBinaryInstruction(mips_operands[0], mips_operands[1],
                                                                                    instruction.operation,
                                                                                    mips_resulting_register)
            mips_mflo_instruction = MipsInstruction.MoveFromLoInstruction(mips_resulting_register)

            current_function.add_instruction(mips_division_instruction)
            current_function.add_instruction(mips_mflo_instruction)
        else:

            if isinstance(mips_operands[0], MipsValue.MipsLiteral):
                assert not isinstance(mips_operands[1], MipsValue.MipsLiteral)
                first_operand = mips_operands[1]
                second_operand = mips_operands[0]
            elif isinstance(mips_operands[1], MipsValue.MipsLiteral):
                assert not isinstance(mips_operands[0], MipsValue.MipsLiteral)
                first_operand = mips_operands[0]
                second_operand = mips_operands[1]
            else:
                # Doesn't really matter here; both are registers
                first_operand = mips_operands[0]
                second_operand = mips_operands[1]

            mips_instruction = MipsInstruction.ArithmeticBinaryInstruction(first_operand, second_operand,
                                                                           instruction.operation,
                                                                           mips_resulting_register)
            current_function.add_instruction(mips_instruction)

    def visit_llvm_call_instruction(self, instruction: LLVMInstruction.LLVMCallInstruction):
        # Callers responsibility: store the registers used that you want to keep after the function call

        # The argument mips registers are used first ($a) to put values in. If this is not enough,
        # The remaining arguments will be stored in memory.
        arg_mips_registers = list()

        # You can only take 4 $a registers, so range is (0, 3) at most
        current_arg_reg_index = 0
        for i in range(0, min(3, len(instruction.args))):

            llvm_arg = instruction.args[i]
            current_mips_reg = MipsValue.MipsRegister.get_arg_registers()[i]

            if isinstance(llvm_arg, LLVMValue.LLVMRegister):

                # Make sure to save the currently assigned register in case its used within the function
                current_assigned_llvm_reg = self.get_mips_builder().get_current_descriptors() \
                    .get_assigned_register_for_mips_reg(current_mips_reg)

                if current_assigned_llvm_reg is not None:
                    self.get_mips_builder().store_in_memory(current_assigned_llvm_reg)

            # Now load the current llvm argument into the argument register for usage
            # We need to generate the correct instructions for loading,
            # but we don't need to update the descriptor to map the llvm argument to the argument mips reg
            # (the argument register is only used in the called function, not from outside)
            self.get_mips_builder().load_in_reg(llvm_value=llvm_arg, store_in_reg=current_mips_reg,
                                                update_reg_descriptor=False)

        if len(instruction.args) > 4:
            # The other arguments need to be stored in memory
            llvm_args_to_be_stored_in_memory = instruction.args[4:]

        else:

            llvm_args_to_be_stored_in_memory = []

        # We need to get the mips args to be stored in memory as all registers,
        # In order to store the arguments into memory
        resulting_mips_reg, mips_args_to_be_stored_in_memory = self.get_mips_builder() \
            .get_mips_values(instruction,
                             instruction.get_resulting_register(),
                             llvm_args_to_be_stored_in_memory,
                             all_registers=True)

        if len(mips_args_to_be_stored_in_memory) > 0:
            # Decrease the top of the stack to make room for the mips arguments stored in memory
            self.get_mips_builder().get_current_function().add_instruction(
                MipsInstruction.ArithmeticBinaryInstruction(first_operand=MipsValue.MipsRegister.STACK_POINTER,
                                                            second_operand=MipsValue.MipsLiteral(
                                                                len(mips_args_to_be_stored_in_memory) * 4),
                                                            token=ASTTokens.BinaryArithmeticExprToken.SUB,
                                                            resulting_register=MipsValue.MipsRegister.STACK_POINTER))

        for mips_arg in mips_args_to_be_stored_in_memory:
            assert isinstance(mips_arg, MipsValue.MipsRegister)

            # storing is a little bit different than in store_in_memory(mips_reg),
            # as the mips registers don't necessarily have an llvm register assigned to it.
            # The offset at which the arguments are stored are thus not saved in a descriptor, but we will be able
            # to retrieve the corresponding arguments in the function body (by convention of args > 4).
            sw_instruction = MipsInstruction \
                .StoreWordInstruction(register_to_store=mips_arg,
                                      register_address=MipsValue.MipsRegister.STACK_POINTER,
                                      offset=self.get_mips_builder().get_current_function().get_new_fp_offset(
                                          initial_instructions=False))

            self.get_mips_builder().get_current_function().add_instruction(sw_instruction)

        self.get_mips_builder().store_temporary_registers()

        self.get_mips_builder().get_current_function().add_instruction(
            MipsInstruction.JumpAndLinkInstruction(
                self.get_mips_builder().get_function_entry_block(instruction.function_to_call.get_identifier()))
        )

        self.get_mips_builder().load_temporary_registers()

        if len(mips_args_to_be_stored_in_memory) > 0:
            # Increase the top of the stack as the arguments stored in memory are no longer of any usage
            # Also increase the current frame pointer offset so that new store instructions
            # will use this new frame pointer offset
            self.get_mips_builder().get_current_function().add_instruction(
                MipsInstruction.ArithmeticBinaryInstruction(first_operand=MipsValue.MipsRegister.STACK_POINTER,
                                                            second_operand=MipsValue.MipsLiteral(
                                                                len(mips_args_to_be_stored_in_memory) * 4),
                                                            token=ASTTokens.BinaryArithmeticExprToken.ADD,
                                                            resulting_register=MipsValue.MipsRegister.STACK_POINTER))

            # Restore the frame pointer back to the state where no arguments were stored, as they are no longer necessary
            self.get_mips_builder().get_current_function().decrease_after_init_fp_offset_index(
                len(mips_args_to_be_stored_in_memory))

        # Put the v0 in the designated mips resulting register
        self.get_mips_builder().get_current_function().add_instruction(
            MipsInstruction.MoveInstruction(register_to_move_in=resulting_mips_reg,
                                            register_to_move_from=MipsValue.MipsRegister.V0)
        )

    def visit_llvm_return_instruction(self, instruction: LLVMInstruction.LLVMReturnInstruction):

        # We assert there is only one or zero return value and this will be placed in v0

        self.get_mips_builder().load_in_reg(instruction.get_return_value(), MipsValue.MipsRegister.V0)
        self.get_mips_builder().get_current_function().add_return_instruction_point()

        super().visit_llvm_return_instruction(instruction)

    def visit_llvm_fpext_instruction(self, instruction: LLVMInstruction.LLVMFpextInstruction):

        resulting_reg, old_reg = self.get_mips_builder().get_mips_values(instruction, instruction.get_resulting_register(), [instruction.old_register])

        old_reg = old_reg[0]

        self.get_mips_builder().get_current_function().add_instruction(MipsInstruction.MoveInstruction(resulting_reg, old_reg))

