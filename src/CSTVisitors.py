from antlr4.tree.Tree import TerminalNodeImpl
from graphviz import Digraph

from antlr4_gen.CVisitor import CVisitor
from src.antlr4_gen.CParser import CParser


class CSTVisitorToDot(CVisitor):

    def __init__(self):
        self.graph = Digraph('Concrete Syntax Tree')

    def toDotCurrent(self, ctx):
        if isinstance(ctx, TerminalNodeImpl):
            self.graph.node(str(id(ctx)), ctx.symbol.text)
        else:
            self.graph.node(str(id(ctx)), type(ctx).__name__)
        if ctx.parentCtx is not None:
            self.graph.edge(str(id(ctx.parentCtx)), str(id(ctx)))

    def visitProgram(self, ctx: CParser.ProgramContext):
        self.toDotCurrent(ctx)
        return super().visitProgram(ctx)

    def visitVarDeclaration(self, ctx: CParser.VarDeclarationContext):
        self.toDotCurrent(ctx)
        return super().visitVarDeclaration(ctx)

    def visitExpression(self, ctx: CParser.ExpressionContext):
        self.toDotCurrent(ctx)
        return super().visitExpression(ctx)

    def visitCompareExpression(self, ctx: CParser.CompareExpressionContext):
        self.toDotCurrent(ctx)
        return super().visitCompareExpression(ctx)

    def visitAddExpression(self, ctx: CParser.AddExpressionContext):
        self.toDotCurrent(ctx)
        return super().visitAddExpression(ctx)

    def visitMultExpression(self, ctx: CParser.MultExpressionContext):
        self.toDotCurrent(ctx)
        return super().visitMultExpression(ctx)

    def visitFinalExpression(self, ctx: CParser.FinalExpressionContext):
        self.toDotCurrent(ctx)
        return super().visitFinalExpression(ctx)

    def visitTypeDeclaration1(self, ctx: CParser.TypeDeclaration1Context):
        self.toDotCurrent(ctx)
        return super().visitTypeDeclaration1(ctx)

    def visitTypeDeclaration2(self, ctx: CParser.TypeDeclaration2Context):
        self.toDotCurrent(ctx)
        return super().visitTypeDeclaration2(ctx)

    def visitConstDeclaration(self, ctx: CParser.ConstDeclarationContext):
        self.toDotCurrent(ctx)
        return super().visitConstDeclaration(ctx)

    def visitVarAssignment(self, ctx: CParser.VarAssignmentContext):
        self.toDotCurrent(ctx)
        return super().visitVarAssignment(ctx)

    def visitTerminal(self, node):
        self.toDotCurrent(node)
        return super().visitTerminal(node)

    def visitUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        self.toDotCurrent(ctx)
        return super().visitUnaryExpression(ctx)

    def visitPointerExpression(self, ctx: CParser.PointerExpressionContext):
        self.toDotCurrent(ctx)
        return super().visitPointerExpression(ctx)

    def visitPrintfStatement(self, ctx: CParser.PrintfStatementContext):
        self.toDotCurrent(ctx)
        return super().visitPrintfStatement(ctx)
