import abc
import src.ast.IAstVisitor as IAstVisitor
import src.interfaces.ILLVMVisitor as ILLVMVisitor


class IVisitable(abc.ABC):

    @abc.abstractmethod
    def accept(self, visitor):
        pass


class IASTVisitable(IVisitable, abc.ABC):

    @abc.abstractmethod
    def accept(self, visitor: IAstVisitor.IASTVisitor):
        pass


class ILLVMVisitable(IVisitable, abc.ABC):

    @abc.abstractmethod
    def accept(self, visitor: ILLVMVisitor.ILLVMVisitor):
        pass
