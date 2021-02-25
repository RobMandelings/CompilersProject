import sys
from antlr4 import *

from AST import AST
from CLexer import CLexer
from CParser import CParser

# TODO order of operations
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    print(argv[1])

    ast = AST()
 
if __name__ == '__main__':
    main(sys.argv)