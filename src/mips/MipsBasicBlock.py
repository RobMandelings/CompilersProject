import src.mips.MipsInstruction as MipsInstruction
import src.BasicBlock as BasicBlock


class MipsBasicBlock(BasicBlock.BasicBlock):
    """
    Basic block for mips. Simply contains instructions for each corresponding basic block from mips
    """

    def __init__(self, name: str):
        """
        return_instruction_points: only used in mips basic blocks. It contains a list of indices at which to insert
        'return' instructions. These instructions are really just JumpInstructions to a specified basic block, but the
        last basic block is not known before the end of the function definition. So, the indices will be replaced
        by actual instructions once this basic block has been created (will be '<basic_block_name>_end')
        """
        super().__init__()
        self.name = name
        self.return_instruction_points = list()

    def replace_return_instruction_points_with_instructions(self, basic_block_to_return_to):
        """
        Places actual instructions at the indices where return instruction points where placed.
        The actual return values should already be put in the corresponding registers as well.
        """
        assert isinstance(basic_block_to_return_to, MipsBasicBlock)
        for return_instruction_point in self.return_instruction_points:
            self.instructions[return_instruction_point] = MipsInstruction.JumpInstruction(basic_block_to_return_to)

    def add_return_instruction_point(self):
        """
        Sets a return instruction point at the current index. That is, a return instruction will later be placed at this
        index.
        """
        # This insertion is just to make it more clear that a return instruction will be placed here
        self.return_instruction_points.append(len(self.instructions))
        self.instructions.insert(len(self.instructions), 'return instruction point')

    def add_instruction(self, instruction: MipsInstruction.MipsInstruction):
        assert isinstance(instruction, MipsInstruction.MipsInstruction)
        super().add_instruction(instruction)

    def to_mips(self):
        mips_code = f"{self.name}:\n"

        for instruction in self.instructions:
            mips_code += f"    {instruction.to_mips()}\n"

        return mips_code
