from src.ast.ASTTokens import *
from src.ast.IAstVisitor import IASTVisitor


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


class IHasDataType:

    @abstractmethod
    def get_data_type(self):
        pass


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


class ASTLValue(ASTLeaf):
    """
    Representation of an L-Value in an Abstract Syntax Tree
    Name which refers to a specific location in memory (l-values, such as variables for example)
    """

    def __init__(self, content: str):
        super().__init__(content)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_identifier(self)


class ASTRValue(ASTLeaf, IHasToken, IHasDataType):
    """
    Representation of an R-Value in an Abstract Syntax Tree
    Basically just literals, they don't refer to any location in memory (r-values)
    """

    def __init__(self, token: DataTypeToken, content: str):
        assert isinstance(token, DataTypeToken)
        super().__init__(content)
        self.token = token

    def get_data_type(self):
        return self.token

    def get_token(self):
        assert isinstance(self.token, DataTypeToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_literal(self)

    def get_content_depending_on_data_type(self):
        if self.token == DataTypeToken.CHAR or self.token == DataTypeToken.INT:
            # Both char and integers are integral types, so return an integer
            return int(self.get_content())
        elif self.token == DataTypeToken.FLOAT:
            return float(self.get_content())
        else:
            raise NotImplementedError


class ASTDataType(ASTLeaf, IHasToken, IHasDataType):

    def __init__(self, token: DataTypeToken):
        super().__init__(token.token_name)
        self.token = token

    def get_data_type(self):
        return self.token

    def get_token(self):
        assert isinstance(self.token, DataTypeToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_data_type(self)


class ASTTypeAttribute(ASTLeaf, IHasToken):

    def __init__(self, token: TypeAttributeToken):
        super().__init__(token.token_name)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, TypeAttributeToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_data_type(self)


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


class ASTScope(ASTInternal):

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_scope(self)


class ASTConditionalStatement(AST):

    def __init__(self, content: str, condition, execution_body: ASTScope):
        super().__init__(content)
        self.condition = condition
        self.execution_body = execution_body
        assert (isinstance(self.condition, ASTUnaryExpression) or
                isinstance(self.condition, ASTBinaryExpression) or
                isinstance(self.condition, ASTVariableDeclarationAndInit))

    def get_condition(self):
        return self.condition

    def get_execution_body(self):
        assert isinstance(self.execution_body, ASTScope)
        return self.execution_body


class ASTIfStatement(ASTConditionalStatement):

    def __init__(self, condition, execution_body: ASTScope, else_statement):
        super().__init__("if", condition, execution_body)
        self.else_statement = else_statement

    def get_else_statement(self):
        assert isinstance(self.else_statement, ASTIfStatement)
        return self.else_statement

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_if_statement(self)


class ASTWhileLoop(ASTConditionalStatement):

    def __init__(self, condition, execution_body: ASTScope):
        super().__init__('while', condition, execution_body)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_while_loop(self)


class ASTUnaryExpression(AST):

    def __init__(self, content: str, value_applied_to: AST):
        super().__init__(content)
        # The value this unary expression is applied to
        self.value_applied_to = value_applied_to
        self.value_applied_to.parent = self

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


class ASTPointerExpression(ASTUnaryExpression, IHasToken):

    def __init__(self, token: UnaryArithmeticExprToken, value_applied_to: AST):
        super().__init__(token.token_name, value_applied_to)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, UnaryArithmeticExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_unary_expression(self)


class ASTUnaryPointerExpression(ASTUnaryExpression, IHasToken):

    def __init__(self, token: UnaryArithmeticExprToken, value_applied_to: AST):
        super().__init__(token.token_name, value_applied_to)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, UnaryArithmeticExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_unary_expression(self)


class ASTBinaryExpression(AST, IHasDataType):

    def __init__(self, content: str, left: AST, right: AST):
        assert isinstance(left, AST) and isinstance(right, AST)
        super().__init__(content)
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def get_data_type(self):
        left_data_type = self.get_left().get_data_type()
        right_data_type = self.get_right().get_data_type()
        if DataTypeToken.is_richer_than(left_data_type, right_data_type):
            return left_data_type
        else:
            return right_data_type

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_binary_expression(self)

    def get_left(self):
        assert isinstance(self.left, IHasDataType)
        return self.left

    def get_right(self):
        assert isinstance(self.right, IHasDataType)
        return self.right


class ASTAssignmentExpression(ASTBinaryExpression):

    # TODO maybe later on +=, -=, *=, /= and %=
    def __init__(self, left: ASTLeaf, right: AST):
        assert isinstance(left, ASTLeaf)
        super().__init__('=', left, right)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_assignment_expression(self)

    def get_left(self):
        """
        Inherits get_left from ASTBinaryExpression to do an extra check: the left must be an identifier in this case
        """
        assert isinstance(self.left, ASTLValue)
        return self.left


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
        visitor.visit_ast_binary_compare_expression(self)


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


class ASTVariableDeclaration(AST):

    def __init__(self, data_type_and_attributes: list, name: ASTLeaf):
        super().__init__('variable declaration')
        data_type, data_type_and_attributes = self.__divide_type_attributes(data_type_and_attributes)

        self.data_type_ast = data_type
        self.data_type_ast.parent = self
        self.type_attributes = list()
        for attribute in self.type_attributes:
            attribute.parent = self
        self.var_name_ast = name
        self.var_name_ast.parent = self

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
        return self.data_type_ast.get_token()

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_variable_declaration(self)

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
            if DataTypeToken.from_str(attribute.get_content()) is not None:
                assert data_type_ast is None, "There are multiple datatypes defined. " \
                                              "This should not be possible as it should have halted with a syntax error"
                data_type_ast = ASTDataType(DataTypeToken.from_str(attribute.get_content()))
            elif attribute.get_content() == 'const':
                type_attribute_asts.append(ASTTypeAttribute(TypeAttributeToken.CONST))
            else:
                NotImplementedError('This attribute is not supported yet')
        assert isinstance(data_type_ast, ASTDataType)

        return data_type_ast, type_attribute_asts


class ASTVariableDeclarationAndInit(ASTVariableDeclaration):

    def __init__(self, data_type_and_attributes: list, name: ASTLeaf, value: AST):
        super().__init__(data_type_and_attributes, name)
        self.content += ' and init'
        self.value = value
        self.value.parent = self

    def accept(self, visitor):
        visitor.visit_ast_variable_declaration_and_init(self)


class ASTPrintfInstruction(AST):

    def __init__(self, value_to_print):
        super().__init__(str(value_to_print))

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_printf_instruction(self)
