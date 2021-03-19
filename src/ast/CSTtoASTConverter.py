from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *


# TODO Improve to use a visitor pattern of the cst instead

def create_ast_var_declaration_and_init(cst: CParser.VarDeclarationAndInitContext, lexer: CLexer):
    assert isinstance(cst.children[0], CParser.TypeDeclaration1Context)
    assert isinstance(cst.children[1], CParser.VarAssignmentContext)

    data_type_and_attributes = create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
    assignment = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)
    assert isinstance(assignment, ASTAssignmentExpression)
    name = assignment.get_left()
    value = assignment.get_right()

    var_declaration_and_init = ASTVariableDeclarationAndInit(data_type_and_attributes, name, value)
    return var_declaration_and_init


def create_ast_var_declaration(cst: CParser.VarDeclarationContext, lexer: CLexer):
    assert isinstance(cst.children[0], CParser.TypeDeclaration1Context)

    data_type_and_attributes = create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
    name = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)

    var_declaration = ASTVariableDeclaration(data_type_and_attributes, name)
    return var_declaration


def create_type_asts(cst, lexer):
    assert isinstance(cst, CParser.TypeDeclaration1Context) or isinstance(cst, CParser.TypeDeclaration2Context)
    ast_children = list()
    for child in cst.children:
        ast_children.append(create_ast_from_concrete_syntax_tree(child, lexer))

    return ast_children


def create_ast_from_terminal_node(cst: TerminalNodeImpl, lexer: CLexer):
    if can_be_skipped(cst, lexer):
        return None
    else:
        if is_identifier(cst, lexer):
            return ASTLValue(cst.getSymbol().text)
        else:
            data_type_token = get_data_type_token(cst, lexer)
            type_attribute_token = get_type_attribute_token(cst)

            if is_rvalue(cst, lexer):
                return ASTRValue(data_type_token, cst.getSymbol().text)
            elif is_type_declaration(cst):
                return ASTDataType(data_type_token)
            elif type_attribute_token is not None:
                return ASTTypeAttribute(type_attribute_token)
            else:
                print(f"WARN: Skipping CST Node (returning null) with value {cst.getSymbol().text}")
                return None


def create_ast_expression(cst, lexer: CLexer):
    if is_binary_expression(cst):

        left_child = create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
        right_child = create_ast_from_concrete_syntax_tree(cst.children[2], lexer)

        if is_assignment_expression(cst):

            return ASTAssignmentExpression(left_child, right_child)

        else:

            binary_arithmetic_token = get_binary_arithmetic_expr_token(cst)
            binary_compare_token = get_relational_expr_token(cst)

            if binary_arithmetic_token is not None:
                return ASTBinaryArithmeticExpression(binary_arithmetic_token, left_child, right_child)
            elif binary_compare_token:
                return ASTRelationalExpression(binary_compare_token, left_child, right_child)
            else:
                raise NotImplementedError

    elif is_unary_expression(cst):

        unary_arithmetic_expr_token = get_unary_arithmetic_expr_token(cst)
        pointer_expr_token = get_pointer_expr_token(cst)

        value_applied_to = create_ast_from_concrete_syntax_tree(cst.children[1], lexer)

        if unary_arithmetic_expr_token is not None:
            return ASTUnaryArithmeticExpression(unary_arithmetic_expr_token, value_applied_to)
        elif pointer_expr_token is not None:
            return ASTUnaryPointerExpression(pointer_expr_token, value_applied_to)
        else:
            raise NotImplementedError


def create_ast_from_concrete_syntax_tree(cst, lexer: CLexer):
    assert isinstance(lexer, CLexer)

    if isinstance(cst, CParser.ProgramContext):
        ast_program = ASTInternal('program')
        append_child_asts_to_ast(ast_program, cst, lexer)
        return ast_program
    elif isinstance(cst, CParser.PrintfStatementContext):
        return ASTPrintfInstruction(create_ast_from_concrete_syntax_tree(cst.children[2], lexer))
    elif isinstance(cst, CParser.VarDeclarationAndInitContext):
        return create_ast_var_declaration_and_init(cst, lexer)
    elif isinstance(cst, CParser.VarDeclarationContext):
        return create_ast_var_declaration(cst, lexer)
    elif isinstance(cst, CParser.TypeDeclaration1Context) or isinstance(cst, CParser.TypeDeclaration2Context):
        return create_type_asts(cst, lexer)
    elif isinstance(cst, TerminalNodeImpl):
        return create_ast_from_terminal_node(cst, lexer)
    else:

        if len(cst.children) == 1:
            # Just pass to the child
            return create_ast_from_concrete_syntax_tree(cst.children[0], lexer)
        else:

            if is_bracket_expression(cst):
                return create_ast_from_concrete_syntax_tree(cst.children[1], lexer)
            else:
                return create_ast_expression(cst, lexer)


def can_be_skipped(cst: TerminalNodeImpl, lexer: CLexer):
    """
    Returns true if a certain terminal node can be skipped or not (braces for example)
    """
    return cst.getSymbol().type == lexer.TO_SKIP


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


def is_rvalue(cst: TerminalNodeImpl, lexer: CLexer):
    """
    In other words, checks if the given node contains a literal
    """
    assert isinstance(cst, TerminalNodeImpl)
    symbol_type = cst.getSymbol().type
    if symbol_type == lexer.CHAR or symbol_type == lexer.INTEGER or symbol_type == lexer.DOUBLE:
        return True

    return False


def is_type_declaration(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    return DataTypeToken.from_str(cst.getSymbol().text) is not None


# Maybe merge 'type' and 'literal' together or something?
def get_data_type_token(cst: TerminalNodeImpl, lexer: CLexer):
    assert isinstance(cst, TerminalNodeImpl)
    symbol_text = cst.getSymbol().text
    symbol_type = cst.getSymbol().type
    if is_type_declaration(cst):
        return DataTypeToken.from_str(symbol_text)
    else:
        if symbol_type == lexer.CHAR:
            return DataTypeToken.CHAR
        elif symbol_type == lexer.INTEGER:
            return DataTypeToken.INT
        elif symbol_type == lexer.DOUBLE:
            return DataTypeToken.FLOAT

    return None


def get_type_attribute_token(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    return TypeAttributeToken.from_str(cst.getSymbol().text)


def get_binary_arithmetic_expr_token(cst: ParserRuleContext):
    if is_binary_expression(cst):
        return BinaryArithmeticExprToken.from_str(cst.children[1].getSymbol().text)

    return None


def get_relational_expr_token(cst: ParserRuleContext):
    if is_binary_expression(cst):
        return RelationalExprToken.from_str(cst.children[1].getSymbol().text)

    return None


def is_unary_expression(cst: ParserRuleContext):
    if len(cst.children) == 2 and isinstance(cst.children[0], TerminalNodeImpl):
        if (UnaryArithmeticExprToken.from_str(cst.children[0].getSymbol().text) is not None or
                PointerExprToken.from_str(cst.children[0].getSymbol().text) is not None):
            return True

    return False


def get_unary_arithmetic_expr_token(cst: ParserRuleContext):
    assert is_unary_expression(cst)
    return UnaryArithmeticExprToken.from_str(cst.children[0].getSymbol().text)


def get_pointer_expr_token(cst: ParserRuleContext):
    assert is_unary_expression(cst)
    return PointerExprToken.from_str(cst.children[0].getSymbol().text)


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
