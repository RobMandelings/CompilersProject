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


    # Enter a parse tree produced by CParser#instructions.
    def enterInstructions(self, ctx:CParser.InstructionsContext):
        pass

    # Exit a parse tree produced by CParser#instructions.
    def exitInstructions(self, ctx:CParser.InstructionsContext):
        pass


    # Enter a parse tree produced by CParser#instruction.
    def enterInstruction(self, ctx:CParser.InstructionContext):
        pass

    # Exit a parse tree produced by CParser#instruction.
    def exitInstruction(self, ctx:CParser.InstructionContext):
        pass


    # Enter a parse tree produced by CParser#printfInstruction.
    def enterPrintfInstruction(self, ctx:CParser.PrintfInstructionContext):
        pass

    # Exit a parse tree produced by CParser#printfInstruction.
    def exitPrintfInstruction(self, ctx:CParser.PrintfInstructionContext):
        pass


    # Enter a parse tree produced by CParser#varDeclaration.
    def enterVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#varDeclaration.
    def exitVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#varInit.
    def enterVarInit(self, ctx:CParser.VarInitContext):
        pass

    # Exit a parse tree produced by CParser#varInit.
    def exitVarInit(self, ctx:CParser.VarInitContext):
        pass


    # Enter a parse tree produced by CParser#varAssignment.
    def enterVarAssignment(self, ctx:CParser.VarAssignmentContext):
        pass

    # Exit a parse tree produced by CParser#varAssignment.
    def exitVarAssignment(self, ctx:CParser.VarAssignmentContext):
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


    # Enter a parse tree produced by CParser#unaryExpr.
    def enterUnaryExpr(self, ctx:CParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by CParser#unaryExpr.
    def exitUnaryExpr(self, ctx:CParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by CParser#finalExpr.
    def enterFinalExpr(self, ctx:CParser.FinalExprContext):
        pass

    # Exit a parse tree produced by CParser#finalExpr.
    def exitFinalExpr(self, ctx:CParser.FinalExprContext):
        pass


    # Enter a parse tree produced by CParser#typeDeclaration1.
    def enterTypeDeclaration1(self, ctx:CParser.TypeDeclaration1Context):
        pass

    # Exit a parse tree produced by CParser#typeDeclaration1.
    def exitTypeDeclaration1(self, ctx:CParser.TypeDeclaration1Context):
        pass


    # Enter a parse tree produced by CParser#typeDeclaration2.
    def enterTypeDeclaration2(self, ctx:CParser.TypeDeclaration2Context):
        pass

    # Exit a parse tree produced by CParser#typeDeclaration2.
    def exitTypeDeclaration2(self, ctx:CParser.TypeDeclaration2Context):
        pass


    # Enter a parse tree produced by CParser#constDeclaration.
    def enterConstDeclaration(self, ctx:CParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#constDeclaration.
    def exitConstDeclaration(self, ctx:CParser.ConstDeclarationContext):
        pass



del CParser