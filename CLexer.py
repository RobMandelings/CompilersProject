# Generated from C.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\f")
        buf.write("D\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\3\3\3\3\4")
        buf.write("\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\6\t\'\n\t\r\t")
        buf.write("\16\t(\3\t\7\t,\n\t\f\t\16\t/\13\t\3\n\6\n\62\n\n\r\n")
        buf.write("\16\n\63\3\n\3\n\6\n8\n\n\r\n\16\n9\5\n<\n\n\3\13\6\13")
        buf.write("?\n\13\r\13\16\13@\3\13\3\13\2\2\f\3\3\5\4\7\5\t\6\13")
        buf.write("\7\r\b\17\t\21\n\23\13\25\f\3\2\5\4\2C\\c|\3\2\62;\5\2")
        buf.write("\13\f\17\17\"\"\2I\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2")
        buf.write("\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21")
        buf.write("\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\3\27\3\2\2\2\5\31\3")
        buf.write("\2\2\2\7\33\3\2\2\2\t\35\3\2\2\2\13\37\3\2\2\2\r!\3\2")
        buf.write("\2\2\17#\3\2\2\2\21&\3\2\2\2\23\61\3\2\2\2\25>\3\2\2\2")
        buf.write("\27\30\7*\2\2\30\4\3\2\2\2\31\32\7+\2\2\32\6\3\2\2\2\33")
        buf.write("\34\7,\2\2\34\b\3\2\2\2\35\36\7\61\2\2\36\n\3\2\2\2\37")
        buf.write(" \7-\2\2 \f\3\2\2\2!\"\7/\2\2\"\16\3\2\2\2#$\7=\2\2$\20")
        buf.write("\3\2\2\2%\'\t\2\2\2&%\3\2\2\2\'(\3\2\2\2(&\3\2\2\2()\3")
        buf.write("\2\2\2)-\3\2\2\2*,\t\3\2\2+*\3\2\2\2,/\3\2\2\2-+\3\2\2")
        buf.write("\2-.\3\2\2\2.\22\3\2\2\2/-\3\2\2\2\60\62\t\3\2\2\61\60")
        buf.write("\3\2\2\2\62\63\3\2\2\2\63\61\3\2\2\2\63\64\3\2\2\2\64")
        buf.write(";\3\2\2\2\65\67\7\60\2\2\668\t\3\2\2\67\66\3\2\2\289\3")
        buf.write("\2\2\29\67\3\2\2\29:\3\2\2\2:<\3\2\2\2;\65\3\2\2\2;<\3")
        buf.write("\2\2\2<\24\3\2\2\2=?\t\4\2\2>=\3\2\2\2?@\3\2\2\2@>\3\2")
        buf.write("\2\2@A\3\2\2\2AB\3\2\2\2BC\b\13\2\2C\26\3\2\2\2\t\2(-")
        buf.write("\639;@\3\b\2\2")
        return buf.getvalue()


class CLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    MUL = 3
    DIV = 4
    ADD = 5
    SUB = 6
    SEMICOLON = 7
    ID = 8
    DOUBLE = 9
    WS = 10

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'*'", "'/'", "'+'", "'-'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "MUL", "DIV", "ADD", "SUB", "SEMICOLON", "ID", "DOUBLE", "WS" ]

    ruleNames = [ "T__0", "T__1", "MUL", "DIV", "ADD", "SUB", "SEMICOLON", 
                  "ID", "DOUBLE", "WS" ]

    grammarFileName = "C.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


