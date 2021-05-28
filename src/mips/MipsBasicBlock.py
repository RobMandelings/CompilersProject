import src.mips.MipsInstruction as MipsInstruction
import src.BasicBlock as BasicBlock


class MipsBasicBlock(BasicBlock.BasicBlock):
    """
    Basic block for mips. Simply contains instructions for each corresponding basic block from mips
    """

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def add_instruction(self, instruction: MipsInstruction.MipsInstruction):
        assert isinstance(instruction, MipsInstruction.MipsInstruction)
        super().add_instruction(instruction)

    def to_mips(self):
        mips_code = f"{self.name}:\n"

        for instruction in self.instructions:
            mips_code += f"  {instruction.to_mips()}\n"

        return mips_code
