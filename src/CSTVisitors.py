from antlr4.RuleContext import Parser
from graphviz import Digraph

from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4_gen.CVisitor import CVisitor
from src.antlr4_gen.CParser import CParser


class CSTVisitorToDot(CVisitor):

    def __init__(self):
        self.graph = Digraph('Concrete Syntax Tree')

    def toDotCurrent(self, ctx, name):
        if isinstance(ctx, TerminalNodeImpl):
            self.graph.node(str(id(ctx)), ctx.symbol.text)
        else:
            self.graph.node(str(id(ctx)), name)
        if ctx.parentCtx is not None:
            self.graph.edge(str(id(ctx.parentCtx)), str(id(ctx)))

    def visitProgram(self, ctx: CParser.ProgramContext):
        self.toDotCurrent(ctx, "ProgramContext")
        return super().visitProgram(ctx)

    def visitStatement(self, ctx: CParser.StatementContext):
        self.toDotCurrent(ctx, "StatementContext")
        return super().visitStatement(ctx)

    def visitVarDeclaration(self, ctx: CParser.VarDeclarationContext):
        self.toDotCurrent(ctx, "VarDeclarationContext")
        return super().visitVarDeclaration(ctx)

    def visitExpr(self, ctx: CParser.ExprContext):
        self.toDotCurrent(ctx, "ExprContext")
        return super().visitExpr(ctx)

    def visitCompareExpr(self, ctx: CParser.CompareExprContext):
        self.toDotCurrent(ctx, "CompareExprContext")
        return super().visitCompareExpr(ctx)

    def visitAddExpr(self, ctx: CParser.AddExprContext):
        self.toDotCurrent(ctx, "AddExprContext")
        return super().visitAddExpr(ctx)

    def visitMultExpr(self, ctx: CParser.MultExprContext):
        self.toDotCurrent(ctx, "MultExprContext")
        return super().visitMultExpr(ctx)

    def visitFinalExpr(self, ctx: CParser.FinalExprContext):
        self.toDotCurrent(ctx, "FinalExprContext")
        return super().visitFinalExpr(ctx)

    def visitTypeDeclaration1(self, ctx: CParser.TypeDeclaration1Context):
        self.toDotCurrent(ctx, "TypeDeclaration1")
        return super().visitTypeDeclaration1(ctx)

    def visitTypeDeclaration2(self, ctx: CParser.TypeDeclaration2Context):
        self.toDotCurrent(ctx, "TypeDeclaration2")
        return super().visitTypeDeclaration2(ctx)

    def visitConstDeclaration(self, ctx: CParser.ConstDeclarationContext):
        self.toDotCurrent(ctx, "ConstDeclaration")
        return super().visitConstDeclaration(ctx)

    def visitVarAssignment(self, ctx: CParser.VarAssignmentContext):
        self.toDotCurrent(ctx, "VarAssignment")
        return super().visitVarAssignment(ctx)

    def visitTerminal(self, node):
        self.toDotCurrent(node, "node")
        super().visitTerminal(node)
