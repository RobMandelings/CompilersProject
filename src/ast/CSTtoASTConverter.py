from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *


# TODO Improve to use a visitor pattern of the cst instead

def create_ast_var_declaration_and_init(cst: CParser.VarDeclarationAndInitContext):
    assert isinstance(cst.children[0], CParser.TypeDeclaration1Context)
    assert isinstance(cst.children[1], CParser.VarAssignmentContext)

    data_type_and_attributes = create_ast_from_cst(cst.children[0])
    assignment = create_ast_from_cst(cst.children[1])
    assert isinstance(assignment, ASTAssignmentExpression)
    name = assignment.get_left()
    value = assignment.get_right()

    var_declaration_and_init = ASTVariableDeclarationAndInit(data_type_and_attributes, name, value)
    return var_declaration_and_init


def create_ast_var_declaration(cst: CParser.VarDeclarationContext):
    assert isinstance(cst.children[0], CParser.TypeDeclaration1Context)

    data_type_and_attributes = create_ast_from_cst(cst.children[0])
    name = create_ast_from_cst(cst.children[1])

    var_declaration = ASTVariableDeclaration(data_type_and_attributes, name)
    return var_declaration


def create_type_asts(cst):
    assert isinstance(cst, CParser.TypeDeclaration1Context) or isinstance(cst, CParser.TypeDeclaration2Context)
    ast_children = list()
    for child in cst.children:
        ast_children.append(create_ast_from_cst(child))

    return ast_children


def create_ast_from_terminal_node(cst: TerminalNodeImpl):
    if is_identifier(cst):
        return ASTVariable(cst.getSymbol().text)
    else:
        data_type_token = get_data_type_token(cst)
        type_attribute_token = get_type_attribute_token(cst)

        if is_rvalue(cst):
            return ASTLiteral(data_type_token, cst.getSymbol().text)
        elif is_type_declaration(cst):
            return ASTDataType(data_type_token)
        elif type_attribute_token is not None:
            return ASTTypeAttribute(type_attribute_token)

    print(f"WARN: Skipping CST Terminal Node (returning None) with value '{cst.getSymbol().text}'")
    return None


def create_ast_expression(cst):
    if is_binary_expression(cst):

        left_child = create_ast_from_cst(cst.children[0])
        right_child = create_ast_from_cst(cst.children[2])

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

        value_applied_to = create_ast_from_cst(cst.children[1])

        if unary_arithmetic_expr_token is not None:
            return ASTUnaryArithmeticExpression(unary_arithmetic_expr_token, value_applied_to)
        elif pointer_expr_token is not None:
            return ASTUnaryPointerExpression(pointer_expr_token, value_applied_to)
        else:
            raise NotImplementedError


def create_ast_scope(cst):
    assert isinstance(cst, CParser.ScopeContext) or isinstance(cst, CParser.ProgramContext)

    ast_scope = ASTScope()

    if isinstance(cst, CParser.ProgramContext):
        ast_scope.content = 'global scope'

    # Skip the curly braces
    for child in cst.children:
        ast_child = create_ast_from_cst(child)
        if ast_child is not None:
            ast_scope.add_child(ast_child)

    return ast_scope


def create_ast_while_loop(cst: CParser.LoopContext):
    assert isinstance(cst, CParser.LoopContext) and cst.children[0].getSymbol().type == CLexer.WHILE

    condition = create_ast_from_cst(cst.children[1])
    execution_body = create_ast_from_cst(cst.children[2])

    loop = ASTWhileLoop(condition, execution_body)
    condition.parent = loop
    execution_body.parent = loop

    return loop


def create_ast_for_loop(cst: CParser.LoopContext):
    assert isinstance(cst, CParser.LoopContext) and cst.children[0].getSymbol().type == CLexer.FOR

    start = create_ast_from_cst(cst.children[2])
    condition = create_ast_from_cst(cst.children[4])
    end = create_ast_from_cst(cst.children[6])
    execution_body = create_ast_from_cst(cst.children[8])

    execution_body.add_child(end)

    while_loop = ASTWhileLoop(condition, execution_body)
    condition.set_parent(while_loop)
    execution_body.set_parent(while_loop)

    to_return = list()
    to_return.append(start)
    to_return.append(while_loop)
    return to_return


def create_ast_if_statement(cst):
    assert isinstance(cst, CParser.IfStatementContext) or isinstance(cst, CParser.ElseStatementContext)

    children_asts = list()

    for child in cst.children:
        child_ast = create_ast_from_cst(child)
        if child_ast is not None:
            children_asts.append(child_ast)

    condition = None
    execution_body = None
    else_statement = None

    for child_ast in children_asts:
        if isinstance(child_ast, ASTExpression) or isinstance(child_ast, ASTLiteral):
            condition = child_ast
        elif isinstance(child_ast, ASTScope):
            execution_body = child_ast
        elif isinstance(child_ast, ASTIfStatement):
            else_statement = child_ast

    token = None
    if cst.children[0].getSymbol().type == CLexer.IF:
        token = IfStatementToken.IF
    elif cst.children[0].getSymbol().type == CLexer.ELSE:
        if isinstance(cst.children[1], TerminalNodeImpl) and cst.children[1].getSymbol().type == CLexer.IF:
            token = IfStatementToken.ELSE_IF
        else:
            token = IfStatementToken.ELSE

    assert token is not None
    if_statement = ASTIfStatement(token, condition, execution_body, else_statement)

    if condition is not None:
        condition.parent = if_statement

    execution_body.parent = if_statement

    if else_statement is not None:
        else_statement.parent = if_statement
    return if_statement


def create_ast_from_cst(cst):
    if isinstance(cst, CParser.PrintfStatementContext):
        return ASTPrintfInstruction(create_ast_from_cst(cst.children[2]))
    elif isinstance(cst, CParser.VarDeclarationAndInitContext):
        return create_ast_var_declaration_and_init(cst)
    elif isinstance(cst, CParser.VarDeclarationContext):
        return create_ast_var_declaration(cst)
    elif isinstance(cst, CParser.TypeDeclaration1Context) or isinstance(cst, CParser.TypeDeclaration2Context):
        return create_type_asts(cst)
    elif isinstance(cst, CParser.ScopeContext) or isinstance(cst, CParser.ProgramContext):
        return create_ast_scope(cst)
    elif isinstance(cst, CParser.LoopContext):
        if cst.children[0].getSymbol().type == CLexer.WHILE:
            return create_ast_while_loop(cst)
        elif cst.children[0].getSymbol().type == CLexer.FOR:
            return create_ast_for_loop(cst)
    elif isinstance(cst, CParser.IfStatementContext) or isinstance(cst, CParser.ElseStatementContext):
        return create_ast_if_statement(cst)
    elif isinstance(cst, CParser.StatementContext):
        if isinstance(cst.children[0], CParser.SingleLineStatementContext):
            return create_ast_from_cst(cst.children[0])
        elif isinstance(cst.children[0], CParser.ScopedStatementContext):
            return create_ast_from_cst(cst.children[0])
    elif isinstance(cst, CParser.EnclosedExpressionContext):
        return create_ast_from_cst(cst.children[1])
    elif isinstance(cst, TerminalNodeImpl):
        return create_ast_from_terminal_node(cst)
    else:

        if len(cst.children) == 1:
            # Just pass to the child
            return create_ast_from_cst(cst.children[0])
        elif is_unary_expression(cst) or is_binary_expression(cst):
            return create_ast_expression(cst)

    raise NotImplementedError


def append_child_asts_to_ast(ast: ASTInternal, cst):
    for child in cst.children:
        new_child = create_ast_from_cst(child)
        if new_child is not None:
            ast.add_child(new_child)


def contains_terminal_as_child(cst):
    assert isinstance(cst, ParserRuleContext)

    for child in cst.children:
        if isinstance(child, TerminalNodeImpl):
            return True

    return False


def is_identifier(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    return cst.getSymbol().type == CLexer.ID


def is_rvalue(cst: TerminalNodeImpl):
    """
    In other words, checks if the given node contains a literal
    """
    assert isinstance(cst, TerminalNodeImpl)
    symbol_type = cst.getSymbol().type
    if symbol_type == CLexer.CHAR or symbol_type == CLexer.INT_LITERAL or symbol_type == CLexer.DOUBLE_LITERAL:
        return True

    return False


def is_type_declaration(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    return DataTypeToken.from_str(cst.getSymbol().text) is not None


def get_data_type_token(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    symbol_text = cst.getSymbol().text
    symbol_type = cst.getSymbol().type
    if is_type_declaration(cst):
        return DataTypeToken.from_str(symbol_text)
    else:
        if symbol_type == CLexer.CHAR:
            return DataTypeToken.CHAR
        elif symbol_type == CLexer.INT_LITERAL:
            return DataTypeToken.INT
        elif symbol_type == CLexer.DOUBLE_LITERAL:
            return DataTypeToken.DOUBLE

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
