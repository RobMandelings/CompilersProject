from CSTVisitorToDot import CSTVisitorToDot
from src.ast.ASTVisitorDot import ASTVisitorDot
from src.ast.CSTtoASTConverter import *
from src.llvm.ASTVisitorToLLVM import ASTVisitorToLLVM
from src.semantic_analysis.ASTVisitorSemanticAnalysis import ASTVisitorSemanticAnalysis, SemanticError
from src.syntacticalAnalysis import CSTErrorListener


# TODO support for unary operations ('-5' for example)
def main(argv):
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

        ast = create_ast_from_cst(tree)
        ast_visitor_dot = ASTVisitorDot()
        ast.accept(ast_visitor_dot)
        ast_visitor_dot.graph.render('output/ast.gv', view=False)

        ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis(optimize=False)
        try:
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
