from antlr4.RuleContext import Parser
from graphviz import Digraph

from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl
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

    def visitInstructions(self, ctx: CParser.InstructionsContext):
        self.toDotCurrent(ctx)
        return super().visitInstructions(ctx)

    def visitInstruction(self, ctx: CParser.InstructionContext):
        self.toDotCurrent(ctx)
        return super().visitInstruction(ctx)

    def visitVarDeclaration(self, ctx: CParser.VarDeclarationContext):
        self.toDotCurrent(ctx)
        return super().visitVarDeclaration(ctx)

    def visitExpr(self, ctx: CParser.ExprContext):
        self.toDotCurrent(ctx)
        return super().visitExpr(ctx)

    def visitCompareExpr(self, ctx: CParser.CompareExprContext):
        self.toDotCurrent(ctx)
        return super().visitCompareExpr(ctx)

    def visitAddExpr(self, ctx: CParser.AddExprContext):
        self.toDotCurrent(ctx)
        return super().visitAddExpr(ctx)

    def visitMultExpr(self, ctx: CParser.MultExprContext):
        self.toDotCurrent(ctx)
        return super().visitMultExpr(ctx)

    def visitFinalExpr(self, ctx: CParser.FinalExprContext):
        self.toDotCurrent(ctx)
        return super().visitFinalExpr(ctx)

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

    def visitVarInit(self, ctx: CParser.VarInitContext):
        self.toDotCurrent(ctx)
        return super().visitVarInit(ctx)

    def visitTerminal(self, node):
        self.toDotCurrent(node)
        return super().visitTerminal(node)

    def visitUnaryExpr(self, ctx: CParser.UnaryExprContext):
        self.toDotCurrent(ctx)
        return super().visitUnaryExpr(ctx)
