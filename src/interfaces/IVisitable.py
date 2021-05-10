import abc
import src.interfaces.IAstVisitor as IAstVisitor
import src.interfaces.ILLVMVisitor as ILLVMVisitor


class IVisitable:

    @abc.abstractmethod
    def visit(self, visitor):
        pass


class IASTVisitable(IVisitable):

    def visit(self, visitor: IAstVisitor.IASTVisitor):
        pass


class ILLVMVisitable(IVisitable):

    def visit(self, visitor: ILLVMVisitor.ILLVMVisitor):
        pass
