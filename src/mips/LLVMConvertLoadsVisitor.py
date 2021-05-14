import src.llvm.visitors.LLVMBaseVisitor as LLVMBaseVisitor
from src.llvm import LLVMCode as LLVMCode, LLVMBasicBlock, LLVMInstruction, LLVMFunction as LLVMFunction


# class LLVMUpdateReferencesVisitor(LLVMBaseVisitor.LLVMBaseVisitor):
#     """
#     Updates the LLVMRegister references by replacing each found register from
#     a key of the reference mapper to its value. This is used so that the llvm code doesn't use the loaded registers
#     anymore but the allocated ones (used by the MIPS builder)
#     """
#
#     def __init__(self, reference_mapper):
#         """
#         Maps the loaded registers from llvm to their corresponding allocated registers
#         """
#         self.reference_mapper = reference_mapper
#
#
#
#
# class LLVMConvertLoadsVisitor(LLVMBaseVisitor.LLVMBaseVisitor):
#     """
#     Preprocessing step of the mips builder: removes the load instructions from llvm and updates the references
#     to these 'loaded' values to their unloaded 'allocated' registers (which corresponds to variables)
#     """
#
#     def __init__(self):
#         self.reference_mapper = None
#
#     def get_reference_mapper(self):
#         assert isinstance(self.reference_mapper, dict)
#         return self.reference_mapper
#
#     def visit_llvm_defined_function(self, llvm_defined_function: LLVMFunction.LLVMDefinedFunction):
#         self.reference_mapper = dict()
#         super().visit_llvm_defined_function(llvm_defined_function)
#         update_references_visitor = LLVMUpdateReferencesVisitor(self.reference_mapper)
#         llvm_defined_function.accept(update_references_visitor)
#
#     def visit_llvm_basic_block(self, llvm_basic_block: LLVMBasicBlock.LLVMBasicBlock):
#         # Used to add entries to the reference mapper
#         load_instructions = [instruction for instruction in llvm_basic_block.instructions if
#                              isinstance(instruction, LLVMInstruction.LLVMLoadInstruction)]
#
#         # For each load instruction found, map the resulting register to the load from register
#         # to prepare for the update references
#         for load_instruction in load_instructions:
#             self.get_reference_mapper()[load_instruction.resulting_reg] = load_instruction.load_from_reg
#
#         # Instructions without any loads, replacing the old basic block
#         filtered_instructions = [instruction for instruction in llvm_basic_block.instructions if
#                                  isinstance(instruction, LLVMInstruction.LLVMLoadInstruction)]
#
#         llvm_basic_block.instructions = filtered_instructions
