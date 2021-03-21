class BasicBlock:

    def __init__(self):
        self.instructions = list()
        self.terminator_instruction = None

    def set_terminator_instruction(self):
        assert self.terminator_instruction
