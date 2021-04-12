import abc


class IToLLVM(abc.ABC):

    def to_llvm(self):
        """
        Returns a string which contains all the LLVM generated llvm code of the object
        """
        raise NotImplementedError
