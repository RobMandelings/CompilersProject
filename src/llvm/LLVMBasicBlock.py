import src.BasicBlock as BasicBlock
import src.interfaces.IVisitable as IVisitable
import src.llvm.LLVMInstruction as LLVMInstruction
import src.llvm.LLVMUtils as LLVMUtils
from src.interfaces import ILLVMVisitor as ILLVMVisitor


class LLVMBasicBlock(IVisitable.ILLVMVisitable, BasicBlock.BasicBlock):

    def __init__(self):
        super().__init__()
        self._number = None

    def __repr__(self):
        return f'LLVMBasicBlock, number: {self._number}. ID: {id(self)}'

    def add_instruction(self, instruction):
        """
        Safely adds a new instruction to the list of instructions
        """
        assert isinstance(instruction, LLVMInstruction.LLVMInstruction)
        assert not isinstance(instruction, LLVMInstruction.LLVMAllocaInstruction)
        super().add_instruction(instruction)

    def get_number(self):
        """
        Returns the _number of this basic block
        """
        assert self._number is not None, "the number of this basic block has not been initialized yet"
        return self._number

    def update_numbering(self, counter: LLVMUtils.LLVMCounter):
        for instruction in self.instructions:
            instruction.update_numbering(counter)

    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        visitor.visit_llvm_basic_block(self)

    def to_llvm(self):
        llvm_code = ""

        for instruction in self.instructions:
            llvm_code += f"  {instruction.to_llvm()}\n"

        return llvm_code
