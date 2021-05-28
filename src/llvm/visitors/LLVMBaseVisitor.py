import src.interfaces.ILLVMVisitor as ILLVMVisitor
import src.llvm.LLVMCode as LLVMCode
import src.llvm.LLVMFunction as LLVMFunction
import src.llvm.LLVMBasicBlock as LLVMBasicBlock
import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMGlobalContainer as LLVMGlobalContainer
import src.llvm.LLVMFunctionHolder as LLVMFunctionHolder


class LLVMBaseVisitor(ILLVMVisitor.ILLVMVisitor):
    """
    Performs the basic traversal
    """

    def visit_llvm_code(self, llvm_code: LLVMCode.LLVMCode):
        llvm_code.global_container.accept(self)
        llvm_code.function_holder.accept(self)

    def visit_llvm_global_container(self, llvm_global_container: LLVMGlobalContainer.LLVMGlobalContainer):
        super().visit_llvm_global_container(llvm_global_container)

    def visit_llvm_function_holder(self, llvm_function_holder: LLVMFunctionHolder.LLVMFunctionHolder):
        for function in llvm_function_holder.functions.values():
            function.accept(self)

    def visit_llvm_declared_function(self, llvm_function_declaration: LLVMFunction.LLVMDeclaredFunction):
        pass

    def visit_llvm_defined_function(self, llvm_defined_function: LLVMFunction.LLVMDefinedFunction):
        for basic_block in llvm_defined_function.basic_blocks.values():
            basic_block.accept(self)

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        for instruction in llvm_basic_block.instructions:
            instruction.accept(self)

    def visit_llvm_assign_instruction(self, instruction: LLVMInstruction.LLVMAssignInstruction):
        pass

    def visit_llvm_return_instruction(self, instruction: LLVMInstruction.LLVMReturnInstruction):
        pass

    def visit_llvm_raw_assign_instruction(self, instruction: LLVMInstruction.LLVMRawAssignInstruction):
        pass

    def visit_llvm_alloca_instruction(self, instruction: LLVMInstruction.LLVMAllocaInstruction):
        pass

    def visit_llvm_alloca_array_instruction(self, instruction: LLVMInstruction.LLVMAllocaArrayInstruction):
        pass

    def visit_llvm_store_instruction(self, instruction: LLVMInstruction.LLVMStoreInstruction):
        pass

    def visit_llvm_load_instruction(self, instruction: LLVMInstruction.LLVMLoadInstruction):
        pass

    def visit_llvm_conditional_instruction(self, instruction: LLVMInstruction.LLVMConditionalBranchInstruction):
        pass

    def visit_llvm_conditional_branch_instruction(self, instruction: LLVMInstruction.LLVMConditionalBranchInstruction):
        pass

    def visit_llvm_unconditional_branch_instruction(self,
                                                    instruction: LLVMInstruction.LLVMUnconditionalBranchInstruction):
        pass

    def visit_llvm_unary_assign_instruction(self, instruction: LLVMInstruction.LLVMUnaryAssignInstruction):
        pass

    def visit_llvm_binary_assign_instruction(self, instruction: LLVMInstruction.LLVMBinaryAssignInstruction):
        pass

    def visit_llvm_binary_arithmetic_instruction(self, instruction: LLVMInstruction.LLVMBinaryArithmeticInstruction):
        pass

    def visit_llvm_data_type_convert_instruction(self, instruction: LLVMInstruction.LLVMDataTypeConvertInstruction):
        pass

    def visit_llvm_compare_instruction(self, instruction: LLVMInstruction.LLVMCompareInstruction):
        pass

    def visit_llvm_unary_arithmetic_instruction(self, instruction: LLVMInstruction.LLVMUnaryArithmeticInstruction):
        pass

    def visit_llvm_get_elementptr_instruction(self, instruction: LLVMInstruction.LLVMGetElementPtrInstruction):
        pass

    def visit_llvm_printf_instruction(self, instruction: LLVMInstruction.LLVMPrintfInstruction):
        pass

    def visit_llvm_call_instruction(self, instruction: LLVMInstruction.LLVMCallInstruction):
        pass

    def visit_llvm_bitcast_instruction(self, instruction: LLVMInstruction.LLVMBitcastInstruction):
        pass

    def visit_llvm_memcpy_instruction(self, instruction: LLVMInstruction.LLVMMemcpyInstruction):
        pass
