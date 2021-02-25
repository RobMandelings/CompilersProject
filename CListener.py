# Generated from C.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#prog.
    def enterProg(self, ctx:CParser.ProgContext):
        pass

    # Exit a parse tree produced by CParser#prog.
    def exitProg(self, ctx:CParser.ProgContext):
        pass


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


    # Enter a parse tree produced by CParser#addExpr.
    def enterAddExpr(self, ctx:CParser.AddExprContext):
        pass

    # Exit a parse tree produced by CParser#addExpr.
    def exitAddExpr(self, ctx:CParser.AddExprContext):
        pass


    # Enter a parse tree produced by CParser#multExpr.
    def enterMultExpr(self, ctx:CParser.MultExprContext):
        pass

    # Exit a parse tree produced by CParser#multExpr.
    def exitMultExpr(self, ctx:CParser.MultExprContext):
        pass


    # Enter a parse tree produced by CParser#finalExpr.
    def enterFinalExpr(self, ctx:CParser.FinalExprContext):
        pass

    # Exit a parse tree produced by CParser#finalExpr.
    def exitFinalExpr(self, ctx:CParser.FinalExprContext):
        pass



del CParser