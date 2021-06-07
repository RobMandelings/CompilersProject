import os
from CSTVisitorToDot import CSTVisitorToDot
from src.ast.ASTVisitorDot import ASTVisitorDot
from src.ast.CSTtoASTConverter import *
from src.llvm.ASTVisitorToLLVM import ASTVisitorToLLVM
from src.semantic_analysis.ASTVisitorSemanticAnalysis import ASTVisitorSemanticAnalysis, SemanticError
from src.syntacticalAnalysis import CSTErrorListener
from src.mips.LLVMToMipsVisitor import LLVMToMipsVisitor
import enum
import traceback


def log(file, log_string):
    f = open(file, "a")
    f.write(log_string)
    f.close()


class CompileResult(enum.Enum):
    SUCCESS = enum.auto()
    SEMANTIC_ERROR = enum.auto()
    SYNTAX_ERROR = enum.auto()
    OTHER_ERROR = enum.auto()


def run_benchmarks(semantic_errors, optimized: bool):
    script_path = os.getcwd()

    benchmark_type = 'SemanticErrors' if semantic_errors else 'CorrectCode'
    code_dir = f'{script_path}/benchmark/{benchmark_type}/'

    benchmark_log_path = os.path.join(code_dir, 'benchmarks.log')
    benchmark_log_file = open(benchmark_log_path, 'w+')
    summary_log_file = open(os.path.join(code_dir, 'summary_benchmarks.log'), 'w+')

    files = os.listdir(code_dir)

    total = 0
    syntax_errors = 0
    semantic_errors = 0
    other_errors = 0
    success = 0

    for filename in os.listdir(code_dir):
        if filename.endswith('.c'):

            total += 1
            print(f"Compiling '{benchmark_type}' benchmark file {filename}...")
            try:

                result = run_benchmark(filename, optimized, base_filedir=code_dir,
                                       benchmark_log_file=benchmark_log_file)

                if result == CompileResult.SUCCESS:
                    success += 1
                elif result == CompileResult.SYNTAX_ERROR:
                    syntax_errors += 1
                elif result == CompileResult.SEMANTIC_ERROR:
                    semantic_errors += 1
                else:
                    raise NotImplementedError('This cannot happen')


            except Exception as e:
                print(
                    f"[Compiler] something went wrong running {benchmark_type} benchmark file {filename}. "
                    f"Compiler might not support certain features in the file.")
                print(e)
                benchmark_log_file.write('OTHER ERROR:\n')
                benchmark_log_file.write(f"{e}\n\n")
                other_errors += 1
                traceback.print_exc(e)

        else:
            print(f"[Compiler] Skipping file {filename} (doesn't have the .c extension)")

    summary_log_file.write('COMPILE SUMMARY:\n')
    summary_log_file.write(f'Total files attempted to compile: {total}\n')
    summary_log_file.write(f'Successful compilations: {success} ({"{:.2f}".format(success / total * 100)}%)\n')
    summary_log_file.write(
        f'Syntax error compilations: {syntax_errors} ({"{:.2f}".format(syntax_errors / total * 100)}%)\n')
    summary_log_file.write(
        f'Semantic error compilations: {semantic_errors} ({"{:.2f}".format(semantic_errors / total * 100)}%)\n\n')
    summary_log_file.write(
        f'Other error compilations: {other_errors} ({"{:.2f}".format(other_errors / total * 100)}%)\n\n')


def run_benchmark(filename: str, optimized: bool, base_filedir=None, benchmark_log_file=None):
    """
    filename: the filename you need to enter to run the script
    to_llvm: true if compiling to llvm, false if compiling to mips
    """

    if base_filedir is not None:
        filepath = os.path.join(base_filedir, filename)
    else:
        filepath = filename

    ast_dir = None if base_filedir is None else base_filedir + 'asts/'
    compiled_dir = None if base_filedir is None else base_filedir + 'compiled_code/'

    if ast_dir is not None and not os.path.exists(ast_dir):
        os.mkdir(ast_dir)

    if compiled_dir is not None and not os.path.exists(compiled_dir):
        os.mkdir(compiled_dir)

    input_stream = FileStream(filepath)
    lexer = CLexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = CParser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(CSTErrorListener())

    try:
        tree = parser.program()

        cst_visitor_to_dot = CSTVisitorToDot()
        tree.accept(cst_visitor_to_dot)

        try:
            ast = create_ast_from_cst(tree)
            ast_visitor_dot = ASTVisitorDot()
            ast.accept(ast_visitor_dot)
            ast_visitor_dot.graph.render(filename=f'{filename}_ast.gv', directory="" if ast_dir is None else ast_dir,
                                         view=False)

            ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis(optimize=optimized)
            ast.accept(ast_visitor_semantic_analysis)

            ast_visitor_dot.reset()
            ast.accept(ast_visitor_dot)
            ast_visitor_dot.graph.render(filename=f'{filename}_ast_optimized.gv',
                                         directory="" if ast_dir is None else ast_dir, view=False)

            ast_visitor_to_llvm = ASTVisitorToLLVM()
            ast.accept(ast_visitor_to_llvm)

            ast_visitor_to_llvm.to_file(f"{'' if compiled_dir is None else compiled_dir}{filename}_llvm.ll")

            llvm_code = ast_visitor_to_llvm.get_builder().build()
            llvm_to_mips_visitor = LLVMToMipsVisitor()
            llvm_code.accept(llvm_to_mips_visitor)

            llvm_to_mips_visitor.get_mips_builder().to_file(
                f'{"" if compiled_dir is None else compiled_dir}{filename}_mips.asm')

        except SemanticError as e:

            if benchmark_log_file is not None:
                benchmark_log_file.write(f"SEMANTIC ERROR with file {filename}:\n")
                benchmark_log_file.write(f'{e}\n\n')
            print("A semantic error occurred: ")
            print(e)
            return CompileResult.SEMANTIC_ERROR

    except SyntaxError as e:

        if benchmark_log_file is not None:
            benchmark_log_file.write(f"SYNTAX ERROR with file {filename}:\n")
            benchmark_log_file.write(f'{e}\n\n')
        print(f"A syntax error occurred with file {filename}")
        print(e)
        return CompileResult.SYNTAX_ERROR

    return CompileResult.SUCCESS


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
