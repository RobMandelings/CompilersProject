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


    # Enter a parse tree produced by CParser#includeStdio.
    def enterIncludeStdio(self, ctx:CParser.IncludeStdioContext):
        pass

    # Exit a parse tree produced by CParser#includeStdio.
    def exitIncludeStdio(self, ctx:CParser.IncludeStdioContext):
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


    # Enter a parse tree produced by CParser#whileLoop.
    def enterWhileLoop(self, ctx:CParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by CParser#whileLoop.
    def exitWhileLoop(self, ctx:CParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by CParser#forLoop.
    def enterForLoop(self, ctx:CParser.ForLoopContext):
        pass

    # Exit a parse tree produced by CParser#forLoop.
    def exitForLoop(self, ctx:CParser.ForLoopContext):
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


    # Enter a parse tree produced by CParser#multiVarDeclaration.
    def enterMultiVarDeclaration(self, ctx:CParser.MultiVarDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#multiVarDeclaration.
    def exitMultiVarDeclaration(self, ctx:CParser.MultiVarDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#singleVarDeclaration.
    def enterSingleVarDeclaration(self, ctx:CParser.SingleVarDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#singleVarDeclaration.
    def exitSingleVarDeclaration(self, ctx:CParser.SingleVarDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx:CParser.ArrayDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#arrayDeclaration.
    def exitArrayDeclaration(self, ctx:CParser.ArrayDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#varInitialization.
    def enterVarInitialization(self, ctx:CParser.VarInitializationContext):
        pass

    # Exit a parse tree produced by CParser#varInitialization.
    def exitVarInitialization(self, ctx:CParser.VarInitializationContext):
        pass


    # Enter a parse tree produced by CParser#normalVarDeclaration.
    def enterNormalVarDeclaration(self, ctx:CParser.NormalVarDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#normalVarDeclaration.
    def exitNormalVarDeclaration(self, ctx:CParser.NormalVarDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#arrayVarDeclaration.
    def enterArrayVarDeclaration(self, ctx:CParser.ArrayVarDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#arrayVarDeclaration.
    def exitArrayVarDeclaration(self, ctx:CParser.ArrayVarDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:CParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:CParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#charTypeDeclaration.
    def enterCharTypeDeclaration(self, ctx:CParser.CharTypeDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#charTypeDeclaration.
    def exitCharTypeDeclaration(self, ctx:CParser.CharTypeDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#varDeclarationAndInit.
    def enterVarDeclarationAndInit(self, ctx:CParser.VarDeclarationAndInitContext):
        pass

    # Exit a parse tree produced by CParser#varDeclarationAndInit.
    def exitVarDeclarationAndInit(self, ctx:CParser.VarDeclarationAndInitContext):
        pass


    # Enter a parse tree produced by CParser#normalVarDeclarationAndInit.
    def enterNormalVarDeclarationAndInit(self, ctx:CParser.NormalVarDeclarationAndInitContext):
        pass

    # Exit a parse tree produced by CParser#normalVarDeclarationAndInit.
    def exitNormalVarDeclarationAndInit(self, ctx:CParser.NormalVarDeclarationAndInitContext):
        pass


    # Enter a parse tree produced by CParser#arrayVarDeclarationAndInit.
    def enterArrayVarDeclarationAndInit(self, ctx:CParser.ArrayVarDeclarationAndInitContext):
        pass

    # Exit a parse tree produced by CParser#arrayVarDeclarationAndInit.
    def exitArrayVarDeclarationAndInit(self, ctx:CParser.ArrayVarDeclarationAndInitContext):
        pass


    # Enter a parse tree produced by CParser#braceInitializer.
    def enterBraceInitializer(self, ctx:CParser.BraceInitializerContext):
        pass

    # Exit a parse tree produced by CParser#braceInitializer.
    def exitBraceInitializer(self, ctx:CParser.BraceInitializerContext):
        pass


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CParser#functionCallExpression.
    def enterFunctionCallExpression(self, ctx:CParser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by CParser#functionCallExpression.
    def exitFunctionCallExpression(self, ctx:CParser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by CParser#accessArrayVarExpression.
    def enterAccessArrayVarExpression(self, ctx:CParser.AccessArrayVarExpressionContext):
        pass

    # Exit a parse tree produced by CParser#accessArrayVarExpression.
    def exitAccessArrayVarExpression(self, ctx:CParser.AccessArrayVarExpressionContext):
        pass


    # Enter a parse tree produced by CParser#compareExpression.
    def enterCompareExpression(self, ctx:CParser.CompareExpressionContext):
        pass

    # Exit a parse tree produced by CParser#compareExpression.
    def exitCompareExpression(self, ctx:CParser.CompareExpressionContext):
        pass


    # Enter a parse tree produced by CParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by CParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
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


    # Enter a parse tree produced by CParser#identifierExpression.
    def enterIdentifierExpression(self, ctx:CParser.IdentifierExpressionContext):
        pass

    # Exit a parse tree produced by CParser#identifierExpression.
    def exitIdentifierExpression(self, ctx:CParser.IdentifierExpressionContext):
        pass


    # Enter a parse tree produced by CParser#typeAttributes.
    def enterTypeAttributes(self, ctx:CParser.TypeAttributesContext):
        pass

    # Exit a parse tree produced by CParser#typeAttributes.
    def exitTypeAttributes(self, ctx:CParser.TypeAttributesContext):
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