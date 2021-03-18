from CSTVisitors import CSTVisitorToDot
from src.ast.CSTtoASTConverter import *
from src.syntacticalAnalysis import CSTErrorListener


# TODO support for unary operations ('-5' for example)
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = CParser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(CSTErrorListener())

    # tree = parser.program()

    # cst_visitor_to_dot = CSTVisitorToDot()
    # tree.accept(cst_visitor_to_dot)
    # cst_visitor_to_dot.graph.render('output/cst.gv', view=False)

    tree = parser.program()

    cst_visitor_to_dot = CSTVisitorToDot()

    # try:
        # tree = parser.program()
        #
        # cst_visitor_to_dot = CSTVisitorToDot()
        # tree.accept(cst_visitor_to_dot)
        # cst_visitor_to_dot.graph.render('output/cst.gv', view=False)

    #     ast = create_ast_from_concrete_syntax_tree(tree, lexer)
    #     ast_visitor_dot = ASTVisitorDot()
    #     ast.accept(ast_visitor_dot)
    #     ast_visitor_dot.graph.render('output/ast.gv', view=False)
    #
    #     ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis(optimize=False)
    #     try:
    #         ast.accept(ast_visitor_semantic_analysis)
    #
    #         ast_visitor_dot.reset()
    #         ast.accept(ast_visitor_dot)
    #         ast_visitor_dot.graph.render('output/ast-optimized.gv', view=False)
    #
    #     except SemanticError as e:
    #         print("A semantic error occurred: ")
    #         print(e)
    #         print("Stopping the compiler...")
    #         sys.exit(0)
    #     print(argv[1])
    #
    #     ast_visitor_to_llvm = ASTVisitorToLLVM()
    #     ast.accept(ast_visitor_to_llvm)
    #     ast_visitor_to_llvm.to_file("output/converted.b")
    #
    # except SyntaxError:
    #     print("Exiting program...", file=sys.stderr)
    #     sys.exit()


if __name__ == '__main__':
    main(sys.argv)
