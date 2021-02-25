# Generated from C.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#stat.
    def enterStat(self, ctx:CParser.StatContext):
        pass

    # Exit a parse tree produced by CParser#stat.
    def exitStat(self, ctx:CParser.StatContext):
        pass


    # Enter a parse tree produced by CParser#expr.
    def enterExpr(self, ctx:CParser.ExprContext):
        pass

    # Exit a parse tree produced by CParser#expr.
    def exitExpr(self, ctx:CParser.ExprContext):
        pass


    # Enter a parse tree produced by CParser#value.
    def enterValue(self, ctx:CParser.ValueContext):
        pass

    # Exit a parse tree produced by CParser#value.
    def exitValue(self, ctx:CParser.ValueContext):
        pass


    # Enter a parse tree produced by CParser#end_of_line.
    def enterEnd_of_line(self, ctx:CParser.End_of_lineContext):
        pass

    # Exit a parse tree produced by CParser#end_of_line.
    def exitEnd_of_line(self, ctx:CParser.End_of_lineContext):
        pass


    # Enter a parse tree produced by CParser#add.
    def enterAdd(self, ctx:CParser.AddContext):
        pass

    # Exit a parse tree produced by CParser#add.
    def exitAdd(self, ctx:CParser.AddContext):
        pass


    # Enter a parse tree produced by CParser#mult.
    def enterMult(self, ctx:CParser.MultContext):
        pass

    # Exit a parse tree produced by CParser#mult.
    def exitMult(self, ctx:CParser.MultContext):
        pass


