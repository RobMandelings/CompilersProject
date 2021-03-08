# Generated from C.g4 by ANTLR 4.9.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\25")
        buf.write("f\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\3\2\6\2\26\n\2\r\2\16\2\27\3\3\3")
        buf.write("\3\3\3\3\3\5\3\36\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6\64")
        buf.write("\n\6\f\6\16\6\67\13\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\7\7B\n\7\f\7\16\7E\13\7\3\b\3\b\3\b\3\b\3\b\3\b\3")
        buf.write("\b\3\b\3\b\7\bP\n\b\f\b\16\bS\13\b\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\5\t\\\n\t\3\n\3\n\3\n\3\n\3\n\3\n\5\nd\n\n\3")
        buf.write("\n\2\5\n\f\16\13\2\4\6\b\n\f\16\20\22\2\2\2l\2\25\3\2")
        buf.write("\2\2\4\35\3\2\2\2\6\37\3\2\2\2\b%\3\2\2\2\n\'\3\2\2\2")
        buf.write("\f8\3\2\2\2\16F\3\2\2\2\20[\3\2\2\2\22c\3\2\2\2\24\26")
        buf.write("\5\4\3\2\25\24\3\2\2\2\26\27\3\2\2\2\27\25\3\2\2\2\27")
        buf.write("\30\3\2\2\2\30\3\3\2\2\2\31\36\5\6\4\2\32\33\5\b\5\2\33")
        buf.write("\34\7\3\2\2\34\36\3\2\2\2\35\31\3\2\2\2\35\32\3\2\2\2")
        buf.write("\36\5\3\2\2\2\37 \5\22\n\2 !\7\22\2\2!\"\7\4\2\2\"#\5")
        buf.write("\b\5\2#$\7\3\2\2$\7\3\2\2\2%&\5\n\6\2&\t\3\2\2\2\'(\b")
        buf.write("\6\1\2()\5\f\7\2)\65\3\2\2\2*+\f\6\2\2+,\7\5\2\2,\64\5")
        buf.write("\f\7\2-.\f\5\2\2./\7\6\2\2/\64\5\f\7\2\60\61\f\4\2\2\61")
        buf.write("\62\7\7\2\2\62\64\5\f\7\2\63*\3\2\2\2\63-\3\2\2\2\63\60")
        buf.write("\3\2\2\2\64\67\3\2\2\2\65\63\3\2\2\2\65\66\3\2\2\2\66")
        buf.write("\13\3\2\2\2\67\65\3\2\2\289\b\7\1\29:\5\16\b\2:C\3\2\2")
        buf.write("\2;<\f\5\2\2<=\7\b\2\2=B\5\16\b\2>?\f\4\2\2?@\7\t\2\2")
        buf.write("@B\5\16\b\2A;\3\2\2\2A>\3\2\2\2BE\3\2\2\2CA\3\2\2\2CD")
        buf.write("\3\2\2\2D\r\3\2\2\2EC\3\2\2\2FG\b\b\1\2GH\5\20\t\2HQ\3")
        buf.write("\2\2\2IJ\f\5\2\2JK\7\n\2\2KP\5\20\t\2LM\f\4\2\2MN\7\13")
        buf.write("\2\2NP\5\20\t\2OI\3\2\2\2OL\3\2\2\2PS\3\2\2\2QO\3\2\2")
        buf.write("\2QR\3\2\2\2R\17\3\2\2\2SQ\3\2\2\2T\\\7\22\2\2U\\\7\24")
        buf.write("\2\2V\\\7\23\2\2WX\7\f\2\2XY\5\b\5\2YZ\7\r\2\2Z\\\3\2")
        buf.write("\2\2[T\3\2\2\2[U\3\2\2\2[V\3\2\2\2[W\3\2\2\2\\\21\3\2")
        buf.write("\2\2]d\3\2\2\2^_\7\16\2\2_d\5\22\n\2`d\7\17\2\2ad\7\20")
        buf.write("\2\2bd\7\21\2\2c]\3\2\2\2c^\3\2\2\2c`\3\2\2\2ca\3\2\2")
        buf.write("\2cb\3\2\2\2d\23\3\2\2\2\f\27\35\63\65ACOQ[c")
        return buf.getvalue()


class CParser ( Parser ):

    grammarFileName = "C.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'='", "'>'", "'<'", "'=='", "'+'", 
                     "'-'", "'*'", "'/'", "'('", "')'", "'const'", "'int'", 
                     "'char'", "'float'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "ID", "INTEGER", "DOUBLE", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_varDeclaration = 2
    RULE_expr = 3
    RULE_compareExpr = 4
    RULE_addExpr = 5
    RULE_multExpr = 6
    RULE_finalExpr = 7
    RULE_typeDeclaration = 8

    ruleNames =  [ "program", "statement", "varDeclaration", "expr", "compareExpr", 
                   "addExpr", "multExpr", "finalExpr", "typeDeclaration" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    ID=16
    INTEGER=17
    DOUBLE=18
    WS=19

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CParser.StatementContext)
            else:
                return self.getTypedRuleContext(CParser.StatementContext,i)


        def getRuleIndex(self):
            return CParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = CParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 18
                self.statement()
                self.state = 21 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CParser.T__9) | (1 << CParser.T__11) | (1 << CParser.T__12) | (1 << CParser.T__13) | (1 << CParser.T__14) | (1 << CParser.ID) | (1 << CParser.INTEGER) | (1 << CParser.DOUBLE))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varDeclaration(self):
            return self.getTypedRuleContext(CParser.VarDeclarationContext,0)


        def expr(self):
            return self.getTypedRuleContext(CParser.ExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = CParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 27
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 23
                self.varDeclaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                self.expr()
                self.state = 25
                self.match(CParser.T__0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeDeclaration(self):
            return self.getTypedRuleContext(CParser.TypeDeclarationContext,0)


        def ID(self):
            return self.getToken(CParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(CParser.ExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_varDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDeclaration" ):
                listener.enterVarDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDeclaration" ):
                listener.exitVarDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDeclaration" ):
                return visitor.visitVarDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def varDeclaration(self):

        localctx = CParser.VarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.typeDeclaration()
            self.state = 30
            self.match(CParser.ID)
            self.state = 31
            self.match(CParser.T__1)
            self.state = 32
            self.expr()
            self.state = 33
            self.match(CParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def compareExpr(self):
            return self.getTypedRuleContext(CParser.CompareExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = CParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.compareExpr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompareExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addExpr(self):
            return self.getTypedRuleContext(CParser.AddExprContext,0)


        def compareExpr(self):
            return self.getTypedRuleContext(CParser.CompareExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_compareExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompareExpr" ):
                listener.enterCompareExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompareExpr" ):
                listener.exitCompareExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompareExpr" ):
                return visitor.visitCompareExpr(self)
            else:
                return visitor.visitChildren(self)



    def compareExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CParser.CompareExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_compareExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.addExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 51
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 49
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = CParser.CompareExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_compareExpr)
                        self.state = 40
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 41
                        self.match(CParser.T__2)
                        self.state = 42
                        self.addExpr(0)
                        pass

                    elif la_ == 2:
                        localctx = CParser.CompareExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_compareExpr)
                        self.state = 43
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 44
                        self.match(CParser.T__3)
                        self.state = 45
                        self.addExpr(0)
                        pass

                    elif la_ == 3:
                        localctx = CParser.CompareExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_compareExpr)
                        self.state = 46
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 47
                        self.match(CParser.T__4)
                        self.state = 48
                        self.addExpr(0)
                        pass

             
                self.state = 53
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AddExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multExpr(self):
            return self.getTypedRuleContext(CParser.MultExprContext,0)


        def addExpr(self):
            return self.getTypedRuleContext(CParser.AddExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_addExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddExpr" ):
                listener.enterAddExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddExpr" ):
                listener.exitAddExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddExpr" ):
                return visitor.visitAddExpr(self)
            else:
                return visitor.visitChildren(self)



    def addExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CParser.AddExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_addExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.multExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 65
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 63
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = CParser.AddExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_addExpr)
                        self.state = 57
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 58
                        self.match(CParser.T__5)
                        self.state = 59
                        self.multExpr(0)
                        pass

                    elif la_ == 2:
                        localctx = CParser.AddExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_addExpr)
                        self.state = 60
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 61
                        self.match(CParser.T__6)
                        self.state = 62
                        self.multExpr(0)
                        pass

             
                self.state = 67
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class MultExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def finalExpr(self):
            return self.getTypedRuleContext(CParser.FinalExprContext,0)


        def multExpr(self):
            return self.getTypedRuleContext(CParser.MultExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_multExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultExpr" ):
                listener.enterMultExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultExpr" ):
                listener.exitMultExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultExpr" ):
                return visitor.visitMultExpr(self)
            else:
                return visitor.visitChildren(self)



    def multExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CParser.MultExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 12
        self.enterRecursionRule(localctx, 12, self.RULE_multExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.finalExpr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 79
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 77
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                    if la_ == 1:
                        localctx = CParser.MultExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_multExpr)
                        self.state = 71
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 72
                        self.match(CParser.T__7)
                        self.state = 73
                        self.finalExpr()
                        pass

                    elif la_ == 2:
                        localctx = CParser.MultExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_multExpr)
                        self.state = 74
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 75
                        self.match(CParser.T__8)
                        self.state = 76
                        self.finalExpr()
                        pass

             
                self.state = 81
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class FinalExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CParser.ID, 0)

        def DOUBLE(self):
            return self.getToken(CParser.DOUBLE, 0)

        def INTEGER(self):
            return self.getToken(CParser.INTEGER, 0)

        def expr(self):
            return self.getTypedRuleContext(CParser.ExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_finalExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFinalExpr" ):
                listener.enterFinalExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFinalExpr" ):
                listener.exitFinalExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFinalExpr" ):
                return visitor.visitFinalExpr(self)
            else:
                return visitor.visitChildren(self)




    def finalExpr(self):

        localctx = CParser.FinalExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_finalExpr)
        try:
            self.state = 89
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 82
                self.match(CParser.ID)
                pass
            elif token in [CParser.DOUBLE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 83
                self.match(CParser.DOUBLE)
                pass
            elif token in [CParser.INTEGER]:
                self.enterOuterAlt(localctx, 3)
                self.state = 84
                self.match(CParser.INTEGER)
                pass
            elif token in [CParser.T__9]:
                self.enterOuterAlt(localctx, 4)
                self.state = 85
                self.match(CParser.T__9)
                self.state = 86
                self.expr()
                self.state = 87
                self.match(CParser.T__10)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeDeclaration(self):
            return self.getTypedRuleContext(CParser.TypeDeclarationContext,0)


        def getRuleIndex(self):
            return CParser.RULE_typeDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeDeclaration" ):
                listener.enterTypeDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeDeclaration" ):
                listener.exitTypeDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeDeclaration" ):
                return visitor.visitTypeDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def typeDeclaration(self):

        localctx = CParser.TypeDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_typeDeclaration)
        try:
            self.state = 97
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CParser.ID]:
                self.enterOuterAlt(localctx, 1)

                pass
            elif token in [CParser.T__11]:
                self.enterOuterAlt(localctx, 2)
                self.state = 92
                self.match(CParser.T__11)
                self.state = 93
                self.typeDeclaration()
                pass
            elif token in [CParser.T__12]:
                self.enterOuterAlt(localctx, 3)
                self.state = 94
                self.match(CParser.T__12)
                pass
            elif token in [CParser.T__13]:
                self.enterOuterAlt(localctx, 4)
                self.state = 95
                self.match(CParser.T__13)
                pass
            elif token in [CParser.T__14]:
                self.enterOuterAlt(localctx, 5)
                self.state = 96
                self.match(CParser.T__14)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[4] = self.compareExpr_sempred
        self._predicates[5] = self.addExpr_sempred
        self._predicates[6] = self.multExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def compareExpr_sempred(self, localctx:CompareExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

    def addExpr_sempred(self, localctx:AddExprContext, predIndex:int):
            if predIndex == 3:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         

    def multExpr_sempred(self, localctx:MultExprContext, predIndex:int):
            if predIndex == 5:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 2)
         




