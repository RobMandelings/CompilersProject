import abc


class ILLVMVisitor(abc.ABC):

    def visit_llvm_code(self, llvm_code):
        pass

    def visit_llvm_global_container(self, llvm_global_container):
        pass

    def visit_llvm_function_holder(self, llvm_function_holder):
        pass

    def visit_llvm_function(self, llvm_function):
        pass

    def visit_llvm_basic_block(self, llvm_basic_block):
        pass

    def visit_llvm_instruction(self, llvm_instruction):
        pass
