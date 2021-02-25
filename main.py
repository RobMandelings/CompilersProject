import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.stat()

    print(argv[1])
 
if __name__ == '__main__':
    main(sys.argv)