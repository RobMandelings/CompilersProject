import src.llvm.LLVMBuilder as LLVMBuilder


class LLVMCode:
    """
    Instances of this class can be generated using the LLVMBuilder class.
    The code can then be traversed using a visitor, and is not meant to be modified anymore
    """

    def __init__(self, llvm_builder: LLVMBuilder.LLVMBuilder):
        self.global_container = llvm_builder.global_container
        self.function_holder = llvm_builder.function_holder

    def visit(self, visitor):
        pass
