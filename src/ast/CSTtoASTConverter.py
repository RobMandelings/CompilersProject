from antlr4.Token import CommonToken
from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr4_gen.CLexer import CLexer
from src.antlr4_gen.CParser import *
from src.ast.ASTs import *

LITERALS = {CLexer.CHAR_LITERAL: DataType.NORMAL_CHAR,
            CLexer.INT_LITERAL: DataType.NORMAL_INT,
            CLexer.DOUBLE_LITERAL: DataType.NORMAL_FLOAT}

DATA_TYPES = {CLexer.CHAR: DataType.DataTypeToken.CHAR,
              CLexer.INT: DataType.DataTypeToken.INT,
              CLexer.FLOAT: DataType.DataTypeToken.FLOAT,
              CLexer.VOID: DataType.DataTypeToken.VOID}

CONTROL_FLOW_STATEMENTS = {
    CLexer.CONTINUE: ControlFlowToken.CONTINUE,
    CLexer.BREAK: ControlFlowToken.BREAK
}

TYPE_ATTRIBUTES = {CLexer.CONST: TypeAttributeToken.CONST}


class CustomTerminalNodeSymbol:
    """
    Used if you want to create custom cst nodes
    """

    def __init__(self, text):
        self.text = text


# TODO fix option to auto dereference

def get_rule_context_function(rule_context_index):
    rule_context_switcher = {
        CParser.RULE_program: __from_program,
        CParser.RULE_includeStdio: from_include_stdio,

        CParser.RULE_functionDefinition: from_function_definition,
        CParser.RULE_functionDeclaration: from_function_declaration,

        CParser.RULE_dataType: from_data_type,
        CParser.RULE_typeAttributes: from_type_attributes,
        CParser.RULE_scope: from_scope,

        CParser.RULE_statement: from_statement,

        CParser.RULE_singleLineStatement: from_single_line_statement,

        CParser.RULE_scopedStatement: from_scoped_statement,
        CParser.RULE_loop: from_loop,
        CParser.RULE_forLoop: from_for_loop,
        CParser.RULE_whileLoop: from_while_loop,

        CParser.RULE_ifStatement: from_if_statement,
        CParser.RULE_elseStatement: from_if_statement,

        CParser.RULE_controlFlowStatement: from_control_flow_statement,
        CParser.RULE_returnStatement: from_return_statement,

        CParser.RULE_typeDeclaration: from_type_declaration,
        CParser.RULE_charTypeDeclaration: from_char_type_declaration,

        CParser.RULE_normalVarDeclaration: from_normal_var_declaration,
        CParser.RULE_arrayVarDeclaration: from_array_var_declaration,

        CParser.RULE_multiVarDeclaration: from_multi_var_declaration,
        CParser.RULE_singleVarDeclaration: from_single_var_declaration,
        CParser.RULE_varDeclarationAndInit: from_var_declaration_and_init,
        CParser.RULE_normalVarDeclarationAndInit: from_normal_var_declaration_and_init,
        CParser.RULE_arrayVarDeclarationAndInit: from_array_var_declaration_and_init,

        CParser.RULE_braceInitializer: from_brace_initializer,
        CParser.RULE_assignmentExpression: from_assignment_expression,
        CParser.RULE_accessArrayVarExpression: from_access_array_var_expression,

        CParser.RULE_expression: from_expression,
        CParser.RULE_functionCallExpression: from_function_call_expression,
        CParser.RULE_enclosedExpression: from_enclosed_expression,
        CParser.RULE_compareExpression: from_compare_expression,
        # The identifier expressions are filtered out in the create_scope method, as it needs to add
        # Some nodes at a higher level in order to increment / decrement properly
        CParser.RULE_identifierExpression: from_identifier_expression,
        CParser.RULE_finalExpression: from_final_expression,
        CParser.RULE_addExpression: from_binary_arithmetic_expression,
        CParser.RULE_multExpression: from_binary_arithmetic_expression,
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


def from_identifier_expression(cst):
    if len(cst.children) == 1:
        return create_ast_from_cst(cst.children[0])

    raise NotImplementedError('The identifier expression should already have been replaced within the scope cst')


def from_terminal_node(cst: TerminalNodeImpl):
    assert isinstance(cst, TerminalNodeImpl)

    symbol_type = cst.getSymbol().type
    symbol_content = cst.getSymbol().text

    if symbol_type in LITERALS:

        if symbol_type == CLexer.CHAR_LITERAL:
            return ASTLiteral(LITERALS.get(symbol_type), str(ord(symbol_content.strip('\''))))
        else:
            return ASTLiteral(LITERALS.get(symbol_type), symbol_content)
    elif symbol_type in TYPE_ATTRIBUTES:
        return ASTTypeAttribute(TYPE_ATTRIBUTES.get(symbol_type))
    elif symbol_type == CLexer.ID:
        return ASTDereference(ASTIdentifier(symbol_content))
    elif symbol_type in CONTROL_FLOW_STATEMENTS:
        return ASTControlFlowStatement(CONTROL_FLOW_STATEMENTS.get(symbol_type))
    elif symbol_type in DATA_TYPES:
        raise NotImplementedError("Data types should be caught elsewhere to support pointers")
    elif symbol_type == CLexer.STRING:

        stripped_string = symbol_content.strip('"')

        values = list()
        for c in stripped_string:
            values.append(ASTLiteral(DataType.NORMAL_CHAR, str(ord(c))))

        array_init_ast = ASTArrayInit(values, DataType.DataType(DataType.DataTypeToken.CHAR, 0, array=True))
        return array_init_ast

    else:
        print(f"[CST TO AST] Skipping terminal node with content {symbol_content}")


def from_rule_context(cst: RuleContext):
    assert isinstance(cst, RuleContext)

    if get_rule_context_function(cst.getRuleIndex()) is None:
        raise NotImplementedError(
            f"RuleContext Node '{str(type(cst).__name__)}' not supported yet (not mapped to function)")
    else:

        rule_context_function = get_rule_context_function(cst.getRuleIndex())
        return rule_context_function(cst)


def from_value(cst):
    return create_ast_from_cst(cst.children[0])


def from_multi_var_declaration(cst):
    """
    Special case: returns a list of var declaration ASTS
    """

    # More than one single var declaration context
    if len(cst.children) > 2:
        ast_var_declarations = list()

        for child in cst.children:
            if isinstance(child, CParser.SingleVarDeclarationContext):
                ast_var_declarations.append(from_single_var_declaration(child))

        return ast_var_declarations
    else:
        return from_single_var_declaration(cst.children[1])


def from_normal_var_declaration_and_init(cst):
    variable_declaration = from_normal_var_declaration(cst)

    initialized_value = create_ast_from_cst(cst.children[3])
    return ASTVarDeclarationAndInit(variable_declaration, initialized_value)


def from_normal_var_declaration(cst):
    data_type_and_attributes = create_ast_from_cst(cst.children[0])
    assert isinstance(data_type_and_attributes, list)

    dereferenced_identifier = create_ast_from_cst(cst.children[1])
    assert isinstance(dereferenced_identifier, ASTDereference)
    identifier = dereferenced_identifier.get_value_to_dereference()

    return ASTVarDeclaration(data_type_and_attributes, identifier)


def from_scoped_statement(cst):
    return create_ast_from_cst(cst.children[0])


def from_loop(cst):
    return create_ast_from_cst(cst.children[0])


def from_for_loop(cst):
    return __create_ast_for_loop(cst)


def from_while_loop(cst):
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
    if len(cst.children) == 1:
        return create_ast_from_cst(cst.children[0])

    lhs = create_ast_from_cst(cst.children[0])
    rhs = create_ast_from_cst(cst.children[2])
    assert isinstance(lhs, AST) and isinstance(rhs, AST)

    # If the lhs dereferences a variable, this means that you just want to put the right hand side into
    # The variable. You don't need to dereference for that as a variable will be internally stored as 1 pointer lever
    # More (for example: int a; a = 5 -> a will be stored as a pointer, and when you want to STORE
    # value 5 into a, you want to store the literal 'int' value into the variable of type int*

    if isinstance(lhs, ASTDereference):
        lhs = lhs.get_value_to_dereference()

    assignment_operation = cst.children[1].getSymbol().text

    return ASTAssignmentExpression(lhs, rhs)


def from_access_array_var_expression(cst):
    var_accessed = create_ast_from_cst(cst.children[0])
    assert isinstance(var_accessed, ASTDereference)

    var_accessed = var_accessed.get_value_to_dereference()

    size = create_ast_from_cst(cst.children[2])

    return ASTDereference(ASTAccessArrayVarExpression(var_accessed, size))


def from_control_flow_statement(cst):
    return create_ast_from_cst(cst.children[0])


def from_return_statement(cst):
    # Return value is given as well
    if len(cst.children) > 1:
        return_value = create_ast_from_cst(cst.children[1])
    else:
        return_value = None
    return ASTReturnStatement(return_value)


def from_type_declaration(cst):
    data_type_and_attributes = list()

    for child in cst.children:
        data_type_and_attributes.append(create_ast_from_cst(child))

    return data_type_and_attributes


def from_var_declaration_and_init(cst):
    return create_ast_from_cst(cst.children[0])


def from_array_var_declaration_and_init(cst):
    array_var_declaration = create_ast_from_cst(cst.children[0])
    value = create_ast_from_cst(cst.children[6])

    return ASTArrayVarDeclarationAndInit(array_var_declaration, value)


def from_char_type_declaration(cst):
    data_types_and_attributes = list()

    for child in cst.children:
        data_types_and_attributes.append(create_ast_from_cst(child))

    return data_types_and_attributes


def from_array_var_declaration(cst):
    data_types_and_attributes = create_ast_from_cst(cst.children[0])
    identifier = create_ast_from_cst(cst.children[1])
    # Currently all identifiers are dereferenced by default, change this
    assert isinstance(identifier, ASTDereference)
    identifier = identifier.get_value_to_dereference()

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
            if not isinstance(value_to_apply, ASTDereference):
                raise SemanticError('Cannot dereference a non-dereferencable object')

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


def create_ast_scope(cst: CParser.ScopeContext):
    ast_scope = ASTScope()

    # Skip the curly braces
    for child in cst.children:
        ast_child = create_ast_from_cst(child)
        if ast_child is not None:

            if isinstance(ast_child, list):
                for subchild in ast_child:
                    ast_scope.add_child(subchild)
            else:
                ast_scope.add_child(ast_child)

    return ast_scope


def reorganize_assignment_expressions(current_scope, scope_child_index: int, current_node):
    """
    Recursively iterates through the tree and finds combined assignments (e.g. a = b = 5)
    It reorganizes the structure so that each assignment can be evaluated individually

    current_scope: ParseRule that currently represents the scope to add children to
    scope child index: the current 'child' index of the scope so that you can add statements in the correct place
    current_node: the current node you are evaluating
    """

    if isinstance(current_node, TerminalNodeImpl):
        # Base case
        return

    elif isinstance(current_node, CParser.ScopeContext):
        for sub_scope_child_index in range(len(current_node.children)):
            reorganize_assignment_expressions(current_node, sub_scope_child_index,
                                              current_node.children[sub_scope_child_index])
    elif isinstance(current_node, CParser.AssignmentExpressionContext):

        if isinstance(current_node.children[0], CParser.AssignmentExpressionContext) and isinstance(
                current_node.children[0].children[0], CParser.AssignmentExpressionContext):
            # This is where we need to adjust the structure of the tree a bit
            # It means that the assignment is build up out of more than one assignment.
            # E.g. a = b = 5 creates this kind of structure
            # We'll make it so that a = b = 5 is seen as two individual statements a = 5 and b = 5

            child_assignment = current_node.children[0]
            child_assignment_rhs = child_assignment.children[2]
            this_assignment_rhs = current_node.children[2]

            # This is making a = 5
            child_assignment.children[2] = this_assignment_rhs

            # This is making b = 5
            current_node.children[0] = child_assignment_rhs

            # Now recursively call the child assignment as well in case it has another assignment
            reorganize_assignment_expressions(current_scope, scope_child_index, child_assignment)

            # And finally add the newly created child assignment to the current scope at current index
            current_scope.children.insert(scope_child_index, child_assignment)

    else:

        for cur_child_index in range(len(current_node.children)):
            reorganize_assignment_expressions(current_scope, scope_child_index, current_node.children[cur_child_index])


def replace_identifier_expressions(scope, scope_child_index: int, current_node, always_before: bool = False):
    """
    Recursively finds identifiers csts and replaces it with already existing expressions.
    E.g. i++ becomes i within the expression that it was found, and another expression i + i will be inserted as next
    statement in the scope (right after the statement which included the increment).
    """
    if isinstance(current_node, TerminalNodeImpl):
        return

    if isinstance(current_node, CParser.ScopeContext):
        for sub_scope_child_index in range(len(current_node.children)):
            replace_identifier_expressions(current_node, sub_scope_child_index,
                                           current_node.children[sub_scope_child_index],
                                           always_before=False)
    else:

        for cur_child_index in range(len(current_node.children)):

            child = current_node.children[cur_child_index]

            if isinstance(child, CParser.ForLoopContext):
                # For loops have a special case, as the update step is different from the function body
                # This is for compatibility with the continue control flow statement, so that the update step
                # Gets executed properly
                replace_identifier_expressions(scope, scope_child_index, child.children[2], always_before)
                replace_identifier_expressions(child, 4, child.children[4], always_before)
                replace_identifier_expressions(child, 6, child.children[6], always_before)

                # This is a special case: the current scope at which to add the instruction children
                # Is the loop context itself, not the body this loop is defined in
                replace_identifier_expressions(child, 8, child.children[8], always_before)
            elif isinstance(child, CParser.WhileLoopContext):

                # Special case: the condition here that is checked must be updated accordingly each time
                # So this must identifier expression must be placed within the body of the while loop
                # The seemingly 'random' indices come from the children of the tree from the grammar
                replace_identifier_expressions(child.children[2], 1, child.children[1], always_before=True)
                replace_identifier_expressions(child.children[2], 0, child.children[2], always_before)
            elif not isinstance(child, CParser.IdentifierExpressionContext):
                replace_identifier_expressions(scope, scope_child_index, child, always_before)
            elif len(child.children) == 1:
                current_node.children[cur_child_index] = child.children[0]
                replace_identifier_expressions(scope, scope_child_index, current_node.children[cur_child_index],
                                               always_before)
            else:

                if isinstance(child.children[0], TerminalNodeImpl) and \
                        (child.children[0].getSymbol().type == CLexer.INCREMENT or \
                         child.children[0].getSymbol().type == CLexer.DECREMENT):
                    identifier_cst = child.children[1]
                    increment = child.children[0].getSymbol().type == CLexer.INCREMENT
                    after = False
                else:
                    identifier_cst = child.children[0]
                    increment = child.children[1].getSymbol().type == CLexer.INCREMENT
                    after = True

                # Just some custom cst nodes created so they can be used in the conversion later on
                # Not everything might be initialized just like the parser would do it, but it works
                literal_token = CommonToken(type=CLexer.INT_LITERAL, start=CLexer.INT_LITERAL, stop=CLexer.INT_LITERAL)
                literal_token.text = '1'
                one_cst = TerminalNodeImpl(literal_token)

                assignment_cst = CParser.AssignmentExpressionContext(CParser)
                assignment_cst.children = []

                assignment_token = CommonToken(type=CLexer.T__0)
                assignment_token.text = '='
                assignment_terminal = TerminalNodeImpl(assignment_token)

                operation_cst = create_operation_cst('+' if increment else '-', identifier_cst, one_cst)

                assignment_cst.children.append(identifier_cst)
                assignment_cst.children.append(assignment_terminal)
                assignment_cst.children.append(operation_cst)

                current_node.children[cur_child_index] = identifier_cst

                # Sometimes (such as in while loops) you always want to execute at an absolute given index (scope index)
                # Disregarding before / after increment
                index_to_insert_at = scope_child_index
                if not always_before and after:
                    index_to_insert_at += 1

                scope.children.insert(index_to_insert_at,
                                      assignment_cst)


def from_single_var_declaration(cst):
    """
    Single var declaration already splitted by the split_multi_var_declarations function.
    Difference here is that the first child is now also a typeDeclaration, instead of just assignment and stuff.
    """

    assert isinstance(cst.parentCtx, CParser.MultiVarDeclarationContext)

    cst_type_declaration = cst.parentCtx.children[0]

    assert isinstance(cst_type_declaration, CParser.TypeDeclarationContext)

    cst_identifier = cst.children[0]
    cst_array_declaration = None
    cst_var_initialization = None

    # Might be only array declaration, no initialization or only var initialization, no array declaration
    if len(cst.children) == 2:
        if isinstance(cst.children[1], CParser.ArrayDeclarationContext):
            cst_array_declaration = cst.children[1]
        else:
            cst_var_initialization = cst.children[1]
    elif len(cst.children) == 3:
        cst_array_declaration = cst.children[1]
        cst_var_initialization = cst.children[2]
    elif len(cst.children) > 3:
        raise AssertionError(
            f"A single var declaration shouldn't have {len(cst.children)} children unless and update happened to the grammar")

    data_type_and_attributes = create_ast_from_cst(cst_type_declaration)
    ast_var_declaration = None

    assert isinstance(data_type_and_attributes, list)

    dereferenced_identifier = create_ast_from_cst(cst_identifier)
    assert isinstance(dereferenced_identifier, ASTDereference)
    ast_identifier = dereferenced_identifier.get_value_to_dereference()

    if cst_array_declaration is None:
        ast_var_declaration = ASTVarDeclaration(data_type_and_attributes, ast_identifier)
    else:
        size = create_ast_from_cst(cst_array_declaration.children[1])
        ast_var_declaration = ASTArrayVarDeclaration(data_type_and_attributes, ast_identifier, size)

    if cst_var_initialization is None:
        return ast_var_declaration
    else:

        if cst_array_declaration is None:
            initialized_value = create_ast_from_cst(cst_var_initialization.children[1])

            return ASTVarDeclarationAndInit(ast_var_declaration, initialized_value)

        else:
            raise NotImplementedError('Not implemented yet')


def pre_parse(scope: CParser.ScopeContext, scope_child_index: int, current_node):
    """
    Must be run before everything else.
    Preparses the current concrete syntax tree to already get rid of some redundant nodes and to make life easier
    to convert into an AST. This puts similar cst nodes into the proper format so that it can easily be converted into the corresponding
    AST nodes.
    """
    replace_identifier_expressions(scope, scope_child_index, current_node)
    reorganize_assignment_expressions(scope, scope_child_index, current_node)
    replace_assignment_expressions(scope, scope_child_index, current_node)


def replace_assignment_expressions(scope: CParser.ScopeContext, scope_child_index: int,
                                   current_node):
    if isinstance(current_node, TerminalNodeImpl):
        return

    for cur_child_index in range(len(current_node.children)):

        child = current_node.children[cur_child_index]

        if isinstance(child, CParser.ScopeContext):
            for sub_scope_child_index in range(len(child.children)):
                replace_assignment_expressions(child, sub_scope_child_index, child.children[sub_scope_child_index])

        elif isinstance(child, CParser.AssignmentExpressionContext):

            if len(child.children) == 1:
                replace_assignment_expressions(scope, scope_child_index, current_node.children[cur_child_index])
            else:

                assignment_operation = child.children[1].getSymbol().text
                if assignment_operation != '=':
                    # E.g. *= becomes *, += becomes +,...
                    operation_token_text = assignment_operation[0]
                    operation_cst = create_operation_cst(operation_token_text, child.children[0], child.children[2])
                    child.children[2] = operation_cst
                    child.children[1].getSymbol().text = '='

        else:

            replace_assignment_expressions(scope, scope_child_index, child)


def create_operation_cst(operation_token_text: str, identifier_cst: TerminalNodeImpl, rhs_cst):
    operation_cst = CParser.AddExpressionContext(CParser)

    operation_cst.children = []
    operation_cst.children.append(identifier_cst)
    operation_token_type = CLexer.T__0
    operation_token = CommonToken(type=operation_token_type, start=operation_token_type, stop=operation_token_type)
    operation_token.text = operation_token_text
    operation_cst.children.append(TerminalNodeImpl(operation_token))

    operation_cst.children.append(rhs_cst)
    return operation_cst


def __from_program(cst):
    """
    Creates an AST from the CST ProgramContext.
    Returns the first (global) scope
    """
    for child_index in range(len(cst.children)):
        pre_parse(cst, child_index, cst.children[child_index])

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

    # Might be multiple statements in case of ++ or -- within an expression
    # for example (is split up into an assignment and then the expression in which the identifier is used)
    update_step_asts = list()

    current_update_step_cst_index = 6
    current_update_step_cst = cst.children[current_update_step_cst_index]
    end_of_update_step_reached = False
    while not end_of_update_step_reached:

        update_step_ast = create_ast_from_cst(current_update_step_cst)
        if update_step_ast is not None:
            update_step_asts.append(update_step_ast)

        current_update_step_cst_index += 1
        current_update_step_cst = cst.children[current_update_step_cst_index]
        if isinstance(current_update_step_cst, TerminalNodeImpl) and current_update_step_cst.getSymbol().text == ')':
            end_of_update_step_reached = True

    update_step = ASTInternal('update step')
    for update_step_ast in update_step_asts:
        update_step.add_child(update_step_ast)

    execution_body = create_ast_from_cst(cst.children[current_update_step_cst_index + 1])

    while_loop = ASTWhileLoop(condition, execution_body, update_step)
    condition.set_parent(while_loop)
    execution_body.set_parent(while_loop)

    to_return = list()
    to_return.append(start)
    to_return.append(while_loop)
    return to_return
