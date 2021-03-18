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


    # Enter a parse tree produced by CParser#singleLineStatement.
    def enterSingleLineStatement(self, ctx:CParser.SingleLineStatementContext):
        pass

    # Exit a parse tree produced by CParser#singleLineStatement.
    def exitSingleLineStatement(self, ctx:CParser.SingleLineStatementContext):
        pass


    # Enter a parse tree produced by CParser#scopedStatement.
    def enterScopedStatement(self, ctx:CParser.ScopedStatementContext):
        pass

    # Exit a parse tree produced by CParser#scopedStatement.
    def exitScopedStatement(self, ctx:CParser.ScopedStatementContext):
        pass


    # Enter a parse tree produced by CParser#loop.
    def enterLoop(self, ctx:CParser.LoopContext):
        pass

    # Exit a parse tree produced by CParser#loop.
    def exitLoop(self, ctx:CParser.LoopContext):
        pass


    # Enter a parse tree produced by CParser#ifStatement.
    def enterIfStatement(self, ctx:CParser.IfStatementContext):
        pass

    # Exit a parse tree produced by CParser#ifStatement.
    def exitIfStatement(self, ctx:CParser.IfStatementContext):
        pass


    # Enter a parse tree produced by CParser#elseStatement.
    def enterElseStatement(self, ctx:CParser.ElseStatementContext):
        pass

    # Exit a parse tree produced by CParser#elseStatement.
    def exitElseStatement(self, ctx:CParser.ElseStatementContext):
        pass


    # Enter a parse tree produced by CParser#scope.
    def enterScope(self, ctx:CParser.ScopeContext):
        pass

    # Exit a parse tree produced by CParser#scope.
    def exitScope(self, ctx:CParser.ScopeContext):
        pass


    # Enter a parse tree produced by CParser#controlFlowStatement.
    def enterControlFlowStatement(self, ctx:CParser.ControlFlowStatementContext):
        pass

    # Exit a parse tree produced by CParser#controlFlowStatement.
    def exitControlFlowStatement(self, ctx:CParser.ControlFlowStatementContext):
        pass


    # Enter a parse tree produced by CParser#printfStatement.
    def enterPrintfStatement(self, ctx:CParser.PrintfStatementContext):
        pass

    # Exit a parse tree produced by CParser#printfStatement.
    def exitPrintfStatement(self, ctx:CParser.PrintfStatementContext):
        pass


    # Enter a parse tree produced by CParser#varDeclaration.
    def enterVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#varDeclaration.
    def exitVarDeclaration(self, ctx:CParser.VarDeclarationContext):
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


    # Enter a parse tree produced by CParser#varDeclarationAndInit.
    def enterVarDeclarationAndInit(self, ctx:CParser.VarDeclarationAndInitContext):
        pass

    # Exit a parse tree produced by CParser#varDeclarationAndInit.
    def exitVarDeclarationAndInit(self, ctx:CParser.VarDeclarationAndInitContext):
        pass


    # Enter a parse tree produced by CParser#varAssignment.
    def enterVarAssignment(self, ctx:CParser.VarAssignmentContext):
        pass

    # Exit a parse tree produced by CParser#varAssignment.
    def exitVarAssignment(self, ctx:CParser.VarAssignmentContext):
        pass


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CParser#compareExpression.
    def enterCompareExpression(self, ctx:CParser.CompareExpressionContext):
        pass

    # Exit a parse tree produced by CParser#compareExpression.
    def exitCompareExpression(self, ctx:CParser.CompareExpressionContext):
        pass


    # Enter a parse tree produced by CParser#addExpression.
    def enterAddExpression(self, ctx:CParser.AddExpressionContext):
        pass

    # Exit a parse tree produced by CParser#addExpression.
    def exitAddExpression(self, ctx:CParser.AddExpressionContext):
        pass


    # Enter a parse tree produced by CParser#multExpression.
    def enterMultExpression(self, ctx:CParser.MultExpressionContext):
        pass

    # Exit a parse tree produced by CParser#multExpression.
    def exitMultExpression(self, ctx:CParser.MultExpressionContext):
        pass


    # Enter a parse tree produced by CParser#unaryExpression.
    def enterUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by CParser#unaryExpression.
    def exitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by CParser#pointerExpression.
    def enterPointerExpression(self, ctx:CParser.PointerExpressionContext):
        pass

    # Exit a parse tree produced by CParser#pointerExpression.
    def exitPointerExpression(self, ctx:CParser.PointerExpressionContext):
        pass


    # Enter a parse tree produced by CParser#enclosedExpression.
    def enterEnclosedExpression(self, ctx:CParser.EnclosedExpressionContext):
        pass

    # Exit a parse tree produced by CParser#enclosedExpression.
    def exitEnclosedExpression(self, ctx:CParser.EnclosedExpressionContext):
        pass


    # Enter a parse tree produced by CParser#finalExpression.
    def enterFinalExpression(self, ctx:CParser.FinalExpressionContext):
        pass

    # Exit a parse tree produced by CParser#finalExpression.
    def exitFinalExpression(self, ctx:CParser.FinalExpressionContext):
        pass



del CParser