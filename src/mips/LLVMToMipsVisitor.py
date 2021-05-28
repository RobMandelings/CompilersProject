import src.llvm.visitors.LLVMBaseVisitor as LLVMBaseVisitor
import src.mips.MipsValue as MipsValue
import src.llvm.LLVMValue as LLVMValue
import src.mips.MipsBuilder as MipsBuilder
import src.mips.LLVMFillRefMapperVisitor as LLVMFillRefMapperVisitor
import src.mips.LLVMFillUsageTableVisitor as FillUsageTableVisitor
from src.llvm import LLVMFunction as LLVMFunction, LLVMCode as LLVMCode, LLVMBasicBlock as LLVMBasicBlock, \
    LLVMInstruction as LLVMInstruction
import src.mips.MipsInstruction as MipsInstruction
import src.ast.ASTTokens as ASTTokens


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

    def visit_llvm_code(self, llvm_code: LLVMCode.LLVMCode):
        self.mips_builder = MipsBuilder.MipsBuilder()
        super().visit_llvm_code(llvm_code)
        self.update_basic_block_references()

    def visit_llvm_defined_function(self, llvm_defined_function: LLVMFunction.LLVMDefinedFunction):

        ref_mapper_visitor = LLVMFillRefMapperVisitor.LLVMFillRefMapperVisitor()
        llvm_defined_function.accept(ref_mapper_visitor)
        ref_mapper = ref_mapper_visitor.ref_mapper

        mips_function = MipsBuilder.MipsFunction(llvm_defined_function.get_identifier(),
                                                 nr_params=len(llvm_defined_function.params), nr_return_values=1,
                                                 ref_mapper=ref_mapper)

        for alloca_instruction in llvm_defined_function.get_alloca_instructions():
            assert isinstance(alloca_instruction, LLVMInstruction.LLVMAllocaInstruction)
            mips_function.descriptors.add_allocated_register(alloca_instruction.get_resulting_register())

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

        print('hi')

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        mips_basic_block = self.get_mips_builder().get_current_function().add_mips_basic_block()
        self.basic_block_mapper[llvm_basic_block] = mips_basic_block

        usage_table_visitor = FillUsageTableVisitor.LLVMFillUsageTableVisitor()
        llvm_basic_block.accept(usage_table_visitor)
        self.get_mips_builder().get_current_function().usage_information = usage_table_visitor.usage_table

        super().visit_llvm_basic_block(llvm_basic_block)

    def visit_llvm_store_instruction(self, instruction: LLVMInstruction.LLVMStoreInstruction):

        mips_values = self.get_mips_builder().get_mips_values(instruction, instruction.resulting_reg,
                                                              [instruction.value_to_store])
        mips_resulting_register = mips_values[0]
        mips_operands = mips_values[1]

        token = ASTTokens.BinaryArithmeticExprToken.ADD

        mips_instruction = MipsInstruction.ArithmeticBinaryInstruction(MipsValue.MipsRegister.ZERO, mips_operands[0],
                                                                       token, mips_resulting_register)

        # Don't forget to update the descriptor properly
        self.get_mips_builder().get_current_descriptors().assign_to_mips_reg(instruction.resulting_reg,
                                                                             mips_resulting_register)

        # Creation of mips instruction is done, now adding the instruction to the current function
        self.get_mips_builder().get_current_function().add_instruction(mips_instruction)

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

        mips_values = self.get_mips_builder().get_mips_values(instruction, instruction.get_resulting_register(),
                                                              [instruction.operand1, instruction.operand2],
                                                              all_registers=True)

        mips_resulting_register = mips_values[0]
        mips_operands = mips_values[1]

        current_function = self.get_mips_builder().get_current_function()

        if instruction.operation == ASTTokens.BinaryArithmeticExprToken.DIV:
            mips_division_instruction = MipsInstruction.ArithmeticBinaryInstruction(mips_operands[0], mips_operands[1],
                                                                                    instruction.operation)
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
        for i in range(0, min(3, len(instruction.args))):

            llvm_arg = instruction.args[i]
            current_mips_reg = MipsValue.MipsRegister.get_arg_registers()[i]

            if isinstance(llvm_arg, LLVMValue.LLVMRegister):

                # Map the loaded value to its allocated register if this is the case (loading isn't used the same
                # way in mips
                if llvm_arg in self.get_mips_builder().get_current_ref_mapper():
                    llvm_arg = self.get_mips_builder().get_current_ref_mapper()[llvm_arg]

                # Make sure to save the currently assigned register in case its used within the function
                current_assigned_llvm_reg = self.get_mips_builder().get_current_descriptors() \
                    .get_assigned_register_for_mips_reg(current_mips_reg)

                if current_assigned_llvm_reg is not None:
                    self.get_mips_builder().store_in_memory(current_assigned_llvm_reg)

                # Now load the current llvm argument into the argument register for usage
                self.get_mips_builder().load_in_reg(llvm_value=llvm_arg, store_in_reg=current_mips_reg)

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
