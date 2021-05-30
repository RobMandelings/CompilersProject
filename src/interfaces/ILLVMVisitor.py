import abc


class ILLVMVisitor(abc.ABC):

    def visit_llvm_code(self, llvm_code):
        pass

    def visit_llvm_global_container(self, llvm_global_container):
        pass

    def visit_llvm_function_holder(self, llvm_function_holder):
        pass

    def visit_llvm_defined_function(self, llvm_defined_function):
        pass

    def visit_llvm_declared_function(self, llvm_declared_function):
        pass

    def visit_llvm_basic_block(self, llvm_basic_block):
        pass

    def visit_llvm_assign_instruction(self, instruction):
        pass

    def visit_llvm_return_instruction(self, instruction):
        pass

    def visit_llvm_raw_assign_instruction(self, instruction):
        pass

    def visit_llvm_alloca_instruction(self, instruction):
        pass

    def visit_llvm_alloca_array_instruction(self, instruction):
        pass

    def visit_llvm_store_instruction(self, instruction):
        pass

    def visit_llvm_load_instruction(self, instruction):
        pass

    def visit_llvm_conditional_instruction(self, instruction):
        pass

    def visit_llvm_conditional_branch_instruction(self, instruction):
        pass

    def visit_llvm_unconditional_branch_instruction(self, instruction):
        pass

    def visit_llvm_unary_assign_instruction(self, instruction):
        pass

    def visit_llvm_binary_assign_instruction(self, instruction):
        pass

    def visit_llvm_binary_arithmetic_instruction(self, instruction):
        pass

    def visit_llvm_data_type_convert_instruction(self, instruction):
        pass

    def visit_llvm_compare_instruction(self, instruction):
        pass

    def visit_llvm_unary_arithmetic_instruction(self, instruction):
        pass

    def visit_llvm_get_elementptr_instruction(self, instruction):
        pass

    def visit_llvm_printf_instruction(self, instruction):
        pass

    def visit_llvm_scanf_instruction(self, instruction):
        pass

    def visit_llvm_call_instruction(self, instruction):
        pass

    def visit_llvm_bitcast_instruction(self, instruction):
        pass

    def visit_llvm_memcpy_instruction(self, instruction):
        pass

    def visit_llvm_fpext_instruction(self, instruction):
        pass
