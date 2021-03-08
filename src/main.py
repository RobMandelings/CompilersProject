from CSTVisitors import CSTVisitorToDot
from src.ast.CSTtoASTConverter import *
from src.ast.ASTVisitors import ASTVisitorDot

# TODO support for unary operations ('-5' for example)
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.program()

    cst_visitor_to_dot = CSTVisitorToDot()
    tree.accept(cst_visitor_to_dot)
    cst_visitor_to_dot.graph.render('output/cst.gv', view=False)


    ast = createASTFromConcreteSyntaxTree(tree, lexer)
    ast_visitor_dot = ASTVisitorDot()
    ast.accept(ast_visitor_dot)

    ast_visitor_dot.graph.render('output/ast.gv', view=False)
    print(argv[1])


if __name__ == '__main__':
    main(sys.argv)
