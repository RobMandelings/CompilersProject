# Generated from C.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx:CParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#instructions.
    def visitInstructions(self, ctx:CParser.InstructionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#instruction.
    def visitInstruction(self, ctx:CParser.InstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#varDeclaration.
    def visitVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#varAssignment.
    def visitVarAssignment(self, ctx:CParser.VarAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expr.
    def visitExpr(self, ctx:CParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compareExpr.
    def visitCompareExpr(self, ctx:CParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#addExpr.
    def visitAddExpr(self, ctx:CParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multExpr.
    def visitMultExpr(self, ctx:CParser.MultExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryExpr.
    def visitUnaryExpr(self, ctx:CParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#finalExpr.
    def visitFinalExpr(self, ctx:CParser.FinalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeDeclaration1.
    def visitTypeDeclaration1(self, ctx:CParser.TypeDeclaration1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeDeclaration2.
    def visitTypeDeclaration2(self, ctx:CParser.TypeDeclaration2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#constDeclaration.
    def visitConstDeclaration(self, ctx:CParser.ConstDeclarationContext):
        return self.visitChildren(ctx)



del CParser