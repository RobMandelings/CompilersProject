import os
from CSTVisitorToDot import CSTVisitorToDot
from src.ast.ASTVisitorDot import ASTVisitorDot
from src.ast.CSTtoASTConverter import *
from src.llvm.ASTVisitorToLLVM import ASTVisitorToLLVM
from src.semantic_analysis.ASTVisitorSemanticAnalysis import ASTVisitorSemanticAnalysis, SemanticError
from src.syntacticalAnalysis import CSTErrorListener


# TODO support for unary operations ('-5' for example)

def log(file, log_string):
    f = open(file, "a")
    f.write(log_string)
    f.close()


def benchmark_file(file, filename):
    input_stream = FileStream(file)
    lexer = CLexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = CParser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(CSTErrorListener())

    try:
        tree = parser.program()

        cst_visitor_to_dot = CSTVisitorToDot()
        tree.accept(cst_visitor_to_dot)
        cst_visitor_to_dot.graph.render('output/cst.gv', view=False)

        try:
            ast = create_ast_from_cst(tree)
            ast_visitor_dot = ASTVisitorDot()
            ast.accept(ast_visitor_dot)
            ast_visitor_dot.graph.render('output/ast.gv', view=False)

            ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis(optimize=False)
            ast.accept(ast_visitor_semantic_analysis)

            ast_visitor_dot.reset()
            ast.accept(ast_visitor_dot)
            ast_visitor_dot.graph.render('output/ast-optimized.gv', view=False)

            ast_visitor_to_llvm = ASTVisitorToLLVM()
            ast.accept(ast_visitor_to_llvm)
            ast_visitor_to_llvm.to_file("testinput/output.ll")

        except SemanticError as e:
            semanticErrorFile = "input/SemanticErrorLog"
            log(semanticErrorFile, filename + ": ")
            log(semanticErrorFile, "A semantic error occurred: ")
            log(semanticErrorFile, e.args[0])
            log(semanticErrorFile, "\n")

    except SyntaxError:
        syntaxErrorFile = "input/SyntaxErrorLog"
        log(syntaxErrorFile, filename + ": ")
        log(syntaxErrorFile, "Syntax error occured:")
        log(syntaxErrorFile, sys.stderr)


def main(argv):
    benchmark = True

    if benchmark:
        directory = "input/SemanticErrors"
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            print(filename)
            benchmark_file(filepath, filename)
    else:
        input_stream = FileStream(argv[1])
        lexer = CLexer(input_stream)

        stream = CommonTokenStream(lexer)
        parser = CParser(stream)

        parser.removeErrorListeners()
        parser.addErrorListener(CSTErrorListener())

        try:
            tree = parser.program()

            cst_visitor_to_dot = CSTVisitorToDot()
            tree.accept(cst_visitor_to_dot)
            cst_visitor_to_dot.graph.render('output/cst.gv', view=False)

            try:
                ast = create_ast_from_cst(tree)
                ast_visitor_dot = ASTVisitorDot()
                ast.accept(ast_visitor_dot)
                ast_visitor_dot.graph.render('output/ast.gv', view=False)

                ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis(optimize=False)
                ast.accept(ast_visitor_semantic_analysis)

                ast_visitor_dot.reset()
                ast.accept(ast_visitor_dot)
                ast_visitor_dot.graph.render('output/ast-optimized.gv', view=False)

                ast_visitor_to_llvm = ASTVisitorToLLVM()
                ast.accept(ast_visitor_to_llvm)
                ast_visitor_to_llvm.to_file("testinput/output.ll")

            except SemanticError as e:
                print("A semantic error occurred: ")
                print(e)
                print("Stopping the compiler...")
                sys.exit(0)

        except SyntaxError:
            print("Exiting program...", file=sys.stderr)
            sys.exit()


if __name__ == '__main__':
    main(sys.argv)
