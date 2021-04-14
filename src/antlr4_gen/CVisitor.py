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


    # Visit a parse tree produced by CParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:CParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#singleLineStatement.
    def visitSingleLineStatement(self, ctx:CParser.SingleLineStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#scopedStatement.
    def visitScopedStatement(self, ctx:CParser.ScopedStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#loop.
    def visitLoop(self, ctx:CParser.LoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#ifStatement.
    def visitIfStatement(self, ctx:CParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#elseStatement.
    def visitElseStatement(self, ctx:CParser.ElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#scope.
    def visitScope(self, ctx:CParser.ScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionCall.
    def visitFunctionCall(self, ctx:CParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#controlFlowStatement.
    def visitControlFlowStatement(self, ctx:CParser.ControlFlowStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#returnStatement.
    def visitReturnStatement(self, ctx:CParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#printfStatement.
    def visitPrintfStatement(self, ctx:CParser.PrintfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#varDeclaration.
    def visitVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:CParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#varDeclarationAndInit.
    def visitVarDeclarationAndInit(self, ctx:CParser.VarDeclarationAndInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#varAssignment.
    def visitVarAssignment(self, ctx:CParser.VarAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compareExpression.
    def visitCompareExpression(self, ctx:CParser.CompareExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#addExpression.
    def visitAddExpression(self, ctx:CParser.AddExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multExpression.
    def visitMultExpression(self, ctx:CParser.MultExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#pointerExpression.
    def visitPointerExpression(self, ctx:CParser.PointerExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enclosedExpression.
    def visitEnclosedExpression(self, ctx:CParser.EnclosedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#finalExpression.
    def visitFinalExpression(self, ctx:CParser.FinalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#dataType.
    def visitDataType(self, ctx:CParser.DataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#value.
    def visitValue(self, ctx:CParser.ValueContext):
        return self.visitChildren(ctx)



del CParser