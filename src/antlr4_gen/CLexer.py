# Generated from C.g4 by ANTLR 4.9.1
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\20")
        buf.write("V\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\5\3")
        buf.write("\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\6")
        buf.write("\f\66\n\f\r\f\16\f\67\3\f\7\f;\n\f\f\f\16\f>\13\f\3\r")
        buf.write("\6\rA\n\r\r\r\16\rB\3\16\6\16F\n\16\r\16\16\16G\3\16\3")
        buf.write("\16\6\16L\n\16\r\16\16\16M\3\17\6\17Q\n\17\r\17\16\17")
        buf.write("R\3\17\3\17\2\2\20\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n")
        buf.write("\23\13\25\f\27\r\31\16\33\17\35\20\3\2\5\4\2C\\c|\3\2")
        buf.write("\62;\5\2\13\f\17\17\"\"\2[\2\3\3\2\2\2\2\5\3\2\2\2\2\7")
        buf.write("\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2")
        buf.write("\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2")
        buf.write("\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\3\37\3\2\2\2")
        buf.write("\5!\3\2\2\2\7#\3\2\2\2\t%\3\2\2\2\13(\3\2\2\2\r*\3\2\2")
        buf.write("\2\17,\3\2\2\2\21.\3\2\2\2\23\60\3\2\2\2\25\62\3\2\2\2")
        buf.write("\27\65\3\2\2\2\31@\3\2\2\2\33E\3\2\2\2\35P\3\2\2\2\37")
        buf.write(" \7=\2\2 \4\3\2\2\2!\"\7@\2\2\"\6\3\2\2\2#$\7>\2\2$\b")
        buf.write("\3\2\2\2%&\7?\2\2&\'\7?\2\2\'\n\3\2\2\2()\7-\2\2)\f\3")
        buf.write("\2\2\2*+\7/\2\2+\16\3\2\2\2,-\7,\2\2-\20\3\2\2\2./\7\61")
        buf.write("\2\2/\22\3\2\2\2\60\61\7*\2\2\61\24\3\2\2\2\62\63\7+\2")
        buf.write("\2\63\26\3\2\2\2\64\66\t\2\2\2\65\64\3\2\2\2\66\67\3\2")
        buf.write("\2\2\67\65\3\2\2\2\678\3\2\2\28<\3\2\2\29;\t\3\2\2:9\3")
        buf.write("\2\2\2;>\3\2\2\2<:\3\2\2\2<=\3\2\2\2=\30\3\2\2\2><\3\2")
        buf.write("\2\2?A\t\3\2\2@?\3\2\2\2AB\3\2\2\2B@\3\2\2\2BC\3\2\2\2")
        buf.write("C\32\3\2\2\2DF\t\3\2\2ED\3\2\2\2FG\3\2\2\2GE\3\2\2\2G")
        buf.write("H\3\2\2\2HI\3\2\2\2IK\7\60\2\2JL\t\3\2\2KJ\3\2\2\2LM\3")
        buf.write("\2\2\2MK\3\2\2\2MN\3\2\2\2N\34\3\2\2\2OQ\t\4\2\2PO\3\2")
        buf.write("\2\2QR\3\2\2\2RP\3\2\2\2RS\3\2\2\2ST\3\2\2\2TU\b\17\2")
        buf.write("\2U\36\3\2\2\2\t\2\67<BGMR\3\b\2\2")
        return buf.getvalue()


class CLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    ID = 11
    INTEGER = 12
    DOUBLE = 13
    WS = 14

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "'>'", "'<'", "'=='", "'+'", "'-'", "'*'", "'/'", "'('", 
            "')'" ]

    symbolicNames = [ "<INVALID>",
            "ID", "INTEGER", "DOUBLE", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "ID", "INTEGER", "DOUBLE", "WS" ]

    grammarFileName = "C.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


