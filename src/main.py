import sys
from antlr4 import *

from graphviz import Digraph
from CLexer import CLexer
from src.ast.AST import Counter
from src.ast.CSTtoASTConverter import *


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    ast = createASTFromConcreteSyntaxTree(tree)
    dot = Digraph(comment='Abstract Syntax Tree')
    ast.createDot(dot, Counter())

    dot.render('output/ast.gv', view=True)
    print(argv[1])
 
if __name__ == '__main__':
    main(sys.argv)