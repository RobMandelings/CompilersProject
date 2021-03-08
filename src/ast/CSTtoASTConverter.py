from src.antlr4_gen.CParser import *
from src.ast.ASTs import *


def createASTFromConcreteSyntaxTree(cst, lexer: CLexer):
    assert isinstance(lexer, CLexer)

    return_value = None

    # Has just one child which is not a terminal node, so just pass the child in to create the AST
    if isinstance(cst, CParser.ProgramContext):
        ast_program = ASTProgram(ASTToken(cst, lexer, TokenType.PROGRAM))
        for child in cst.children:
            ast_program.addChild(createASTFromConcreteSyntaxTree(child, lexer))
        return_value = ast_program
    elif isinstance(cst, CParser.StatementContext):
        ast_statement = ASTStatement(ASTToken(cst, lexer, TokenType.STATEMENT))
        ast_statement.addChild(createASTFromConcreteSyntaxTree(cst.children[0], lexer))
        return_value = ast_statement
    # TODO maybe improve so that the children don't have hard coded locations in case the grammar changes.
    #  Create a find_child function or something to find a child based on some name.
    elif isinstance(cst, CParser.VarDeclarationContext):
        return_value = ASTVariableDeclaration(createASTFromConcreteSyntaxTree(cst.children[0], lexer),
                                             createASTFromConcreteSyntaxTree(cst.children[1], lexer),
                                             ASTToken(cst, lexer, TokenType.VARIABLE_DECLARATION))
    elif isinstance(cst, CParser.TypeDeclaration1Context):
        ast_type = ASTType(ASTToken(cst, lexer, TokenType.TYPE_DECLARATION))
        for child in cst.children:
            ast_type.addChild(createASTFromConcreteSyntaxTree(child, lexer))
        return_value = ast_type
    elif isinstance(cst, TerminalNodeImpl):
        return_value = ASTLeaf(ASTToken(cst, lexer))
    else:

        print(cst)

        if len(cst.children) == 1:
            return_value = createASTFromConcreteSyntaxTree(cst.children[0], lexer)
        else:

            if isBinaryExpression(cst):
                token = ASTToken(cst.children[1], lexer)
                return_value = ASTBinaryOperation(token, createASTFromConcreteSyntaxTree(cst.children[0], lexer),
                                                 createASTFromConcreteSyntaxTree(cst.children[2], lexer))
            elif isBracketExpression(cst):
                return_value = createASTFromConcreteSyntaxTree(cst.children[1], lexer)

    assert return_value is not None
    return return_value


def containsTerminalAsChild(cst):
    assert isinstance(cst, ParserRuleContext)

    for child in cst.children:
        if isinstance(child, TerminalNodeImpl):
            return True

    return False


def isBinaryExpression(cst: ParserRuleContext):
    if len(cst.children) == 3 and isinstance(cst.children[1], TerminalNodeImpl):
        return True

    return False


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
