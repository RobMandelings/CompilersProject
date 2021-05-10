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
        for function in llvm_function_holder.functions:
            function.accept(self)

    def visit_llvm_declared_function(self, llvm_function_declaration: LLVMFunction.LLVMDeclaredFunction):
        pass

    def visit_llvm_defined_function(self, llvm_defined_function: LLVMFunction.LLVMDefinedFunction):
        for basic_block in llvm_defined_function.basic_blocks:
            basic_block.accept(self)

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        for instruction in llvm_basic_block.instructions:
            instruction.accept(self)

    def visit_llvm_assign_instruction(self, instruction: LLVMInstruction.AssignInstruction):
        pass

    def visit_llvm_return_instruction(self, instruction: LLVMInstruction.ReturnInstruction):
        pass

    def visit_llvm_raw_assign_instruction(self, instruction: LLVMInstruction.RawAssignInstruction):
        pass

    def visit_llvm_alloca_instruction(self, instruction: LLVMInstruction.AllocaInstruction):
        pass

    def visit_llvm_alloca_array_instruction(self, instruction: LLVMInstruction.AllocaArrayInstruction):
        pass

    def visit_llvm_store_instruction(self, instruction: LLVMInstruction.StoreInstruction):
        pass

    def visit_llvm_load_instruction(self, instruction: LLVMInstruction.LoadInstruction):
        pass

    def visit_llvm_conditional_instruction(self, instruction: LLVMInstruction.ConditionalBranchInstruction):
        pass

    def visit_llvm_conditional_branch_instruction(self, instruction: LLVMInstruction.ConditionalBranchInstruction):
        pass

    def visit_llvm_unconditional_branch_instruction(self, instruction: LLVMInstruction.UnconditionalBranchInstruction):
        pass

    def visit_llvm_unary_assign_instruction(self, instruction: LLVMInstruction.UnaryAssignInstruction):
        pass

    def visit_llvm_binary_assign_instruction(self, instruction: LLVMInstruction.BinaryAssignInstruction):
        pass

    def visit_llvm_binary_arithmetic_instruction(self, instruction: LLVMInstruction.BinaryArithmeticInstruction):
        pass

    def visit_llvm_data_type_convert_instruction(self, instruction: LLVMInstruction.DataTypeConvertInstruction):
        pass

    def visit_llvm_compare_instruction(self, instruction: LLVMInstruction.CompareInstruction):
        pass

    def visit_llvm_unary_arithmetic_instruction(self, instruction: LLVMInstruction.UnaryArithmeticInstruction):
        pass

    def visit_llvm_get_elementptr_instruction(self, instruction: LLVMInstruction.GetElementPtrInstruction):
        pass

    def visit_llvm_printf_instruction(self, instruction: LLVMInstruction.PrintfInstruction):
        pass

    def visit_llvm_call_instruction(self, instruction: LLVMInstruction.CallInstruction):
        pass

    def visit_llvm_bitcast_instruction(self, instruction: LLVMInstruction.BitcastInstruction):
        pass

    def visit_llvm_memcpy_instruction(self, instruction: LLVMInstruction.MemcpyInstruction):
        pass
