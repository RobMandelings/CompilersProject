from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *


def createASTFromConcreteSyntaxTree(cst, lexer: CLexer):
    assert isinstance(lexer, CLexer)

    if isinstance(cst, CParser.ProgramContext):
        ast_program = ASTInternal(ASTToken(TokenType.PROGRAM))
        appendChildASTsToAST(ast_program, cst, lexer)
        return ast_program
    elif isinstance(cst, CParser.StatementContext):
        ast_statement = ASTInternal(ASTToken(TokenType.STATEMENT))
        appendChildASTsToAST(ast_statement, cst, lexer)
        return ast_statement
    elif isinstance(cst, CParser.VarDeclarationContext):
        ast_variable_declaration = ASTInternal(ASTToken(TokenType.VARIABLE_DECLARATION))
        appendChildASTsToAST(ast_variable_declaration, cst, lexer)
        return ast_variable_declaration
    elif isinstance(cst, CParser.TypeDeclaration1Context):
        ast_type_declaration1 = ASTInternal(ASTToken(TokenType.TYPE_DECLARATION))
        appendChildASTsToAST(ast_type_declaration1, cst, lexer)
        return ast_type_declaration1
    elif isinstance(cst, TerminalNodeImpl):
        token = getTokenFromTerminalNode(cst, lexer)
        if token is None:
            print("Token is none for terminal: " + cst.symbol.text + ", no ast is created for this node")
            return None
        else:
            return ASTLeaf(getTokenFromTerminalNode(cst, lexer))
    else:

        if len(cst.children) == 1:
            # Just pass to the child
            return createASTFromConcreteSyntaxTree(cst.children[0], lexer)
        else:

            binary_expression, binary_operator_token = isBinaryExpression(cst)
            unary_expression, unary_operator_token = isUnaryExpression(cst)
            if binary_expression:
                ast_binary_expression = ASTInternal(binary_operator_token)
                ast_binary_expression.addChild(createASTFromConcreteSyntaxTree(cst.children[0], lexer))
                ast_binary_expression.addChild(createASTFromConcreteSyntaxTree(cst.children[2], lexer))
                return ast_binary_expression
            elif unary_expression:
                ast_unary_expression = ASTInternal(ASTToken(TokenType.UNARY_EXPRESSION))
                ast_unary_expression.addChild(ASTLeaf(unary_operator_token))
                ast_unary_expression.addChild(createASTFromConcreteSyntaxTree(cst.children[1], lexer))
                return ast_unary_expression
            elif isBracketExpression(cst):
                return createASTFromConcreteSyntaxTree(cst.children[1], lexer)


def appendChildASTsToAST(ast: ASTInternal, cst, lexer: CLexer):
    for child in cst.children:
        new_child = createASTFromConcreteSyntaxTree(child, lexer)
        if new_child is not None:
            ast.addChild(new_child)


def getTokenFromTerminalNode(cst: TerminalNodeImpl, lexer: CLexer):
    symbol_text = cst.getSymbol().text
    token_type = None
    if symbol_text == 'int':
        token_type = TokenType.INT_TYPE
    elif symbol_text == 'float':
        token_type = TokenType.FLOAT_TYPE
    elif symbol_text == 'char':
        token_type = TokenType.CHAR_TYPE
    elif symbol_text == 'const':
        token_type = TokenType.CONST_TYPE
    # These 'symbolic' tokens are recognized by a regular expression so we can check if the ID corresponds to one
    # of the parsers' token IDs
    elif cst.getSymbol().type == lexer.INTEGER:
        token_type = TokenType.INT_LITERAL
    elif cst.getSymbol().type == lexer.DOUBLE:
        token_type = TokenType.DOUBLE_LITERAL
    elif cst.getSymbol().type == lexer.ID:
        token_type = TokenType.IDENTIFIER
    else:
        return None

    assert token_type is not None
    return ASTToken(token_type, symbol_text)


def containsTerminalAsChild(cst):
    assert isinstance(cst, ParserRuleContext)

    for child in cst.children:
        if isinstance(child, TerminalNodeImpl):
            return True

    return False


def isBinaryExpression(cst: ParserRuleContext):
    if len(cst.children) == 3 and isinstance(cst.children[1], TerminalNodeImpl):
        token_type = None
        symbol_text = cst.children[1].getSymbol().text
        if symbol_text == '+':
            token_type = TokenType.ADD_OPERATOR
        elif symbol_text == '-':
            token_type = TokenType.SUB_OPERATOR
        elif symbol_text == '/':
            token_type = TokenType.DIV_OPERATOR
        elif symbol_text == '*':
            token_type = TokenType.MULT_OPERATOR
        elif symbol_text == '>':
            token_type = TokenType.MULT_OPERATOR
        elif symbol_text == '<':
            token_type = TokenType.MULT_OPERATOR
        elif symbol_text == '==':
            token_type = TokenType.MULT_OPERATOR
        elif symbol_text == '=':
            token_type = TokenType.MULT_OPERATOR
        assert token_type is not None
        return True, ASTToken(token_type, symbol_text)

    return False, None


def isUnaryExpression(cst: ParserRuleContext):
    if len(cst.children) == 2 and isinstance(cst.children[0], TerminalNodeImpl):
        token_type = None
        symbol_text = cst.children[0].getSymbol().text
        if symbol_text == '+':
            token_type = TokenType.UNARY_PLUS_OPERATOR
        elif symbol_text == '-':
            token_type = TokenType.UNARY_MINUS_OPERATOR
        elif symbol_text == '*':
            token_type = TokenType.DEREFERENCE_OPERATOR
        elif symbol_text == '&':
            token_type = TokenType.ADDRESS_OPERATOR
        assert token_type is not None
        return True, ASTToken(token_type, symbol_text)

    return False, None


def isBracketExpression(cst: ParserRuleContext):
    if len(cst.children) == 3:
        if isBracket(cst.children[0]) and isinstance(cst.children[1], CParser.ExprContext) and isBracket(
                cst.children[2]):
            return True

    return False


def isBracket(cst):
    if isinstance(cst, TerminalNodeImpl):
        if cst.symbol.text == "(" or ")":
            return True
    else:
        return False
