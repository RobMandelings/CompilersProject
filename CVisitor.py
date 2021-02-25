# Generated from C.g4 by ANTLR 4.7.2
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


    # Visit a parse tree produced by CParser#value.
    def visitValue(self, ctx:CParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#add.
    def visitAdd(self, ctx:CParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#mult.
    def visitMult(self, ctx:CParser.MultContext):
        return self.visitChildren(ctx)



del CParser