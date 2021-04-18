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


    # Enter a parse tree produced by CParser#functionStatement.
    def enterFunctionStatement(self, ctx:CParser.FunctionStatementContext):
        pass

    # Exit a parse tree produced by CParser#functionStatement.
    def exitFunctionStatement(self, ctx:CParser.FunctionStatementContext):
        pass


    # Enter a parse tree produced by CParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:CParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:CParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by CParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
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


    # Enter a parse tree produced by CParser#functionCall.
    def enterFunctionCall(self, ctx:CParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by CParser#functionCall.
    def exitFunctionCall(self, ctx:CParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by CParser#controlFlowStatement.
    def enterControlFlowStatement(self, ctx:CParser.ControlFlowStatementContext):
        pass

    # Exit a parse tree produced by CParser#controlFlowStatement.
    def exitControlFlowStatement(self, ctx:CParser.ControlFlowStatementContext):
        pass


    # Enter a parse tree produced by CParser#returnStatement.
    def enterReturnStatement(self, ctx:CParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by CParser#returnStatement.
    def exitReturnStatement(self, ctx:CParser.ReturnStatementContext):
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


    # Enter a parse tree produced by CParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx:CParser.ArrayDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#arrayDeclaration.
    def exitArrayDeclaration(self, ctx:CParser.ArrayDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:CParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:CParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#varDeclarationAndInit.
    def enterVarDeclarationAndInit(self, ctx:CParser.VarDeclarationAndInitContext):
        pass

    # Exit a parse tree produced by CParser#varDeclarationAndInit.
    def exitVarDeclarationAndInit(self, ctx:CParser.VarDeclarationAndInitContext):
        pass


    # Enter a parse tree produced by CParser#assignment.
    def enterAssignment(self, ctx:CParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CParser#assignment.
    def exitAssignment(self, ctx:CParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CParser#arrayDeclarationAndInit.
    def enterArrayDeclarationAndInit(self, ctx:CParser.ArrayDeclarationAndInitContext):
        pass

    # Exit a parse tree produced by CParser#arrayDeclarationAndInit.
    def exitArrayDeclarationAndInit(self, ctx:CParser.ArrayDeclarationAndInitContext):
        pass


    # Enter a parse tree produced by CParser#accessArrayElement.
    def enterAccessArrayElement(self, ctx:CParser.AccessArrayElementContext):
        pass

    # Exit a parse tree produced by CParser#accessArrayElement.
    def exitAccessArrayElement(self, ctx:CParser.AccessArrayElementContext):
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


    # Enter a parse tree produced by CParser#dataType.
    def enterDataType(self, ctx:CParser.DataTypeContext):
        pass

    # Exit a parse tree produced by CParser#dataType.
    def exitDataType(self, ctx:CParser.DataTypeContext):
        pass


    # Enter a parse tree produced by CParser#value.
    def enterValue(self, ctx:CParser.ValueContext):
        pass

    # Exit a parse tree produced by CParser#value.
    def exitValue(self, ctx:CParser.ValueContext):
        pass



del CParser