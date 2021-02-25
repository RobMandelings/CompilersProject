# Generated from C.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f")
        buf.write("\64\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3")
        buf.write("\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\5\3\27\n\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\7\3!\n\3\f\3\16\3$\13\3\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\5\4,\n\4\3\5\3\5\3\6\3\6\3\7\3\7\3\7\2")
        buf.write("\3\4\b\2\4\6\b\n\f\2\4\3\2\7\b\3\2\5\6\2\62\2\16\3\2\2")
        buf.write("\2\4\26\3\2\2\2\6+\3\2\2\2\b-\3\2\2\2\n/\3\2\2\2\f\61")
        buf.write("\3\2\2\2\16\17\5\4\3\2\17\20\7\t\2\2\20\3\3\2\2\2\21\22")
        buf.write("\b\3\1\2\22\23\5\n\6\2\23\24\5\6\4\2\24\27\3\2\2\2\25")
        buf.write("\27\5\6\4\2\26\21\3\2\2\2\26\25\3\2\2\2\27\"\3\2\2\2\30")
        buf.write("\31\f\5\2\2\31\32\5\f\7\2\32\33\5\4\3\6\33!\3\2\2\2\34")
        buf.write("\35\f\4\2\2\35\36\5\n\6\2\36\37\5\4\3\5\37!\3\2\2\2 \30")
        buf.write("\3\2\2\2 \34\3\2\2\2!$\3\2\2\2\" \3\2\2\2\"#\3\2\2\2#")
        buf.write("\5\3\2\2\2$\"\3\2\2\2%,\7\n\2\2&,\7\13\2\2\'(\7\3\2\2")
        buf.write("()\5\4\3\2)*\7\4\2\2*,\3\2\2\2+%\3\2\2\2+&\3\2\2\2+\'")
        buf.write("\3\2\2\2,\7\3\2\2\2-.\7\t\2\2.\t\3\2\2\2/\60\t\2\2\2\60")
        buf.write("\13\3\2\2\2\61\62\t\3\2\2\62\r\3\2\2\2\6\26 \"+")
        return buf.getvalue()


class CParser ( Parser ):

    grammarFileName = "C.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'*'", "'/'", "'+'", "'-'", 
                     "';'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "MUL", "DIV", 
                      "ADD", "SUB", "SEMICOLON", "ID", "DOUBLE", "WS" ]

    RULE_stat = 0
    RULE_expr = 1
    RULE_value = 2
    RULE_end_of_line = 3
    RULE_add = 4
    RULE_mult = 5

    ruleNames =  [ "stat", "expr", "value", "end_of_line", "add", "mult" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    MUL=3
    DIV=4
    ADD=5
    SUB=6
    SEMICOLON=7
    ID=8
    DOUBLE=9
    WS=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class StatContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CParser.ExprContext,0)


        def SEMICOLON(self):
            return self.getToken(CParser.SEMICOLON, 0)

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
        self.enterRule(localctx, 0, self.RULE_stat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.expr(0)
            self.state = 13
            self.match(CParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def add(self):
            return self.getTypedRuleContext(CParser.AddContext,0)


        def value(self):
            return self.getTypedRuleContext(CParser.ValueContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CParser.ExprContext)
            else:
                return self.getTypedRuleContext(CParser.ExprContext,i)


        def mult(self):
            return self.getTypedRuleContext(CParser.MultContext,0)


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



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CParser.ADD, CParser.SUB]:
                self.state = 16
                self.add()
                self.state = 17
                self.value()
                pass
            elif token in [CParser.T__0, CParser.ID, CParser.DOUBLE]:
                self.state = 19
                self.value()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 32
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 30
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = CParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 22
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 23
                        self.mult()
                        self.state = 24
                        self.expr(4)
                        pass

                    elif la_ == 2:
                        localctx = CParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 26
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 27
                        self.add()
                        self.state = 28
                        self.expr(3)
                        pass

             
                self.state = 34
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class ValueContext(ParserRuleContext):

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
            return CParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = CParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_value)
        try:
            self.state = 41
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 35
                self.match(CParser.ID)
                pass
            elif token in [CParser.DOUBLE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 36
                self.match(CParser.DOUBLE)
                pass
            elif token in [CParser.T__0]:
                self.enterOuterAlt(localctx, 3)
                self.state = 37
                self.match(CParser.T__0)
                self.state = 38
                self.expr(0)
                self.state = 39
                self.match(CParser.T__1)
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

    class End_of_lineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMICOLON(self):
            return self.getToken(CParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return CParser.RULE_end_of_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd_of_line" ):
                listener.enterEnd_of_line(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd_of_line" ):
                listener.exitEnd_of_line(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnd_of_line" ):
                return visitor.visitEnd_of_line(self)
            else:
                return visitor.visitChildren(self)




    def end_of_line(self):

        localctx = CParser.End_of_lineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_end_of_line)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.match(CParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AddContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD(self):
            return self.getToken(CParser.ADD, 0)

        def SUB(self):
            return self.getToken(CParser.SUB, 0)

        def getRuleIndex(self):
            return CParser.RULE_add

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdd" ):
                listener.enterAdd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdd" ):
                listener.exitAdd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdd" ):
                return visitor.visitAdd(self)
            else:
                return visitor.visitChildren(self)




    def add(self):

        localctx = CParser.AddContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_add)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            _la = self._input.LA(1)
            if not(_la==CParser.ADD or _la==CParser.SUB):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MultContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MUL(self):
            return self.getToken(CParser.MUL, 0)

        def DIV(self):
            return self.getToken(CParser.DIV, 0)

        def getRuleIndex(self):
            return CParser.RULE_mult

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMult" ):
                listener.enterMult(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMult" ):
                listener.exitMult(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMult" ):
                return visitor.visitMult(self)
            else:
                return visitor.visitChildren(self)




    def mult(self):

        localctx = CParser.MultContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_mult)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            _la = self._input.LA(1)
            if not(_la==CParser.MUL or _la==CParser.DIV):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
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
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         




