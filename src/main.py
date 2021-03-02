import sys
from antlr4 import *

from graphviz import Digraph
from CLexer import CLexer
from src.ast.CSTtoASTConverter import *
from src.ast.ASTVisitor import ASTVisitorDot


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    ast = createASTFromConcreteSyntaxTree(tree)
    ast_visitor_dot = ASTVisitorDot()
    ast.accept(ast_visitor_dot)

    ast_visitor_dot.graph.render('output/ast.gv', view=True)
    print(argv[1])


if __name__ == '__main__':
    main(sys.argv)
