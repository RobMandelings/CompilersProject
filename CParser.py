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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f")
        buf.write("=\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\6\2\20\n\2\r\2\16\2\21\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\3\5\7\5\"\n\5\f\5\16\5%\13\5\3")
        buf.write("\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6\60\n\6\f\6\16\6")
        buf.write("\63\13\6\3\7\3\7\3\7\3\7\3\7\3\7\5\7;\n\7\3\7\2\4\b\n")
        buf.write("\b\2\4\6\b\n\f\2\2\2=\2\17\3\2\2\2\4\23\3\2\2\2\6\26\3")
        buf.write("\2\2\2\b\30\3\2\2\2\n&\3\2\2\2\f:\3\2\2\2\16\20\5\4\3")
        buf.write("\2\17\16\3\2\2\2\20\21\3\2\2\2\21\17\3\2\2\2\21\22\3\2")
        buf.write("\2\2\22\3\3\2\2\2\23\24\5\6\4\2\24\25\7\3\2\2\25\5\3\2")
        buf.write("\2\2\26\27\5\b\5\2\27\7\3\2\2\2\30\31\b\5\1\2\31\32\5")
        buf.write("\n\6\2\32#\3\2\2\2\33\34\f\5\2\2\34\35\7\4\2\2\35\"\5")
        buf.write("\n\6\2\36\37\f\4\2\2\37 \7\5\2\2 \"\5\n\6\2!\33\3\2\2")
        buf.write("\2!\36\3\2\2\2\"%\3\2\2\2#!\3\2\2\2#$\3\2\2\2$\t\3\2\2")
        buf.write("\2%#\3\2\2\2&\'\b\6\1\2\'(\5\f\7\2(\61\3\2\2\2)*\f\5\2")
        buf.write("\2*+\7\6\2\2+\60\5\f\7\2,-\f\4\2\2-.\7\7\2\2.\60\5\f\7")
        buf.write("\2/)\3\2\2\2/,\3\2\2\2\60\63\3\2\2\2\61/\3\2\2\2\61\62")
        buf.write("\3\2\2\2\62\13\3\2\2\2\63\61\3\2\2\2\64;\7\n\2\2\65;\7")
        buf.write("\13\2\2\66\67\7\b\2\2\678\5\6\4\289\7\t\2\29;\3\2\2\2")
        buf.write(":\64\3\2\2\2:\65\3\2\2\2:\66\3\2\2\2;\r\3\2\2\2\b\21!")
        buf.write("#/\61:")
        return buf.getvalue()


class CParser ( Parser ):

    grammarFileName = "C.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'+'", "'-'", "'*'", "'/'", "'('", 
                     "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "ID", "DOUBLE", "WS" ]

    RULE_prog = 0
    RULE_stat = 1
    RULE_expr = 2
    RULE_addExpr = 3
    RULE_multExpr = 4
    RULE_finalExpr = 5

    ruleNames =  [ "prog", "stat", "expr", "addExpr", "multExpr", "finalExpr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    ID=8
    DOUBLE=9
    WS=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CParser.StatContext)
            else:
                return self.getTypedRuleContext(CParser.StatContext,i)


        def getRuleIndex(self):
            return CParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProg" ):
                return visitor.visitProg(self)
            else:
                return visitor.visitChildren(self)




    def prog(self):

        localctx = CParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.stat()
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CParser.T__5) | (1 << CParser.ID) | (1 << CParser.DOUBLE))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CParser.ExprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_stat

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStat" ):
                listener.enterStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStat" ):
                listener.exitStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStat" ):
                return visitor.visitStat(self)
            else:
                return visitor.visitChildren(self)




    def stat(self):

        localctx = CParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.expr()
            self.state = 18
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

        def addExpr(self):
            return self.getTypedRuleContext(CParser.AddExprContext,0)


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
        self.enterRule(localctx, 4, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.addExpr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
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
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_addExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.multExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 33
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 31
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = CParser.AddExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_addExpr)
                        self.state = 25
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 26
                        self.match(CParser.T__1)
                        self.state = 27
                        self.multExpr(0)
                        pass

                    elif la_ == 2:
                        localctx = CParser.AddExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_addExpr)
                        self.state = 28
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 29
                        self.match(CParser.T__2)
                        self.state = 30
                        self.multExpr(0)
                        pass

             
                self.state = 35
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

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
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_multExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.finalExpr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 47
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 45
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = CParser.MultExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_multExpr)
                        self.state = 39
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 40
                        self.match(CParser.T__3)
                        self.state = 41
                        self.finalExpr()
                        pass

                    elif la_ == 2:
                        localctx = CParser.MultExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_multExpr)
                        self.state = 42
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 43
                        self.match(CParser.T__4)
                        self.state = 44
                        self.finalExpr()
                        pass

             
                self.state = 49
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

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
        self.enterRule(localctx, 10, self.RULE_finalExpr)
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.match(CParser.ID)
                pass
            elif token in [CParser.DOUBLE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 51
                self.match(CParser.DOUBLE)
                pass
            elif token in [CParser.T__5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 52
                self.match(CParser.T__5)
                self.state = 53
                self.expr()
                self.state = 54
                self.match(CParser.T__6)
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
        self._predicates[3] = self.addExpr_sempred
        self._predicates[4] = self.multExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def addExpr_sempred(self, localctx:AddExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

    def multExpr_sempred(self, localctx:MultExprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         




