import abc


class Instruction(abc.ABC):

    def is_terminator(self):
        raise NotImplementedError('Generic method')
