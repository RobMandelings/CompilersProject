import abc


class IToLLVM(abc.ABC):

    def to_llvm(self):
        """
        Updates the counter if necessary and returns a string which contains all the LLVM generated llvm code of the object
        """
        raise NotImplementedError

    def update_numbering(self, counter):
        raise NotImplementedError
