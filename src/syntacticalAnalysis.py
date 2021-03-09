import sys

from antlr4.error.ErrorListener import ErrorListener


class CSTErrorListener(ErrorListener):

    def __init__(self):
        super(CSTErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("SYNTAX ERROR: line " + str(line) + ":" + str(column) + " " + msg, file=sys.stderr)
        raise SyntaxError("Syntax_error")




