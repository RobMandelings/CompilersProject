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
        super().visit_llvm_code(llvm_code)

    def visit_llvm_global_container(self, llvm_global_container: LLVMGlobalContainer.LLVMGlobalContainer):
        super().visit_llvm_global_container(llvm_global_container)

    def visit_llvm_function_holder(self, llvm_function_holder: LLVMFunctionHolder.LLVMFunctionHolder):
        super().visit_llvm_function_holder(llvm_function_holder)

    def visit_llvm_function(self, llvm_function: LLVMFunction.LLVMFunction):
        super().visit_llvm_function(llvm_function)

    def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
        super().visit_llvm_basic_block(llvm_basic_block)

    def visit_llvm_instruction(self, llvm_instruction: LLVMInstruction.Instruction):
        super().visit_llvm_instruction(llvm_instruction)
