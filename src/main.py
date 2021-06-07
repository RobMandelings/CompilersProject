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


def run_benchmarks(semantic_errors, optimized: bool):
    script_path = os.getcwd()

    benchmark_type = 'SemanticErrors' if semantic_errors else 'CorrectCode'
    semantic_errors_dir = f'{script_path}/benchmark/{benchmark_type}/'

    for filename in os.listdir(semantic_errors_dir):
        if filename.endswith('.c'):

            filepath = os.path.join(semantic_errors_dir, filename)

            print(f"Compiling '{benchmark_type}' benchmark file {filename}...")
            try:
                run_benchmark(filepath, optimized)
            except Exception as e:
                print(
                    f"[Compiler] something went wrong running {benchmark_type} benchmark file {filename}. "
                    f"Compiler might not support certain features in the file.")
        else:
            print(f"[Compiler] Skipping file {filename} (doesn't have the .c extension)")


def run_benchmark(filename: str, optimized: bool):
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

            ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis(optimize=optimized)
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


def get_optimized_bool(arg: str):
    if arg.lower() == 'true':
        return True
    elif arg.lower() == 'false':
        return False
    else:
        raise ValueError(f"Could not deduce whether or not optimization is enabled from input '{arg}'")


def main(argv):
    if len(argv) == 1:
        print("[Compiler] parameter 'optimized' not specified (should be true or false)")
        return
    elif len(argv) == 2:
        print("[Compiler] running all 'CorrectCode' and 'SemanticErrors' benchmarks...")
        try:
            optimized = get_optimized_bool(argv[1])
            run_benchmarks(semantic_errors=True, optimized=optimized)
            run_benchmarks(semantic_errors=False, optimized=optimized)
        except ValueError as e:
            print(f"[Compiler] a ValueError occurred: {e}")
            return

    elif len(argv) == 3:

        filepath = argv[1]

        if not os.path.exists(filepath):
            print(f"[Compiler] file {filepath} not found")
            return

        try:
            optimized = get_optimized_bool(argv[2])
            run_benchmark(filepath, optimized)
        except ValueError as e:
            print(f"[Compiler] a ValueError occurred: {e}")
            return
    else:
        print(f"[Compiler] too many arguments specified (should be 1 or 2; is {len(argv)}")
        return


if __name__ == '__main__':
    main(sys.argv)
