import src.llvm.visitors.LLVMBaseVisitor as LLVMBaseVisitor
import src.mips.MipsValue as MipsValue
import src.llvm.LLVMValue as LLVMValue
import src.mips.MipsBuilder as MipsBuilder
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
        """
        self.mips_builder = None

    def get_mips_builder(self):
        assert isinstance(self.mips_builder, MipsBuilder.MipsBuilder)
        return self.mips_builder

    def visit_llvm_code(self, llvm_code: LLVMCode.LLVMCode):
        self.mips_builder = MipsBuilder.MipsBuilder(llvm_code)

    def visit_llvm_defined_function(self, llvm_defined_function: LLVMFunction.LLVMDefinedFunction):
        mips_function = MipsBuilder.MipsFunction(llvm_defined_function.get_identifier(),
                                                 nr_params=len(llvm_defined_function.params), nr_return_values=1)
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
            current_fp_offset = (len(llvm_defined_function.params) - 4) * 4
            for stored_llvm_reg in llvm_defined_function.params[4:]:
                self.get_mips_builder().get_current_descriptors().assign_address_location_to_llvm_reg(stored_llvm_reg,
                                                                                                      current_fp_offset)
                current_fp_offset -= 4

        # Continue visiting the other instructions / basic blocks
        super().visit_llvm_defined_function(llvm_defined_function)

        # We need to do this after the visitor has been through all instructions, in order to know which
        # Registers needs to be saved
        # We need to save the used registers from within the function definition to make sure that the
        # Registers can be restored after the function is done.
        self.get_mips_builder().add_function_body_initial_instructions()

        # Load the saved registers after executing instructions. This just adds the final basic block to the function
        self.get_mips_builder().add_function_body_ending_instructions()

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        self.get_mips_builder().get_current_function().add_mips_basic_block()
        super().visit_llvm_basic_block(llvm_basic_block)

    def visit_llvm_store_instruction(self, instruction: LLVMInstruction.LLVMStoreInstruction):
        super().visit_llvm_store_instruction(instruction)

        mips_values = self.get_mips_builder().get_mips_values(instruction, instruction.resulting_reg,
                                                              [instruction.value_to_store])
        mips_resulting_register = mips_values[0]
        mips_operands = mips_values[1]

        token = ASTTokens.BinaryArithmeticExprToken.ADD

        mips_instruction = MipsInstruction.ArithmeticBinaryInstruction(MipsValue.MipsRegister.ZERO, mips_operands[0],
                                                                       token, mips_resulting_register)

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
        self.get_mips_builder().get_current_function().add_instruction(mips_instruction_beq)

    def visit_llvm_unconditional_branch_instruction(self,
                                                    instruction: LLVMInstruction.LLVMUnconditionalBranchInstruction):
        super().visit_llvm_unconditional_branch_instruction(instruction)

        mips_instruction = MipsInstruction.JumpInstruction(instruction.destination)

        # Creation of mips instruction is done, now adding the instruction to the current function
        self.get_mips_builder().get_current_function().add_instruction(mips_instruction)

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
                                                              [instruction.operand1, instruction.operand2])

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
            mips_instruction = MipsInstruction.ArithmeticBinaryInstruction(mips_operands[0], mips_operands[1],
                                                                           instruction.operation,
                                                                           mips_resulting_register)
            current_function.add_instruction(mips_instruction)

    def visit_llvm_call_instruction(self, instruction: LLVMInstruction.LLVMCallInstruction):
        # Callers responsibility: store the registers used that you want to keep after the function call
        self.get_mips_builder().store_temporary_registers()

        # The argument mips registers are used first ($a) to put values in. If this is not enough,
        # The remaining arguments will be stored in memory.
        arg_mips_registers = list()

        # You can only take 4 $a registers, so range is (0, 3) at most
        for i in range(0, min(3, len(instruction.args))):

            llvm_arg = instruction.args[i]
            current_mips_reg = MipsValue.MipsRegister.get_arg_registers()

            if isinstance(llvm_arg, LLVMValue.LLVMRegister):
                # Make sure to save the currently assigned register in case its used within the function
                current_assigned_llvm_reg = self.get_mips_builder().get_current_descriptors() \
                    .get_assigned_register_for_mips_reg(current_mips_reg)
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
        mips_result, mips_args_to_be_stored_in_memory = self.get_mips_builder() \
            .get_mips_values(instruction,
                             instruction.get_resulting_register(),
                             llvm_args_to_be_stored_in_memory,
                             all_registers=True)

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
            sw_instruction = MipsInstruction.StoreWordInstruction(register_to_store=mips_arg,
                                                                  register_address=MipsValue.MipsRegister.STACK_POINTER,
                                                                  offset=self.get_mips_builder().get_current_function().get_frame_pointer_offset())

            self.get_mips_builder().get_current_function().frame_pointer_offset -= 4
            self.get_mips_builder().get_current_function().add_instruction(sw_instruction)

        super().visit_llvm_call_instruction(instruction)

        # Increase the top of the stack as the arguments stored in memory are no longer of any usage
        # Also increase the current frame pointer offset so that new store instructions
        # will use this new frame pointer offset
        self.get_mips_builder().get_current_function().add_instruction(
            MipsInstruction.ArithmeticBinaryInstruction(first_operand=MipsValue.MipsRegister.STACK_POINTER,
                                                        second_operand=MipsValue.MipsLiteral(
                                                            len(mips_args_to_be_stored_in_memory) * 4),
                                                        token=ASTTokens.BinaryArithmeticExprToken.ADD,
                                                        resulting_register=MipsValue.MipsRegister.STACK_POINTER))
        self.get_mips_builder().get_current_function().frame_pointer_offset += len(mips_args_to_be_stored_in_memory) * 4

        # Callers responsibility: load the registers used that you want to keep
        self.get_mips_builder().load_temporary_registers()
