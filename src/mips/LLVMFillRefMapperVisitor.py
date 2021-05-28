import src.llvm.visitors.LLVMBaseVisitor as LLVMBaseVisitor
from src.llvm import LLVMInstruction as LLVMInstruction


class LLVMFillRefMapperVisitor(LLVMBaseVisitor.LLVMBaseVisitor):
    """
    Creates and fills a reference mapper dictionary with as keys the loaded llvm registers and as values
    the allocated llvm registers where they were loaded from. This shall be used in the LLVMBuilder
    (see get_llvm_values method) to get the correct mips register.

    The reason for doing this is because the load and store of llvm do not correspond to the load and store of mips.
    In mips you can directly assign a new value to a variable whereas in llvm this is impossible,
    so you would need to use load and store for this. So in mips,
    you can directly assign to the 'allocated' register a new value, thus the load and stores of llvm are redundant now.
    """

    def __init__(self):
        self.ref_mapper = dict()

    def get_ref_mapper(self):
        assert self.ref_mapper
        return self.ref_mapper

    def visit_llvm_load_instruction(self, instruction: LLVMInstruction.LLVMLoadInstruction):
        self.ref_mapper[instruction.get_resulting_register()] = instruction.load_from_reg
