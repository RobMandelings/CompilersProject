from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *
from src.ast.ASTTokens import *


# TODO Improve to use a visitor pattern of the cst instead


def create_ast_from_concrete_syntax_tree(cst, lexer: CLexer):
    assert isinstance(lexer, CLexer)

    if isinstance(cst, CParser.ProgramContext):
        ast_program = ASTInternal('program')
        append_child_asts_to_ast(ast_program, cst, lexer)
        return ast_program
    elif isinstance(cst, CParser.InstructionsContext):
        ast_instructions = ASTInternal('instructions')
        append_child_asts_to_ast(ast_instructions, cst, lexer)
        return ast_instructions
    elif isinstance(cst, CParser.InstructionContext):
        ast_instruction = ASTInternal('instruction')
        append_child_asts_to_ast(ast_instruction, cst, lexer)
        return ast_instruction
    elif isinstance(cst, CParser.PrintfInstructionContext):
        # TODO less hardcoding
        ast_prinf_instruction = ASTPrintfInstruction(create_ast_from_concrete_syntax_tree(cst.children[2], lexer))
        return ast_prinf_instruction
    elif isinstance(cst, CParser.VarDeclarationContext):

        data_type_and_attributes = create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
        assert isinstance(data_type_and_attributes, list)

        if isinstance(cst.children[1], CParser.VarInitContext):

            name_and_value = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)
            assert isinstance(name_and_value, list) and len(name_and_value) == 2

            return ASTVariableDeclarationAndInit(data_type_and_attributes, name_and_value[0], name_and_value[1])
        else:

            name = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)
            return ASTVariableDeclaration(data_type_and_attributes, name)
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

        if is_identifier(cst, lexer):
            return ASTLValue(cst.getSymbol().text)
        else:
            data_type_token = get_data_type_token(cst, lexer)
            type_attribute_token = get_type_attribute_token(cst)

            if is_literal(cst, lexer):
                return ASTRValue(data_type_token, cst.getSymbol().text)
            elif is_type_declaration(cst):
                return ASTDataType(data_type_token)
            elif type_attribute_token is not None:
                return ASTTypeAttribute(type_attribute_token)
            else:
                print(f"WARN: Skipping CST Node (returning null) with value {cst.getSymbol().text}")
                return None
    else:

        if len(cst.children) == 1:
            # Just pass to the child
            return create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
        else:

            unary_expression_token = get_unary_expr_token(cst)

            if is_binary_expression(cst):

                left_child = create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
                right_child = create_ast_from_concrete_syntax_tree(cst.children[2], lexer)

                if is_assignment_expression(cst):

                    return ASTAssignmentExpression(left_child, right_child)

                else:

                    binary_arithmetic_token = get_binary_arithmetic_expr_token(cst)
                    binary_compare_token = get_binary_compare_expr_token(cst)

                    if binary_arithmetic_token is not None:
                        return ASTBinaryArithmeticExpression(binary_arithmetic_token, left_child, right_child)
                    elif binary_compare_token:
                        return ASTBinaryCompareExpression(binary_compare_token, left_child, right_child)
                    else:
                        raise NotImplementedError

            elif unary_expression_token is not None:

                value_applied_to = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)
                return ASTUnaryExpression(unary_expression_token, value_applied_to)
            elif is_bracket_expression(cst):
                return create_ast_from_concrete_syntax_tree(cst.children[1], lexer)


def append_child_asts_to_ast(ast: ASTInternal, cst, lexer: CLexer):
    for child in cst.children:
        new_child = create_ast_from_concrete_syntax_tree(child, lexer)
        if new_child is not None:
            ast.add_child(new_child)


def contains_terminal_as_child(cst):
    assert isinstance(cst, ParserRuleContext)

    for child in cst.children:
        if isinstance(child, TerminalNodeImpl):
            return True

    return False


def is_identifier(cst: TerminalNodeImpl, lexer: CLexer):
    assert isinstance(cst, TerminalNodeImpl)
    return cst.getSymbol().type == lexer.ID


def is_literal(cst: TerminalNodeImpl, lexer: CLexer):
    assert isinstance(cst, TerminalNodeImpl)
    symbol_type = cst.getSymbol().type
    if symbol_type == lexer.CHAR or symbol_type == lexer.INTEGER or symbol_type == lexer.DOUBLE:
        return True

    return False


def is_type_declaration(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    symbol_text = cst.getSymbol().text
    # TODO Automatically by the grammar
    if symbol_text == 'char' or symbol_text == 'int' or symbol_text == 'float':
        return True

    return False


# Maybe merge 'type' and 'literal' together or something?
def get_data_type_token(cst: TerminalNodeImpl, lexer: CLexer):
    assert isinstance(cst, TerminalNodeImpl)
    symbol_text = cst.getSymbol().text
    symbol_type = cst.getSymbol().type
    if symbol_text == 'char' or symbol_type == lexer.CHAR:
        return DataTypeToken.CHAR
    if symbol_text == 'int' or symbol_type == lexer.INTEGER:
        return DataTypeToken.INT
    if symbol_text == 'float' or symbol_type == lexer.DOUBLE:
        return DataTypeToken.FLOAT

    return None


def get_type_attribute_token(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    symbol_text = cst.getSymbol().text
    if symbol_text == 'const':
        return TypeAttributeToken.CONST

    return None


def get_binary_arithmetic_expr_token(cst: ParserRuleContext):
    if is_binary_expression(cst):
        symbol_text = cst.children[1].getSymbol().text
        if symbol_text == '+':
            return BinaryArithmeticExprToken.ADD_EXPRESSION
        elif symbol_text == '-':
            return BinaryArithmeticExprToken.SUB_EXPRESSION
        elif symbol_text == '*':
            return BinaryArithmeticExprToken.MUL_EXPRESSION
        elif symbol_text == '/':
            return BinaryArithmeticExprToken.DIV_EXPRESSION
        else:
            return None

    return None


def get_binary_compare_expr_token(cst: ParserRuleContext):
    if is_binary_expression(cst):

        symbol_text = cst.children[1].getSymbol().text
        if symbol_text == '<':
            return BinaryCompareExprToken.LESS_THAN_EXPRESSION
        elif symbol_text == '>':
            return BinaryCompareExprToken.GREATER_THAN_EXPRESSION
        elif symbol_text == '==':
            return BinaryCompareExprToken.EQUALS_EXPRESSION
        else:
            return None

    return None


def get_unary_expr_token(cst: ParserRuleContext):
    if len(cst.children) == 2 and isinstance(cst.children[0], TerminalNodeImpl):
        symbol_text = cst.children[0].getSymbol().text
        if symbol_text == '+':
            return UnaryExprToken.UNARY_PLUS_EXPRESSION
        elif symbol_text == '-':
            return UnaryExprToken.UNARY_MINUS_EXPRESSION
        elif symbol_text == '*':
            return UnaryExprToken.DEREFERENCE_EXPRESSION
        elif symbol_text == '&':
            return UnaryExprToken.ADDRESS_EXPRESSION
        else:
            return None

    return None


def is_assignment_expression(cst: ParserRuleContext):
    if is_binary_expression(cst):

        if cst.children[1].getSymbol().text == '=':
            return True

    return False


def is_binary_expression(cst: ParserRuleContext):
    if len(cst.children) == 3 and isinstance(cst.children[1], TerminalNodeImpl):
        return True
    else:
        return False


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
