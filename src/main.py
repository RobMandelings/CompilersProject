from CSTVisitors import CSTVisitorToDot
from src.ast.CSTtoASTConverter import *
from src.ast.ASTVisitors import ASTVisitorDot
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


        ast = createASTFromConcreteSyntaxTree(tree, lexer)
        ast_visitor_dot = ASTVisitorDot()
        ast.accept(ast_visitor_dot)

        ast_visitor_dot.graph.render('output/ast.gv', view=False)
        print(argv[1])

    except SyntaxError:
        print("Exiting program...", file=sys.stderr)
        sys.exit()



if __name__ == '__main__':
    main(sys.argv)
