import src.llvm.LLVMFunction as LLVMFunction
import src.llvm.LLVMInterfaces as LLVMInterfaces
import src.interfaces.IVisitable as IVisitable


class LLVMFunctionHolder(LLVMInterfaces.IToLLVM):

    def __init__(self):
        self.functions = dict()
        self.current_function = None

    def accept(self, visitor):
        visitor.visit_llvm_function_holder(self)

    def add_function(self, function: LLVMFunction.LLVMFunction):
        assert isinstance(function, LLVMFunction.LLVMFunction)
        self.functions[function.get_identifier()] = function

    def set_current_function(self, function: LLVMFunction.LLVMDefinedFunction):
        assert isinstance(function, LLVMFunction.LLVMDefinedFunction)
        self.current_function = function

    def get_current_function(self):
        assert isinstance(self.current_function, LLVMFunction.LLVMDefinedFunction)
        return self.current_function

    def get_function(self, function_identifier):
        function = self.functions.get(function_identifier)
        assert isinstance(function, LLVMFunction.LLVMFunction)
        return function

    def to_llvm(self):
        llvm_code = ''

        for function in self.functions.values():
            llvm_code += function.to_llvm() + "\n"

        return llvm_code

    def update_numbering(self, counter):
        pass
