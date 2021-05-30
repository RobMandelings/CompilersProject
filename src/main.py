import os
from CSTVisitorToDot import CSTVisitorToDot
from src.ast.ASTVisitorDot import ASTVisitorDot
from src.ast.CSTtoASTConverter import *
from src.llvm.ASTVisitorToLLVM import ASTVisitorToLLVM
from src.semantic_analysis.ASTVisitorSemanticAnalysis import ASTVisitorSemanticAnalysis, SemanticError
from src.syntacticalAnalysis import CSTErrorListener
from src.mips.LLVMToMipsVisitor import LLVMToMipsVisitor


def log(file, log_string):
    f = open(file, "a")
    f.write(log_string)
    f.close()


def run_benchmark(filename: str):
    """
    filename: the filename you need to enter to run the script
    to_llvm: true if compiling to llvm, false if compiling to mips
    """

    input_stream = FileStream(filename)
    lexer = CLexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = CParser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(CSTErrorListener())

    try:
        tree = parser.program()

        cst_visitor_to_dot = CSTVisitorToDot()
        tree.accept(cst_visitor_to_dot)
        cst_visitor_to_dot.graph.render(f'{filename}_cst.gv', view=False)

        try:
            ast = create_ast_from_cst(tree)
            ast_visitor_dot = ASTVisitorDot()
            ast.accept(ast_visitor_dot)
            ast_visitor_dot.graph.render(f'{filename}_ast.gv', view=False)

            ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis(optimize=False)
            ast.accept(ast_visitor_semantic_analysis)

            ast_visitor_dot.reset()
            ast.accept(ast_visitor_dot)
            ast_visitor_dot.graph.render(f'{filename}_ast-optimized.gv', view=False)

            ast_visitor_to_llvm = ASTVisitorToLLVM()
            ast.accept(ast_visitor_to_llvm)

            ast_visitor_to_llvm.to_file(f"{filename}_output.ll")

            llvm_code = ast_visitor_to_llvm.get_builder().build()
            llvm_to_mips_visitor = LLVMToMipsVisitor()
            llvm_code.accept(llvm_to_mips_visitor)

            llvm_to_mips_visitor.get_mips_builder().to_file('testinput/mips.asm')


        except SemanticError as e:
            print("A semantic error occurred: ")
            print(e)
            print("Stopping the compiler...")
            sys.exit(0)

    except SyntaxError:
        print("Exiting program...", file=sys.stderr)
        sys.exit()


def main(argv):
    filename = argv[1]
    run_benchmark(filename)


if __name__ == '__main__':
    main(sys.argv)
