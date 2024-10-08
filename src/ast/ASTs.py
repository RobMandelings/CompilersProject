from abc import abstractmethod

import src.DataType as DataType
from src.DataType import IHasDataType
from src.ast.ASTTokens import *
from src.ast.IAstVisitor import IASTVisitor


class SemanticError(Exception):
    pass


class AST:

    def __init__(self, content: str):
        self.parent = None
        self.content = content

    def __str__(self):
        return self.get_content()

    def set_parent(self, parent):
        assert isinstance(parent, AST) and not isinstance(parent, ASTLeaf)
        self.parent = parent
        return self

    def is_root(self):
        return self.parent is None

    def accept(self, visitor: IASTVisitor):
        raise NotImplementedError('Generic method')

    def get_content(self):
        assert isinstance(self.content, str)
        return self.content


class IHasToken:
    """
    Interface which provides a get_token method for the ASTs which contain tokens
    """

    @abstractmethod
    def get_token(self):
        pass


class ASTLeaf(AST):

    def __init__(self, content: str):
        super().__init__(content)

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_leaf(self)


class ASTIdentifier(ASTLeaf):
    """
    Representation of an L-Value in an Abstract Syntax Tree
    Name which refers to a specific location in memory (l-values, such as variables for example)
    """

    def __init__(self, variable_name: str):
        self.variable_name = variable_name
        super().__init__(variable_name)

    def get_name(self):
        return self.get_content()

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_identifier(self)


class ASTLiteral(ASTLeaf, IHasDataType):
    """
    Representation of an R-Value in an Abstract Syntax Tree
    Basically just literals, they don't refer to any location in memory (r-values)
    """

    def __init__(self, data_type: DataType, content: str):
        assert isinstance(data_type, DataType.DataType) and not data_type.is_pointer()
        super().__init__(content)
        self.data_type = data_type

    def get_data_type(self):
        assert isinstance(self.data_type, DataType.DataType)
        return self.data_type

    def get_data_type_token(self):
        assert self.get_data_type().get_pointer_level() == 0
        return self.get_data_type().get_token()

    def get_content(self):
        """
        Returns a string of the content this node is holding
        If you want to get the actual content of corresponding datatype, use get_value() instead!
        """
        return super().get_content()

    def get_value(self):
        """
        Same as get_content but used to return the actual value of corresponding type (such as int or double), instead of string
        """
        if self.get_data_type_token().is_integral():
            # Char and ints are both numerical so return this
            return int(self.get_content())
        elif self.get_data_type_token().is_floating_point():
            return float(self.get_content())
        else:
            raise NotImplementedError

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_literal(self)

    def get_content_depending_on_data_type(self):
        if self.get_data_type_token() == DataType.DataTypeToken.CHAR or self.get_data_type_token() == DataType.DataTypeToken.INT:
            # Both char and integers are integral types, so return an integer
            return int(self.get_content())
        elif self.get_data_type_token() == DataType.DataTypeToken.FLOAT:
            return float(self.get_content())
        else:
            raise NotImplementedError


class ASTDataType(ASTLeaf, IHasToken, IHasDataType):

    def __init__(self, data_type: DataType):
        super().__init__(data_type.get_name())
        self.data_type = data_type

    def get_data_type(self):
        return self.data_type

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_data_type(self)


class ASTArray(ASTLeaf, IHasDataType):

    def __init__(self, data_type: DataType, size):
        """
        data_type: the underlying data type of this array
        """
        super().__init__()
        self.size = size
        self.data_type = data_type

    def get_size(self):
        assert isinstance(self.size, int)
        return self.size

    def get_data_type(self):
        assert isinstance(self.data_type, DataType.DataType)
        return self.data_type


class ASTTypeAttribute(ASTLeaf, IHasToken):

    def __init__(self, token: TypeAttributeToken):
        super().__init__(token.token_name)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, TypeAttributeToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_type_attribute(self)


class ASTInternal(AST):

    def __init__(self, content: str):
        super().__init__(content)
        self.children = list()

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_internal(self)

    def add_child(self, child):
        assert child is not None

        if isinstance(child, list):
            for sub_child in child:
                self.add_child(sub_child)
        else:
            child.parent = self
            self.children.append(child)


class ASTExpression(AST):

    def accept(self, visitor: IASTVisitor):
        raise NotImplementedError


class ASTIdentifierExpression(ASTExpression):
    """
    The identifier expression is only a temporary AST that is used in the conversion from CST To AST.
    After each scope has been made,
    """

    def accept(self, visitor: IASTVisitor):
        pass

    def __init__(self, token: IdentifierExprToken, id_applied_to: ASTIdentifier):
        super().__init__(token.token_name)
        self.token = token
        self.id_applied_to = id_applied_to

    def get_token(self):
        assert isinstance(self.token, IdentifierExprToken)
        return self.token

    def get_id_applied_to(self):
        assert isinstance(self.id_applied_to, ASTIdentifier)
        return self.id_applied_to


class ASTUnaryExpression(ASTExpression):

    def __init__(self, content: str, value_applied_to: AST):
        super().__init__(content)
        # The value this unary expression is applied to
        self.value_applied_to = value_applied_to
        self.value_applied_to.parent = self

    def get_value_applied_to(self):
        assert isinstance(self.value_applied_to, AST)
        return self.value_applied_to

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_unary_expression(self)


class ASTUnaryArithmeticExpression(ASTUnaryExpression, IHasToken):

    def __init__(self, token: UnaryArithmeticExprToken, value_applied_to: AST):
        super().__init__(token.token_name, value_applied_to)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, UnaryArithmeticExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_unary_expression(self)


class ASTBinaryExpression(ASTExpression, IHasToken):

    def __init__(self, content: str, left: AST, right: AST):
        assert isinstance(left, AST) and isinstance(right, AST)
        super().__init__(content)
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def get_token(self):
        raise NotImplementedError("Generic method")

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_binary_expression(self)

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right


class ASTAccessArrayVarExpression(ASTLeaf):

    def __init__(self, variable_accessed: ASTIdentifier, index_accessed: AST):
        super().__init__(f'access[]')
        self.variable_accessed = variable_accessed
        self.index_accessed = index_accessed
        self.variable_accessed.parent = self
        self.index_accessed.parent = self

    def get_variable_accessed(self):
        assert isinstance(self.variable_accessed, ASTIdentifier)
        return self.variable_accessed

    def get_index_accessed(self):
        return self.index_accessed

    def get_content(self):
        return self.variable_accessed.get_content()

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_access_element(self)


class ASTAssignmentExpression(ASTBinaryExpression):

    # TODO maybe later on +=, -=, *=, /= and %=
    def __init__(self, left: AST, right: AST):
        assert isinstance(left, AST)
        super().__init__('=', left, right)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_assignment_expression(self)

    def get_left(self):
        """
        Inherits get_left from ASTBinaryExpression to do an extra check: the left must be an identifier in this case

        returns: an instance of ASTVariable (left side of the equation)
        """
        return super().get_left()


class ASTBinaryArithmeticExpression(ASTBinaryExpression, IHasToken):

    # TODO maybe later on also %
    def __init__(self, token: BinaryArithmeticExprToken, left: AST, right: AST):
        super().__init__(token.token_name, left, right)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, BinaryArithmeticExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_binary_arithmetic_expression(self)


class ASTRelationalExpression(ASTBinaryExpression, IHasToken):

    # TODO maybe soon also !=, <=, >=
    def __init__(self, token: RelationalExprToken, left: AST, right: AST):
        super().__init__(token.token_name, left, right)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, RelationalExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_relational_expression(self)


class ASTLogicalExpression(ASTBinaryExpression, IHasToken):
    """
    TODO Binary Expression Node which represents the logical expressions &&, || and !
    """

    def __init__(self, token: LogicalExprToken, left: AST, right: AST):
        super().__init__(token.token_name, left, right)
        self.token = token


class ASTBitwiseExpression(ASTBinaryExpression, IHasToken):
    """
    TODO Binary Expression Node which represents the bitwise expressions &, |, ^, ~, <<, >>
    """

    def __init__(self, token: BitwiseExprToken, left: AST, right: AST):
        super().__init__(token.token_name, left, right)
        self.token = token


class ASTScope(ASTInternal):

    def __init__(self):
        super().__init__('body (scope)')

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_scope(self)

    def is_empty(self):
        return len(self.children) == 0


class ASTConditionalStatement(AST):

    def __init__(self, content: str, condition, execution_body: ASTScope):
        super().__init__(content)
        self.condition = condition
        self.execution_body = execution_body
        assert isinstance(self.execution_body, ASTScope)

    def accept(self, visitor: IASTVisitor):
        raise NotImplementedError

    def get_condition(self):
        return self.condition

    def get_execution_body(self):
        assert isinstance(self.execution_body, ASTScope)
        return self.execution_body


class ASTIfStatement(ASTConditionalStatement, IHasToken):

    def __init__(self, token: IfStatementToken, condition, execution_body: ASTScope, else_statement):
        super().__init__(token.token_name, condition, execution_body)
        if token == IfStatementToken.ELSE:
            assert else_statement is None
        self.else_statement = else_statement
        self.token = token

    def get_token(self):
        assert isinstance(self.token, IfStatementToken)
        return self.token

    def has_condition(self):
        return self.get_condition() is not None

    def has_else_statement(self):
        return self.get_else_statement() is not None

    def get_else_statement(self):
        assert self.else_statement is None or isinstance(self.else_statement, ASTIfStatement)
        return self.else_statement

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_if_statement(self)


class ASTWhileLoop(ASTConditionalStatement):
    """
    the update step is necessary to support the control flow statements in a for loop as it works a bit different than in
    a while loop. The update step in the while loop is an integral part of the execution body, with a for loop it is not.
    The 'continue' statement for example will always do the update step in the for loop, which is why this is necessary.

    So in short: the update_step is only used with for loops, set to None with a while loop
    """

    def __init__(self, condition, execution_body: ASTScope, update_step):
        super().__init__('while', condition, execution_body)
        self.update_step = update_step
        if self.update_step is not None:
            self.update_step.parent = self

    def get_update_step(self):
        """
        Returns what update step needs to happen when the end of the execution body
        is reached before the condition is checked.
        """
        return self.update_step

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_while_loop(self)


class ASTVarDeclaration(AST):

    def __init__(self, data_type_and_attributes: list, name: ASTIdentifier):
        super().__init__('variable declaration')
        data_type, type_attributes = self.__divide_type_attributes(data_type_and_attributes)

        self.data_type_ast = data_type
        self.data_type_ast.parent = self
        self.type_attributes = type_attributes
        for attribute in self.type_attributes:
            attribute.parent = self
        self.var_name_ast = name
        self.var_name_ast.parent = self

    def get_var_name_ast(self):
        """
        Returns the AST version of the variable name
        """
        return self.var_name_ast

    def get_var_name(self):
        return self.get_var_name_ast().get_name()

    def is_const(self):
        for attribute in self.type_attributes:
            if isinstance(attribute, ASTTypeAttribute) and attribute.token == TypeAttributeToken.CONST:
                return True

        return False

    def get_data_type(self):
        """
        Returns the token that represents the DataType of this variable (DataTypeToken)
        """
        assert isinstance(self.data_type_ast, ASTDataType)
        return self.data_type_ast.get_data_type()

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_var_declaration(self)

    def __remove_attributes_recursion(self, type_attributes: list, new_type_attributes: list):
        """
        Remove the recursion from the type attributes list (lists contained within the list), output value in out_type_attributes.
        The recursion in the list is because the grammar is designed that way.
        """
        for attribute in type_attributes:
            if isinstance(attribute, list):
                self.__remove_attributes_recursion(attribute, new_type_attributes)
            else:
                new_type_attributes.append(attribute)

    def __divide_type_attributes(self, type_attributes: list):
        """
        Separates the type attributes from the list into a tuple of and ASTDataType and one or more ASTTypeAttributes
        Returns: tuple (data_type, const)
        """

        new_type_attributes_list = list()
        # First remove the recursion from the list
        self.__remove_attributes_recursion(type_attributes, new_type_attributes_list)

        data_type_ast = None
        type_attribute_asts = list()
        for attribute in new_type_attributes_list:
            assert isinstance(attribute, AST)
            if isinstance(attribute, ASTDataType):
                assert data_type_ast is None, "There are multiple datatypes defined. " \
                                              "This should not be possible as it should have halted with a syntax error"
                data_type_ast = attribute
            elif attribute.get_content() == 'const':
                type_attribute_asts.append(ASTTypeAttribute(TypeAttributeToken.CONST))
            else:
                NotImplementedError('This attribute is not supported yet')
        assert isinstance(data_type_ast, ASTDataType)

        return data_type_ast, type_attribute_asts


class ASTFunctionDeclaration(AST):

    def __init__(self, function_name: str, params: list, return_type: ASTDataType):
        super().__init__(f'function declaration:\n')
        assert isinstance(function_name, str)
        self.function_name = function_name
        self.params = params
        for param in self.params:
            assert isinstance(param, ASTVarDeclaration)
            param.parent = self
        self.return_type = return_type
        self.return_type.parent = self
        self.content += self.get_full_name(with_return_type=True)

    def get_identifier(self):
        """
        Just returns the identifier of the function. E.g: 'main'
        """
        return self.function_name

    def get_full_name(self, with_return_type: bool):
        full_name = ''
        if with_return_type:
            full_name = f'{self.return_type.get_data_type().get_name()} '

        full_name += f'{self.function_name}('
        for param in self.params:
            assert isinstance(param, ASTVarDeclaration)
            full_name += f'{param.get_data_type().get_name()} {param.get_var_name()}'
        full_name += ')'

        return full_name

    def get_params(self):
        return self.params

    def get_return_type_ast(self):
        assert isinstance(self.return_type, ASTDataType)
        return self.return_type

    def accept(self, visitor):
        visitor.visit_ast_function_declaration(self)


class ASTFunctionDefinition(AST):

    def __init__(self, function_declaration: ASTFunctionDeclaration, execution_body: ASTScope):
        super().__init__('function definition')
        self.function_declaration = function_declaration
        self.function_declaration.parent = self
        self.execution_body = execution_body
        self.execution_body.parent = self

    def get_function_declaration(self):
        assert isinstance(self.function_declaration, ASTFunctionDeclaration)
        return self.function_declaration

    def get_execution_body(self):
        assert isinstance(self.execution_body, ASTScope)
        return self.execution_body

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_function_definition(self)


class ASTArrayInit(AST):

    def __init__(self, values: list, data_type: DataType.DataType):
        array_init_string = '{'
        for i in range(len(values)):
            value = values[i]
            value.parent = self
            if i != len(values) - 1:
                array_init_string += value.get_content() + ','
            else:
                array_init_string += value.get_content()

        array_init_string += '}'
        super().__init__(array_init_string)
        self.values = values
        self.data_type = data_type

    def get_values(self):
        return self.values

    def get_data_type(self):
        return self.data_type

    def is_root(self):
        return False

    def accept(self, visitor: IASTVisitor):
        return visitor.visit_ast_array_init(self)


class ASTFunctionCall(ASTExpression):

    def __init__(self, function_called: str, params: list):
        super().__init__(f'function call: {function_called}')

        self.function_called = function_called
        self.params = params
        for param in self.params:
            param.parent = self

    def get_arguments(self):
        return self.params

    def get_function_called_id(self):
        assert isinstance(self.function_called, str)
        return self.function_called

    def get_function_called_full_name(self):
        full_name = f'{self.function_called}'
        return full_name

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_function_call(self)


class ASTReturnStatement(AST):

    def __init__(self, return_value: AST or None):
        super().__init__(f'return statement')
        self.return_value = return_value

        if return_value is not None:
            self.return_value.parent = self

    def get_return_value(self) -> AST or None:
        return self.return_value

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_return_statement(self)


class ASTVarDeclarationAndInit(AST):

    def __init__(self, var_declaration: ASTVarDeclaration, initial_value: AST):
        super().__init__('var declaration and init')
        self.var_declaration = var_declaration
        self.var_declaration.parent = self
        self.initial_value = initial_value
        self.initial_value.parent = self

    def is_const(self):
        return self.get_var_declaration().is_const()

    def get_data_type(self):
        return self.get_var_declaration().get_data_type()

    def get_var_name(self):
        return self.get_var_declaration().get_var_name()

    def get_initial_value(self) -> AST:
        return self.initial_value

    def get_var_declaration(self):
        assert isinstance(self.var_declaration, ASTVarDeclaration)
        return self.var_declaration

    def accept(self, visitor):
        visitor.visit_ast_var_declaration_and_init(self)


class ASTArrayVarDeclaration(ASTVarDeclaration):

    def __init__(self, data_type_and_attributes: list, name: ASTIdentifier, size: ASTLiteral):
        super().__init__(data_type_and_attributes, name)
        assert size.get_data_type() == DataType.NORMAL_INT
        self.size = size
        self.content = f'variable declaration: array (size_ast: {self.size})'

    def get_array_size(self):
        assert isinstance(self.size, ASTLiteral) and self.size.get_data_type() == DataType.NORMAL_INT
        return self.size

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_array_declaration(self)


class ASTArrayVarDeclarationAndInit(AST):

    def __init__(self, array_declaration_ast: ASTArrayVarDeclaration,
                 array_init: ASTArrayInit):
        super().__init__(f'array var declaration and init (size: {array_declaration_ast.get_array_size()})')
        self.array_declaration_ast = array_declaration_ast
        self.array_init = array_init

    def get_array_size(self):
        self.get_array_declaration_ast().get_array_size()

    def get_data_type(self):
        self.get_array_declaration_ast().get_data_type()

    def get_var_name(self):
        return self.get_array_declaration_ast().get_var_name()

    def is_const(self):
        return self.get_array_declaration_ast().is_const()

    def get_array_declaration_ast(self):
        assert isinstance(self.array_declaration_ast, ASTArrayVarDeclaration)
        return self.array_declaration_ast

    def get_array_init(self):
        return self.array_init

    def accept(self, visitor):
        visitor.visit_ast_array_declaration_and_init(self)


class ASTControlFlowStatement(AST):

    def __init__(self, control_flow_token: ControlFlowToken):
        super().__init__(control_flow_token.name.lower())
        self.control_flow_token = control_flow_token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_control_flow_statement(self)


class ASTDereference(ASTExpression):

    def __init__(self, value_to_dereference):
        super().__init__('deref')
        self.value_to_dereference = value_to_dereference
        self.value_to_dereference.parent = self

    def get_value_to_dereference(self):
        return self.value_to_dereference

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_dereference(self)


class ASTPrintfInstruction(AST):

    def __init__(self, value_to_print):
        super().__init__(str(value_to_print))

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_printf_instruction(self)


class ASTInclude(AST):

    def __init__(self, include: str):
        super().__init__(str(include))

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_include(self)
