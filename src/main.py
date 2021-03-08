import sys
from antlr4 import *

from graphviz import Digraph
from antlr4_gen.CLexer import CLexer
from src.ast.CSTtoASTConverter import *
from src.ast.ASTVisitors import ASTVisitorDot

# Read from C.tokens file
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    ast = createASTFromConcreteSyntaxTree(tree, lexer)
    ast_visitor_dot = ASTVisitorDot()
    ast.accept(ast_visitor_dot)

    ast_visitor_dot.graph.render('output/ast.gv', view=True)
    print(argv[1])


if __name__ == '__main__':
    main(sys.argv)
