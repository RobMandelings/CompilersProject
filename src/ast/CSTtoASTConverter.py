from antlr4.tree.Tree import TerminalNodeImpl

from src.CParser import *
from src.ast.ASTs import Token, ASTBinaryOperation, ASTLeaf


def createASTFromConcreteSyntaxTree(cst):
    assert isinstance(cst, ParserRuleContext)

    # Has just one child which is not a terminal node, so just pass the child in to create the AST
    if len(cst.children) == 1:
        if containsTerminalAsChild(cst):
            return ASTLeaf(Token(cst.children[0]))
        else:
            return createASTFromConcreteSyntaxTree(cst.children[0])
    else:

        print(cst)

        if isinstance(cst, CParser.StatContext):
            return createASTFromConcreteSyntaxTree(cst.children[0])
        else:

            if isBinaryExpression(cst):

                token = Token(cst.children[1])
                return ASTBinaryOperation(token, createASTFromConcreteSyntaxTree(cst.children[0]),
                                          createASTFromConcreteSyntaxTree(cst.children[2]))


def containsTerminalAsChild(cst):
    assert isinstance(cst, ParserRuleContext)

    for child in cst.children:
        if isinstance(child, TerminalNodeImpl):
            return True

    return False


def isBinaryExpression(cst):
    assert isinstance(cst, ParserRuleContext)
    if cst.children == 3 and isinstance(cst.children[1], TerminalNodeImpl):
        text = cst.children[1].symbol.text
        if text == '+' or text == '-' or text == '/' or text == '*':
            return True, text

    return False, None
