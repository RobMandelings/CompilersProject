import src.ast.ASTs as ASTs


class LLVMFunctionHolder:

    def __init__(self):
        self.defined_functions = dict()
        self.declared_functions = dict()

    def add_declared_function(self, function: ASTs.ASTFunctionDeclaration):
        pass

    def add_defined_function(self, function: ASTs.ASTFunctionDefinition):
        pass

    def set_current_function(self):

    def get_current_function(self):
