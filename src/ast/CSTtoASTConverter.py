from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *


# TODO Improve to use a visitor pattern of the cst instead


def create_ast_from_concrete_syntax_tree(cst, lexer: CLexer):
    assert isinstance(lexer, CLexer)

    if isinstance(cst, CParser.ProgramContext):
        ast_program = ASTInternal(ASTToken(TokenType.PROGRAM))
        append_child_asts_to_ast(ast_program, cst, lexer)
        return ast_program
    elif isinstance(cst, CParser.InstructionsContext):
        ast_instructions = ASTInternal(ASTToken(TokenType.INSTRUCTIONS))
        append_child_asts_to_ast(ast_instructions, cst, lexer)
        return ast_instructions
    elif isinstance(cst, CParser.InstructionContext):
        ast_instruction = ASTInternal(ASTToken(TokenType.INSTRUCTION))
        append_child_asts_to_ast(ast_instruction, cst, lexer)
        return ast_instruction
    elif isinstance(cst, CParser.VarDeclarationContext):

        type_attributes = create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
        assert isinstance(type_attributes, list)

        if isinstance(cst.children[1], CParser.VarInitContext):

            name_and_value = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)
            assert isinstance(name_and_value, list) and len(name_and_value) == 2

            return ASTVariableDeclarationAndInit(type_attributes, name_and_value[0], name_and_value[1])
        else:

            name = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)
            return ASTVariableDeclaration(type_attributes, name)
    elif isinstance(cst, CParser.VarInitContext):
        children_to_return = list()
        children_to_return.append(create_ast_from_concrete_syntax_tree(cst.children[0], lexer))
        children_to_return.append(create_ast_from_concrete_syntax_tree(cst.children[2], lexer))
        return children_to_return
    elif isinstance(cst, CParser.TypeDeclaration1Context) or isinstance(cst, CParser.TypeDeclaration2Context):
        ast_children = list()
        for child in cst.children:
            ast_children.append(create_ast_from_concrete_syntax_tree(child, lexer))

        return ast_children
    elif isinstance(cst, TerminalNodeImpl):
        token = get_token_from_terminal_node(cst, lexer)
        if token is None:
            print("Token is none for terminal: " + cst.symbol.text + ", no ast is created for this node")
            return None
        else:
            return ASTLeaf(get_token_from_terminal_node(cst, lexer))
    else:

        if len(cst.children) == 1:
            # Just pass to the child
            return create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
        else:

            binary_expression, binary_operator_token = is_binary_expression(cst)
            unary_expression, unary_operator_token = is_unary_expression(cst)
            if binary_expression:
                if binary_operator_token.token_type == TokenType.ASSIGNMENT_EXPRESSION:
                    # Special case of the binary expression: the assignment expression
                    ast_binary_expression = ASTAssignmentExpression(
                        create_ast_from_concrete_syntax_tree(cst.children[0],
                                                             lexer),
                        create_ast_from_concrete_syntax_tree(cst.children[2],
                                                             lexer))
                else:
                    ast_binary_expression = ASTBinaryExpression(binary_operator_token,
                                                                create_ast_from_concrete_syntax_tree(cst.children[0],
                                                                                                     lexer),
                                                                create_ast_from_concrete_syntax_tree(cst.children[2],
                                                                                                     lexer))
                return ast_binary_expression
            elif unary_expression:
                ast_unary_expression = ASTInternal(ASTToken(TokenType.UNARY_EXPRESSION))
                ast_unary_expression.add_child(ASTLeaf(unary_operator_token))
                ast_unary_expression.add_child(create_ast_from_concrete_syntax_tree(cst.children[1], lexer))
                return ast_unary_expression
            elif is_bracket_expression(cst):
                return create_ast_from_concrete_syntax_tree(cst.children[1], lexer)


def append_child_asts_to_ast(ast: ASTInternal, cst, lexer: CLexer):
    for child in cst.children:
        new_child = create_ast_from_concrete_syntax_tree(child, lexer)
        if new_child is not None:
            ast.add_child(new_child)


def get_token_from_terminal_node(cst: TerminalNodeImpl, lexer: CLexer):
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
    elif cst.getSymbol().type == lexer.CHAR:
        token_type = TokenType.CHAR_LITERAL
        symbol_text = symbol_text.replace("\'", "")
        char = list()
        for c in symbol_text:
            char.append(c)

        assert len(char) == 1, "Character defined consists of multiple characters. This should not be possible"
        # Store its value as an integer as its an integral type, much easier to work with afterwards.
        # You can always reverse to char notation when visualising
        symbol_text = str(ord(char[0]))
    elif cst.getSymbol().type == lexer.INTEGER:
        token_type = TokenType.INT_LITERAL
    elif cst.getSymbol().type == lexer.DOUBLE:
        token_type = TokenType.FLOAT_LITERAL
    elif cst.getSymbol().type == lexer.ID:
        token_type = TokenType.IDENTIFIER
    else:
        return None

    return ASTToken(token_type, symbol_text)


def contains_terminal_as_child(cst):
    assert isinstance(cst, ParserRuleContext)

    for child in cst.children:
        if isinstance(child, TerminalNodeImpl):
            return True

    return False


def is_binary_expression(cst: ParserRuleContext):
    if len(cst.children) == 3 and isinstance(cst.children[1], TerminalNodeImpl):
        token_type = None
        symbol_text = cst.children[1].getSymbol().text
        if symbol_text == '+':
            token_type = TokenType.ADD_EXPRESSION
        elif symbol_text == '-':
            token_type = TokenType.SUB_EXPRESSION
        elif symbol_text == '/':
            token_type = TokenType.DIV_EXPRESSION
        elif symbol_text == '*':
            token_type = TokenType.MULT_EXPRESSION
        elif symbol_text == '>':
            token_type = TokenType.GREATER_THAN_EXPRESSION
        elif symbol_text == '<':
            token_type = TokenType.LESS_THAN_EXPRESSION
        elif symbol_text == '==':
            token_type = TokenType.EQUALS_EXPRESSION
        elif symbol_text == '=':
            token_type = TokenType.ASSIGNMENT_EXPRESSION
        assert token_type is not None
        return True, ASTToken(token_type, symbol_text)

    return False, None


def is_unary_expression(cst: ParserRuleContext):
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


def is_bracket_expression(cst: ParserRuleContext):
    if len(cst.children) == 3:
        if is_bracket(cst.children[0]) and isinstance(cst.children[1], CParser.ExprContext) and is_bracket(
                cst.children[2]):
            return True

    return False


def is_bracket(cst):
    if isinstance(cst, TerminalNodeImpl):
        if cst.symbol.text == "(" or ")":
            return True
    else:
        return False
