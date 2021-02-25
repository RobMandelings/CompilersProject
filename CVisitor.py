# Generated from C.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#prog.
    def visitProg(self, ctx:CParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#stat.
    def visitStat(self, ctx:CParser.StatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expr.
    def visitExpr(self, ctx:CParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#addExpr.
    def visitAddExpr(self, ctx:CParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multExpr.
    def visitMultExpr(self, ctx:CParser.MultExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#finalExpr.
    def visitFinalExpr(self, ctx:CParser.FinalExprContext):
        return self.visitChildren(ctx)



del CParser