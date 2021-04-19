from re import split

from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *

LITERALS = {CLexer.CHAR_LITERAL: DataType.NORMAL_CHAR,
            CLexer.INT_LITERAL: DataType.NORMAL_INT,
            CLexer.DOUBLE_LITERAL: DataType.NORMAL_DOUBLE}

DATA_TYPES = {CLexer.CHAR: DataType.NORMAL_CHAR,
              CLexer.INT: DataType.NORMAL_INT,
              CLexer.FLOAT: DataType.NORMAL_FLOAT}

TYPE_ATTRIBUTES = {CLexer.CONST: TypeAttributeToken.CONST}


# TODO Improve to use a visitor pattern of the cst instead

def create_ast_array_init(cst, initializer: CParser.BraceInitializerContext):
    list_of_values = list()
    for child in initializer.children:
        value = create_ast_from_cst(child)
        if value is not None:
            list_of_values.append(value)
            assert isinstance(value, ASTLiteral)

    return ASTArrayInit(list_of_values)


def create_ast_var_declaration_and_init(cst):
    if len(cst.children) == 1 and isinstance(cst.children[0], CParser.ArrayDeclarationAndInitContext):

        array_declaration = cst.children[0]

        data_types_and_attributes = create_type_asts(array_declaration.children[0])
        name = create_ast_from_cst(array_declaration.children[1])
        size = create_ast_from_cst(array_declaration.children[3])

        initializer = array_declaration.children[6]

        if isinstance(initializer, TerminalNodeImpl) and \
                initializer.getSymbol().type == CLexer.STRING:
            char_literals = list()
            string = initializer.getSymbol().text
            string = string.strip('"')

            for char in string:
                char_literals.append(ASTLiteral(DataType.NORMAL_CHAR, str(ord(char))))

            array_init = ASTArrayInit(char_literals)
        elif isinstance(initializer, CParser.BraceInitializerContext):
            array_init = create_ast_array_init(array_declaration, initializer)
        else:
            raise NotImplementedError

        array_declaration_and_init = ASTArrayDeclarationAndInit(data_types_and_attributes, name, size, array_init)
        return array_declaration_and_init

    else:
        assert isinstance(cst.children[0], CParser.TypeDeclarationContext)

        lhs_assignment = create_ast_from_cst(cst.children[1])
        rhs_assignment = create_ast_from_cst(cst.children[3])

        data_type_and_attributes = create_ast_from_cst(cst.children[0])
        assignment = ASTAssignmentExpression(lhs_assignment, rhs_assignment)
        assert isinstance(assignment, ASTAssignmentExpression)
        name = assignment.get_left()
        value = assignment.get_right()

        var_declaration_and_init = ASTVariableDeclarationAndInit(data_type_and_attributes, name, value)
        return var_declaration_and_init


def create_ast_var_declaration(cst):
    assert isinstance(cst.children[0], CParser.TypeDeclarationContext) or isinstance(cst.children[0],
                                                                                     CParser.ArrayDeclarationContext)

    data_type_and_attributes = create_ast_from_cst(cst.children[0])
    # By default it is wrapped in a Dereference Node
    variable = create_ast_from_cst(cst.children[1])

    if len(cst.children) == 3 and isinstance(cst.children[2], CParser.ArrayDeclarationContext):
        array_declaration = cst.children[2]
        size = create_ast_from_cst(array_declaration.children[1])
        return ASTArrayDeclaration(data_type_and_attributes, variable, size)
    else:
        return ASTVariableDeclaration(data_type_and_attributes, variable)


def create_type_asts(cst):
    ast_children = list()
    for child in cst.children:
        if child is not None:
            ast_children.append(create_ast_from_cst(child))

    return ast_children


def create_ast_from_terminal_node(cst: TerminalNodeImpl):
    symbol_type = cst.getSymbol().type
    if symbol_type == CLexer.ID:
        return ASTIdentifier(cst.getSymbol().text)
    elif symbol_type in DATA_TYPES:
        return ASTDataType(DATA_TYPES[symbol_type])
    elif symbol_type in TYPE_ATTRIBUTES:
        return ASTTypeAttribute(TYPE_ATTRIBUTES[symbol_type])
    elif symbol_type in LITERALS:
        return ASTLiteral(LITERALS[symbol_type], cst.getSymbol().text)

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

        value_applied_to = create_ast_from_cst(cst.children[1])

        if unary_arithmetic_expr_token is not None:
            return ASTUnaryArithmeticExpression(unary_arithmetic_expr_token, value_applied_to)
        elif is_pointer_expression(cst):

            # In this compiler, the address operator only undo's the implicit
            # derefence, so it must be a dereferenced node
            variable = create_ast_from_cst(cst.children[1])
            if not isinstance(variable, ASTIdentifier):
                raise SemanticError(f'{variable.get_content()} can not be used for references or dereferencing')

            if cst.children[0].getSymbol().text == '&':
                variable.decrease_dereference_count()
                return variable
            elif cst.children[0].getSymbol().text == '*':
                variable.increase_dereference_count()
                return variable
            else:
                raise NotImplementedError
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

    loop = ASTWhileLoop(condition, execution_body, None)
    condition.parent = loop
    execution_body.parent = loop

    return loop


def create_ast_for_loop(cst: CParser.LoopContext):
    assert isinstance(cst, CParser.LoopContext) and cst.children[0].getSymbol().type == CLexer.FOR

    start = create_ast_from_cst(cst.children[2])
    condition = create_ast_from_cst(cst.children[4])
    end = create_ast_from_cst(cst.children[6])
    execution_body = create_ast_from_cst(cst.children[8])

    while_loop = ASTWhileLoop(condition, execution_body, end)
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


def create_ast_control_flow_statement(cst):
    # Then it must be a break or a continue statement
    if isinstance(cst, TerminalNodeImpl):
        if cst.getSymbol().type == CLexer.BREAK:
            return ASTControlFlowStatement(ControlFlowToken.BREAK)
        elif cst.getSymbol().type == CLexer.CONTINUE:
            return ASTControlFlowStatement(ControlFlowToken.CONTINUE)
    elif isinstance(cst, CParser.ReturnStatementContext):

        return_value = create_ast_from_cst(cst.children[1])
        return ASTReturnStatement(return_value)

    elif cst.getSymbol().type == CLexer.RETURN:
        return ASTControlFlowStatement(ControlFlowToken.RETURN)
    else:
        raise ValueError("Wrong terminal node given")


def create_ast_function_declaration(cst: CParser.FunctionDeclarationContext):
    # Function declaration always starts with a data type (first child)
    return_type = cst.children[0]
    assert isinstance(return_type, CParser.DataTypeContext)
    return_type = ASTDataType(get_data_type(return_type))

    assert isinstance(cst.children[1], TerminalNodeImpl) and cst.children[1].getSymbol().type == CLexer.ID
    name = cst.children[1].getSymbol().text

    # Parameters are the children in between
    param_range = range(2, len(cst.children))
    params = list()
    for i in param_range:
        param = create_ast_from_cst(cst.children[i])
        if param is not None:
            params.append(param)

    return ASTFunctionDeclaration(name, params, return_type)


def create_ast_function_definition(cst: CParser.FunctionDefinitionContext):
    function_declaration = create_ast_function_declaration(cst.children[0])
    execution_body = create_ast_scope(cst.children[1])

    return ASTFunctionDefinition(function_declaration, execution_body)


def create_ast_include(cst: CParser.IncludeStdioContext):
    return ASTInclude("include")


def create_ast_from_cst(cst):
    if isinstance(cst, CParser.FunctionDeclarationContext):
        return create_ast_function_declaration(cst)
    elif isinstance(cst, CParser.FunctionDefinitionContext):
        return create_ast_function_definition(cst)
    elif isinstance(cst, CParser.FunctionStatementContext):
        return create_ast_from_cst(cst.children[0])
    elif isinstance(cst, CParser.PrintfStatementContext):
        return ASTPrintfInstruction(create_ast_from_cst(cst.children[2]))
    elif isinstance(cst, CParser.AccessArrayElementContext):
        # We know the children of the arrayAccessElement are terminal nodes (being the identifier and the size required)
        return ASTArrayAccessElement(create_ast_from_terminal_node(cst.children[0]),
                                     create_ast_from_terminal_node(cst.children[2]))
    elif isinstance(cst, CParser.FunctionCallContext):
        function_called = cst.children[0].getSymbol().text
        param_range = range(1, len(cst.children) - 1)
        params = list()
        for i in param_range:
            param = create_ast_from_cst(cst.children[i])
            if param is not None:
                params.append(param)

        return ASTFunctionCall(function_called, params)
    elif isinstance(cst, CParser.VarDeclarationAndInitContext):
        return create_ast_var_declaration_and_init(cst)
    elif isinstance(cst, CParser.VarDeclarationContext) or isinstance(cst, CParser.ArrayDeclarationContext):
        return create_ast_var_declaration(cst)
    elif isinstance(cst, CParser.TypeDeclarationContext):
        return create_type_asts(cst)
    elif isinstance(cst, CParser.DataTypeContext):
        return ASTDataType(get_data_type(cst))
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
    elif isinstance(cst, CParser.ControlFlowStatementContext):
        return create_ast_control_flow_statement(cst.children[0])
    elif isinstance(cst, CParser.EnclosedExpressionContext):
        return create_ast_from_cst(cst.children[1])
    elif isinstance(cst, CParser.IncludeStdioContext):
        return create_ast_include(cst)
    elif isinstance(cst, TerminalNodeImpl):
        return create_ast_from_terminal_node(cst)
    else:

        if len(cst.children) == 1:
            # Just pass to the child
            return create_ast_from_cst(cst.children[0])
        elif is_unary_expression(cst) or is_binary_expression(cst):
            return create_ast_expression(cst)

    raise NotImplementedError(f"CST Node '{str(type(cst).__name__)}' not supported yet")


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


def is_literal(cst: TerminalNodeImpl):
    """
    In other words, checks if the given node contains a literal
    """
    assert isinstance(cst, TerminalNodeImpl)
    symbol_type = cst.getSymbol().type
    if symbol_type == CLexer.CHAR_LITERAL or symbol_type == CLexer.INT_LITERAL or symbol_type == CLexer.DOUBLE_LITERAL:
        return True

    return False


def get_data_type(cst):
    if isinstance(cst, CParser.DataTypeContext):
        assert isinstance(cst.children[0], TerminalNodeImpl)

        cst_data_type = cst.children[0]
        symbol_type = cst_data_type.getSymbol().type

        # Always defined as 'type ('*')*', e.g. int *** -> children 1 -
        # the end are pointer indicators so *** means pointer level of 3
        pointer_level = len(cst.children) - 1

        if symbol_type == CLexer.CHAR:
            return DataType.DataType(DataType.DataTypeToken.CHAR, pointer_level)
        elif symbol_type == CLexer.INT:
            return DataType.DataType(DataType.DataTypeToken.INT, pointer_level)
        elif symbol_type == CLexer.FLOAT:
            return DataType.DataType(DataType.DataTypeToken.FLOAT, pointer_level)
        elif symbol_type == CLexer.VOID:
            return DataType.DataType(DataType.DataTypeToken.VOID, pointer_level)
        else:
            raise NotImplementedError(f'Symbol type {symbol_type} not recognized for terminal node {cst_data_type}')

    elif isinstance(cst, TerminalNodeImpl):

        symbol_type = cst.getSymbol().type

        if symbol_type == CLexer.CHAR_LITERAL or symbol_type == CLexer.CHAR:
            return DataType.NORMAL_CHAR
        elif symbol_type == CLexer.INT_LITERAL or symbol_type == CLexer.INT:
            return DataType.NORMAL_INT
        elif symbol_type == CLexer.DOUBLE_LITERAL:
            return DataType.NORMAL_DOUBLE
        else:
            raise NotImplementedError(f'Node {cst} not recognized for data type')


def get_type_attribute_token(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)
    test = cst.getSymbol().text
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
                cst.children[0].getSymbol().text == '&' or cst.children[
                    0].getSymbol().text == '*'):
            return True

    return False


def get_unary_arithmetic_expr_token(cst: ParserRuleContext):
    assert is_unary_expression(cst)
    return UnaryArithmeticExprToken.from_str(cst.children[0].getSymbol().text)


def is_pointer_expression(cst: ParserRuleContext):
    if len(cst.children) == 2 and isinstance(cst.children[0], TerminalNodeImpl):
        if cst.children[0].getSymbol().text == '&' or \
                cst.children[0].getSymbol().text == '*':
            return True

    return False


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
