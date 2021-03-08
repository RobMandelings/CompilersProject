# Generated from C.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#program.
    def enterProgram(self, ctx:CParser.ProgramContext):
        pass

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#varDeclaration.
    def enterVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#varDeclaration.
    def exitVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#expr.
    def enterExpr(self, ctx:CParser.ExprContext):
        pass

    # Exit a parse tree produced by CParser#expr.
    def exitExpr(self, ctx:CParser.ExprContext):
        pass


    # Enter a parse tree produced by CParser#compareExpr.
    def enterCompareExpr(self, ctx:CParser.CompareExprContext):
        pass

    # Exit a parse tree produced by CParser#compareExpr.
    def exitCompareExpr(self, ctx:CParser.CompareExprContext):
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


    # Enter a parse tree produced by CParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:CParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:CParser.TypeDeclarationContext):
        pass



del CParser