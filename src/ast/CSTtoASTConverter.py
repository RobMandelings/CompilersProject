from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *

LITERALS = {CLexer.CHAR_LITERAL: DataType.NORMAL_CHAR,
            CLexer.INT_LITERAL: DataType.NORMAL_INT,
            CLexer.DOUBLE_LITERAL: DataType.NORMAL_DOUBLE}

DATA_TYPES = {CLexer.CHAR: DataType.DataTypeToken.CHAR,
              CLexer.INT: DataType.DataTypeToken.INT,
              CLexer.FLOAT: DataType.DataTypeToken.FLOAT,
              CLexer.VOID: DataType.DataTypeToken.VOID}

TYPE_ATTRIBUTES = {CLexer.CONST: TypeAttributeToken.CONST}


def get_rule_context_function(rule_context_index):
    rule_context_switcher = {
        CParser.RULE_program: __from_program,
        CParser.RULE_includeStdio: from_include_stdio,

        CParser.RULE_functionStatement: from_function_statement,
        CParser.RULE_functionDefinition: from_function_definition,
        CParser.RULE_functionDeclaration: from_function_declaration,

        CParser.RULE_dataType: from_data_type,
        CParser.RULE_typeAttributes: from_type_attributes,
        CParser.RULE_varDeclaration: from_var_declaration,
        CParser.RULE_scope: from_scope,

        CParser.RULE_statement: from_statement,

        CParser.RULE_singleLineStatement: from_single_line_statement,

        CParser.RULE_scopedStatement: from_scoped_statement,
        CParser.RULE_loop: from_loop,
        CParser.RULE_ifStatement: from_if_statement,
        CParser.RULE_elseStatement: from_if_statement,

        CParser.RULE_controlFlowStatement: from_control_flow_statement,
        CParser.RULE_returnStatement: from_return_statement,

        CParser.RULE_typeDeclaration: from_type_declaration,
        CParser.RULE_charTypeDeclaration: from_char_type_declaration,

        CParser.RULE_normalVarDeclaration: from_normal_var_declaration,
        CParser.RULE_arrayVarDeclaration: from_array_var_declaration,

        CParser.RULE_varDeclarationAndInit: from_var_declaration_and_init,
        CParser.RULE_normalVarDeclarationAndInit: from_normal_var_declaration_and_init,
        CParser.RULE_arrayVarDeclarationAndInit: from_array_var_declaration_and_init,

        CParser.RULE_braceInitializer: from_brace_initializer,
        CParser.RULE_assignmentExpression: from_assignment_expression,
        CParser.RULE_accessArrayVarExpression: from_access_array_var_expression,

        CParser.RULE_expression: from_expression,
        CParser.RULE_functionCallExpression: from_function_call_expression,
        CParser.RULE_enclosedExpression: from_enclosed_expression,
        CParser.RULE_finalExpression: from_final_expression,
        CParser.RULE_addExpression: from_binary_arithmetic_expression,
        CParser.RULE_multExpression: from_binary_arithmetic_expression,
        CParser.RULE_compareExpression: from_compare_expression,
        CParser.RULE_pointerExpression: from_pointer_expression,
        CParser.RULE_unaryExpression: from_unary_expression,

        CParser.RULE_value: from_value,

    }

    if rule_context_index in rule_context_switcher:
        return rule_context_switcher.get(rule_context_index)
    else:
        return None


def create_ast_from_cst(cst):
    if isinstance(cst, RuleContext):
        return from_rule_context(cst)
    else:
        return from_terminal_node(cst)


def from_terminal_node(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)

    symbol_type = cst.getSymbol().type
    symbol_content = cst.getSymbol().text

    if symbol_type in LITERALS:
        return ASTLiteral(LITERALS.get(symbol_type), symbol_content)
    elif symbol_type in TYPE_ATTRIBUTES:
        return ASTTypeAttribute(TYPE_ATTRIBUTES.get(symbol_type))
    elif symbol_type == CLexer.ID:
        return ASTDereference(ASTIdentifier(symbol_content))
    elif symbol_type in DATA_TYPES:
        raise NotImplementedError("Data types should be caught elsewhere to support pointers")
    else:
        print(f"[CST TO AST] Skipping terminal node with content {symbol_content}")


def from_rule_context(cst: RuleContext):
    assert isinstance(cst, RuleContext)

    if get_rule_context_function(cst.getRuleIndex()) is None:
        raise NotImplementedError(f"RuleContext Node '{str(type(cst).__name__)}' not supported yet")
    else:

        rule_context_function = get_rule_context_function(cst.getRuleIndex())
        return rule_context_function(cst)


def from_value(cst):
    return create_ast_from_cst(cst.children[0])


def from_normal_var_declaration_and_init(cst):
    data_type_and_attributes = create_ast_from_cst(cst.children[0])
    assert isinstance(data_type_and_attributes, list)

    identifier = create_ast_from_cst(cst.children[1])
    initialized_value = create_ast_from_cst(cst.children[3])
    return ASTVariableDeclarationAndInit(data_type_and_attributes, identifier, initialized_value)


def from_normal_var_declaration(cst):
    data_type_and_attributes = create_ast_from_cst(cst.children[0])
    assert isinstance(data_type_and_attributes, list)

    identifier = create_ast_from_cst(cst.children[1])
    return ASTVariableDeclaration(data_type_and_attributes, identifier)


def from_scoped_statement(cst):
    return create_ast_from_cst(cst)


def from_loop(cst):
    if cst.children[0].getSymbol().type == CLexer.FOR:
        return __create_ast_for_loop(cst)
    else:
        return __create_ast_while_loop(cst)


def from_if_statement(cst):
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


def from_data_type(cst):
    pointer_level = len(cst.children) - 1
    data_type_token = DATA_TYPES.get(cst.children[0].getSymbol().type)
    return ASTDataType(DataType.DataType(data_type_token, pointer_level))


def from_type_attributes(cst):
    type_attributes = list()

    for child in cst.children:
        type_attribute_token = TYPE_ATTRIBUTES.get(child.getSymbol().type)
        type_attributes.append(ASTTypeAttribute(type_attribute_token))

    return type_attributes


def from_var_declaration(cst):
    return create_ast_from_cst(cst.children[0])


def from_scope(cst):
    return create_ast_scope(cst)


def from_statement(cst):
    return create_ast_from_cst(cst.children[0])


def from_single_line_statement(cst):
    return create_ast_from_cst(cst.children[0])


def from_function_definition(cst):
    function_declaration = create_ast_from_cst(cst.children[0])
    execution_body = create_ast_scope(cst.children[1])

    return ASTFunctionDefinition(function_declaration, execution_body)


def from_function_declaration(cst):
    return_type = create_ast_from_cst(cst.children[0])

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


def from_assignment_expression(cst):
    lhs = create_ast_from_cst(cst.children[0])
    rhs = create_ast_from_cst(cst.children[2])
    assert isinstance(lhs, AST) and isinstance(rhs, AST)

    return ASTAssignmentExpression(lhs, rhs)


def from_access_array_var_expression(cst):
    var_accessed = create_ast_from_cst(cst.children[0])
    size = create_ast_from_cst(cst.children[0])
    return ASTAccessArrayVarExpression(var_accessed, size)


def from_control_flow_statement(cst):
    return create_ast_from_cst(cst.children[0])


def from_return_statement(cst):
    return_value = create_ast_from_cst(cst.children[1])
    return ASTReturnStatement(return_value)


def from_type_declaration(cst):
    data_type_and_attributes = list()

    for child in cst.children:
        data_type_and_attributes.append(create_ast_from_cst(child))

    return data_type_and_attributes


def from_var_declaration_and_init(cst):
    return create_ast_from_cst(cst.children[0])


def from_array_var_declaration_and_init(cst):
    data_types_and_attributes = create_ast_from_cst(cst.children[0])

    identifier = create_ast_from_cst(cst.children[1])
    size = create_ast_from_cst(cst.children[3])

    value = create_ast_from_cst(cst.children[6])

    return ASTArrayVarDeclarationAndInit(data_types_and_attributes, identifier, size, value)


def from_char_type_declaration(cst):
    data_types_and_attributes = list()

    for child in cst.children:
        data_types_and_attributes.append(create_ast_from_cst(child))

    return data_types_and_attributes


def from_array_var_declaration(cst):
    data_types_and_attributes = create_ast_from_cst(cst.children[0])
    identifier = create_ast_from_cst(cst.children[1])
    size = create_ast_from_cst(cst.children[3])

    return ASTArrayVarDeclaration(data_types_and_attributes, identifier, size)


def from_brace_initializer(cst):
    raise NotImplementedError("Braces not supported yet")


def from_include_stdio(cst):
    return ASTInclude('include')


def from_function_statement(cst):
    return create_ast_from_cst(cst.children[0])


def from_pointer_expression(cst):
    if len(cst.children) == 1:
        return create_ast_from_cst(cst.children[0])
    else:

        value_to_apply = create_ast_from_cst(cst.children[1])

        if cst.children[0].getSymbol().text == '&':
            # Undo the dereference
            assert isinstance(value_to_apply, ASTDereference)
            return value_to_apply.get_value_to_dereference()
        else:
            # Add another dereference node to the value
            return ASTDereference(value_to_apply)


def from_expression(cst):
    return create_ast_from_cst(cst.children[0])


def from_function_call_expression(cst):
    function_called = cst.children[0].getSymbol().text
    param_range = range(1, len(cst.children) - 1)
    params = list()
    for i in param_range:
        param = create_ast_from_cst(cst.children[i])
        if param is not None:
            params.append(param)

    return ASTFunctionCall(function_called, params)


def from_enclosed_expression(cst):
    # Skip the brackets
    return create_ast_from_cst(cst.children[1])


def from_unary_expression(cst):
    if len(cst.children) == 1:
        return create_ast_from_cst(cst.children[0])
    else:

        token = UnaryArithmeticExprToken.from_str(cst.children[0].getSymbol().text)
        value_applied_to = create_ast_from_cst(cst.children[1])
        return ASTUnaryArithmeticExpression(token, value_applied_to)


def from_compare_expression(cst):
    if len(cst.children) == 1:
        return create_ast_from_cst(cst.children[0])
    else:

        token = RelationalExprToken.from_str(cst.children[1].getSymbol().text)
        lhs = create_ast_from_cst(cst.children[0])
        rhs = create_ast_from_cst(cst.children[2])
        return ASTRelationalExpression(token, lhs, rhs)


def from_final_expression(cst):
    return create_ast_from_cst(cst.children[0])


def from_binary_arithmetic_expression(cst):
    if len(cst.children) == 1:
        return create_ast_from_cst(cst.children[0])
    else:

        token = BinaryArithmeticExprToken.from_str(cst.children[1].getSymbol().text)
        lhs = create_ast_from_cst(cst.children[0])
        rhs = create_ast_from_cst(cst.children[2])
        return ASTBinaryArithmeticExpression(token, lhs, rhs)


def create_ast_scope(cst):
    ast_scope = ASTScope()

    # Skip the curly braces
    for child in cst.children:
        ast_child = create_ast_from_cst(child)
        if ast_child is not None:
            ast_scope.add_child(ast_child)

    return ast_scope


def __from_program(cst):
    """
    Creates an AST from the CST ProgramContext.
    Returns the first (global) scope
    """
    ast_scope = create_ast_scope(cst)
    ast_scope.content = 'global scope'
    return ast_scope


def __create_ast_while_loop(cst):
    condition = create_ast_from_cst(cst.children[1])
    execution_body = create_ast_from_cst(cst.children[2])

    loop = ASTWhileLoop(condition, execution_body, None)
    condition.parent = loop
    execution_body.parent = loop

    return loop


def __create_ast_for_loop(cst: CParser.LoopContext):
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
