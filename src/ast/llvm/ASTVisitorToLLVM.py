from src.ast.ASTVisitor import ASTVisitor


class ASTVisitorToLLVM(ASTVisitor):

    def __init__(self, output_filename):
        self.llvm_builder
        self.output_file = open(output_filename, "w+")

    def visit_ast_leaf(self, ast):
        super().visit_ast_leaf(ast)

    def visit_ast_internal(self, ast):
        super().visit_ast_internal(ast)

    def visit_ast_binary_expression(self, ast):
        self.llvm_builder.buildBinaryExpressionCode(mult)
        super().visit_ast_binary_expression(ast)

    def visit_ast_variable_declaration(self, ast):
        super().visit_ast_variable_declaration(ast)

    def visit_ast_variable_declaration_and_init(self, ast):
        super().visit_ast_variable_declaration_and_init(ast)


