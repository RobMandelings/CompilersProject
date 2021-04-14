from antlr4.tree.Tree import TerminalNodeImpl
from graphviz import Digraph

from antlr4_gen.CVisitor import CVisitor
from src.antlr4_gen.CParser import CParser


class CSTVisitorToDot(CVisitor):

    def __init__(self):
        self.graph = Digraph('Concrete Syntax Tree')

    def to_dot_current(self, ctx):
        if isinstance(ctx, TerminalNodeImpl):
            self.graph.node(str(id(ctx)), ctx.symbol.text)
        else:
            self.graph.node(str(id(ctx)), type(ctx).__name__)
        if ctx.parentCtx is not None:
            self.graph.edge(str(id(ctx.parentCtx)), str(id(ctx)))

    # Visit any node in the concrete syntax tree to create a dot node
    def visit_node(self, ctx):
        self.to_dot_current(ctx)
        return super().visitChildren(ctx)

    def visitProgram(self, ctx: CParser.ProgramContext):
        self.visit_node(ctx)

    def visitStatement(self, ctx: CParser.StatementContext):
        self.visit_node(ctx)

    def visitSingleLineStatement(self, ctx: CParser.SingleLineStatementContext):
        self.visit_node(ctx)

    def visitScopedStatement(self, ctx: CParser.ScopedStatementContext):
        self.visit_node(ctx)

    def visitLoop(self, ctx: CParser.LoopContext):
        self.visit_node(ctx)

    def visitIfStatement(self, ctx: CParser.IfStatementContext):
        self.visit_node(ctx)

    def visitElseStatement(self, ctx: CParser.ElseStatementContext):
        self.visit_node(ctx)

    def visitScope(self, ctx: CParser.ScopeContext):
        self.visit_node(ctx)

    def visitControlFlowStatement(self, ctx: CParser.ControlFlowStatementContext):
        self.visit_node(ctx)

    def visitPrintfStatement(self, ctx: CParser.PrintfStatementContext):
        self.visit_node(ctx)

    def visitVarDeclaration(self, ctx: CParser.VarDeclarationContext):
        self.visit_node(ctx)

    def visitTypeDeclaration(self, ctx: CParser.TypeDeclarationContext):
        self.visit_node(ctx)

    def visitVarDeclarationAndInit(self, ctx: CParser.VarDeclarationAndInitContext):
        self.visit_node(ctx)

    def visitAssignment(self, ctx: CParser.AssignmentContext):
        self.visit_node(ctx)

    def visitArrayDeclaration(self, ctx: CParser.ArrayDeclarationContext):
        self.visit_node(ctx)

    def visitArrayDeclarationAndInit(self, ctx: CParser.ArrayDeclarationAndInitContext):
        self.visit_node(ctx)

    def visitAccessArrayElement(self, ctx: CParser.AccessArrayElementContext):
        self.visit_node(ctx)

    def visitExpression(self, ctx: CParser.ExpressionContext):
        self.visit_node(ctx)

    def visitCompareExpression(self, ctx: CParser.CompareExpressionContext):
        self.visit_node(ctx)

    def visitAddExpression(self, ctx: CParser.AddExpressionContext):
        self.visit_node(ctx)

    def visitMultExpression(self, ctx: CParser.MultExpressionContext):
        self.visit_node(ctx)

    def visitUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        self.visit_node(ctx)

    def visitPointerExpression(self, ctx: CParser.PointerExpressionContext):
        self.visit_node(ctx)

    def visitEnclosedExpression(self, ctx: CParser.EnclosedExpressionContext):
        self.visit_node(ctx)

    def visitFinalExpression(self, ctx: CParser.FinalExpressionContext):
        self.visit_node(ctx)

    def visitFunctionDeclaration(self, ctx: CParser.FunctionDeclarationContext):
        self.visit_node(ctx)

    def visitFunctionCall(self, ctx: CParser.FunctionCallContext):
        self.visit_node(ctx)

    def visitReturnStatement(self, ctx: CParser.ReturnStatementContext):
        self.visit_node(ctx)

    def visitDataType(self, ctx: CParser.DataTypeContext):
        self.visit_node(ctx)

    def visitValue(self, ctx: CParser.ValueContext):
        self.visit_node(ctx)

    def visitTerminal(self, node):
        self.to_dot_current(node)
        super().visitTerminal(node)
